# B06｜纹理采样、Mip、LOD 与过滤

> 核心问题：同一张清晰贴图，为什么远处闪烁、斜看模糊？关闭 Mip 为什么可能让静帧更锐却让运动更差？
>
> 结论：一个屏幕像素可能覆盖多个纹理 texel。采样必须考虑这片区域的尺度与形状；Mip 提供预滤波层级，过滤与各向异性控制怎样重建结果，单次读取最清晰层并不能解决缩小混叠。

本卡面向 Unity URP NPR（非真实感渲染），独立解释必要采样概念。文档依据 Unity 6.7 Beta / 6000.7（2026-06-26）；源码固定 Graphics `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`、Core/URP 17.0.4。主要讨论普通二维纹理和片元阶段，不讨论虚拟纹理、阴影比较采样与纹理数组的完整语义。

## 1. 采样不是“给 UV，取一个像素”

Texel 是纹理离散样本，pixel 是输出图像位置；UV 是纹理坐标。以宽 W、高 H 的普通归一化二维纹理为例，第 `(i,j)` 个 texel 中心对应 $((i+0.5)/W,(j+0.5)/H)$。

一次采样还需要纹理格式、可访问 Mip、地址模式和过滤规则。Repeat、Clamp 等处理坐标边界；Point、Bilinear、Trilinear 处理样本重建。格式解码、sRGB 解释又是其他层次，不能通过切换过滤方式修复错误颜色编码。

普通双线性过滤在一层内根据位置混合邻近四个 texel。若局部四值为 `0,1;1,0`，采样点位于四者中心，结果为 0.5。硬件可复用缓存和专用过滤单元，不能因此推断每次 Sample 都产生四次独立外存事务。

## 2. Mip 编号与过滤

Mip 0 是最高分辨率层；Mip 1 通常宽高各减半，Mip 2 再减半。**编号越大，分辨率越低。** 本地 Mip 概述中个别“higher/lower level”措辞容易混淆，此处始终用明确编号与尺寸。

| 方式 | 主要行为 | 仍不能保证什么 |
| --- | --- | --- |
| Point | 在选定层按最近规则取样 | 缩小时不混叠 |
| Bilinear | 在选定层内做二维线性重建 | 层级切换一定平滑 |
| Trilinear | 层内过滤并在邻近 Mip 间混合 | 倾斜足迹的细节完全保留 |
| Anisotropic | 更重视非等向采样区域的形状 | 固定次数、固定成本或零模糊 |

