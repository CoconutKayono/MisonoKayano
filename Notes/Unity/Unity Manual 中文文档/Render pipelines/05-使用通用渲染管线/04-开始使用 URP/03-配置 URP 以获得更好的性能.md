# 配置 URP 以获得更好的性能

> 原文：[Configure for better performance in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/configure-for-better-performance.html)

您可以禁用或更改对性能有重大影响的通用渲染管线 (URP) 设置和功能。这有助于提高项目的性能，尤其是在低端平台上。

根据项目或目标平台，以下一项或所有项可能会产生重大影响：

- 所选的渲染路径
- URP 使用的内存量
- CPU 上的处理时间
- GPU 上的处理时间

可使用 Unity Profiler 或 GPU 性能分析器（例如 RenderDoc 或 Xcode）来衡量各设置对项目性能的影响。

如果项目需要某些功能，则可能无法禁用它们。

## 选择渲染路径

请参阅 [[02-URP 的通用渲染器资源参考]]，了解 URP 中三种渲染路径以及每种路径的性能影响和限制。

## 减少 URP 使用的内存量

您可以在 [[01-URP 通用渲染管线资源参考]] 中执行以下操作：

- 除非有需要（例如使用了对场景深度进行采样的着色器），否则请禁用**深度纹理 (Depth Texture)**，使 URP 不必在不需要时存储深度纹理。
- 禁用**不透明纹理 (Opaque Texture)**，使 URP 不必在不需要时存储场景中不透明对象的快照。
- 如果使用延迟渲染路径，请禁用**使用渲染层 (Use Rendering Layers)**，使 URP 不会创建额外的渲染目标。
- 如果不需要，请禁用**高动态范围 (High Dynamic Range (HDR))**，使 URP 不必执行 HDR 计算。如果需要 HDR，请将 **HDR 精度 (HDR Precision)** 设置为 **32 位**。
- 降低**主光源 (Main Light) > 阴影分辨率 (Shadow Resolution)**，以降低主光源阴影贴图的分辨率。
- 如果使用其他光源，请降低**其他光源 (Additional Lights) > 阴影图集分辨率 (Shadow Atlas Resolution)**，以降低其他光源阴影贴图的分辨率。
- 如果不需要**光照剪影 (Light Cookies)**，请将其禁用，或降低**剪影图集分辨率 (Cookie Atlas Resolution)** 和**剪影图集格式 (Cookie Atlas Format)**。
- 在低端移动平台上，将**存储操作 (Store Actions)** 设置为 **Auto** 或 **Discard**，使 URP 不会使用内存带宽将各个通道的渲染目标复制到内存中或从内存中复制出来。

