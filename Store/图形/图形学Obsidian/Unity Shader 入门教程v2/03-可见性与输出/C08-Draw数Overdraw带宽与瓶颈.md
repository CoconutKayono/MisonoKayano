# C08｜Draw 数、Overdraw、带宽与瓶颈

> **核心问题：一个全屏 Draw，为什么可能比几十个小 Draw 更贵？**
> 
> Draw 数描述提交数量，不能同时代表顶点、片元、采样、附件流量和等待。优化应先定位限制当前帧关键路径的工作，再做保持目标画面的对照修改。

## 1. 范围与术语

本卡依据本地 Unity 6.7 Beta / 6000.7 文档（2026-06-26 构建），实验为 Unity 6 / URP 项目中的独立离屏绘制。这里只构造可控负载，不冒充完整角色项目的性能评估，也不给出跨设备固定毫秒数。

- **Draw Calls**：Unity 发出的绘制调用数；**SetPass**：设置/切换相关 Shader Pass 的计数，不能当作同一个指标。
- **Overdraw**：同一屏幕区域被多份几何/片元工作覆盖的情况。讨论时需说明是几何覆盖、通过深度的样本、实际片元调用还是混合层数。
- **带宽**：单位时间实际传输的数据量。资源容量、源码读取次数和外部总线字节数不是同一量。
- **瓶颈**：在当前输入和平台上限制完成时间的资源或依赖。改变设置后瓶颈可以转移。
- **吞吐率/延迟**：连续帧产出速度/一项输入到显示的时间；CPU/GPU 重叠可以改善吞吐，但不意味着延迟等于其中最大的一段。

## 2. 把一帧成本拆开

| 维度 | 常见驱动因素 | 应寻找的证据 |
| --- | --- | --- |
| CPU 场景与提交 | 剔除、排序、状态准备、Draw 数、数据上传 | CPU Timeline、主/渲染线程工作，而非仅看等待标记 |
| 几何与顶点 | 顶点数、蒙皮、Pass 重复、微小三角形 | 顶点工作、图元计数及相关 GPU 时间 |
| 片元运算 | 实际调用数、ALU、分歧、寄存器和延迟 | 片元时间/调用及目标 GPU 计数器 |
| 纹理与附件 | 访问局部性、过滤、格式、MSAA、Load/Store | 缓存、纹理单元、外部读写量和输出负载 |
| 同步与帧节奏 | 依赖、队列等待、Present、VSync、帧率限制 | 时间线、等待位置和限帧配置 |

一个理想稳态模型为 `T_frame ≈ max(T_CPU, T_GPU)`，前提是可重叠且没有其他限制；不要把所有 GPU 阶段当成严格串行再简单求和。VSync、队列深度和同步会改变观察结果。

例如理想 CPU=8 ms、GPU=12 ms，先把 CPU 降到 4 ms，吞吐瓶颈仍约为 12 ms；将 GPU 降到 6 ms 后，瓶颈才转向 CPU 的 8 ms。这是数学模型，不是设备测试报告。

## 3. 三个数量反例

1. 全屏 1920×1080 的一次覆盖约 207 万像素位置；100 个互不重叠的 32×32 小块总共约 10.24 万位置。前者的覆盖量约为后者 20.25 倍，但后者有更多提交和边界成本，不能只凭这个比例决定快慢。
2. 8 层完全重叠透明几何与 8 个平铺块，Draw 数可以相同，实际片元和混合工作却不同。深度优化还会让不透明遮挡情况与透明叠加不同。
3. 两种方案同样写一张全屏图，但其中一种额外经过中间目标保存/读取，Draw 数和外部流量不再一一对应。是否真有该流量还受 tile memory、压缩与缓存影响。

**Overdraw 可视化只显示某种代理量。** 替换材质可能改变 clip、深度、混合和片元复杂度；诊断图颜色越红不能直接换算成原始材质耗时倍数。

## 4. 一次只改变一个主要变量

| 对照修改 | 若时间明显变化，支持什么假设 | 仍不能排除什么 |
| --- | --- | --- |
| 离屏边长减半，保持其余设置 | 与像素数量有关的负载重要 | ALU、采样、输出、带宽都可能随像素缩小，不能直接断言带宽瓶颈 |
| 增加全覆盖叠加层，简化几何 | 遮挡/片元/混合工作重要 | 同时增加 Draw，需另做提交量对照 |
| 保持总覆盖，把平面分成更多 Draw | 提交/几何/边界工作重要 | quad 辅助调用、tile 列表和调度也会变化 |
| 保持覆盖，增加依赖于输出的运算 | Shader 运算相关限制可能重要 | 编译器优化、寄存器和占用率也会改变 |

分辨率降低后不提速，也不能直接证明 CPU 瓶颈：可能有帧率上限、固定几何负载、其他分辨率未变的目标，或者测量噪声。

