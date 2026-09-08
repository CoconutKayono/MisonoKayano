# B01｜HLSL 编译、Shader 变体与精度

> 核心问题：一份 Shader 文件，为什么会产生多个 GPU 程序？把 `float` 改成 `half`，究竟改变了什么？
>
> 结论：ShaderLab 描述材质属性与 Pass，HLSL 描述可编程阶段；关键字可以让同一源码产生不同程序。最终机器指令和数据精度还受编译器、图形 API、精度模型与 GPU 支持约束。

本卡面向 Unity URP 的 NPR（非真实感渲染），独立解释必要概念。文档依据 Unity 6.7 Beta / 6000.7，构建日期 2026-06-26；Shader 骨架参考 Graphics 固定提交 `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`，Core/URP 17.0.4。两者不是同一个版本快照。示例面向普通 URP Forward 单相机，无额外 Renderer Feature、Depth Priming、SSAO、后处理和 XR。

## 1. 从资产到 GPU 程序

**Shader 资产**是一份描述文件；**Pass** 指定一次绘制采用的阶段程序和渲染状态；**顶点阶段 VS** 处理几何输入；**片元阶段 FS/PS** 处理光栅化产生的片元输入。**变体 variant** 是某个阶段程序在一组编译条件下的专门版本，不是新增一个物体或一次 Draw。

```mermaid
flowchart LR
    A[ShaderLab 与 HLSL 源码] --> B[Pass/阶段/关键字/API 条件]
    B --> C[预处理与编译优化]
    C --> D[目标 API 接受的程序表示]
    D --> E[驱动/平台编译与管线准备]
    E --> F[GPU 机器指令]
```

这表示逻辑层次，不规定所有平台都经过相同中间语言或在相同时间完成编译。`#include` 展开、条件选择、常量折叠、死代码删除和寄存器分配，使源码行数与最终指令数之间不存在固定比例。