在 [[02-URP 的通用渲染器资源参考]] 中，可将**中间纹理 (Intermediate Texture)** 设置为 **Auto**，使 Unity 仅在必要时使用中间纹理进行渲染。这还可以减少 URP 使用的 GPU 内存带宽。更改此设置时，可使用[帧调试器](https://docs.unity3d.com/6000.7/Documentation/Manual/frame-debugger-window.html)检查 URP 是否删除了中间纹理。

您还可以执行以下操作：

- 尽量减少使用贴花渲染器功能，因为 URP 会创建额外的渲染通道来渲染贴花。这也会减少 CPU 和 GPU 上的处理时间。请参阅[贴花渲染器功能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-feature-decal.html)了解更多信息。
- 剥离未使用功能的[着色器变体](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shader-stripping.html)。

## 减少在 CPU 上的处理时间

您可以在 URP 资产 (URP Asset) 中执行以下操作：

- 将**体积更新模式 (Volume Update Mode)** 设置为 **Via Scripting**，使 URP 不会每帧更新体积。需使用 API（例如 [UpdateVolumeStack](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/api/UnityEngine.Rendering.Universal.CameraExtensions.html#UnityEngine_Rendering_Universal_CameraExtensions_UpdateVolumeStack_UnityEngine_Camera_)）手动更新体积。
- 在低端移动平台上，如果使用[反射探针](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting/reflection-probes.html)，请禁用**探针混合 (Probe Blending)** 和**盒体投影 (Box Projection)**。
- 在**阴影 (Shadows)** 部分中，减小**最大距离 (Max Distance)**，使 URP 可以在阴影通道中处理更少的对象。这也会减少 GPU 上的处理时间。
- 在**阴影 (Shadows)** 部分中，减少**级联数量 (Cascade Count)** 以减少渲染通道的数量。这也会减少 GPU 上的处理时间。
- 在**其他光源 (Additional Lights)** 部分中，禁用**投射阴影 (Cast Shadows)**。这也会减少 GPU 上的处理时间和 URP 使用的内存量。

场景中的每个摄像机都需要 URP 剔除和渲染资源。如要优化 URP 来获得更好的性能，请尽量减少使用的摄像机数量。这也会减少 GPU 上的处理时间。

## 减少 GPU 上的处理时间

您可以在 URP 资产 (URP Asset) 中执行以下操作：

- 减少或禁用**抗锯齿 (Anti-aliasing (MSAA))**，使 URP 不会使用内存带宽将帧缓冲区附件复制到内存中或从内存中复制出来。这也会减少 URP 使用的内存量。
- 禁用**地形孔洞 (Terrain Holes)**。
- 启用 **SRP 批处理程序 (SRP Batcher)**，使 URP 能减少绘制调用之间的 GPU 设置，并使材质数据持久保存在 GPU 内存中。首先检查着色器是否与 SRP 批处理程序兼容。这也会减少 CPU 上的处理时间。
- 在低端移动平台上，禁用 **LOD 交叉淡化 (LOD Cross Fade)**，使 URP 不会使用 Alpha 测试来淡入和淡出细节级别 (LOD) 网格。
- 将**其他光源 (Additional Lights)** 设置为 **Disabled**；如果使用前向渲染路径，则设置为 **Per Vertex**。这可以减少 URP 的光照计算工作。如果设置为 **Disabled**，还可以减少 CPU 上的处理时间。
- 禁用**柔和阴影 (Soft Shadows)**，或启用柔和阴影但降低**质量 (Quality)**。

您可以在通用渲染器资产中执行以下操作：

- 如果使用 Vulkan、Metal 或 DirectX 12 图形 API，请启用**原生渲染通道 (Native RenderPass)**，使 URP 可以自动减少将渲染纹理复制到内存中和从内存中复制出的频率。这也会减少 URP 使用的内存量。
- 如果使用前向 (Forward) 或前向+ (Forward+) 渲染路径，对于 PC 和游戏主机平台，请将**深度引动模式 (Depth Priming Mode)** 设置为 **Auto** 或 **Forced**；对于移动平台，则设置为 **Disabled**。在 PC 和游戏主机平台上，这使 URP 可以创建和使用深度纹理，从而避免在被遮挡的像素上运行像素着色器。
- 将**深度纹理模式 (Depth Texture Mode)** 设置为 **After Transparents**，使 URP 可以避免在不透明通道和透明通道之间切换渲染目标。

您还可以执行以下操作：

- 避免使用具有复杂光照计算的[复杂光照着色器](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shader-complex-lit.html)。如果使用复杂光照着色器，请禁用 **Clear Coat**。
- 在低端移动平台上，对静态对象使用[烘焙光照着色器](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/baked-lit-shader.html)，对动态对象使用[简单光照着色器](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/simple-lit-shader.html)。
- 如果使用屏幕空间环境光遮挡 (SSAO)，请参阅[环境光遮挡](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing-ssao.html)，了解有关对性能有重大影响的设置的更多信息。

## 其他资源

- [了解 URP 的性能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/understand-performance.html)
- [进行优化以获得更好的性能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/optimize-for-better-performance.html)
- [高阶 Unity 创作者通用渲染管线简介](https://resources.unity.com/games/introduction-universal-render-pipeline-for-advanced-unity-creators)
- [PC 和游戏主机高端图形的性能优化](https://unity.com/how-to/performance-optimization-high-end-graphics)
- [创建 Alba：如何构建高性能的开放世界游戏](https://www.youtube.com/watch?v=YOtDVv5-0A4)
- [移动设备上的 URP 后期处理](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/integration-with-post-processing.html)
- [优化光照以实现良好的帧率](https://unity.com/how-to/advanced/optimize-lighting-mobile-games)

请参阅以下内容了解有关设置的更多信息：

- [[00-URP 中的延迟渲染路径]]
- [前向+渲染路径](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/forward-plus-rendering-path.html)
- [[01-URP 通用渲染管线资源参考]]
- [[02-URP 的通用渲染器资源参考]]

---

## 文档导航

- 上一页：[[05-URP 中的已知问题：]]
- 目录：[[00-开始使用 URP]]
- 下一页：[[00-URP 中的图形质量设置]]
