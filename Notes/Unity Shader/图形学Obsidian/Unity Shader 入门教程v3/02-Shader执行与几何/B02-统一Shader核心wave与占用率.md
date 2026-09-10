# B02｜统一 Shader 核心、wave 与占用率

> 核心问题：GPU 上成千上万的 Shader 实例怎样执行？为什么增加线程、删除 if 或提高占用率，都不保证更快？
>
> 结论：Shader 实例以执行组共享部分调度与指令资源。性能取决于有效工作、依赖等待、数据访问和可驻留资源之间的关系；源码线程数并不等于每个时刻实际执行的算术通道数。

本卡面向 Unity URP NPR。默认普通顶点/片元 Shader，不讨论 Mesh Shader 或光追调度。Unity 文档基线为 6.7 Beta / 6000.7（2026-06-26），示例引用 Core/URP 17.0.4 的固定 Graphics 提交 `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`。NVIDIA 与 AMD 资料分别用于说明厂商模型，不把 CUDA 的线程块规则直接套给像素 Shader。

## 1. 先分清四个数量

| 术语 | 本卡含义 | 不能等同于 |
| --- | --- | --- |
| Invocation / 实例 | 一次顶点或片元程序的逻辑执行 | 一个独占物理核心 |
| Lane / 通道 | wave 内参与执行的一个位置 | 一个 RGB 分量 |
| Wave / 执行组 | 被相关硬件以组管理的执行实例集合 | 一个三角形或一个固定屏幕方块 |
| Shader Core / 执行硬件 | 调度和执行指令的物理资源 | 一个 ShaderLab Pass |

现代常见 GPU 使用可承担不同 Shader 阶段工作的统一可编程执行资源；顶点、片元、计算是工作种类，不能从逻辑管线图推定芯片存在三套互不共享的专用算术核心。纹理采样、光栅化等还可能使用专门单元，因此也不能把整张 GPU 简化成只有 ALU。

GPU 擅长让大量独立工作重叠，并在某些工作等待时调度其他就绪工作；这并不代表一条依赖链本身没有延迟。

## 2. wave 的宽度不能写死为 32

