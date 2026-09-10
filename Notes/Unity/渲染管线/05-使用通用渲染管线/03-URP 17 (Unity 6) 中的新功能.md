# URP 17 (Unity 6) 中的新功能

> 原文：[What’s new in URP 17 (Unity 6.0)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/whats-new/urp-whats-new.html)

本节介绍 URP 17 中的新功能、改进和已修复的问题。

> **注意：**对于 URP 17.2（Unity 6.2）及更高版本，请参阅主 [Unity 新功能](https://docs.unity3d.com/6000.7/Documentation/Manual/WhatsNew.html)章节。

有关 URP 17 中所有更改的完整列表，请参阅 [Changelog](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/changelog/CHANGELOG.html)。

## 功能

本节概述此版本中的新功能。

### Render Graph 系统

此版本引入了 [[07-在 URP 中自定义渲染和后期处理/05-URP 中的渲染图系统/00-URP 中的渲染图系统]]。Render Graph 系统是构建在 Scriptable Render Pipeline（SRP）API 之上的框架，可改进自定义和维护渲染管线的方式。

Render Graph 系统减少了 URP 使用的内存量，并使内存管理更加高效。它只为当前帧实际使用的资源分配内存，因此不再需要编写复杂逻辑来处理资源分配，也不必为少见的最坏情况预留资源。Render Graph 系统还会在 compute queue 与 graphics queue 之间生成正确的同步点，从而减少帧时间。

[[07-在 URP 中自定义渲染和后期处理/05-URP 中的渲染图系统/11-URP 的渲染图查看器 (Render Graph Viewer) 窗口参考]] 可以可视化 Render Pass 如何使用帧资源，并调试渲染过程。

有关 Render Graph 系统的更多信息，请参阅 [[07-在 URP 中自定义渲染和后期处理/05-URP 中的渲染图系统/00-URP 中的渲染图系统]]。

### 后期处理中的 Alpha Processing 设置

URP 17 新增 **Alpha Processing** 设置（**URP Asset** > **Post-processing** > **Alpha Processing**）。启用此设置后，URP 会将后期处理输出渲染到带有 Alpha 通道的 Render Texture 中。在以前的版本中，URP 会将 Alpha 值替换为 1，从而丢弃 Alpha 通道。

Render Target 需要使用包含 Alpha 通道的格式。对于 SDR（HDR 关闭），Camera Color Buffer 格式必须为 RGBA8；对于 HDR（64 位），必须为 RGBA16F。您可以使用 **URP Asset** > **Quality** 中的设置配置格式。

此功能的示例用途包括：

- 渲染游戏内 UI，例如 head-up display。您可以使用不同的后期处理配置渲染多个 Render Texture，并使用 Alpha 通道合成最终输出。
- 渲染角色自定义界面：Unity 使用不同的后期处理效果渲染背景界面和 3D 角色，然后使用 Alpha 通道将二者混合。
- 支持视频透视的 XR 应用。

### 减少 CPU 上的渲染工作

URP 17 包含一些新功能，可以将特定任务移交给 GPU，从而减少 CPU 的工作负载并加快渲染过程。

#### GPU Resident Drawer

URP 17 包含一种名为 **GPU Resident Drawer** 的新渲染系统。

此系统会自动使用 [BatchRendererGroup API](https://docs.unity3d.com/6000.7/Documentation/Manual/batch-renderer-group.html)，通过 GPU instancing 绘制 GameObject，从而减少 Draw Call 数量并释放 CPU 处理时间。

有关 GPU Resident Drawer 的更多信息，请参阅 [Reduce rendering work on the CPU](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/reduce-rendering-work-on-cpu.html)章节。

#### GPU occlusion culling

使用 GPU occlusion culling 时，当对象被其他对象遮挡，Unity 会使用 GPU 而不是 CPU 将其排除在渲染之外。Unity 会利用这些信息，加快遮挡较多场景中的渲染速度。

有关 GPU occlusion culling 的更多信息，请参阅 [Reduce rendering work on the CPU](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/gpu-culling.html)章节。

### Forward+ Rendering Path 中的 Foveated Rendering

Forward+ Rendering Path 现在支持 Foveated Rendering。

### Camera History API

此版本包含 [Camera History API](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.UniversalCameraHistory.html)，可让您访问每个 Camera 的 History Texture，并在自定义 Render Pass 中使用这些纹理。History Texture 是 Unity 在之前帧中为每个 Camera 渲染的颜色纹理和深度纹理。

对于需要使用一个或多个之前帧的帧数据的渲染算法，可以使用 History Texture。

URP 实现了每个 Camera 的颜色和深度纹理历史记录，并为自定义 Render Pass 提供历史记录访问能力。

### Rendering Debugger 中的 Mipmap Streaming 部分

[Rendering Debugger](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/rendering-debugger.html) 现在包含 **Mipmap Streaming** 部分。此部分可用于检查 Texture Streaming 活动。

### Spatial Temporal Post-Processing（STP）

Spatial Temporal Post-Processing（STP）通过放大 Unity 以较低分辨率渲染的帧来优化 GPU 性能并提升视觉质量。STP 适用于支持 compute shader 的桌面平台、游戏主机和移动设备。

要启用 STP，请在当前激活的 **URP Asset** 中选择 **Quality** > **Upscaling Filter** > **Spatial Temporal Post-Processing (STP)**。

## 改进

本节概述此版本中的主要改进。

### Adaptive Probe Volumes（APV）

此版本对 [Adaptive Probe Volumes](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/probevolumes.html) 做出了以下改进：

- [APV Lighting Scenario Blending](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/probevolumes-bakedifferentlightingsetups.html)。
- [APV sky occlusion support](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/probevolumes-skyocclusion.html)。
- [APV disk streaming](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/probevolumes-streaming.html)。

### Volume framework 增强

此版本针对所有平台（尤其是移动平台）优化了 Volume framework 的 CPU 性能。现在可以设置全局 Volume 默认值，并在 Quality 设置中覆盖这些默认值。

### 8192 阴影纹理分辨率

**Shadow Resolution** 属性现在为 Main Light 和 Additional Lights 提供 `8192` 选项。

### 使用 URP Config package 更改渲染管线设置

[[05-URP 中的图形质量设置/06-使用 URP 配置包配置设置]] 可更改 Editor 界面中不可用的某些渲染管线设置。

例如，可以[[04-开始使用 URP/01-通用渲染管线基础知识/02-URP 中的渲染路径/06-URP 中的 Forward+ 渲染路径的故障排除]]。

### URP 文档已移至 Unity Manual

Unity 6 中 Universal Render Pipeline 的文档已从独立的 URP 文档网站移至主 Unity Manual。Unity 重新组织了 URP 专属页面和通用图形页面，使其更关注用户最终要完成的任务。这一更改旨在提升 URP 文档的可发现性和阅读体验。

指向独立 URP 网站页面的链接现在会重定向到主 Manual 中重新定位的页面（或等效页面）。

[URP scripting API](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/api/index.html) 文档仍保留在独立网站上。

## 已解决的问题

有关 URP 17 中已解决问题的完整列表，请参阅 [Changelog](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/changelog/CHANGELOG.html)。

## 已知问题

有关 URP 17 中已知问题的信息，请参阅 [[04-开始使用 URP/02-安装和升级 URP/05-URP 中的已知问题：]]。

---

## 文档导航

- 上一页：[[02-URP 的要求和兼容性]]
- 目录：[[00-使用通用渲染管线]]
- 下一页：[[04-开始使用 URP/00-开始使用 URP]]
