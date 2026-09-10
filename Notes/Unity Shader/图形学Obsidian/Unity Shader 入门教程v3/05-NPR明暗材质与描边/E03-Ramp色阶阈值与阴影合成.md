# E03｜Ramp、色阶阈值与阴影合成

> 核心问题：先把朝向变成色阶再乘阴影，与先乘阴影再查 Ramp，为什么完全不是同一种画面？本卡用可切换的三种合成规则，明确每个输入的含义。

## 1. Ramp 是一个函数，不只是渐变图片

Ramp 将输入标量 q 映射为输出值或颜色：`R(q)`。输入可以是 N·L、Half-Lambert、归一化亮度或人工控制量；横坐标不是天然的物理照度。输出可以是颜色，也可以是权重，必须先约定。

本卡 q 为 `saturate(0.5×dot(N,L)+0.5)`，N 是单位世界法线，L 是表面到主方向光的方向。S 为 URP 主光阴影可见性：1 可见、0 遮挡，中间值可能来自过滤、Shadow Strength 或距离淡出。颜色 Ramp 记为 R，投射阴影指定颜色记为 Ccast。

本地文档为 **Unity 6.7 Beta / 6000.7，2026-06-26**。Graphics 固定提交 `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`（URP/Core **17.0.4、Unity 6000.0**）；UTS 固定 `1520a78a95292cb045f1edb4d60ea0dba2f213b3`（**0.15.1-preview、Unity 6000.0**）。示例是教学模型，不是完整 UTS 移植。

## 2. 三种规则与可检验的反例

| 规则 | 公式 | 视觉含义 |
| --- | --- | --- |
| 先查表，再乘可见性 | A = R(q) × S | 投射阴影缩放整个调色板；全遮挡趋向黑 |
| 先合成信号，再查表 | B = R(q × S) | 投射阴影推动 Ramp 坐标，可能跨越色阶 |
| 阴影颜色独立覆盖 | C = lerp(Ccast, R(q), S) | 可明确设计投射阴影颜色，软边在颜色间过渡 |

取一个输出 0/1 的教学 Ramp：`R(x)=step(0.5,x)`。令 q=0.8、S=0.4、Ccast=0.2，则 A=0.4，B=0，C=0.52。这个单通道例子已经证明三者不等价；真实 RGB Ramp 可以同时改变色相与亮度，差异更大。

当 S=0 时：A=0，B=R(0)，C=Ccast。如果你需要暗部保留紫色，直接将整个材质颜色乘 S 会破坏这一要求；可以选择 B 或 C，也可以另建明确的填充光模型。

当 q=0.8、阈值为 0.5，B 在 `S=0.625` 附近跨级。因此 PCF 的平滑 S 经过硬 Ramp 后可能重新变成锐利边界，也可能把细小波动放大为闪烁。空间采样精度和非线性映射要一起考虑。

## 3. GPU 如何采样这张表

一维 Ramp 通常存成窄的二维纹理。对宽度 W，以 `u = (0.5 + q×(W-1))/W` 映射，q=0、1 分别落到首尾 texel 中心。本文使用两行相同颜色，并在 v=0.5 读取。

| 设置 | 对颜色 Ramp 的影响 | 对阈值/控制图的影响 |
| --- | --- | --- |
| sRGB | 美术按 sRGB 绘制的颜色图通常需要正确解码到线性 | 数值图误解码会改变阈值；例如 0.5 约变为 0.214 |
| Bilinear | 邻近色阶之间产生插值，过渡可能只有约一个 texel 宽 | 插值改变边界信号，需和制图约定匹配 |
| Point | 保留离散 texel 颜色，但坐标跨 texel 时突变 | 可能造成台阶与抖动 |
| Mip | 缩小采样足迹可过滤多个色阶，也可能混合你希望分开的颜色 | 普通平均 Mip 不保证保留原阈值边界 |
| Wrap | Repeat 会让越界或端点采样接触另一端 | Clamp 更适合多数非周期阈值表 |
| 压缩/低精度 | 改变颜色，可能出现色带 | 改变跨阈值的角度或位置 |

不能制定“所有 NPR 贴图都关闭 sRGB”的规则。**颜色按颜色语义处理，控制数据按数据语义处理。** 本例程序直接写入约定为线性的数值，故创建 linear=true 的纹理；这不代表美术导入的 PNG 也应照搬相同设置。

## 4. 与 Unity Toon Shader 对照

固定 UTS 的 `UniversalToonBodyDoubleShadeWithFeather.hlsl` 将 Half-Lambert 与受控系统阴影结合，再进入阈值与羽化处理，并使用控制图调整分区；它不是单纯在最后乘一个黑影。

