# URP 中的可编程渲染通道简介

> 原文：[Introduction to Scriptable Render Passes in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/intro-to-scriptable-render-passes.html)


可编程渲染通道是一种用于更改 Unity 渲染场景或场景内对象的方式。通过它们，您可以针对项目中的每个场景进行独立的渲染微调。

您可以通过将可编程渲染通道注入渲染管线来实现自定义的视觉效果。有关详细信息，请参阅[[06-在 URP 中将可编程渲染通道添加到帧渲染循环/00-在 URP 中将可编程渲染通道添加到帧渲染循环]]。

可编程渲染通道允许您执行以下操作：

- 修改场景中材质的属性。
- 调整 Unity 渲染游戏对象的顺序。
- 使 Unity 能够读取摄像机缓冲区，并在着色器中使用这些缓冲区。

例如，在显示游戏内菜单时，您可以使用可编程渲染通道来模糊摄像机的视图。

在 URP 渲染循环的某些特定点，Unity 会注入可编程渲染通道。这些特定点被称为注入点。通过更改注入点，您可以控制可编程渲染通道对场景外观的影响。有关注入点的更多信息，请参阅[[06-在 URP 中将可编程渲染通道添加到帧渲染循环/04-URP 的注入点参考]]。

## 其他资源

- [[02-通过 URP 中的渲染器功能添加预构建效果/00-通过 URP 中的渲染器功能添加预构建效果]]
- [如何创建自定义渲染器功能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/create-custom-renderer-feature.html)
- [可编程渲染器功能参考](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/scriptable-renderer-features/scriptable-renderer-feature-reference.html)
- [[06-在 URP 中将可编程渲染通道添加到帧渲染循环/04-URP 的注入点参考]]

---

## 文档导航

- 上一页：[[00-在 URP 中自定义渲染和后期处理]]
- 目录：[[00-在 URP 中自定义渲染和后期处理]]
- 下一页：[[02-通过 URP 中的渲染器功能添加预构建效果/00-通过 URP 中的渲染器功能添加预构建效果]]
