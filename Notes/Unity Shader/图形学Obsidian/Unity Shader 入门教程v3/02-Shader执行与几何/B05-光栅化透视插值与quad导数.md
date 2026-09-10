# B05｜光栅化、透视插值与 quad 导数

> 核心问题：三角形怎样变成片元输入？为什么倾斜表面的 UV 不能简单按屏幕位置线性插值？`ddx` 又从哪里得到邻居？
>
> 结论：光栅化先确定采样覆盖，再按插值规则产生属性。普通表面属性通常需要透视校正；片元导数借助局部执行分组估计屏幕变化率，并不是对源码公式做符号求导。

本卡自包含，面向 Unity URP NPR（非真实感渲染）。文档基线为 Unity 6.7 Beta / 6000.7（2026-06-26）；示例采用 Graphics 固定提交 `275a7f9ad9330e3cf7f3ea57a0b242a551fde291` 的 Core/URP 17.0.4 公共接口。首先讨论普通单采样、无可变速率着色的三角形；MSAA、Early-Z 和时间抗锯齿仅指出边界，不在这里完整展开。

## 1. Pixel、sample、fragment 与 invocation

| 概念 | 本卡定义 |
| --- | --- |
| Pixel 像素 | 输出图像上的一个离散位置 |
| Sample 样本 | 在像素区域内用于覆盖、深度模板等判断的采样位置 |
| Fragment 片元 | 图元光栅化产生、携带属性与覆盖信息的候选贡献 |
| Invocation 执行实例 | 一次片元 Shader 的逻辑执行，未必最终写入目标 |

三角形覆盖某个采样点，并不保证最终写颜色：还可能被深度、模板、Shader 裁弃和写掩码等机制阻止。多个重叠三角形可以为同一个像素产生多个候选贡献。

在常见单采样规则中，覆盖判断参考像素中心。边界上需要约定归属，例如 D3D 的 top-left 规则让共享边上的样本归到相邻三角形之一，避免两边都包含。它不是“只要碰到像素小方格就覆盖”。MSAA 改为多个样本位置测试，也不必为每个样本独立执行完整片元着色。[Microsoft 光栅化规则](https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-rasterizer-stage-rules)

## 2. 重心坐标是插值权重

投影后三角形的三个点为 `P₀,P₁,P₂`。点 P 的屏幕重心坐标 `λ₀,λ₁,λ₂` 满足：

$$P=\lambda_0P_0+\lambda_1P_1+\lambda_2P_2,\qquad\sum_i\lambda_i=1$$

在理想非退化三角形内部，权重非负。可用有向子三角形面积与总面积之比求权重；边界是否纳入仍由覆盖规则决定，不能仅用浮点 `λ≥0` 逐位复刻 GPU。

对屏幕仿射属性，插值为 `a_affine=Σλᵢaᵢ`。但一个透视投影后的屏幕中点，通常不是原三维线段的中点。

## 3. 透视校正为何需要 w

VS 输出裁剪坐标 `(x_c,y_c,z_c,w_c)`；透视除法把位置变为 `(x_c/w_c,y_c/w_c,z_c/w_c)`。一般表面属性的透视校正插值为：

$$a(P)=\frac{\sum_i\lambda_i\,a_i/w_i}{\sum_i\lambda_i/w_i}$$

可理解为在屏幕上插值 `a/w` 与 `1/w`，再相除。公式要求对应的有效裁剪和投影条件；跨相机平面的原始三角形不能跳过裁剪直接套算。

反例：一条边两端的属性为 `0,1`，裁剪 w 为 `1,4`。屏幕中点权重各 0.5：

$$a=\frac{0.5\times0/1+0.5\times1/4}{0.5/1+0.5/4}=0.2$$

直接屏幕线性插值却得到 0.5。使用后者给斜面贴图，会造成纹理变形，并可能显出三角形划分。正交投影中各顶点 w 相同时，两种公式退化为同一种插值。

普通 HLSL varying 默认通常采用透视校正；`noperspective` 表达屏幕线性插值，`nointerpolation` 表达不插值，其他修饰符还影响采样位置。具体支持取决于目标后端。下面通过数值构造演示仿射插值，避免把某个修饰符当作全平台前提。

## 4. quad 导数怎样产生

普通片元路径经常以 2×2 的局部位置组织导数计算。`ddx(v)` 估计值沿屏幕 x 的变化，`ddy(v)` 沿 y；结果单位是“v 的单位 / 屏幕像素间隔”。这是局部差分模型，不是去读取邻近像素已经写入颜色缓冲的值。[HLSL ddx](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-ddx)

例如某个线性场在 2×2 位置的值为：

```text
0.10  0.12
0.13  0.15
```

在按图定义的 +x/+y 方向上，差分分别为 `0.02` 和 `0.03`；`fwidth(v)=abs(ddx(v))+abs(ddy(v))=0.05`。它是两方向绝对变化量之和，不是欧氏梯度长度。[HLSL fwidth](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-fwidth)

三角形边缘处可能执行用于导数的 helper invocation（辅助实例），即使它不对应该图元的有效覆盖写入。因此“一像素一线程”和“四个实例都必须可见”都不可靠。quad 与 wave 也不同：一个 wave 可以包含多个局部分组，不能把它们画成同一个概念。

