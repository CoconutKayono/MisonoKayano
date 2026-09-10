# URP 中的自定义渲染通道工作流程

> 原文：[Custom render pass workflow in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/custom-rendering-pass-workflow-in-urp.html)


自定义渲染通道是一种用于更改通用渲染管线 (URP) 渲染场景或场景中对象的方式的方法。自定义渲染通道包含您自己的渲染代码，您可以在注入点将其插入到渲染管线中。

要添加自定义渲染通道，请完成以下任务：

- 使用可编程渲染通道 API 给自定义渲染通道。
- 通过或 将自定义渲染通道添加到 URP 的帧渲染循环中。

## 创建自定义渲染通道的代码

要为自定义渲染通道创建代码，需编写一个继承 `ScriptableRenderPass` 的类。在此类中，使用[[05-URP 中的渲染图系统/01-URP 中的渲染图系统简介]] 来告知 Unity 要使用哪些纹理和渲染目标以及要对它们执行哪些操作。

请参阅[[01-URP 中的可编程渲染通道简介]]了解更多信息。

## 创建可编程渲染器功能

要将自定义渲染通道添加到 URP 的帧渲染循环，需编写一个继承 `ScriptableRendererFeature` 的类。

可编程渲染器功能会执行以下操作：

1. 给创建的自定义渲染通道创建实例。
2. 将自定义渲染通道插入到渲染管线中。

请参阅[[06-在 URP 中将可编程渲染通道添加到帧渲染循环/01-在 URP 中创建可编程渲染器功能]]了解更多信息。

## 使用 RenderPipelineManager API

要将自定义渲染通道添加到 URP 的帧渲染循环，还可以将方法订阅到 [RenderPipelineManager](https://docs.unity3d.com/ScriptReference/Rendering.RenderPipelineManager.html) 类中的某个事件。

请参阅[[06-在 URP 中将可编程渲染通道添加到帧渲染循环/02-在 URP 中通过脚本注入渲染通道]]了解更多信息。

## 其他资源

- [[05-URP 中的渲染图系统/01-URP 中的渲染图系统简介]]
- [完整的可编程渲染器功能示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/create-custom-renderer-feature.html)

---

## 文档导航

- 上一页：[[02-通过 URP 中的渲染器功能添加预构建效果/03-URP 的渲染对象渲染器功能 (Render Objects Renderer Feature) 参考]]
- 目录：[[00-在 URP 中自定义渲染和后期处理]]
- 下一页：[[04-在 URP 中执行 Blit 的最佳实践]]
