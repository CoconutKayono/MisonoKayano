# URP 的渲染图查看器 (Render Graph Viewer) 窗口参考

> 原文：[Render Graph Viewer window reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-viewer-reference.html)


**渲染图查看器 (Render Graph Viewer)** 窗口显示通用渲染管线 (URP) 中当前场景的[[00-URP 中的渲染图系统]]。

有关**渲染图查看器 (Render Graph Viewer)** 窗口的更多信息，请参阅[[08-在 URP 中分析渲染图]]。

## 工具栏

| **控件** | **子控件** | **描述** |
| --- | --- | --- |
| **Capture** | 显示当前帧的渲染图。 |  |
| **Render graph** | 选择要显示渲染循环的渲染图。 |  |
| **Camera** | 选择要显示渲染循环的摄像机。 |  |
| **Pass Filter** | 选择要显示的渲染通道。 |  |
|  | **Nothing** | 不显示任何渲染通道。 |
|  | **Everything** | 显示所有渲染通道。 |
|  | **Culled** | 显示 URP 尚未包含在渲染图中的渲染通道，因为它们对最终图像没有影响。 |
|  | **Raster** | 仅显示使用 `renderGraph.AddRasterRenderPass` 创建的光栅渲染通道。 |
|  | **Unsafe** | 仅显示使用兼容性模式 API 的渲染通道。请参阅[[10-在渲染图渲染通道中使用兼容性模式 API]]。 |
|  | **Compute** | 仅显示使用 `renderGraph.AddComputePass` 创建的计算渲染通道。 |
| **Resource Filter** | 选择要显示的资源。 |  |
|  | **Nothing** | 不显示任何资源。 |
|  | **Everything** | 显示所有资源。 |
|  | **Imported** | 仅显示使用 `ImportTexure` 导入到渲染图中的资源。 |
|  | **Textures** | 仅显示纹理。 |
|  | **Buffers** | 仅显示缓冲区。 |
|  | **Acceleration Structures** | 仅显示在计算渲染通道中使用的加速结构。 |

### Pass Filter 下拉菜单

Pass Filter 下拉菜单用于按渲染通道类型筛选主窗口中的通道。各选项及其作用见上表。

### Resource Filter 下拉菜单

Resource Filter 下拉菜单用于按资源类型筛选主窗口中的资源。各选项及其作用见上表。

## 主窗口

主窗口是一个时间轴图，其在渲染图中显示渲染通道。显示以下内容：

- 左侧是渲染通道使用的资源列表，按 URP 创建它们的顺序列出。
- 顶部是渲染通道的列表，按 URP 执行它们的顺序列出。

当渲染通道和纹理在图形上相交时，资源访问块会显示渲染通道如何使用资源。访问块使用以下图标和颜色：

| **访问块图标或颜色** | **描述** |
| --- | --- |
| 带虚线 | 尚未创建资源。 |
| 绿色 | 渲染通道对资源具有只读访问权限。渲染通道可以读取资源。 |
| 红色 | 渲染通道对资源具有只读访问权限。渲染通道可以写入资源。 |
| 绿色和红色 | 渲染通道对资源具有读写访问权限。渲染通道可以读取或写入资源。 |
| 灰色 | 渲染通道无法访问资源。 |
| 地球图标 | 渲染通道将纹理设置为全局资源。如果地球图标具有灰色背景，则资源作为 `TextureHandle` 对象导入到渲染图中，并且通道使用 `SetGlobalTextureAfterPass` API。请参阅[[02-在 URP 中的渲染图形系统中创建纹理]]和[[00-在 URP 中的渲染通道之间传输纹理]]。 |
| **F** | 渲染通道可以使用帧缓冲区获取读取资源。请参阅[通过帧缓冲区获取来获取当前帧缓冲区](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-framebuffer-fetch.html)。 |
| 空白 | 资源已在内存中取消分配，因此不再存在。 |

选择一个访问块以在资源列表中显示资源，并在通道检视面板列表中显示渲染通道。

### 渲染通道

| **控件** | **描述** |
| --- | --- |
| 渲染通道名称 | 渲染通道的名称。此名称在 `AddRasterRenderPass` 或 `AddComputePass` 方法中设置。 |
| 合并条 | 如果 URP 将此通道与其他通道合并，则 Render Graph Viewer 会在合并的通道下方显示蓝色条。 |
| 资源访问概述条 | 选择渲染通道名称时，资源访问概述条会显示有关所选通道和相关通道的信息。将光标悬停在概述块上以了解更多信息。选择一个概述代码块以打开渲染通道的 C# 文件。 <br><br>概述块使用以下颜色： 白色：已选通道。 灰色：通道与所选通道无关。 蓝色：通道读取或写入所选通道使用的资源。 蓝色闪烁：通道读取或写入所选通道使用的资源，并可与当前通道合并。 &#124; |

### 资源

