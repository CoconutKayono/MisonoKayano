# D02｜ShaderLab Pass、LightMode 与渲染状态覆盖

>**核心问题：Shader 写了多个 Pass，为什么只执行其中一些？代码写了 ZTest，为什么抓帧看到另一种比较？**
>
>ShaderLab 描述可用程序和默认状态，渲染管线决定何时选择哪些 Pass；绘制配置还能覆盖被明确指定的状态部分。文件排列顺序不是整帧执行顺序。

## 1. 版本与术语

本卡对照 Graphics `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`（URP 17.0.4 / 6000.0）和本地 Unity 6000.7 Beta 文档（2026-06-26 构建）。示例使用普通 Forward、单 Base Game Camera、Render Graph 路径。

- **SubShader**：Shader 中的一组管线兼容实现。
- **Pass**：一组程序入口及相关渲染状态，不代表一定会被调度。
- **Name**：Pass 的名称，可用于按名称查找、UsePass 等；不是 LightMode 的同义词。
- **LightMode**：在 URP 常规列表绘制中用于说明 Pass 用途的标签值，例如 UniversalForward、ShadowCaster、DepthOnly。
- **RenderStateBlock**：一组可覆盖的状态值，配合 RenderStateMask 指定哪些部分实际覆盖。
- **Queue**：对象参与排序/过滤的队列分类，既不是 Pass 的执行入口，也不是完整的透明渲染设置。

## 2. 选择程序与选择时机

一次物体绘制要同时满足几个条件：该对象进入当前候选集合；队列/层等过滤通过；有符合这次任务的 Pass；管线在当前配置下确实安排了此任务。

| 标签/名称 | 应如何理解 | 常见误读 |
| --- | --- | --- |
| `Name "MyPass"` | 为这个 Pass 命名 | 以为 ShaderTagId("MyPass") 必然选择它 |
| `LightMode="DepthOnly"` | 提供深度用途的实现 | 以为每台相机每帧必执行一次 |
| `LightMode="ShadowCaster"` | 提供投射阴影实现 | 以为 Shader 中存在就会自动产生阴影图 |
| `LightMode="SRPDefaultUnlit"` | 可被对应 URP 绘制路径选中 | 以为它代表所有自定义 Pass 自动逐个执行 |
| 自定义 LightMode | 可以由自定义列表指定 | 以为 URP 默认识别任意自定义字符串 |

源码 `DrawObjectsPass` 的默认标签列表包含 SRPDefaultUnlit、UniversalForward、UniversalForwardOnly。不同 Renderer 和绘制任务会使用不同列表；不要由这个默认集合推出 ShadowCaster 或所有多 Pass 都在同一次调用中执行。[固定 DrawObjectsPass.cs](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.universal/Runtime/Passes/DrawObjectsPass.cs)

