# URP 中渲染路径简介

> 原文：[Introduction to rendering paths in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-paths-introduction-urp.html)


您可以在通用渲染管线 (URP) 中选择以下渲染路径之一：

- 前向
- Forward+
- 延迟

每个渲染路径都会影响 Unity 绘制和光照对象的方式，从而影响光照结果和渲染时间。效果取决于您为其构建的平台。

有关选择渲染路径的更多信息，请参阅[[02-在 URP 中选择渲染路径]]。

## URP 中的渲染路径要求

| **功能** | **前向** | **Forward+** | **延迟** |
| --- | --- | --- | --- |
| 最小着色器模型 | 2.0 | 2.0 | 4.5 |
| OpenGL 和 OpenGL ES 支持 | 是 | 是 | 否 |

## 其他资源

- 在 Unity 学习网站上[了解渲染路径](https://learn.unity.com/tutorial/understanding-rendering-paths)
- [Unity LTS 2022 Release Live!](https://www.youtube.com/watch?v=oUQapNQgpRI&t=8183s) - 演示 Forward+ 渲染路径的 Unity YouTube 视频

---

## 文档导航

- 上一页：[[00-URP 中的渲染路径]]
- 目录：[[00-URP 中的渲染路径]]
- 下一页：[[02-在 URP 中选择渲染路径]]
