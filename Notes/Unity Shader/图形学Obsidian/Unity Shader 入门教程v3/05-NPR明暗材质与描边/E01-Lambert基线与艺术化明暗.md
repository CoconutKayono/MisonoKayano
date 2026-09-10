# E01｜Lambert 基线与艺术化明暗

> 核心问题：一个卡通明暗边界究竟由几何朝向、光照强度，还是美术阈值控制？本卡建立可分解的直接光基线，再明确选择两段色阶的规则。

## 1. 必要概念与适用范围

NPR 指非真实感渲染，赛璐璐明暗是其中一种。它可以使用真实几何和光方向，但不必服从物理材质的颜色分布。实现之前，必须知道自己修改的是哪一层。

对表面位置 P，记单位世界法线为 N，表面指向光源的单位方向为 L。`x = dot(N,L)` 是夹角余弦，范围为 -1 到 1。方向光的 L 不随 P 改变；点光的 L 则由光位置减 P 后归一化得到。Unity 方向光 Transform.forward 表示光线传播方向，作为表面到光方向时通常需取反；使用 `GetMainLight().direction` 可避免再次自行翻转。

本地文档：**Unity 6.7 Beta / 6000.7，2026-06-26 构建**。Graphics 固定提交 `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`，包 manifest 为 **URP/Core 17.0.4、Unity 6000.0**。UTS 固定提交 `1520a78a95292cb045f1edb4d60ea0dba2f213b3`，manifest 为 **0.15.1-preview、Unity 6000.0**。引用快照并不等于这些包已在本地 6000.7 项目验证兼容。

实验使用 PC、URP Forward、Linear 色彩空间、单 Base Game Camera 和一盏方向主光。关闭附加光、阴影、GI/烘焙光、后处理、SSAO、Depth Priming、GPU Resident Drawer 与其他 Renderer Feature。示例没有完整角色 Shader 的辅助 Pass。

## 2. 从投影面积推导 Lambert 角度项

同一束平行光落在倾斜平面上时，能量分布到更大的表面面积，因此单位面积接收量含 `max(0, cosθ)`。这是表面接收光照的几何项，不是“让球变好看的经验乘法”。

理想 Lambert 漫反射 BRDF 为 `f_r = ρ / π`，ρ 是漫反射反照率。对于单方向入射，可写成 `L_o = (ρ/π) × E_perpendicular × max(0,N·L)`。入射照度、辐亮度和引擎灯光 RGB 的单位约定需要单独对应；不能只看到 Unity 代码没有 `/π` 就断言其物理归一化错误。

URP 的工程函数 `LightingLambert(lightColor, lightDir, normal)` 使用角度项乘灯光颜色。本文把它作为可解释的着色基线，不声称自己的简化颜色参数就是完整物理照明标定。[URP Lighting.hlsl](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl)。

| θ | x = cosθ | Lambert：max(0,x) | 本卡 Half-Lambert：(x+1)/2 |
| --- | --- | --- | --- |
| 0° | 1 | 1 | 1 |
| 60° | 0.5 | 0.5 | 0.75 |
| 90° | 0 | 0 | 0.5 |
| 120° | -0.5 | 0 | 0.25 |
| 180° | -1 | 0 | 0 |

Half-Lambert 将背光半球也映射到正值，属于艺术控制。不同资料可能再对该值平方；**本文没有平方**，必须按公式比较，不能只按名称套参数。

## 3. 把方向、遮挡、强度与颜色拆开

一个可设计的 NPR 模型可以分为：

`方向信号 q → 明暗分类 m → 明暗颜色 lerp(Cshade, Clit, m) → 可选光色/强度调制`。

其中 q 可选 Lambert 或 Half-Lambert；m 可为 `step(t,q)`，或有过渡宽度的 `smoothstep(t-w,t+w,q)`。t 是分类阈值，w 是信号域中的过渡半宽。

光源被另一物体挡住时产生的可见性 S 是另一项。`N·L` 只知道局部朝向，不知道前方是否有墙。阴影图解决 S，不能用降低 N·L 阈值来修复漏掉的投射阴影。

光强是否参与分类也应明确选择：

- `step(t,q)`：强度变化通常不移动分界，适合稳定角色色块。
- `step(t,I×q)`：强度 I 变化会移动分界；I 可能大于 1，阈值含义随之改变。
- 将色阶颜色再乘灯光颜色：光色改变输出，但不一定改变分区。

例如 x=0.4、阈值 0.5，纯朝向分类为暗。将光强 2 放入分类得 `step(0.5,0.8)=1`，立刻变亮。这是模型差异，不是浮点误差。

Half-Lambert 阈值 t 对应 `x=2t-1`。t=0.5 的边界在 90°，t=0.75 的边界在 60°；Lambert 的 t=0.5 则在 60°。因此更换信号后照抄阈值，会改变明暗面积。

## 4. Unity Toon Shader 源码对照