深度可能来自 DepthOnly 预通道，也可能复制已有深度；阴影依赖灯光、设置、距离和投射对象。任务存在、输入可用和 Pass 存在是不同条件。URP 支持的标签用途见本地 `Manual/urp/urp-shaders/urp-shaderlab-pass-tags.html`，以及 [URP Pass 标签参考](https://docs.unity3d.com/6000.0/Documentation/Manual/urp/urp-shaders/urp-shaderlab-pass-tags.html)。

## 3. 最终状态不是只看 Shader 文件

可以把一次绘制的状态理解成：先取得被选 Pass 的状态，再应用这次绘制明确要求的状态覆盖。覆盖只对 mask 指定部分生效；没有被覆盖的部分继续由对应 Pass 等配置决定。

例如构造 `RenderStateBlock(RenderStateMask.Depth)`，设置 `DepthState(false, CompareFunction.Always)`，表达“不写深度、深度比较总通过”。若 mask 改为 Nothing，即使 depthState 字段仍然填了 Always，也不表示覆盖生效。

一个真实源码例子是 `DrawObjectsPass.InitRendererLists`：使用 Depth Priming、绘制不透明且满足相机条件时，代码设置 `DepthState(false, Equal)` 并把 Depth 加入 mask。它利用前面已有深度限制主体绘制，因此材质写着 LEqual，并不能证明这次绘制最终就是 LEqual。

这里的 Equal 并非“更高精度”。它要求当前几何结果与已写深度一致；如果深度 Pass 与主体的顶点位移、Alpha Clip 或姿态不一致，可能出现缺口。源码还处理退出该路径后的状态恢复，不能把覆盖条件孤立摘出来当作全局规则。

## 4. Unity 实验：Shader 写 Never，列表可覆盖为 Always

保存两份文件，在当前 URP Forward Renderer Data 添加 Feature。Render Graph 开启、Compatibility Mode 关闭，使用单 Base Game Camera，关闭 Depth Priming、MSAA、GPU Resident Drawer、后处理和其他 Feature。

给 Cube 使用实验材质。基础 Pass 正常显示蓝色，检查 Pass 输出黄色但故意写 `ZTest Never`。Feature 只选择 `D02Inspect`，可通过 RenderStateBlock 覆盖深度比较。副本：[Feature](../实验/D02StateOverrideFeature.cs)、[Shader](../实验/D02PassLab.shader)。

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RendererUtils;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class D02StateOverrideFeature : ScriptableRendererFeature
{
    public LayerMask layers=~0;
    public bool overrideDepth=true;
    public bool includeDepthInMask=true;
    InspectPass pass;
    public override void Create()
    {
        pass=new InspectPass { renderPassEvent=RenderPassEvent.AfterRenderingOpaques };
    }
    public override void AddRenderPasses(ScriptableRenderer renderer,ref RenderingData data)
    {
        if(data.cameraData.cameraType!=CameraType.Game || data.cameraData.renderType!=CameraRenderType.Base) return;
        pass.layers=layers.value;
        pass.overrideDepth=overrideDepth;
        pass.includeDepthInMask=includeDepthInMask;
        renderer.EnqueuePass(pass);
    }
    class InspectPass : ScriptableRenderPass
    {
        public int layers;
        public bool overrideDepth, includeDepthInMask;
        class PassData { public RendererListHandle list; }
        public override void RecordRenderGraph(RenderGraph graph,ContextContainer frameData)
        {
            var rendering=frameData.Get<UniversalRenderingData>();
            var camera=frameData.Get<UniversalCameraData>();
            var resources=frameData.Get<UniversalResourceData>();
            var desc=new RendererListDesc(new ShaderTagId("D02Inspect"),rendering.cullResults,camera.camera)
            {
                renderQueueRange=RenderQueueRange.opaque,
                sortingCriteria=camera.defaultOpaqueSortFlags,
                layerMask=layers
            };
            if(overrideDepth)
            {
                var state=new RenderStateBlock(includeDepthInMask ? RenderStateMask.Depth : RenderStateMask.Nothing);
                state.depthState=new DepthState(false,CompareFunction.Always);
                desc.stateBlock=state;
            }
            using(var builder=graph.AddRasterRenderPass<PassData>("D02 State Override",out var data))
            {
                data.list=graph.CreateRendererList(desc);
                builder.UseRendererList(data.list);
                builder.SetRenderAttachment(resources.activeColorTexture,0,AccessFlags.ReadWrite);
                builder.SetRenderAttachmentDepth(resources.activeDepthTexture,AccessFlags.Read);
                builder.SetRenderFunc(static (PassData p,RasterGraphContext ctx)=>ctx.cmd.DrawRendererList(p.list));
            }
        }
    }
}
```

```shaderlab
Shader "Encyclopedia/D02PassLab"
{
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Geometry" }
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        float4 Vert(float3 p:POSITION):SV_POSITION { return TransformObjectToHClip(p); }
        float4 BaseFrag():SV_Target { return float4(0.15,0.4,1,1); }
        float4 InspectFrag():SV_Target { return float4(1,1,0,1); }
        ENDHLSL
        Pass
        {
            Name "VisibleBase"
            Tags { "LightMode"="SRPDefaultUnlit" }
            ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment BaseFrag
            ENDHLSL
        }
        Pass
        {
            Name "NamedInspectPass"
            Tags { "LightMode"="D02Inspect" }
            ZWrite Off ZTest Never
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment InspectFrag
            ENDHLSL
        }
    }
}
```

## 5. 预测、抓帧与反例

1. Override Depth 关闭：检查 Pass 即使被选择，也因 Never 不贡献颜色，Cube 保留蓝色。
2. Override Depth 和 Include Depth In Mask 都开启：最终深度比较被覆盖为 Always，Cube 变黄。
3. Override 开启、Include Depth In Mask 关闭：设置值仍是 Always，但 mask 不要求覆盖，结果恢复蓝色。
4. 只修改 `Name "NamedInspectPass"`：本 Feature 按 LightMode 选择，改 Name 不应移除黄色覆盖。修改 `LightMode="D02Inspect"` 才会让它不再匹配。
5. 添加前方遮挡物可以观察 Always 的穿透效果，但先关闭遮挡剔除等干扰，确保后方对象确实仍在候选列表里；Depth Always 无法恢复未提交的几何。

Frame Debugger/原生抓帧中应确认实际 Draw 的 Pass、深度比较和写入状态，而非只停留在材质 Inspector。Never 模式下没有颜色变化不等于没有选择 Pass；相反，标签不匹配时可能根本没有该对象的绘制，两种原因应分开查。

该例未设置 overrideMaterial，因为替换材质与覆盖状态是不同机制。使用 overrideMaterial/overrideShader 时，还需检查替代程序与 Pass 索引；显式 CommandBuffer.DrawMesh 的 Pass 索引调用也不能等同于 RendererList 的 LightMode 选择。

## 6. NPR 中如何使用

头发模板、面部遮罩、轮廓和角色 ID 常需要专用 Pass。把选对象、选程序、覆写深度/模板和输出附件分别设计，才能解释“为什么只有某个 Renderer Feature 开启时效果才错”。不要用 Always 掩盖深度预通道与主体不一致，否则会引入穿墙和错误遮挡。

## 7. 自测与核验

1. **Name 和 LightMode 相同吗？** 不同，必须看调用方按哪一种信息查找。
2. **Shader 写 LEqual，是否证明最终如此？** 不证明，RenderStateBlock 等绘制配置可能覆盖。
3. **只填 state.depthState，mask 为 Nothing，覆盖生效吗？** 本例不会。
4. **DepthOnly 在 Shader 中靠前，是否一定先执行？** 不一定，管线按任务和配置调度，不按文件顺序执行所有 Pass。

已核对固定 DrawObjectsPass 和 RendererListDesc 的 stateBlock 转换；`RendererListDesc` 属于 `UnityEngine.Rendering.RendererUtils`。源码入口：[RendererList.bindings.cs](https://github.com/Unity-Technologies/UnityCsReference/blob/9d487cab41b00c50af020b56d27a3c768d54f770/Runtime/Export/RenderPipeline/RendererList.bindings.cs)。本地文档根目录 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。未运行 Unity 编译、GPU 抓帧或深度覆盖实验，预期不是实测记录。

前一张：[D01 相机与 RendererList](D01-相机入口剔除与RendererList.md)。下一张：[D03 Render Graph 记录与执行](D03-RenderGraph记录编译与执行.md)。
