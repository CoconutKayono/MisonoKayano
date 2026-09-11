# 在 URP 中将可编程渲染通道添加到帧渲染循环

> 原文：[Adding a Scriptable Render Pass to the frame rendering loop in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/inject-a-render-pass.html)


通过创建可编程渲染器功能或使用 `RenderPipelineManager` API 将自定义渲染通道添加到通用渲染管线 (URP) 的帧渲染循环中。

| 页面 | 描述 |
| --- | --- |
| [通过可编程渲染器功能注入渲染通道](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/scriptable-renderer-features/scriptable-renderer-features-landing.html) | 编写一个继承自 `ScriptableRendererFeature` 的类，并通过该类实例化自定义渲染通道，将其插入渲染管线。 |
| [[02-在 URP 中通过脚本注入渲染通道]] | 使用 `RenderPipelineManager` API 将自定义渲染通道插入渲染管线。 |
| [[04-URP 的注入点参考]] | URP 提供多个注入点，允许在帧渲染循环的不同阶段插入渲染通道。 |

---


## 目录

| 页面 | 说明 |
| --- | --- |
| [[01-在 URP 中创建可编程渲染器功能]] | Inject a render pass with a Scriptable Renderer Feature in URP |
| [[02-在 URP 中通过脚本注入渲染通道]] | Inject a render pass using the RenderPipelineManager API in URP |
| [[03-将渲染通道限制到 URP 场景区域]] | Restrict a render pass to a scene area in URP |
| [[04-URP 的注入点参考]] | Injection points reference for URP |

## 文档导航

- 上一页：[[11-URP 的渲染图查看器 (Render Graph Viewer) 窗口参考]]
- 目录：
- 下一页：[[01-在 URP 中创建可编程渲染器功能]]
