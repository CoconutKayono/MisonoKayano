# URP 中的渲染图系统

> 原文：[Render graph system in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph.html)


渲染图系统是用于创建[[01-URP 中的可编程渲染通道简介]]的一组 API。

| 页面 | 描述 |
| --- | --- |
| [[01-URP 中的渲染图系统简介]] | 什么是渲染图系统以及渲染系统如何优化渲染。 |
| [[02-在 URP 中使用渲染图系统编写渲染通道]] | 使用渲染图 API 编写可编程渲染通道。 |
| [[00-URP 中的 Render Graph 系统中的纹理]] | 在渲染通道中访问和使用纹理以及如何执行__ blit__“位块传输 (Bit Block Transfer)”的简写。blit 操作是将数据块从内存中的一个位置传输到另一个位置的过程。 <br><br>执行 Blit 操作。有关 Blit 术语，请参阅 [Glossary](https://docs.unity3d.com/6000.7/Documentation/Manual/Glossary.html#blit)。 &#124; |
| [[00-URP 中的渲染图系统中的帧数据]] | 获取 URP 为当前帧创建的纹理并在渲染通道中使用它们。 |
| [[06-在 URP 中的渲染图形系统中绘制对象]] | 使用 `RendererList` API 在渲染图系统中绘制对象。 |
| [[00-在 URP 的渲染图系统中的计算着色器]] | 创建一个运行计算着色器的渲染通道。 |
| [[08-在 URP 中分析渲染图]] | 使用渲染图查看器、渲染调试器或帧调试器检查渲染图。 |
| [[10-在渲染图渲染通道中使用兼容性模式 API]] | 要在渲染图系统中使用兼容性模式 API（例如 `SetRenderTarget`），请使用渲染图 `UnSafePass` API。 |
| [[11-URP 的渲染图查看器 (Render Graph Viewer) 窗口参考]] | **渲染图查看器 (Render Graph Viewer)** 窗口的参考。 |

## 其他资源

- [帧调试器](https://docs.unity3d.com/2023.3/Documentation/Manual/frame-debugger-window.html)
- [完整的可编程渲染器功能示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/create-custom-renderer-feature.html)

---


## 目录

| 页面 | 说明 |
| --- | --- |
| [[01-URP 中的渲染图系统简介]] | Introduction to the render graph system in URP |
| [[02-在 URP 中使用渲染图系统编写渲染通道]] | Write a render pass using the render graph system in URP |
| [[03-在 URP 中使用渲染图系统执行 Blit]] | Blit using the render graph system in URP |
| [[00-URP 中的 Render Graph 系统中的纹理]] | Textures in the Render Graph system in URP |
| [[00-URP 中的渲染图系统中的帧数据]] | Frame data in the render graph system in URP |
| [[06-在 URP 中的渲染图形系统中绘制对象]] | Draw objects in the render graph system in URP |
| [[00-在 URP 的渲染图系统中的计算着色器]] | Compute shaders in the render graph system in URP |
| [[08-在 URP 中分析渲染图]] | Analyze a render graph in URP |
| [[09-优化渲染图]] | Optimize a render graph |
| [[10-在渲染图渲染通道中使用兼容性模式 API]] | Use the CommandBuffer interface in a render graph |
| [[11-URP 的渲染图查看器 (Render Graph Viewer) 窗口参考]] | Render Graph Viewer window reference for URP |

## 文档导航

- 上一页：[[04-在 URP 中执行 Blit 的最佳实践]]
- 目录：
- 下一页：[[01-URP 中的渲染图系统简介]]