固定 UTS 的 URP `UniversalToonBodyDoubleShadeWithFeather.hlsl` 中，基础 Half-Lambert 来自法线和光方向点积的线性重映射；随后结合 Base Step、Feather、阴影控制及贴图决定分区。其法线还可以在顶点法线与扰动法线间选择或混合，所以分界取决于法线来源。[固定 UTS 分区源码](https://github.com/Unity-Technologies/com.unity.toonshader/blob/1520a78a95292cb045f1edb4d60ea0dba2f213b3/com.unity.toonshader/Runtime/Shaders/URP/UniversalToonBodyDoubleShadeWithFeather.hlsl)。

读源码时逐个追问：输入是何种法线、Half-Lambert 是否平方、阈值在哪个域、输出掩码中 1 表示亮还是暗、羽化区在哪一侧。UTS 的完整模型包含多层颜色与控制贴图，不能将下面的双颜色教学例子称为 UTS 复刻。

## 5. 完整 Unity 实验

保存为 `E01LightingBasis.shader`，创建材质选择 `Encyclopedia/E01LightingBasis`，赋给 Sphere 或有正确法线的头模。本卡不依赖任何纹理或其他自定义脚本。

```c
Shader "Encyclopedia/E01LightingBasis"
{
    Properties
    {
        _LitColor("Lit Color", Color) = (1,0.7,0.4,1)
        _ShadeColor("Shade Color", Color) = (0.18,0.12,0.28,1)
        [Enum(Lambert,0,HalfLambert,1)] _Basis("Direction Signal", Float) = 0
        [Enum(Continuous,0,TwoColors,1)] _View("View", Float) = 0
        _Threshold("Threshold", Range(0,1)) = 0.5
        _Feather("Signal Feather Half Width", Range(0,0.3)) = 0.02
        [Toggle] _UseLightColor("Multiply By Main Light Color", Float) = 0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "E01Forward"
            Tags { "LightMode"="UniversalForward" }
            Cull Back ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _LitColor, _ShadeColor;
                float _Basis, _View, _Threshold, _Feather, _UseLightColor;
            CBUFFER_END
            struct Attributes { float4 positionOS : POSITION; float3 normalOS : NORMAL; };
            struct Varyings { float4 positionCS : SV_POSITION; float3 normalWS : TEXCOORD0; };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionCS = TransformObjectToHClip(i.positionOS.xyz);
                o.normalWS = TransformObjectToWorldNormal(i.normalOS);
                return o;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                Light light = GetMainLight();
                float3 n = normalize(i.normalWS);
                float x = dot(n, light.direction);
                float q = _Basis < 0.5 ? saturate(x) : saturate(0.5 * x + 0.5);
                float w = max(_Feather, 0.00001);
                float m = _Feather <= 0 ? step(_Threshold, q) :
                    smoothstep(_Threshold - w, _Threshold + w, q);
                float3 color = _View < 0.5 ? q.xxx : lerp(_ShadeColor.rgb, _LitColor.rgb, m);
                color *= lerp(float3(1,1,1), light.color * light.distanceAttenuation,
                              saturate(_UseLightColor));
                return float4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

### 操作与预期

1. 按第 1 节基线设置场景，方向光指定为 Sun Source。先看 Continuous / Lambert：旋转主光，灰度的正值半球移动，背光半球为零。
2. 改 HalfLambert，保持灯不动：原本 x=0 的位置变为数值 0.5，背面不再全黑。屏幕显示编码会改变视觉亮度，精确值应在颜色附件中读。
3. 改 TwoColors、Feather=0。Lambert 的 Threshold=0.5 与 HalfLambert 的 Threshold=0.75 应产生同一条理论角度边界；这比“两个都设 0.5”更能验证映射。
4. Feather 设为 0.02，过渡发生在信号阈值附近。它是信号宽度，不保证屏幕上恒定两像素；掠射、曲率和距离会改变屏幕宽度。
5. 保持 Multiply By Main Light Color 关闭，改变灯光强度与颜色，分区和调色板输出应保持；开启后颜色受灯光调制，但本例仍不会把强度送入分类阈值。
6. 换 Cube、平滑球和头模。Cube 的平面法线使一整个面共享 q；平滑球的插值法线形成连续边界。若头模面部有细碎明暗，先看法线，而非盲目增加羽化。

没有灯也能看到色块并不代表照明已正确建立：本例的独立调色板有意不乘灯光颜色，必须保留有效的方向主光来定义方向。此例没有接收/投射阴影、DepthNormals、MotionVectors、附加光、XR 或实例化支持。

## 6. 硬件与视觉稳定性

点积与色阶在 fragment Shader 中执行；逐顶点变换后的法线会被插值，必须在片元归一化。若省略归一化，插值长度变化会改变阈值边界，即使法线朝向看似正常。

硬 `step` 引入高频边界，轻微摄像机移动可能改变覆盖采样，造成闪烁。`fwidth` 可依据局部屏幕导数提供空间平滑宽度，但不会修复错误法线或缺失运动矢量，也不等于时间抗锯齿。先确定模型与数据，再在后续稳定性阶段处理采样问题。

## 7. 自测与核验

1. **Lambert 为何含 cosθ？** 投影面积决定单位表面接收的直接照度。
2. **Half-Lambert 是物理漫反射定律吗？** 不是，它是明确扩展背光响应的艺术映射。
3. **相同 0.5 阈值是否在两种信号下表示同一角度？** 不是，分别对应 60° 与 90°。
4. **遮挡物挡住光，N·L 会自动变小吗？** 不会，遮挡需要独立可见性信息。
5. **调色板颜色是否必须乘真实灯色？** 由艺术模型决定，但应明确规则，不能依赖偶然漏乘。

已核对 [URP 自定义光照文档](https://docs.unity3d.com/6000.0/Documentation/Manual/urp/use-built-in-shader-methods-lighting.html)、本地同路径 6000.7 页面、固定 Graphics Lighting/RealtimeLights 和固定 UTS 分区实现。本地文档根目录 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。数学例子可直接按正文核算；**未在 Unity 编译、运行或抓帧**。

前置导航：[D 阶段检查点](../实验/D阶段检查点.md)。下一张：[E02 阴影图、Bias 与级联](E02-阴影图投影Bias与级联.md)。本组实践：[E01—E04 实验说明](../实验/E01-E04实验说明.md)。
