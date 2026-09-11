# 内置渲染管线中 CommandBuffer 的基础知识

> 原文：[CommandBuffer fundamentals in the Built-In Render Pipeline](https://docs.unity3d.com/6000.7/Documentation/Manual/GraphicsCommandBuffers.html)

> [!IMPORTANT]
> 内置渲染管线已弃用，并将在未来版本中废止。在整个 Unity 6.7 LTS 生命周期内，Unity 仍会支持它，包括错误修复和维护。有关迁移的信息，请参阅[从内置渲染管线迁移到通用渲染管线](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrading-from-birp.html)和[渲染管线功能比较](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines-feature-comparison.html)。

[`CommandBuffer`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CommandBuffer.html) 保存一系列渲染命令，例如设置渲染目标或绘制给定网格。你可以指示 Unity 在内置渲染管线的各个时间点调度并执行这些命令，从而自定义和扩展 Unity 的渲染功能。

![使用 Command Buffer 实现的模糊折射效果。](RenderingCommandBufferBlurryRefraction.jpg)

使用 Command Buffer 实现的模糊折射效果。

你可以使用 [`Graphics.ExecuteCommandBuffer`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Graphics.ExecuteCommandBuffer.html) API 立即执行 CommandBuffer，也可以安排它们在渲染管线中的指定时间点执行。要调度 CommandBuffer，请将 [`Camera.AddCommandBuffer`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Camera.AddCommandBuffer.html) API 与 [`CameraEvent`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.html) 枚举结合使用，并将 [`Light.AddCommandBuffer`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Light.AddCommandBuffer.html) API 与 [`LightEvent`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.LightEvent.html) 枚举结合使用。要查看 Unity 何时执行按这种方式调度的 CommandBuffer，请参阅[[02-针对内置渲染管线的 CameraEvent 和 LightEvent 事件顺序参考]]。

如需查看可通过 CommandBuffer 执行的完整命令列表，请参阅 [`CommandBuffer` API 文档](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CommandBuffer.html)。请注意，某些命令仅在特定硬件上受支持；例如，与 Ray Tracing 相关的命令仅在 DX12 上受支持。

## 其他资源

- [[01-渲染管线简介]]
- [在可编程渲染管线中执行渲染命令](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/manual/index.html)
- [[00-在 URP 中自定义渲染和后期处理]]

---

## 文档导航

- 上一页：[[00-在内置渲染管线中自定义渲染]]
- 目录：[[00-在内置渲染管线中自定义渲染]]
- 下一页：[[02-针对内置渲染管线的 CameraEvent 和 LightEvent 事件顺序参考]]
