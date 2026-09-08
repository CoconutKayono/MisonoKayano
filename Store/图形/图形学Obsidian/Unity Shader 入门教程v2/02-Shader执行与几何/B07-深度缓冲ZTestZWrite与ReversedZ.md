# B07｜深度缓冲、ZTest、ZWrite 与 Reversed-Z

> 核心问题：深度值是不是“离相机多远”？`ZWrite Off` 是否让对象穿墙？为什么 Reversed-Z 平台上仍常写 `ZTest LEqual`？
>
> 结论：原始深度是投影编码后的数值，不通常等于距离。深度比较和深度写入是不同控制；Unity 的 ShaderLab 状态还需经后端转换，不能把原生深度比较方向直接当作跨平台 ShaderLab 写法。

本卡独立说明普通光栅化深度。文档依据 Unity 6.7 Beta / 6000.7（2026-06-26），源码固定 Graphics `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`、Core/URP 17.0.4。主要数学模型采用近面 n>0、远面 f>n、有限远面的普通透视投影；z 是沿相机前向的正眼空间深度。斜截投影、自定义 SV_Depth、深度偏置和 MSAA 的完整规则不在本卡范围内。

## 1. 三种“深度”先分开

| 数值 | 含义 |
| --- | --- |
| 原始设备深度 d | 投影与视口编码后用于深度测试的数值，常在 `[0,1]` |
| 眼空间线性深度 z | 沿相机前向轴的距离分量，单位与场景一致 |
| 欧氏距离 r | 点到相机位置的三维距离 |

在以 +Z 为前方的教学观察坐标里，点 `(3,0,4)` 的 z=4、r=5。它们都不是原始深度。Unity 的视图矩阵惯用轴方向还需相应处理，不能把例子的 +Z 直接当作所有 Unity 矩阵的符号。

深度缓冲通常为每个深度样本保存一个值，用于后续比较；它不保存全部被遮挡表面的距离列表。原始深度也不是把 VS 的 z 值原封不动写入：通常涉及 `z_clip/w_clip` 和深度映射。正常投影后的设备深度在屏幕三角形上具有相应线性插值关系，不要再对它套一次普通 UV 的透视校正公式。

## 2. 普通透视深度为什么集中在近处

在近面编码为 0、远面为 1 的模型里：

$$d(z)=\frac{f}{f-n}-\frac{fn}{(f-n)z}=A-\frac{B}{z}$$

其反函数为：

$$z(d)=\frac{fn}{f-d(f-n)}$$

取 `n=0.1,f=100`：

| 眼空间 z | 普通 d | 反向 dᵣ=1−d |
| --- | --- | --- |
| 0.1 | 0 | 1 |
| 1 | 约 0.900901 | 约 0.099099 |
| 10 | 约 0.990991 | 约 0.009009 |
| 100 | 1 | 0 |

所以普通深度图看起来大部分接近白色，不一定是损坏。`d=0.5` 在这个例子中只对应约 `z=0.199800`，远非近远面的距离中点 `50.05`。

正交投影的正常编码则可为 `(z-n)/(f-n)`，具有不同反函数。使用一个只适用于透视的线性化函数处理正交相机，会产生错误。

## 3. ZTest 与 ZWrite 是两道独立决策

下面先按“普通 d 越小越近”的原始数值模型计算：

| 已存 d | 新 d | 比较 | 是否允许当前贡献通过 | ZWrite Off 时已有 d |
| --- | --- | --- | --- | --- |
| 0.4 | 0.7 | `new≤stored` | 否 | 0.4 |
| 0.4 | 0.2 | `new≤stored` | 是 | 仍为 0.4 |
| 0.4 | 0.7 | Always | 是 | 仍为 0.4 |

若第二行启用写入且其他必要条件通过，新的深度可更新为 0.2。因此 **ZWrite Off 不会自动关闭深度测试**；它让后面的绘制不能通过这个对象新写入的深度获得遮挡信息。

`ZTest Always` 与 `ZWrite On` 可以使本来较远的对象覆盖已有颜色并更新深度，影响后续对象。`ColorMask 0` 只阻止颜色通道写入，不天然阻止深度或模板更新；输出 Alpha=0 也不自动关闭深度写入，效果取决于混合、裁弃和状态。

Unity 的状态语义分别见 [ZTest](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-ZTest.html) 与 [ZWrite](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-ZWrite.html)。这里说明可观察结果，不把测试固定安排在片元着色之前或之后；Early-Z/Late-Z 另有条件，下一阶段 C01 解释。

## 4. Reversed-Z 改变编码方向

反向编码把近面映射到 1、远面映射到 0。本卡有限远面模型下：

$$d_r=1-d,\qquad z(d_r)=\frac{fn}{n+d_r(f-n)}$$

直接操作原生比较时，“更近或相等”应从普通模型的 `new≤stored` 变为反向模型的 `new≥stored`，背景清除值也需匹配方向。但在 Unity 常规 ShaderLab 中，应使用其抽象语义和引擎映射；不能看到 `UNITY_REVERSED_Z` 就手工把所有 `ZTest LEqual` 改成 `GEqual`。

通过 `SystemInfo.usesReversedZBuffer` 或 Shader 的 `UNITY_REVERSED_Z` 判断当前路径，而不是仅凭显卡品牌猜测。[Unity 查询接口](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SystemInfo-usesReversedZBuffer.html)、[平台差异说明](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-PlatformDifferences.html)

