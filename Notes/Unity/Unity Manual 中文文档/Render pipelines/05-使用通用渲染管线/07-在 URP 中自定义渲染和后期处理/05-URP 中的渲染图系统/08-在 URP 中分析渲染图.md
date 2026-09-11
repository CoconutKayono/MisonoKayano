# 在 URP 中分析渲染图

> 原文：[Analyze a render graph in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-view.html)


有几种方法可用于分析渲染图：




## 使用渲染图查看器

要打开**渲染图查看器 (Render Graph Viewer)** 窗口，请选择**窗口 (Window) > 分析 (Analysis) > 渲染图查看器 (Render Graph Viewer)**。

Render Graph Viewer 窗口显示一个渲染图，这是通用渲染管线 (URP) 逐步完成每一帧的经过优化的渲染序列。Render Graph Viewer 显示内置渲染通道和您创建的任何[[01-URP 中的可编程渲染通道简介]]。

有关 **Render Graph Viewer** 窗口的更多信息，请参阅[[11-URP 的渲染图查看器 (Render Graph Viewer) 窗口参考]]。

### 查看渲染图

默认情况下，**渲染图查看器 (Render Graph Viewer)** 窗口显示当前场景的渲染图。要选择另一个渲染图，请使用工具栏中的下拉选单。

#### 示例：检查 URP 如何使用资源

您可以使用资源名称旁边的资源访问块来检查渲染通道如何使用资源。

![渲染图查看器 (Render Graph Viewer) 示例](render-graph-viewer.png)

渲染图查看器 (Render Graph Viewer) 示例

在前面的示例中，`_MainLightShadowmapTexture_` 纹理经历了以下几个阶段：

1. 在 **InitFrame** 和 **SetupCameraProperties** 之间的前五次渲染通道中，纹理不存在。
2. **主光源阴影贴图 (Main Light Shadowmap)** 渲染通道将纹理创建为全局纹理，并且对其具有只读访问权限。有关全局纹理的更多信息，请参阅[[00-在 URP 中的渲染通道之间传输纹理]]。  **主光源阴影贴图 (Main Light Shadowmap)** 下方的蓝色合并栏表示 URP 将**主光源阴影贴图 (Main Light Shadowmap)**、**附加光源阴影贴图 (Additional Lights Shadowmap)** 和 **SetupCameraProperties** 合并到单个渲染通道。
3. 接下来的五个渲染通道无法访问纹理。
4. 第一个**绘制对象**渲染通道对纹理具有只读访问权限。
5. 接下来的两个渲染通道无法访问纹理。
6. 第二个**绘制对象**渲染通道对纹理具有只读访问权限。
7. Unity 会销毁该纹理，因为不再需要该纹理。

### 检查 URP 如何优化渲染通道

要检查渲染通道的详细信息，例如，要了解其不是原生渲染通道或合并通道的原因，请执行以下操作之一：

- 选择渲染通道名称可在通道列表中显示详细信息。
- 在渲染通道名称下方，将光标悬停在灰色、蓝色或闪烁的蓝色资源访问概述块上。

有关显示渲染通道详细信息的更多信息，请参阅[[11-URP 的渲染图查看器 (Render Graph Viewer) 窗口参考]]。



## 使用渲染调试器

您可以使用渲染调试器在**控制台 (Console)** 窗口中记录 URP 使用的资源及其如何使用它们。

要启用日志记录，请遵循以下步骤：

1. 选择**窗口 (Window) > 分析 (Analysis) > 渲染调试器 (Rendering Debugger)** 以打开**渲染调试器 (Rendering Debugger)** 窗口。
2. 在左侧面板中，选择**渲染图 (Render Graph)** 选项卡。
3. 选择**启用日志记录 (Enable Logging)**。
4. 选择**记录帧信息 (Log Frame Information)** 以记录 URP 如何使用资源，或选择**记录资源 (Log Resources)** 以记录有关资源的详细信息。
5. 在**控制台 (Console)** 窗口中选择新的项目以显示完整日志。

有关渲染调试器的更多信息，请参阅[渲染调试器](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/rendering-debugger.html)。



## 使用帧调试器

使用[帧调试器](https://docs.unity3d.com/2023.3/Documentation/Manual/frame-debugger-window.html)可检查渲染通道并在渲染循环中绘制调用。

当渲染图系统处于活动状态时，帧调试器在 [Event Hierarchy 面板](https://docs.unity3d.com/Manual/frame-debugger-window-event-hierarchy.html)中显示以下内容：

- 名为 **ExecuteRenderGraph** 的父渲染事件。
- 名为 **(RP <render-pass>:<subpass>)** 的子渲染事件，其中 `<render-pass>` 表示渲染通道编号，`<subpass>` 表示子通道编号。

帧调试器仅显示包含绘制调用的渲染通道。

有关帧调试器的更多信息，请参阅[帧调试器](https://docs.unity3d.com/2023.3/Documentation/Manual/frame-debugger-window.html)。

## 其他资源

- [[00-URP 中的渲染图系统]]
- [[01-通用渲染管线中的渲染]]
- [帧调试器](https://docs.unity3d.com/2023.3/Documentation/Manual/frame-debugger-window.html)
- [渲染调试器](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/rendering-debugger.html)
- [了解性能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/understand-performance.html)

---

## 文档导航

- 上一页：[[02-在 URP 中为计算着色器创建输入数据]]
- 目录：[[00-URP 中的渲染图系统]]
- 下一页：[[09-优化渲染图]]
