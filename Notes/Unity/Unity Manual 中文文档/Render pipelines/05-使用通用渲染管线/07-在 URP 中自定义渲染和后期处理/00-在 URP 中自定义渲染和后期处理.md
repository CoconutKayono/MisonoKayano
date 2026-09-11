# 在 URP 中自定义渲染和后期处理

> 原文：[Custom rendering and post-processing in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customizing-urp.html)


在通用渲染管线 (URP) 中自定义和扩展渲染过程。在 C# 脚本中创建自定义渲染通道并将其注入 URP 帧渲染循环。

| 页面 | 描述 |
| --- | --- |
| [[01-URP 中的可编程渲染通道简介]] | 了解如何使用可编程渲染通道更改 Unity 渲染场景或场景中的对象的方式。 |
| [[00-通过 URP 中的渲染器功能添加预构建效果]] | 用于将预构建的渲染通道添加到 URP 并配置其行为的资源。 |
| [[03-URP 中的自定义渲染通道工作流程]] | 添加和注入自定义渲染通道。 |
| [[00-URP 中的渲染图系统]] | 使用 `RenderGraph` API 创建可编程渲染通道的资源和方法。 |
| [[00-在 URP 中将可编程渲染通道添加到帧渲染循环]] | 通过可编程渲染器功能或 `RenderPipelineManager` API 注入自定义渲染通道的资源和技术。 |
| [兼容性模式](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/compatibility-mode.html) | 当 URP 图形设置中启用了**兼容性模式（禁用了渲染图）**时，编写可编程渲染通道。Unity 不再开发或改进此渲染路径。 |

## 其他资源

- [[01-通用渲染管线中的渲染]]
- [[00-通用渲染管线基础知识]]
- [[01-向 URP 渲染器添加渲染器功能]]
- [如何创建自定义后处理效果](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing/post-processing-custom-effect-low-code.html)
- [在自定义渲染管线中执行渲染命令](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/manual/srp-using-scriptable-render-context.html)

---


## 目录

| 页面 | 说明 |
| --- | --- |
| [[01-URP 中的可编程渲染通道简介]] | Introduction to Scriptable Render Passes in URP |
| [[00-通过 URP 中的渲染器功能添加预构建效果]] | Adding pre-built effects via Renderer Features in URP |
| [[03-URP 中的自定义渲染通道工作流程]] | Custom render pass workflow in URP |
| [[04-在 URP 中执行 Blit 的最佳实践]] | Blit in URP |
| [[00-URP 中的渲染图系统]] | Render graph system in URP |
| [[00-在 URP 中将可编程渲染通道添加到帧渲染循环]] | Adding a Scriptable Render Pass to the frame rendering loop in URP |
| [[07-修改 URP 源代码]] | Modify URP source code |

## 文档导航

- 上一页：[[06-在通用渲染管线中添加抗锯齿]]
- 目录：
- 下一页：[[01-URP 中的可编程渲染通道简介]]
