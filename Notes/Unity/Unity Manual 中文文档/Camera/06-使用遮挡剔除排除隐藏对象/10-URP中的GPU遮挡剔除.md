# URP 中的 GPU 遮挡剔除

> 原文：[Enable GPU occlusion culling in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/gpu-culling.html)

GPU Occlusion Culling 表示 Unity 使用 GPU 而不是 CPU，在对象被其他对象遮挡时将其从 Camera 渲染中排除。为了加速包含大量被遮挡对象的 Scene 中的 GPU 渲染，Unity 使用深度信息。

GPU Occlusion Culling 与 GPU Resident Drawer 配合工作，并且具有类似的限制。

## GPU Occlusion Culling 的工作原理

Unity 会从 Scene 中 Camera 的视角生成 depth texture。GPU 随后使用当前帧和前一帧的 depth texture 执行对象剔除。Unity 只渲染在其中任意一帧中被判断为未遮挡的对象。

GPU Occlusion Culling 使用保守方式判断对象在某帧中是否可见，具体如下：

- **Bounding sphere 近似**：每个可能被遮挡的对象都由 bounding sphere 表示。因此，细长对象相较实际网格具有更粗略的球形表示，Unity 不太可能检测到它们被遮挡。
- **降采样深度缓冲区**：Unity 使用降采样深度缓冲区的多个层级测试遮挡。选择的层级取决于 bounding sphere 的投影屏幕大小，确保该层级中的像素大小大于投影 sphere。Unity 会使用更粗略的深度缓冲区近似层级测试更大的 bounding sphere。

## 适用场景

GPU Occlusion Culling 是否能加速渲染取决于 Scene。它在以下设置中最有效：

- 多个对象使用同一个 Mesh，使 Unity 能将它们组合到一个 draw call 中。
- Scene 中有大量遮挡，尤其是被遮挡对象具有较多顶点时。
- 被遮挡对象的 screen-space bounding radius 较小。

如果 Occlusion Culling 对 Scene 没有明显效果，渲染时间可能会因为 GPU 为设置 GPU Occlusion Culling 执行额外工作而增加。

## 启用 GPU Occlusion Culling

1. [启用 GPU Resident Drawer](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/gpu-resident-drawer.html)。
2. 在当前 [Universal Renderer](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html) 中启用 **GPU Occlusion**。

## 分析 GPU Occlusion Culling

可以使用以下工具分析 GPU Occlusion Culling：

- [Rendering Statistics overlay](https://docs.unity3d.com/6000.7/Documentation/Manual/RenderingStatistics.html)，检查渲染速度是否提升。
- [Rendering Debugger](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/rendering-debugger-reference.html)，排查问题。

## 其他资源

- [减少 CPU 上的渲染工作](https://docs.unity3d.com/6000.7/Documentation/Manual/reduce-rendering-work-on-cpu.html)
- [Occlusion Culling](https://docs.unity3d.com/6000.7/Documentation/Manual/OcclusionCulling.html)
- [选择优化 draw call 的方法](https://docs.unity3d.com/6000.7/Documentation/Manual/optimizing-draw-calls-choose-method.html)

---

## 文档导航

- 上一页：[[09-遮挡剔除故障排查]]
- 目录：[[00-使用遮挡剔除排除隐藏对象]]
- 下一页：[[07-渲染队列与排序行为]]