## 5. Unity 实验：同一画面的叠加与分块提交

脚本构造两种布局：Layered 用多个全屏 Draw 叠加，各层权重为 `1/N`；Partitioned 用不重叠视口分块，总覆盖近似相同但 Draw 数增加。Shader 使用相同屏幕坐标函数，所以切换布局时应保持近似同一图案，允许附件量化与边界误差。

为避免隐藏面消除抹掉重复层，实验使用 Additive Blend、ZTest Always、无深度附件。它故意隔离可见片元/输出成本，不能直接模拟正常不透明角色的 Early-Z 效率。

保存文件，URP 空场景挂脚本并赋 Shader。改变配置后在 Play 模式调用 **Rebuild Workload**；重建与资源创建发生在测量窗口外。副本：[C#](../实验/C08WorkloadLab.cs)、[Shader](../实验/C08WorkloadLab.shader)。

```shaderlab
Shader "Encyclopedia/C08WorkloadLab"
{
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            Cull Off ZWrite Off ZTest Always Blend One One
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            float _Contribution;
            int _Iterations;
            float4 Vert(float3 p:POSITION):SV_POSITION { return float4(p.xy,0.5,1); }
            float4 Frag(float4 p:SV_POSITION):SV_Target
            {
                float v=frac(p.x*0.0021+p.y*0.0013);
                [loop] for(int i=0;i<_Iterations;i++) v=frac(v*1.371+0.173);
                return float4(0.1+0.6*v,0.2+0.3*v,0.7-0.4*v,1)*_Contribution;
            }
            ENDHLSL
        }
    }
}
```

```csharp
using UnityEngine;
using UnityEngine.Rendering;

public class C08WorkloadLab : MonoBehaviour
{
    public enum Layout { Layered, Partitioned }
    public Shader labShader;
    public Layout layout;
    [Range(64,2048)] public int resolution=512;
    [Range(1,64)] public int layers=8;
    [Range(1,16)] public int gridSide=4;
    [Range(0,128)] public int iterations=16;
    public bool showPreview=true;
    Material material;
    Mesh quad;
    RenderTexture target;
    CommandBuffer commands;
    string status;
    bool ready;
    void Start()
    {
        if(labShader==null || !labShader.isSupported) return;
        material=new Material(labShader);
        quad=new Mesh { name="C08 Owned Quad" };
        quad.vertices=new Vector3[] {
            new Vector3(-1,-1,0),new Vector3(1,-1,0),
            new Vector3(1,1,0),new Vector3(-1,1,0) };
        quad.triangles=new int[] {0,1,2,0,2,3};
        commands=new CommandBuffer { name="C08 Replayed Workload" };
        RebuildWorkload();
    }
    [ContextMenu("Rebuild Workload")]
    public void RebuildWorkload()
    {
        if(!Application.isPlaying || material==null) return;
        ready=false;
        commands.Clear();
        if(target!=null) { target.Release(); Destroy(target); }
        int size=Mathf.Clamp(resolution,64,2048);
        int n=Mathf.Clamp(gridSide,1,16), count=Mathf.Clamp(layers,1,64);
        target=new RenderTexture(size,size,0,RenderTextureFormat.ARGBHalf,RenderTextureReadWrite.Linear);
        target.name="C08 Workload Color";
        target.filterMode=FilterMode.Point;
        if(!target.Create()) { Debug.LogError("C08 target creation failed."); return; }
        var properties=new MaterialPropertyBlock();
        properties.SetInt("_Iterations",Mathf.Clamp(iterations,0,128));
        properties.SetFloat("_Contribution",layout==Layout.Layered ? 1f/count : 1f);
        commands.SetRenderTarget(target);
        commands.SetViewport(new Rect(0,0,size,size));
        commands.ClearRenderTarget(false,true,Color.clear);
        commands.BeginSample("C08 Workload");
        if(layout==Layout.Layered)
        {
            for(int i=0;i<count;i++) commands.DrawMesh(quad,Matrix4x4.identity,material,0,0,properties);
        }
        else
        {
            count=n*n;
            for(int y=0;y<n;y++) for(int x=0;x<n;x++)
            {
                int x0=x*size/n, x1=(x+1)*size/n;
                int y0=y*size/n, y1=(y+1)*size/n;
                commands.SetViewport(new Rect(x0,y0,x1-x0,y1-y0));
                commands.DrawMesh(quad,Matrix4x4.identity,material,0,0,properties);
            }
        }
        commands.EndSample("C08 Workload");
        status=layout+" | "+size+" square | draws="+count+" | iterations="+Mathf.Clamp(iterations,0,128);
        ready=true;
        Debug.Log("C08 rebuilt: "+status);
    }
    void Update() { if(ready) Graphics.ExecuteCommandBuffer(commands); }
    void OnGUI()
    {
        if(!ready || !showPreview) return;
        GUI.Label(new Rect(10,10,750,25),status);
        GUI.DrawTexture(new Rect(10,40,512,512),target,ScaleMode.ScaleToFit,false);
    }
    void OnDestroy()
    {
        if(commands!=null) commands.Release();
        if(target!=null) { target.Release(); Destroy(target); }
        if(material!=null) Destroy(material);
        if(quad!=null) Destroy(quad);
    }
}
```

## 6. 运行四组对照，不预填实测数字

| 组别 | 基准 → 修改 | 主要观察 |
| --- | --- | --- |
| 分辨率 | Layered，8 层，512² → 256² | 覆盖位置降到约 1/4，GPU 时间是否随之下降 |
| 层数 | Layered，512²，1 → 8 层 | 同图案近似亮度下，额外混合与片元是否增加时间 |
| 提交量 | Partitioned，512²，Grid Side 1 → 8 | Draw 从 1 到 64，总覆盖近似不变；区分 CPU/GPU 变化 |
| 运算 | 固定布局、尺寸、层数，Iterations 0 → 64 | 片元计算及寄存器/调度变化对时间的影响 |

每组独立恢复基准。脚本在重建时记录命令，运行时重放；因此提交量组不包含大量 GameObject 的 Transform 更新、场景剔除和逐帧 C# 循环录制成本。若要诊断这些 CPU 场景成本，还需在真实 Renderer 场景中单独改变对象数。

先用 Frame Debugger 确认离屏目标、视口、Draw 数和 Blend。再在支持的 GPU Profiler 或厂商工具中查看 `C08 Workload` 范围及整帧时间。BeginSample/EndSample 是标记范围，不保证当前平台能提供有效 GPU 时间，也不意味着范围外的 Clear、附件结束处理和显示免费。

Unity 的 Rendering 模块提供 Draw/SetPass/顶点等计数；GPU 模块的支持取决于平台、API 和配置，应按目标文档核对。CPU 提交函数的耗时不能直接当 GPU Draw 时间。[Rendering Profiler](https://docs.unity3d.com/6000.0/Documentation/Manual/ProfilerRendering.html)、[GPU Profiler](https://docs.unity3d.com/6000.0/Documentation/Manual/ProfilerGPU.html)

测量时固定设备、API、分辨率、帧率限制和电源条件；先预热，避开 Shader 首次编译、资源重建和后台变化；用多帧中位数及波动范围比较。可关闭 Show Preview，避免 GUI 采样进入测量，但离屏工作仍执行。不要为了读一个漂亮数字而忽略帧率上限或温度降频。

## 7. 常见误诊与 NPR 取舍

- **Draw 少就一定快**：全屏描边或后处理仍可能读写大量像素；先看它是否在 GPU 关键路径上。
- **降低分辨率提速就是带宽瓶颈**：片元 ALU 和采样数量也降了，需要进一步区分。
- **等待标记大就是等待代码慢**：可能是 CPU 在等 GPU、Present 或帧节奏，需关联时间线。
- **优化前后 FPS 差就是局部收益**：FPS 是时间的倒数，且受上限影响；优先比较毫秒和具体工作范围。
- **运行 64 次循环就是 64 条机器指令**：编译器、精度和执行组调度都可能改变实际程序。

NPR 中反壳描边会增加几何/覆盖工作，屏幕描边会增加全屏采样和附件依赖；头发透明常增加重叠和排序压力；更复杂的 Ramp、高光和法线处理可能增加片元成本。应该根据目标平台与视觉收益选择，而不是依据“哪种技术 Draw 更少”直接下结论。

## 8. 自测、验证与下一阶段

1. **CPU 从 8 ms 优化到 4 ms，GPU 仍为 12 ms，是否一定提高吞吐？** 在理想 GPU 限制模型中不会；其他实际约束还要看时间线。
2. **Overdraw 图的红色能否直接当耗时倍数？** 不能，它只体现某种覆盖/代理计数，替换 Shader 可能改变原程序行为。
3. **分块提交组为什么还不是纯 CPU 测试？** Draw 数增加也改变顶点、图元边界和 GPU 调度。
4. **一张纹理 8 MiB 是否表示每次采样都读 8 MiB 外部显存？** 否，采样范围、缓存、压缩与复用决定实际流量。

本地已核对 `Manual/ProfilerRendering.html`、`Manual/ProfilerGPU.html`、`ScriptReference/Rendering.CommandBuffer.BeginSample.html`，根目录为 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。本文实验未在 Unity 编译、播放或实机计时，表中不填造出的测量值。

前一张：[C07 几何数据来源](C07-蒙皮顶点动画与几何数据来源.md)。完成后进入 [C 阶段检查点](../实验/C阶段检查点.md)。下一阶段从 **D01：URP 相机入口、剔除与 RendererList** 开始，尚未生成。
