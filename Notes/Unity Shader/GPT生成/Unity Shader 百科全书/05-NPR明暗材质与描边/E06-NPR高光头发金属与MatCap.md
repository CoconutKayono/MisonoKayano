# E06｜NPR 高光、头发、金属与 MatCap

> 核心问题：材质辨识依赖哪些方向与视角关系？本卡在同一物体上比较阈值高光、沿发流方向的带状高光和 MatCap，并明确它们各自能表达什么。

## 1. 先确定高光由谁控制

记 N 为单位表面法线，L 为表面指向光的方向，V 为表面指向相机的方向。半程向量 `H=normalize(L+V)`；L 与 V 相反时必须处理长度退化。高光通常随观察方向变化，不能只用 N·L 代替。

| 模型 | 主要输入 | 移动灯 | 移动相机 |
| --- | --- | --- | --- |
| 阈值化 N·H | N、L、V、阈值与遮罩 | 通常改变高光 | 通常改变高光 |
| 发流高光 | 发流方向 T、L、V、位移参数和遮罩 | 改变带状响应 | 改变带状响应 |
| 本卡 MatCap | 观察空间法线、预制颜色图 | 不直接改变纹理图案 | 按观察空间映射改变 |

本地文档为 Unity **6.7 Beta / 6000.7、2026-06-26**。Graphics 固定 `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`（URP/Core **17.0.4、6000.0**）；UTS 固定 `1520a78a95292cb045f1edb4d60ea0dba2f213b3`（**0.15.1-preview、6000.0**）。本例是方向响应实验，不是完整物理材质或 UTS 移植。

## 2. 形状、强度、遮罩与材质颜色分开处理

常见连续高光为 `pow(saturate(N·H),p)`，p 越大高光越集中。卡通高光也可以对 N·H 直接设阈值，再用 smoothstep 软化边界。阈值 0.95 表示约 18.2° 的半程向量夹角范围；这与 pow 指数 0.95 完全不是同一参数。

遮罩 M(uv) 用来控制高光能出现在哪些区域；方向函数控制何时出现，两者可相乘。把眼眶、发根等位置排除在高光之外，通常不应通过扭曲整个模型的 N 来实现。