`UniversalToonBodyShadingGradeMap.hlsl` 中，Shading Grade 因子会调制送入分类的信号。其方向可概括为 `控制量 × 受阴影调制的 Half-Lambert`，随后生成多层掩码，最终在 Base/1st Shade/2nd Shade 等颜色之间合成。

对照 [UTS DoubleShadeWithFeather](https://github.com/Unity-Technologies/com.unity.toonshader/blob/1520a78a95292cb045f1edb4d60ea0dba2f213b3/com.unity.toonshader/Runtime/Shaders/URP/UniversalToonBodyDoubleShadeWithFeather.hlsl) 和 [UTS ShadingGradeMap](https://github.com/Unity-Technologies/com.unity.toonshader/blob/1520a78a95292cb045f1edb4d60ea0dba2f213b3/com.unity.toonshader/Runtime/Shaders/URP/UniversalToonBodyShadingGradeMap.hlsl)。这些是算法关系概述，不把本文 Ramp 和 UTS 的控制图参数逐一等同。

## 5. 完整 Unity 实验：程序创建 Ramp，实际接收阴影

保存为 `E03RampShadow.shader`，创建对应材质并赋给 Sphere。此 Shader **只接收阴影**；用另一个 URP/Lit Cube 作为投射者，使本例不依赖其他自定义 Shader。

```shaderlab
Shader "Encyclopedia/E03RampShadow"
{
    Properties
    {
        _Ramp("Linear Color Ramp", 2D) = "white" {}
        _CastShadowColor("Cast Shadow Color", Color) = (0.08,0.05,0.15,1)
        [Enum(RampThenMultiply,0,MultiplyThenRamp,1,ShadowColorOverride,2,DirectionSignal,3,Visibility,4)]
        _Mode("Composition", Float) = 0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "E03Forward"
            Tags { "LightMode"="UniversalForward" }
            Cull Back ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE
            #pragma multi_compile_fragment _ _SHADOWS_SOFT _SHADOWS_SOFT_LOW _SHADOWS_SOFT_MEDIUM _SHADOWS_SOFT_HIGH
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            TEXTURE2D(_Ramp);
            SAMPLER(sampler_Ramp);
            CBUFFER_START(UnityPerMaterial)
                float4 _Ramp_TexelSize;
                float4 _CastShadowColor;
                float _Mode;
            CBUFFER_END
            struct Attributes { float4 positionOS : POSITION; float3 normalOS : NORMAL; };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionWS : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
            };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionWS = TransformObjectToWorld(i.positionOS.xyz);
                o.positionCS = TransformWorldToHClip(o.positionWS);
                o.normalWS = TransformObjectToWorldNormal(i.normalOS);
                return o;
            }
            float3 Ramp(float q)
            {
                float edge = 0.5 * _Ramp_TexelSize.x;
                float u = lerp(edge, 1.0 - edge, saturate(q));
                return SAMPLE_TEXTURE2D(_Ramp, sampler_Ramp, float2(u,0.5)).rgb;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                float4 sc = TransformWorldToShadowCoord(i.positionWS);
                Light light = GetMainLight(sc, i.positionWS, half4(1,1,1,1));
                float q = saturate(0.5 * dot(normalize(i.normalWS), light.direction) + 0.5);
                float s = saturate(light.shadowAttenuation);
                float3 color;
                if (_Mode < 0.5) color = Ramp(q) * s;
                else if (_Mode < 1.5) color = Ramp(q * s);
                else if (_Mode < 2.5) color = lerp(_CastShadowColor.rgb, Ramp(q), s);
                else if (_Mode < 3.5) color = q.xxx;
                else color = s.xxx;
                return float4(color,1);
            }
            ENDHLSL
        }
    }
}
```

保存下面代码为 `E03RampTexture.cs`，挂到使用上述材质的 Sphere。进入 Play 时自动创建两行 256 texel 的三色表，克隆材质后绑定；退出/禁用时只释放自己创建的对象。

```csharp
using UnityEngine;

[RequireComponent(typeof(MeshRenderer))]
public class E03RampTexture : MonoBehaviour
{
    MeshRenderer target;
    Material original, owned;
    Texture2D ramp;
    void OnEnable()
    {
        if (!Application.isPlaying) return;
        target = GetComponent<MeshRenderer>();
        original = target.sharedMaterial;
        if (original == null || !original.HasProperty("_Ramp"))
        {
            Debug.LogWarning("E03: assign the E03RampShadow material first.", this);
            return;
        }
        owned = new Material(original);
        ramp = new Texture2D(256, 2, TextureFormat.RGBA32, false, true)
        {
            name = "E03 Runtime Linear Ramp",
            wrapMode = TextureWrapMode.Clamp,
            filterMode = FilterMode.Bilinear
        };
        var pixels = new Color[256 * 2];
        for (int x = 0; x < 256; ++x)
        {
            float q = x / 255f;
            Color c = q < 0.4f ? new Color(0.08f,0.05f,0.18f,1) :
                      q < 0.7f ? new Color(0.4f,0.18f,0.2f,1) :
                                 new Color(1,0.65f,0.32f,1);
            pixels[x] = pixels[256 + x] = c;
        }
        ramp.SetPixels(pixels);
        ramp.Apply(false, false);
        owned.SetTexture("_Ramp", ramp);
        target.sharedMaterial = owned;
    }
    void OnDisable()
    {
        if (target != null && owned != null && target.sharedMaterial == owned)
            target.sharedMaterial = original;
        if (owned != null) Destroy(owned);
        if (ramp != null) Destroy(ramp);
        owned = null;
        ramp = null;
    }
}
```

### 基线与观察

1. URP Forward、Linear、单相机、主方向光实时阴影。关闭附加光、屏幕空间阴影 Feature、后处理、SSAO、Depth Priming、MSAA、GPU Resident Drawer 和其他 Feature。先用 Hard Shadows，再做 Soft 对照。
2. 放置 Sphere 作为接收者，URP/Lit Cube 放在主光与球之间，使影子跨过球的亮面。用 Visibility 模式确认球上存在 S<1 的区域；Cube 可先水平移动寻找投影位置。
3. 进入 Play 后，组件替换为运行时克隆材质。通过 Sphere 的 Renderer 材质槽打开**当前实例材质**修改 Composition，避免只修改未被使用的原始资产。
4. DirectionSignal 模式确认 q 不受遮挡物平移影响；Visibility 模式确认 S 的阴影随 Cube 移动。随后保持场景不动，依次查看 A/B/C。
5. A 的全遮挡部分趋于黑；B 进入 Ramp 左端紫色；C 进入 Cast Shadow Color。切 Soft Shadows 后，比较边缘是否保持连续颜色或重新跨入硬色阶。
6. 修改主光 Shadow Strength，比较可见性变化如何进入三种模型。此例没有乘 `light.color`，调色板颜色有意独立于主光色与强度，不能用调灯强来验证最终颜色亮度。
7. 把 Ramp 过滤从 Bilinear 改为 Point，观察过渡与移动边界；之后恢复。程序表无 Mip，远处 aliasing 是待解决的问题，不把这套设置当作所有场景的性能/质量最优解。

真实颜色读取还受目标格式和显示变换影响。若需要验证 q=0.8、S=0.4 的精确数学例子，直接按第 2 节核算；自然场景不保证恰好产生这两个值。

## 6. 多灯与美术控制的进一步约束

`R(q1+q2)` 一般不等于 `R(q1)+R(q2)`。逐灯都生成一套完整亮暗颜色再相加，容易重复累加暗色底、过曝并改变色阶数量。可以明确规定主光控制形体、附加光只调制亮部，或者以统一标量汇总后分类；这是艺术选择，必须与实际光源循环一起实现。

控制图也不一定是最终可见颜色：改变阈值、乘 q、覆盖掩码，三者的语义不同。若角色左右脸需要特定的角度变化，普通 Shading Grade 图与面部角度阈值图不能互换；后者需要另定头部空间与左右约定。

## 7. 自测与验证边界

1. **为何 B 会把软阴影重新变硬？** 连续 S 经过非线性 Ramp，跨阈值时可能突变。
2. **暗部变黑是否一定是灯光强度不足？** 不一定，A 在 S=0 时按公式必为零。
3. **颜色 Ramp 和阈值图能统一关闭 sRGB 吗？** 不能，前者按制作颜色空间决定，后者应保持数值语义。
4. **Bilinear 能保证色阶边缘恒定一像素吗？** 不能，它按纹理坐标过滤，屏幕足迹仍取决于 q 的空间变化。
5. **把 UTS 的 Shading Grade 图当颜色 Ramp 会怎样？** 数据含义不匹配；应先追其输入域、采样和参与运算的位置。

已核对固定 UTS 两种分区实现、URP RealtimeLights/Shadows，以及本地纹理与阴影 API 文档。`Texture2D(..., linear:true)` 和运行时纹理写入可对照 [Texture2D 构造 API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Texture2D-ctor.html)。本地根目录 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。**未进行 Unity 编译、画面验证或 GPU 测时**。

前一张：[E02 阴影生产](E02-阴影图投影Bias与级联.md)。下一张：[E04 面部 SDF 与方向空间](E04-面部SDF与光照方向空间.md)。实验导航：[E01—E04](../实验/E01-E04实验说明.md)。
