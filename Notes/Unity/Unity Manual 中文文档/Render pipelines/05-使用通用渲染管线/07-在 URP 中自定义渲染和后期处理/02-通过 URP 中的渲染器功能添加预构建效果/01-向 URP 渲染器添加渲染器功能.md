# 向 URP 渲染器添加渲染器功能

> 原文：[Add a Renderer Feature to a URP Renderer](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-renderer-feature.html)


URP 在 **DrawOpaqueObjects** 和 **DrawTransparentObjects** 通道中绘制对象。您可能需要在帧渲染中的不同点绘制对象，或者以其他方式解释和写入渲染数据（如深度和模板）。渲染对象渲染器功能 (Render Objects Renderer Feature) 允许您通过特定的覆盖，在特定的图层、特定的时间绘制对象，以进行此类自定义。

有关如何使用渲染器功能的示例，请参阅 [[03-在 URP 中导入包示例]]。

要向渲染器添加渲染器功能，请执行以下操作：

1. 在**项目 (Project)** 窗口中，选择一个渲染器。  ![选择一个渲染器。](renderer-feature-select-renderer.png) 选择一个渲染器。  检视面板 (Inspector) 窗口显示渲染器属性。  ![检视面板 (Inspector) 窗口显示渲染器属性。](renderer-feature-inspector-no-rend-features.png) 检视面板 (Inspector) 窗口显示渲染器属性。
2. 在检视面板 (Inspector) 窗口中，选择**添加渲染器功能 (Add Renderer Feature)**。在列表中，选择一项渲染器功能 (Renderer Feature)。  ![选择添加渲染器功能 (Add Renderer Feature)，然后选择一项渲染器功能 (Renderer Feature)。](renderer-feature-select-renderer-feature.png) 选择**添加渲染器功能 (Add Renderer Feature)**，然后选择一项渲染器功能 (Renderer Feature)。  Unity 会向渲染器添加选定的渲染器功能。  ![新的渲染器功能已添加。](renderer-feature-created.png) 新的渲染器功能已添加。

Unity 在项目 (Project) 窗口中将渲染器功能显示为渲染器的子项：

![Unity 在项目 (Project) 窗口中将渲染器功能显示为渲染器的子项](renderer-feature-project-window.png)

Unity 在项目 (Project) 窗口中将渲染器功能显示为渲染器的子项

## 其他资源

- [[02-通过 URP 中的渲染对象渲染器功能 (Render Objects Renderer Feature) 创建自定义渲染效果的示例]]
- [贴花渲染器功能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-feature-decal-landing.html)
- [屏幕空间环境光遮挡 (SSAO) 渲染器功能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing-ssao.html)
- [屏幕空间阴影渲染器功能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-feature-screen-space-shadows.html)

---

## 文档导航

- 上一页：[[00-通过 URP 中的渲染器功能添加预构建效果]]
- 目录：[[00-通过 URP 中的渲染器功能添加预构建效果]]
- 下一页：[[02-通过 URP 中的渲染对象渲染器功能 (Render Objects Renderer Feature) 创建自定义渲染效果的示例]]