双线性不等于“关闭 Mip”，Point 也不等于“强制 Mip 0”。实际层级选择还受 sampler 与可用资源约束。Unity 的过滤接口说明见 [FilterMode](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/FilterMode.html)，Mip 概念见 [Unity Mipmaps](https://docs.unity3d.com/6000.0/Documentation/Manual/texture-mipmaps-introduction.html)。

Mip 是经过预滤波的一组数据，不是运行时把任何四个数字平均后就天然正确。颜色、法线、遮罩覆盖率、SDF 和类别编号有不同语义；例如平均类别 1 和 3 得到 2，并不表示区域中真的有类别 2。

## 3. 从屏幕变化率估算 LOD

设连续 UV 对屏幕像素的变化为 `ddx(uv)`、`ddy(uv)`，乘上纹理尺寸得到 texel 单位梯度：

$$g_x=(W\,\partial u/\partial x,H\,\partial v/\partial x),\quad
g_y=(W\,\partial u/\partial y,H\,\partial v/\partial y)$$

一个常见的各向同性教学估算是：

$$\rho=\max(\|g_x\|,\|g_y\|),\qquad LOD\approx\log_2\rho$$

当每像素跨约 4 texel，估计 LOD 为 2；Mip 2 把每方向尺度缩小约四倍。`ρ<1` 表示放大，最终还要受可用层级、偏置与限制影响。

这不是所有硬件的逐位 LOD 公式。更完整的采样区域由 UV 局部雅可比矩阵描述；若一个方向跨 16 texel，另一个方向只跨 1 texel，用一个很粗的各向同性层会同时模糊短轴。各向异性过滤能改善这种情况，但具体采样策略属于实现。[Unity 各向异性设置](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Texture-anisoLevel.html)

## 4. 隐式采样、显式 LOD 与显式梯度

| Unity 宏 | 提供给采样操作的信息 |
| --- | --- |
| `SAMPLE_TEXTURE2D` | 普通片元路径由隐式梯度参与选择 |
| `SAMPLE_TEXTURE2D_LOD` | 显式给出层级 |
| `SAMPLE_TEXTURE2D_GRAD` | 显式给出 UV 对屏幕的两个梯度 |

显式 LOD 0 不等于 Point，也不关闭层内过滤。显式梯度让你保留正确的坐标变化率，例如在坐标 wrapping 或分歧之前先算梯度。它并不使错误梯度自动正确。[HLSL SampleLevel](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-samplelevel)、[HLSL SampleGrad](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-samplegrad)

一个重要反例：连续 u 从 `0.99` 到 `1.01`，真实差是 `0.02`；提前 `frac` 后变为 `0.99` 到 `0.01`，差成 `-0.98`。后者的绝对值大了 49 倍，会误导依赖该差分的层级估计，理论 LOD 差约 `log₂49≈5.61`。对于普通 Repeat 纹理，直接让 sampler 处理 wrapping 通常更清楚；图集需要另外处理边缘、padding 与各级 Mip，不能靠 `frac` 一步解决。

## 5. 完整实验：自己生成棋盘贴图

保存以下脚本为 `B06TextureLab.cs`，挂到有 Renderer 的 Quad，指定后附 Shader。进入 Play Mode，脚本创建自己的材质与 `256×256` 黑白棋盘，每格 `8×8 texel`。它使用线性未压缩数据，避开导入压缩和 sRGB 对本实验的干扰。

```csharp
using UnityEngine;

[RequireComponent(typeof(Renderer))]
public class B06TextureLab : MonoBehaviour
{
    public Shader labShader;
    public bool mipChain=true;
    public FilterMode filter=FilterMode.Trilinear;
    [Range(1,16)] public int anisotropy=1;
    [Range(0,3)] public int mode=0;
    [Range(1,32)] public float tiling=8;
    Renderer rendererComponent;
    Material previousMaterial, ownedMaterial;
    Texture2D texture;
    void Start()
    {
        if(labShader==null || !labShader.isSupported) { enabled=false; return; }
        rendererComponent=GetComponent<Renderer>();
        previousMaterial=rendererComponent.sharedMaterial;
        ownedMaterial=new Material(labShader);
        rendererComponent.sharedMaterial=ownedMaterial;
        Rebuild();
    }
    [ContextMenu("Rebuild Checker Texture")]
    public void Rebuild()
    {
        if(!Application.isPlaying || ownedMaterial==null) return;
        if(texture!=null) Destroy(texture);
        texture=new Texture2D(256,256,TextureFormat.RGBA32,mipChain,true);
        texture.name="B06 Owned Checker";
        texture.wrapMode=TextureWrapMode.Repeat;
        var pixels=new Color32[256*256];
        for(int y=0;y<256;y++) for(int x=0;x<256;x++)
        {
            byte v=(byte)(((x/8+y/8)%2)*255);
            pixels[y*256+x]=new Color32(v,v,v,255);
        }
        texture.SetPixels32(pixels);
        texture.Apply(true,false);
        ownedMaterial.SetTexture("_MainTex",texture);
    }
    void Update()
    {
        if(texture==null || ownedMaterial==null) return;
        texture.filterMode=filter;
        texture.anisoLevel=anisotropy;
        ownedMaterial.SetFloat("_Mode",mode);
        ownedMaterial.SetFloat("_Tiling",tiling);
    }
    void OnDestroy()
    {
        if(rendererComponent!=null && rendererComponent.sharedMaterial==ownedMaterial)
            rendererComponent.sharedMaterial=previousMaterial;
        if(texture!=null) Destroy(texture);
        if(ownedMaterial!=null) Destroy(ownedMaterial);
    }
}
```

保存为 `B06SamplingLab.shader`：

```c
Shader "Encyclopedia/B06SamplingLab"
{
    Properties
    {
        _MainTex("Checker",2D)="white" {}
        _Mode("Mode",Float)=0
        _Tiling("Tiling",Float)=8
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            Cull Off
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            TEXTURE2D(_MainTex); SAMPLER(sampler_MainTex);
            CBUFFER_START(UnityPerMaterial)
                float _Mode, _Tiling;
            CBUFFER_END
            struct A { float3 p:POSITION; float2 uv:TEXCOORD0; };
            struct V { float4 p:SV_POSITION; float2 uv:TEXCOORD0; };
            V Vert(A input)
            {
                V o;
                o.p=TransformObjectToHClip(input.p);
                o.uv=input.uv*_Tiling;
                return o;
            }
            half4 Frag(V input):SV_Target
            {
                float2 gx=ddx(input.uv), gy=ddy(input.uv);
                if(_Mode<0.5) return SAMPLE_TEXTURE2D(_MainTex,sampler_MainTex,input.uv);
                if(_Mode<1.5) return SAMPLE_TEXTURE2D_LOD(_MainTex,sampler_MainTex,input.uv,0);
                if(_Mode<2.5) return SAMPLE_TEXTURE2D(_MainTex,sampler_MainTex,frac(input.uv));
                return SAMPLE_TEXTURE2D_GRAD(_MainTex,sampler_MainTex,frac(input.uv),gx,gy);
            }
            ENDHLSL
        }
    }
}
```

在 URP Forward 单相机测试场景中倾斜 Quad，固定分辨率，关闭后处理、Depth Priming、SSAO、额外 Renderer Feature、XR 和动态分辨率。开始用 anisotropy=1，Quality 的各向异性设置允许逐纹理控制，避免 Forced On 覆盖参数。

模式 0 普通 Repeat；1 强制 LOD 0；2 先 frac 再隐式采样；3 先保留连续梯度再 frac。比较远处与缓慢移动时的闪烁，并在重复接缝附近比较模式 2/3。重复纹理本身需要边缘匹配；此棋盘按周期生成。梯度错误是否显著受 quad 位置、编译优化和实际 LOD 限制影响，不能保证每帧都出现明显线条。

改变 mipChain 后执行 `Rebuild Checker Texture`；filter、anisotropy 和 tiling 在 Play 中直接生效。把各向异性从 1 增到 8，观察斜面细节与 GPU 时间，分别记录质量和成本，不宣称固定提升倍数。

## 6. NPR 应用与证据范围

颜色 Ramp 要明确颜色编码；数值 Ramp 要保持函数含义。面部 SDF 的普通平均 Mip 不保证仍是精确距离场；类别 ID 不应通过过滤制造不存在的类别；细线遮罩缩小后需要保留覆盖或能量的策略。**清晰、稳定、语义正确是三个不同要求。**

固定源码 [D3D11.hlsl](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.core/ShaderLibrary/API/D3D11.hlsl) 将 `_LOD` 映射到 `SampleLevel`，`_GRAD` 映射到 `SampleGrad`；其他 API 有各自头文件。宏能证明调用语义，不能证明实际访存次数。

自测：① Mip 2 比 Mip 0 大吗？**分辨率更低。** ② 强制 LOD 0 就没有过滤吗？**仍受 sampler 的层内规则影响。** ③ 各向异性是增强锐化吗？**它处理非等向采样区域，不是普通后处理锐化。** ④ frac 前后导数相同吗？**跨重复边界时通常不同。**

Python 检查双线性、层级估算、跨层混合和 wrapping 反例；未模拟硬件过滤。Unity 示例未编译运行。已核对本地 `Manual/texture-mipmaps-introduction.html`、`ScriptReference/FilterMode.html`、`Texture-anisoLevel.html`，文档根目录为 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。

下一张：[B07｜深度缓冲、ZTest、ZWrite 与 Reversed-Z](B07-深度缓冲ZTestZWrite与ReversedZ.md)。