金属外观常依赖有色反射、明暗环境结构与观察方向；把白高光改成黄色并叠在强漫反射上，不保证表现为金属。真实导体 BRDF 还涉及复折射率、Fresnel 和粗糙度等条件，参见 [PBRT：Conductor BRDF](https://www.pbr-book.org/4ed/Reflection_Models/Conductor_BRDF)。本文可用低底色、有色锐高光制作风格化金属提示，但不声称能量守恒或具有完整环境反射。

## 3. 发流方向为何不是随便取 TANGENT.xyz

网格切线通常对应纹理 U 方向，头发走向却可能沿 V。若单位切线为 T，法线为 N，手性为 s，则副切线 `B=normalize(cross(N,T))×s`。Unity 的镜像变换还需要考虑负缩放手性。采样前要确定美术的“发根到发梢”沿哪个 UV 轴。

本卡用一个简化带状响应：

`T' = normalize(Tflow + shift×N)`，`spec = pow(sqrt(saturate(1-(T'·H)^2)),p)`。

当 T' 与 H 垂直时响应最强。shift 改变高光轴，不是把纹理在屏幕上平移。该公式用来演示各向异性方向，**不是完整 Kajiya–Kay 或 Marschner 模型**；真实毛发还包含多种散射与内部传播。对照 [Marschner 等：Light Scattering from Human Hair Fibers](https://graphics.stanford.edu/papers/hair/)。

本例再用 N·L 的正半球约束直接高光。它无法表达逆光透射或头发内部多次散射；不能因为逆光发丝不亮，就先把这个约束删掉并称之为真实头发模型。

## 4. MatCap 的空间约定

基础映射为 `uv = 0.5×Nview.xy+0.5`，从预制的“材质球图”取颜色。它编码了一种已设计的光照外观，常用来稳定显示陶瓷、金属或头发装饰光。

本例使用最基础的观察空间法线映射，不做透视偏斜、相机 roll 稳定或镜面相机修正。它不是世界环境反射：场景灯旋转时图案不会自动跟随灯；转动物体/相机则通过 Nview 改变取样。在完美球体上绕中心观察时，整体图案可能看似仍固定在屏幕上，应同时比较非球形对象或表面固定位置。

固定 UTS 的 MatCap 路径包含视方向修正、正交/透视选择、相机 roll 控制、旋转 UV、遮罩与阴影合成。参见 [UTS MatCap 文档](https://github.com/Unity-Technologies/com.unity.toonshader/blob/1520a78a95292cb045f1edb4d60ea0dba2f213b3/com.unity.toonshader/Documentation~/MatCap.md) 与 [URP 主体实现](https://github.com/Unity-Technologies/com.unity.toonshader/blob/1520a78a95292cb045f1edb4d60ea0dba2f213b3/com.unity.toonshader/Runtime/Shaders/URP/UniversalToonBodyDoubleShadeWithFeather.hlsl)。

## 5. 完整 Unity 实验

保存为 `E06MaterialResponse.shader`，创建材质赋给有法线/切线的 Capsule 或 Sphere。Highlight Mask 默认白色，不需要外部遮罩。

```shaderlab
Shader "Encyclopedia/E06MaterialResponse"
{
    Properties
    {
        [Enum(ToonSpecular,0,Strand,1,MatCap,2)] _Mode("Response", Float) = 0
        _BaseColor("Base Color", Color) = (0.12,0.08,0.03,1)
        [HDR] _SpecColor("Highlight Color", Color) = (1,0.65,0.2,1)
        _SpecThreshold("NdotH Threshold", Range(0,1)) = 0.95
        _SpecFeather("Threshold Half Width", Range(0.001,0.1)) = 0.01
        _Exponent("Strand Exponent", Range(1,128)) = 40
        _Shift("Strand Axis Shift", Range(-1,1)) = 0.2
        [Toggle] _FlowAlongV("Use V As Flow Direction", Float) = 1
        _HighlightMask("Highlight Mask (data)", 2D) = "white" {}
        _MatCap("Linear Runtime MatCap", 2D) = "gray" {}
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            Cull Back ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            TEXTURE2D(_HighlightMask); SAMPLER(sampler_HighlightMask);
            TEXTURE2D(_MatCap); SAMPLER(sampler_MatCap);
            CBUFFER_START(UnityPerMaterial)
                float4 _BaseColor, _SpecColor;
                float _Mode, _SpecThreshold, _SpecFeather, _Exponent, _Shift, _FlowAlongV;
            CBUFFER_END
            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float4 tangentOS : TANGENT;
                float2 uv : TEXCOORD0;
            };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionWS : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
                float4 tangentWS : TEXCOORD2;
                float2 uv : TEXCOORD3;
            };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionWS = TransformObjectToWorld(i.positionOS.xyz);
                o.positionCS = TransformWorldToHClip(o.positionWS);
                o.normalWS = TransformObjectToWorldNormal(i.normalOS);
                o.tangentWS = float4(TransformObjectToWorldDir(i.tangentOS.xyz, false),
                                    i.tangentOS.w * GetOddNegativeScale());
                o.uv = i.uv;
                return o;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                float3 n = normalize(i.normalWS);
                if (_Mode > 1.5)
                {
                    float3 nv = TransformWorldToViewDir(n,true);
                    return float4(SAMPLE_TEXTURE2D(_MatCap,sampler_MatCap,nv.xy*0.5+0.5).rgb,1);
                }
                Light light = GetMainLight();
                float3 v = GetWorldSpaceNormalizeViewDir(i.positionWS);
                float3 sum = light.direction + v;
                float validH = dot(sum,sum) > 1e-8 ? 1 : 0;
                float3 h = sum * rsqrt(max(dot(sum,sum),1e-8));
                float spec;
                if (_Mode < 0.5)
                {
                    spec = smoothstep(_SpecThreshold-_SpecFeather,
                                      _SpecThreshold+_SpecFeather,saturate(dot(n,h)));
                }
                else
                {
                    float3 tangent = i.tangentWS.xyz - n * dot(n,i.tangentWS.xyz);
                    if (dot(tangent,tangent) < 1e-8 || abs(i.tangentWS.w) < 0.5)
                        return float4(1,0,1,1);
                    tangent = normalize(tangent);
                    float3 bitangent = normalize(cross(n,tangent)) * i.tangentWS.w;
                    float3 flow = _FlowAlongV > 0.5 ? bitangent : tangent;
                    flow = normalize(flow + _Shift*n);
                    float th = dot(flow,h);
                    spec = pow(sqrt(saturate(1-th*th)),_Exponent);
                }
                float mask = SAMPLE_TEXTURE2D(_HighlightMask,sampler_HighlightMask,i.uv).r;
                float nl = saturate(dot(n,light.direction));
                float baseBand = lerp(0.3,1.0,step(0.5,nl));
                float3 directSpec = _SpecColor.rgb * spec * mask * validH * nl *
                                    light.color * light.distanceAttenuation;
                return float4(_BaseColor.rgb * baseBand + directSpec,1);
            }
            ENDHLSL
        }
    }
}
```

保存下面代码为 `E06MatCapTexture.cs`，挂到使用该材质的 MeshRenderer。进入 Play 后生成一张蓝灰底、亮斑和暗带的教学 MatCap；数值直接按线性颜色写入。真实美术 sRGB 颜色图则应按其编码正确解码。

```csharp
using UnityEngine;

[RequireComponent(typeof(MeshRenderer))]
public class E06MatCapTexture : MonoBehaviour
{
    MeshRenderer target;
    Material original, owned;
    Texture2D texture;
    void OnEnable()
    {
        if (!Application.isPlaying) return;
        target = GetComponent<MeshRenderer>();
        original = target.sharedMaterial;
        if (original == null || !original.HasProperty("_MatCap")) return;
        owned = new Material(original);
        const int size = 128;
        texture = new Texture2D(size,size,TextureFormat.RGBA32,false,true)
        {
            name = "E06 Runtime MatCap",
            filterMode = FilterMode.Bilinear,
            wrapMode = TextureWrapMode.Clamp
        };
        var pixels = new Color[size*size];
        for (int y=0; y<size; ++y)
        for (int x=0; x<size; ++x)
        {
            float u=(x+0.5f)/size, v=(y+0.5f)/size;
            float dx=u-0.35f, dy=v-0.75f;
            float spot=Mathf.Exp(-(dx*dx/0.012f+dy*dy/0.025f));
            float band=Mathf.Exp(-Mathf.Pow((v-0.35f)/0.07f,2));
            Color c=new Color(0.08f,0.12f,0.2f,1)*(1-0.7f*band) +
                    new Color(0.9f,0.8f,0.55f,0)*spot;
            c.a=1;
            pixels[y*size+x]=c;
        }
        texture.SetPixels(pixels);
        texture.Apply(false,false);
        owned.SetTexture("_MatCap",texture);
        target.sharedMaterial=owned;
    }
    void OnDisable()
    {
        if(target!=null && owned!=null && target.sharedMaterial==owned) target.sharedMaterial=original;
        if(owned!=null) Destroy(owned);
        if(texture!=null) Destroy(texture);
        owned=null; texture=null;
    }
}
```

### 操作与预期

1. URP Forward、Linear、单方向主光、透视相机；关闭阴影、GI、附加光、后处理、SSAO、Depth Priming、GPU Resident Drawer 与其他 Feature。使用 Capsule，并在旁边放一个缩放不同的 Cube/球作为形体对照。
2. ToonSpecular：固定物体，分别转灯和相机。观察高光是否随 L/V 改变，增加阈值是否缩小高光。不要同时改灯光强度掩盖高光形状。
3. Strand：比较 Use V 与 Use U、Shift 的正负值和 Exponent。洋红表示切线基缺失或退化，应修网格数据；不是把指数调小就能解决。
4. MatCap：进入 Play 后通过对象 Renderer 的**当前克隆材质**选择模式。旋转灯不应改变这个独立 MatCap；旋转物体、相机或 camera roll 则比较不同表面位置的映射。
5. 给高光模式选择低底色、有色锐高光，比较风格化金属；给 Strand 较深底色和更长的流向，比较头发带。差异来自模型和数据，不是材质名称。
6. 若自行添加 Highlight Mask，按数据图处理 sRGB，先用明确黑白区域验证位置。MatCap 模式在本例独立输出，不使用该高光遮罩。

示例只含主体颜色 Pass，不含阴影、法线输出、透明发丝、骨骼自定义数据或时间稳定处理。MatCap 无 Mip，窄高光也可能闪烁；实际角色还需检查视角范围、抗锯齿、HDR 与后处理。

## 6. 自测与证据边界

1. **只依赖 N·L 的亮斑能完整表示镜面响应吗？** 不能，通常还需要 V 或预制观察空间约定。
2. **发流必定沿网格 tangent 吗？** 不一定，可能沿副切线或独立梳理方向。
3. **MatCap 为什么不随场景灯转？** 本例直接查预制颜色，没有使用灯作为取样输入。
4. **金色高光加黄色底色就是物理金属吗？** 不是，真实反射模型有额外方向、环境和能量条件。
5. **UTS 的 MatCap 能否用两行 Nview.xy 公式完全概括？** 不能，固定实现还有相机与采样修正及合成规则。

已核对固定 UTS 高光/MatCap、Graphics SpaceTransforms、毛发与导体的原始资料，并核对本地 Texture2D 与 Mesh 数据 API。文档根目录 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。**Unity 编译、实际外观与 GPU 性能未实测**。

前一张：[E05 法线用途](E05-美术法线平滑法线与轮廓法线.md)。下一张：[E07 反壳描边](E07-反壳描边与宽度控制.md)。实践汇总：[E 阶段检查点](../实验/E阶段检查点.md)。