普通 `ddx/ddy` 不保证总与自己选定的一对邻居作差；fine/coarse 语义与实现允许差别。在非一致控制流里临时计算导数，参与位置可能不完整，结果可能未定义或不适合原算法。稳妥做法是在需要分歧之前计算连续坐标的梯度，再按需要传给显式梯度采样。

## 5. fwidth 如何帮助 NPR 阈值

卡通色阶 `step(t,v)` 在阈值 t 处跳变，微小移动可能让一列像素突然换色。可用局部变化量估算约一个像素宽的过渡：

$$w=\max(\operatorname{fwidth}(v),\epsilon),\qquad
c=\operatorname{smoothstep}(t-w/2,t+w/2,v)$$

这只是局部平滑近似，不是准确积分，也不等于 MSAA 或时间抗锯齿。它通常适合连续标量场的单条边界；高频条纹、远处多个边界落入同一像素、压缩跳变和不连续 UV 需要额外处理。缩小阈值锯齿时还要检查是否破坏作者想要的硬边风格。

## 6. 完整实验：透视、仿射与导数视图

保存为 `B05InterpolationLab.shader`，在 URP Forward 的透视相机前放一个有 UV 的 Quad，绕 Y 轴转约 60°，使两侧距相机不同且整个 Quad 位于近、远裁剪面之间。关闭后处理、SSAO、Depth Priming、额外 Renderer Feature、XR、MSAA 和动态分辨率。

```shaderlab
Shader "Encyclopedia/B05InterpolationLab"
{
    Properties
    {
        [Enum(PerspectiveUV,0,AffineUV,1,Derivatives,2,Threshold,3)] _Mode("View",Float)=0
        _Threshold("Threshold",Range(0,1))=0.5
        _DerivativeScale("Derivative Display Scale",Float)=32
        _AA("Threshold AA (0 or 1)",Range(0,1))=1
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            Cull Off
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Mode, _Threshold, _DerivativeScale, _AA;
            CBUFFER_END
            struct A { float3 p:POSITION; float2 uv:TEXCOORD0; };
            struct V {
                float4 p:SV_POSITION;
                float2 uv:TEXCOORD0;
                float3 affinePack:TEXCOORD1;
            };
            V Vert(A input)
            {
                V o;
                o.p=TransformObjectToHClip(input.p);
                o.uv=input.uv;
                o.affinePack=float3(input.uv*o.p.w,o.p.w);
                return o;
            }
            half4 Frag(V input):SV_Target
            {
                float2 affineUV=input.affinePack.xy/input.affinePack.z;
                float dx=ddx(input.uv.x);
                float dy=ddy(input.uv.x);
                float width=max(abs(dx)+abs(dy),1e-5);
                float3 color;
                if(_Mode<0.5) color=float3(input.uv,0);
                else if(_Mode<1.5) color=float3(affineUV,0);
                else if(_Mode<2.5)
                    color=float3(abs(dx),abs(dy),width)*_DerivativeScale;
                else
                {
                    float hard=step(_Threshold,input.uv.x);
                    float soft=smoothstep(_Threshold-width*0.5,
                                         _Threshold+width*0.5,input.uv.x);
                    float value=_AA>0.5 ? soft : hard;
                    color=float3(value,value,value);
                }
                return half4(saturate(color),1);
            }
            ENDHLSL
        }
    }
}
```

为什么 `affinePack` 有效？其 xy 默认插值后为 `Σλᵢuvᵢ / D`，z 为 `1/D`，其中 `D=Σλᵢ/wᵢ`；相除得到 `Σλᵢuvᵢ`。这里用的是自己传递的 varying，不是误把片元 `SV_POSITION.w` 当作原 VS 的 w。

预测：正对相机且所有顶点深度相同时，两种 UV 接近一致；倾斜后不同。导数视图表示当前像素尺度下的 UV 变化，颜色显示会裁到 `[0,1]`，不是原始导数读回。阈值模式中缓慢移动相机，比较 AA 开关，记录边缘变化；不得预填“完全不闪烁”。

代码使用的变换入口见 [固定提交 SpaceTransforms.hlsl](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.core/ShaderLibrary/SpaceTransforms.hlsl)。插值和导数来自图形 API/硬件执行语义，不由该变换函数的源码实现。

## 7. 自测与验证边界

① UV 为什么要除以插值后的 `1/w`？**屏幕权重不等于原表面权重。** ② helper 的输出必然写入颜色吗？**不是。** ③ fwidth 是固定世界宽度吗？**不是，它跟屏幕变化率有关。** ④ 光栅覆盖通过就一定显示吗？**还有后续可见性与输出规则。**

本文给出可直接核算的重心/透视数值、仿射构造和差分模型；这些模型不等于硬件覆盖或 helper 调度。实践以文内 Unity Shader 的预测和观察为准，示例尚未在 Unity 编译、运行或抓帧。下一张：[B06｜纹理采样、Mip、LOD 与过滤](B06-纹理采样MipLOD与过滤.md)。