| **属性** | **描述** |
| --- | --- |
| Resource type | 资源的类型。请参阅以下屏幕截图。 |
| Resource name | 资源名称。 |
| Imported resource | 如果导入了资源，则显示向左箭头。请参阅[[03-将纹理导入 URP 中的渲染图系统]]。 |

![渲染图查看器 (Render Graph Viewer) 图标](render-graph-viewer-icons.png)

渲染图查看器 (Render Graph Viewer) 图标

### 渲染图查看器图标

| **图标** | **描述** |
| --- | --- |
| ![纹理图标](render-graph-viewer-icon-texture.png) | 纹理。 |
| ![加速结构图标](render-graph-viewer-icon-acceleration-structure.png) | 加速结构。 |
| ![缓冲区图标](render-graph-viewer-icon-buffer.png) | 缓冲区。 |

## 资源列表

在资源列表中选择资源以展开或折叠有关该资源的信息。

还可以使用搜索栏来按名称查找资源。

| **属性** | **描述** |
| --- | --- |
| Resource name | 资源名称。 |
| Imported resource | 如果导入资源，则显示向左箭头。 |
| **Size** | 资源大小（以像素为单位）。 |
| **Format** | 纹理格式。有关纹理格式的更多信息，请参阅 [GraphicsFormat](https://docs.unity3d.com/2023.3/Documentation/ScriptReference/Experimental.Rendering.GraphicsFormat.html)。 |
| **Clear** | 如果 URP 清除纹理，则显示 **True**。 |
| **BindMS** | 纹理是否绑定为多重采样纹理。有关多重采样纹理的更多信息，请参阅 [RenderTextureDescriptor.BindMS](https://docs.unity3d.com/ScriptReference/RenderTextureDescriptor-bindMS.html)。 |
| **Samples** | 多重采样抗锯齿 (MSAA) 对纹理进行采样的次数。请参阅[[06-在通用渲染管线中添加抗锯齿]]。 |
| **Memoryless** | 如果在使用基于图块的延迟渲染 (TBDR) 的移动平台上将资源存储在图块内存中，则显示 **True**。有关 TBDR 的更多信息，请参阅[[01-URP 中的渲染图系统简介]]。 |

## 通道列表

在主窗口中选择一个渲染通道可在通道列表中显示有关渲染通道的信息。

还可以使用搜索栏来按名称查找渲染通道。

| **属性** | **描述** |
| --- | --- |
| Pass name | 渲染通道名称。如果 URP 合并了多个通道，此属性将显示所有合并通道的名称。 |
| **Native Render Pass Info** | 显示有关 URP 是否通过合并多个渲染通道为此渲染通道创建了原生渲染通道的信息。有关原生渲染通道的更多信息，请参阅[[01-URP 中的渲染图系统简介]]。 |
| **Pass break reasoning** | 显示 URP 无法将此渲染通道与下一个渲染通道合并的原因。 |

### 渲染图形通道信息 (Render Graph Pass Info)

**Render Graph Pass Info** 部分显示有关渲染通道及其使用的每个资源的信息。

如果 URP 将多个通道合并到此通道中，则该部分将显示每个合并通道的信息。

| **属性** | **描述** |
| --- | --- |
| **Name** | 渲染通道名称。 |
| **Attachment dimensions** | 渲染通道使用的资源的大小（以像素为单位）。如果渲染通道不使用资源，则显示 **0x0x0**。 |
| **Has depth attachment** | 资源是否具有深度纹理。 |
| **MSAA samples** | 多重采样抗锯齿 (MSAA) 对纹理进行采样的次数。请参阅[[06-在通用渲染管线中添加抗锯齿]]。 |
| **Async compute** | 渲染通道是否使用计算着色器访问资源。 |

### 附件加载/存储操作 (Attachments Load/Store Actions)

**Attachments Load/Store Actions** 部分显示渲染通道使用的资源。如果渲染通道不使用任何资源，则此部分显示**无附件 (No attachments)**。

| **属性** | **描述** |
| --- | --- |
| **Name** | 资源名称。 |
| **Load Action** | 资源的加载操作。请参阅 [RenderBufferLoadAction](https://docs.unity3d.com/ScriptReference/Rendering.RenderBufferLoadAction.html)。 |
| **Store Action** | 资源的存储操作，以及 URP 稍后在另一个渲染通道中或图形外部如何使用资源。请参阅 [RenderBufferStoreAction](https://docs.unity3d.com/ScriptReference/Rendering.RenderBufferStoreAction.html)。 |

## 其他资源

- [帧调试器](https://docs.unity3d.com/2023.3/Documentation/Manual/frame-debugger-window.html)
- [了解性能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/understand-performance.html)

---

## 文档导航

- 上一页：[[10-在渲染图渲染通道中使用兼容性模式 API]]
- 目录：[[00-URP 中的渲染图系统]]
- 下一页：[[00-在 URP 中将可编程渲染通道添加到帧渲染循环]]