NVIDIA CUDA 的 warp 是 32 个线程；SIMT 允许用逐线程程序表达组执行，分支路径不同会涉及不同活动掩码。现代 NVIDIA 的独立线程调度也意味着不应依赖“所有线程在每条指令上天然同步”的旧假设。[NVIDIA SIMT 架构](https://docs.nvidia.com/cuda/archive/13.0.0/cuda-c-programming-guide/index.html#simt-architecture)

AMD RDNA 支持 Wave32 / Wave64 等具体运行模式，资源限制要按架构和编译模式读取。[AMD RDNA 架构资料](https://gpuopen.com/wp-content/uploads/2019/08/RDNA_Architecture_public.pdf)

HLSL 的 `WaveGetLaneCount()` 提供查询入口，Microsoft 的该接口文档给出 4—128 的范围与实现差异。它不是本卡普通 URP Shader 可以无条件使用的函数：仍需合适 Shader Model、Unity 编译支持和设备能力。[HLSL WaveGetLaneCount](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/wavegetlanecount)

`float4` 只是一个实例里的四分量数据，不会自动创建四个 lane；一次纹理采样返回四个通道，也不是四个像素线程。

## 3. 分支分歧：看同一执行组的条件

假设教学 wave 有 8 个 lane，一条路径 A 需 10 个指令步骤，另一条 B 需 6 个。忽略调度、编译优化和其他开销，并假设不同路径依次以掩码执行：

| lane 条件分布 | 组需要执行的路径步骤 | 有效 lane-step / 可用 lane-step |
| --- | --- | --- |
| 8 个都走 A | 10 | `80/80=100%` |
| 4 个 A、4 个 B | 16 | `(4×10+4×6)/(8×16)=50%` |
| 1 个 A、7 个 B | 16 | `(1×10+7×6)/(8×16)=40.625%` |

这只是掩码模型的利用率计算，**不是预测某款 GPU 会慢 2 倍或 2.46 倍**。编译器可能展开、谓词化或消除分支；硬件也有不同的调度方式。

不同 wave 分别完全执行 A 和 B，不等于同一 wave 内分歧。材质级统一开关可以对整次 Draw 保持一致；像素级噪声遮罩可能使局部相邻实例条件不一致。屏幕相邻性通常有参考价值，但不能按 `x/32` 猜出确切 wave 成员。

## 4. latency、throughput 和 occupancy

**延迟 latency** 是某个操作到结果可用的等待；**吞吐 throughput** 是单位时间能够完成的工作量；**占用率 occupancy** 在明确架构口径下通常描述已驻留 wave 相对硬件上限的比例。驻留只表示执行状态已占用资源，不表示每个时刻都在发射有效指令。

寄存器保存尚在使用的中间值。每个实例需要更多寄存器，可能减少同一硬件单元可驻留的 wave；寄存器不足还可能产生 spill，即将部分中间数据放到其他存储，增加访问成本。实际分配有粒度和其他限制。[AMD 占用率解释](https://gpuopen.com/presentations/2024/GPC24_Occupancy_explained.pdf)

简化教学模型：某单元有 `R=65536` 个寄存器槽，wave 宽 `W=32`，每 lane 使用 `r` 槽，最大驻留 64 个 wave，则只考虑寄存器约束时：

$$N_{resident}\leq\min\left(64,\left\lfloor\frac{65536}{32r}\right\rfloor\right)$$

`r=32` 时模型上限 64；`r=64` 时上限 32。这组常数是人为选定的练习条件，**不对应某块 Unity GPU 的已测配置**。真实限制还包括分配粒度、线程/组限制、共享资源和程序类别。

增加驻留工作有助于隐藏等待，但若吞吐已经饱和，继续提高 occupancy 可能没有收益；为减少寄存器而重复大量计算，也可能得不偿失。应同时记录 GPU 时间、寄存器、实际 wave 模式与瓶颈指标。

## 5. 最小实验：控制一致性，而非预设输赢

保存为 `B02BranchLab.shader`，在 URP Forward 测试场景中赋给覆盖较大区域的 Quad。关闭后处理、Depth Priming、SSAO、额外 Renderer Feature、XR 和动态分辨率。用同一分辨率和覆盖面积比较模式；此 Shader 不采样贴图，避开本实验中的隐式导数采样问题。

```shaderlab
Shader "Encyclopedia/B02BranchLab"
{
    Properties
    {
        [Enum(AllA,0,AllB,1,LargeTiles,2,PixelChecker,3)] _Mode("Branch Pattern", Float)=0
        _TilePixels("Large Tile Size", Range(8,256))=64
        _Seed("Runtime Seed", Range(0.01,1))=0.3
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Mode;
                float _TilePixels;
                float _Seed;
            CBUFFER_END
            struct A { float4 p:POSITION; float2 uv:TEXCOORD0; };
            struct V { float4 p:SV_POSITION; float2 uv:TEXCOORD0; };
            V Vert(A input)
            {
                V output;
                output.p=TransformObjectToHClip(input.p.xyz);
                output.uv=input.uv;
                return output;
            }
            float WorkA(float x)
            {
                [loop] for(int k=0;k<24;k++) x=frac(x*1.31+0.17);
                return x;
            }
            float WorkB(float x)
            {
                [loop] for(int k=0;k<24;k++) x=frac(x*1.73+0.29);
                return x;
            }
            half4 Frag(V input):SV_Target
            {
                bool chooseA;
                if(_Mode<0.5) chooseA=true;
                else if(_Mode<1.5) chooseA=false;
                else
                {
                    float tile=_Mode<2.5 ? max(_TilePixels,1.0) : 1.0;
                    float2 cell=floor(input.p.xy/tile);
                    chooseA=fmod(cell.x+cell.y,2.0)<1.0;
                }
                float value;
                [branch] if(chooseA) value=WorkA(input.uv.x+_Seed);
                else value=WorkB(input.uv.x+_Seed);
                return half4(value,value,value,1);
            }
            ENDHLSL
        }
    }
}
```

AllA/AllB 为统一条件；LargeTiles 使用较大屏幕区域；PixelChecker 每像素交错。`[branch]` 表达编译意图，不能用源码注解代替最终控制流检查；两个函数也可能被优化或合并。

实验记录顺序：先确认四种模式输出确有区别；再查看目标编译信息，确认循环和分支是否保留；预热后在目标 Player 中多次测量 GPU Pass 时间，记录中位数与波动。不要把 Editor CPU 帧时间当 GPU 指令成本，也不要假设棋盘模式一定慢。

如果结果几乎相同，合理结论是“这组条件下未测得差异”，随后检查优化、覆盖量、测量分辨率与瓶颈。不要为了符合理论图强行改写数据。

## 6. NPR 的具体取舍

角色材质开关可以采用静态变体或统一动态条件；面部 SDF、噪声边界和逐像素材质分类则要关注条件的空间分布。删掉 `if` 后无条件采样两套贴图，可能增加工作与带宽；拆成更多 Draw 又会增加提交和几何成本，应测量完整路径。

片元阶段还存在用于导数等目的的执行分组与 helper invocation（辅助实例）。它们不等于最终可见像素，不能从屏幕像素数直接推断有效 lane 数。本卡不展开导数与覆盖规则，后续 B05 单独解释。

自测：① `float4` 是四线程吗？**不是。** ② 100% occupancy 等于 100% 算术吞吐吗？**不是。** ③ 不同 wave 各走不同路径是 wave 内分歧吗？**不是。** ④ 寄存器越少一定越快吗？**要看是否引入重算、访存或其他瓶颈。**

验证状态：Python 只校验掩码模型和寄存器约束算术，不模拟真实调度；Shader 未经 Unity 编译或 GPU 性能测量。示例公共入口为 [固定提交 Core.hlsl](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl)。Unity HLSL 源码不能揭示最终每个 wave 的寄存器分配与执行轨迹。

下一张：[B03｜管线状态、Draw 命令、队列与 CPU/GPU 并行](B03-管线状态Draw命令队列与CPUGPU并行.md)。