Reversed-Z 的重要收益来自与浮点深度分布配合：浮点在接近零的范围具有更密的绝对数值间隔，能够改善透视深度精度分布。**仅把固定点 UNorm 深度的码值倒过来，不会凭空增加编码数量或改变对应的间距集合。** 实际收益取决于格式和投影路径。[NVIDIA 深度精度可视化](https://developer.nvidia.com/blog/visualizing-depth-precision/)

由 `dd/dz=B/z²` 得到局部误差关系 `δz≈z²δd/B`。在上述 n/f、普通 24 位 UNorm 模型下，z=10 的一个码值间隔约对应 `0.0000595` 个场景单位，z=100 附近约 `0.00595`。它是局部一阶估算，不是任意深度格式的硬件误差上限。近面过近、共面表面、变换精度与偏置都可能影响 Z-fighting，不能只调整一个开关。

## 5. 线性化源码与“相机深度纹理”

固定提交 [Common.hlsl](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl) 的两参数 `LinearEyeDepth(depth,zBufferParam)` 计算：

$$z=1/(zBufferParam.z\times depth+zBufferParam.w)$$

注释明确该重载不适用于正交和斜截投影。函数依赖匹配该相机与编码的参数；不能从别的相机拿一份 `_ZBufferParams` 处理任意深度图。

同文件的 `Linear01Depth` 在正常透视条件下表达近似 z/f，即相机位置为 0、远面为 1；它不是默认把近裁剪面归零。不要把它与 `(z-n)/(f-n)` 混淆。

**深度附件**是当前深度测试使用的存储；**相机深度纹理**是管线提供给 Shader 采样的资源，可能通过预通道或复制得到。两者的生产时点、包含的对象与可采样格式不一定相同。ZWrite On 不能保证对象在任意时点的 `_CameraDepthTexture` 中存在；正式 URP 生产路径在 D05 单独追踪。

## 6. 完整实验：同一材质分别控制比较和写入

保存为 `B07DepthLab.shader`，创建两个材质分别用于近处红物体、远处蓝物体，令它们在屏幕上部分重叠。使用普通透视 URP Forward 相机，关闭 Depth Priming、SSAO、后处理、额外 Renderer Feature、MSAA 和 XR，避免额外深度 Pass 干扰。

```shaderlab
Shader "Encyclopedia/B07DepthLab"
{
    Properties
    {
        _Color("Color",Color)=(1,0,0,1)
        [Enum(UnityEngine.Rendering.CompareFunction)] _ZTest("ZTest",Float)=4
        [Enum(Off,0,On,1)] _ZWrite("ZWrite",Float)=1
        [Enum(Color,0,IncomingRawDepth,1,IncomingEyeDepth,2)] _View("View",Float)=0
        _EyeRange("Eye Depth Display Range",Float)=10
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            ZTest [_ZTest]
            ZWrite [_ZWrite]
            Blend Off
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _Color;
                float _ZTest, _ZWrite, _View, _EyeRange;
            CBUFFER_END
            float4 Vert(float3 position:POSITION):SV_POSITION
            {
                return TransformObjectToHClip(position);
            }
            half4 Frag(float4 position:SV_POSITION):SV_Target
            {
                if(_View<0.5) return _Color;
                float value=position.z;
                if(_View>1.5)
                    value=LinearEyeDepth(position.z,_ZBufferParams)/max(_EyeRange,1e-4);
                return half4(saturate(value),saturate(value),saturate(value),1);
            }
            ENDHLSL
        }
    }
}
```

使用材质 Render Queue 设置或调试 Inspector，把近处红材质设为 2000、远处蓝材质设为 2001，并在 Frame Debugger 确认红先蓝后。队列值用于控制测试顺序，最终以实际事件为准；只按 Hierarchy 列表位置推断绘制顺序不可靠。

| 状态修改 | 重叠区域的预测 |
| --- | --- |
| 两者 LEqual、ZWrite On | 红先写近深度，蓝被挡住 |
| 红 ZWrite Off；蓝仍 LEqual | 红不更新深度，后画蓝可覆盖红；前提是无其他遮挡深度 |
| 红写深度；蓝改 Always | 蓝可覆盖红，且蓝若写深度会影响后续绘制 |
| 恢复深度状态，切换 View | 显示当前通过到可见输出的片元自身原始/眼空间深度 |

最后两种视图**没有采样深度缓冲**，显示的是当前输入片元的 `SV_POSITION.z` 及其线性化，不可拿它证明 `_CameraDepthTexture` 的内容。EyeDepth 视图仅适用于上述普通透视相机，超过 EyeRange 会饱和。

## 7. NPR 应用与自测

面部遮挡、头发裁剪、描边和局部覆盖都依赖正确的深度语义。透明对象常关闭写入，但仍需深度测试和排序策略；反壳描边若无意写入错误深度，可能挡住本应出现的主体或特效。用深度差做描边时，先把两份数据转换到相同、有明确单位的表示，再设置阈值。

① ZWrite Off 等于穿墙吗？**不等于关闭测试。** ② 原始 0.5 是相机距离中点吗？**透视下通常不是。** ③ 所有 Linear01Depth 都把近面归零吗？**必须看具体函数。** ④ 反向深度应在每个 Unity Shader 手动翻比较吗？**不能绕过引擎抽象机械翻转。**

验证状态：投影端点、反函数、距离与比较/写入例子属于文内数学模型；实践使用红蓝物体的 Unity 对照实验。Shader 尚未在 Unity 编译、运行或抓帧。已核对本地 `Manual/SL-ZTest.html`、`SL-ZWrite.html`、`SL-PlatformDifferences.html`、`ScriptReference/SystemInfo-usesReversedZBuffer.html`，根目录为 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。

下一张：[B08｜Stencil 模板测试与操作](B08-Stencil模板测试与操作.md)。