Unity Editor 可以按需编译并缓存变体；构建则面向所需平台与图形 API 处理需要保留的程序。首次使用卡顿也可能包含驱动管线准备，不能看到一次卡顿就认定是 HLSL 编译。[Unity Shader 编译](https://docs.unity3d.com/6000.0/Documentation/Manual/shader-compilation.html)

本地该页列出了 FXC/HLSLcc 等编译链，但本卡没有项目编译日志，**不把该列表外推为 Unity 所有版本、全部功能的唯一工具链**。确认实际链路时记录 Editor、包锁、平台、API、编译参数与日志。Graphics 仓库公开的 HLSL 也不是 Unity 完整编译器和原生驱动后端源码。

## 2. 静态选择与运行时选择

| 写法 | 发生在哪一层 | 主要代价 |
| --- | --- | --- |
| `#if defined(KEYWORD)` | 预处理时选择源码 | 编译程序数量与管理成本 |
| `if (_Toggle > 0.5)` | 同一程序中的运行时条件 | 最终指令、寄存器与实际控制流 |
| `lerp(a,b,t)` | 表达数值插值 | 一般不能假定只计算选中的输入 |

运行时条件也可能被编译器改成选择指令或谓词执行。写了 `if` 不等于机器上一定出现跳转；写了 `lerp` 也不能保证更快。

Unity 的 `shader_feature` 与 `multi_compile` 都可用于生成静态变体。前者通常按构建时材质使用等信息保留所需变体；后者声明所有组合的候选，但仍可能经过管线或自定义剥离。`dynamic_branch` 用于保留动态分支，不因该声明增加静态变体。`_local` 约束关键字作用域，**不会自动减少每个关键字集合的组合数**。[关键字声明](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-MultipleProgramVariants-declare.html)

运行时临时启用一个已经被剥离的静态功能，不会自动补出丢失程序。应让构建保留必要组合，并在 Player 验证；不要只凭 Editor 切换成功判断构建完整。

## 3. 怎样计算候选组合，而不是虚报构建数量

固定一个阶段、Pass 和目标 API，若有互相独立的关键字集合，每组分别有 `k₁,k₂,…,kₙ` 种选择，候选数为：

$$N=\prod_{i=1}^{n}k_i$$

两个布尔开关和一个三选一模式给出 `2×2×3=12` 个候选；十个独立布尔开关为 `2¹⁰=1024`。这是组合算术，不含跨阶段共享、平台限制、内置关键字、去重和剥离。

注意“一组的三个关键字”表达三选一候选，不能擅自按三个独立布尔开关计算。运行时关键字 API 也不替你维持这种互斥关系。实际构建数量应从编译统计读取，不能把所有 Pass 数、阶段数、API 数无条件相乘后当作最终二进制个数。[Unity 变体数量](https://docs.unity3d.com/6000.0/Documentation/Manual/shader-variants.html)

## 4. target、类型、格式和指令是四个层次

`#pragma target` 表达 Unity 的一组功能要求；Unity 官方说明它与 DirectX Shader Model 并非严格一一对应。提高 target 不会自动提高画质，也不是启用一切优化的按钮。[Unity target 参考](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Pragma-target.html)

`half` 涉及运算精度意图；`RGBA16F` 涉及纹理存储格式；C# 上传结构的大小涉及 CPU/GPU 布局。这三者不能互相推定。Unity 的 Shader Precision Model 可把 `half` 映射为 `float` 或 `min16float`；后者允许最低精度实现，并不保证每条指令都使用原生 FP16。

按照本地 Unity 6 的普通缓冲约定，相关标量上传大小/对齐仍是 4 字节；特定 Metal 兼容编译选项另有规则。因此把常量缓冲里的 `float4` 改成 `half4`，不能直接认定 C# 应上传 8 字节。[精度模型 API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/ShaderPrecisionModel.html)、[16 位精度说明](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Use16BitPrecisionInShaders.html)

以真正的二进制 FP16 存储作数值反例：在 `[1024,2048)` 内，相邻数间隔是 1。`1024.25` 和 `1024.5` 都可能在最近偶数舍入下变成 `1024`，随后相减失去原本的 `0.25`。不能先把巨大世界位置转为低精度，再期望相减恢复局部细节。

NPR 中优先保住投影、世界位置、深度和敏感阈值计算的数值稳定性；有界颜色和部分方向运算可在误差允许时尝试较低精度。是否节省寄存器和时间，需要看目标编译结果与实机画面。

## 5. 最小实验：同一条色阶，两种控制方式

保存为 `B01VariantLab.shader`，创建两个材质，赋给两个具有 `[0,1]` UV 的 Quad。该 Shader 不使用纹理或场景光：上半区由静态关键字控制两段色阶，下半区由运行时参数控制。

```shaderlab
Shader "Encyclopedia/B01VariantLab"
{
    Properties
    {
        [Toggle(_B01_BANDS)] _Bands("Static Bands", Float) = 0
        _RuntimeBands("Runtime Bands (0 or 1)", Range(0,1)) = 0
        _Threshold("Threshold", Range(0,1)) = 0.5
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma shader_feature_local _ _B01_BANDS
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Bands;
                float _RuntimeBands;
                float _Threshold;
            CBUFFER_END
            struct A { float4 p : POSITION; float2 uv : TEXCOORD0; };
            struct V { float4 p : SV_POSITION; float2 uv : TEXCOORD0; };
            V Vert(A input)
            {
                V output;
                output.p = TransformObjectToHClip(input.p.xyz);
                output.uv = input.uv;
                return output;
            }
            half4 Frag(V input) : SV_Target
            {
                float t = saturate(input.uv.x);
                float staticValue = t;
                #if defined(_B01_BANDS)
                    staticValue = step(_Threshold, t);
                #endif
                float runtimeValue = t;
                if (_RuntimeBands > 0.5)
                    runtimeValue = step(_Threshold, t);
                float value = input.uv.y >= 0.5 ? staticValue : runtimeValue;
                return half4(value, value, value, 1);
            }
            ENDHLSL
        }
    }
}
```

1. 两个开关都关：两半均为渐变；都开：两半均在阈值处变为黑白两段。
2. 单独切换 Static Bands：观察上半区，并检查当前 `_B01_BANDS` 状态。
3. 单独将 Runtime Bands 参数设为 0 或 1：观察下半区。它只改变运行时数值，不声明额外静态变体。
4. 在 Shader Inspector 的编译信息中选择实际目标 API，查看关键字与代码；记录构建前候选和剥离后数量。不要预填“必然编译两个 GPU 程序”，因为阶段和平台统计口径不同。
5. 构建测试场景时让两种静态材质都被引用，核对两种状态。这个很短的分支很可能被优化，实验不承诺可测的性能差距。

固定源码入口：[Core.hlsl](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl) 提供本例公共定义；[SpaceTransforms.hlsl](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.core/ShaderLibrary/SpaceTransforms.hlsl) 提供位置变换。它们能解释源码输入，不能证明最终 ISA。

## 6. 自测与证据范围

- 关键字多一倍，变体必然多一倍吗？**取决于集合选项与独立性，不能只数名字。**
- 运行时 uniform 分支必然导致 lane 分歧吗？**不必，所有执行实例可能采用同一条件。**
- `half` 必然让缓冲占用减半吗？**不能据类型名推定布局。**
- 显示相同就证明两个 Shader 指令相同吗？**不能，只说明该输入下结果相同。**

配套 Python 检查组合算术与 FP16 数值反例；Shader 只做静态核对，尚未 Unity 编译、构建或测时。本地来源位于 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`：`Manual/shader-compilation.html`、`shader-variants.html`、`SL-MultipleProgramVariants-declare.html`、`SL-Pragma-target.html`、`SL-Use16BitPrecisionInShaders.html` 及 `ScriptReference/ShaderPrecisionModel.html`。

下一张：[B02｜统一 Shader 核心、wave 与占用率](B02-统一Shader核心wave与占用率.md)。
