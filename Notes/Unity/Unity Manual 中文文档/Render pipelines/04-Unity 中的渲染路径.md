# Unity 中的渲染路径

> 原文：[Rendering paths in Unity](https://docs.unity3d.com/6000.7/Documentation/Manual/rendering-paths-introduction.html)

> [!IMPORTANT]
> 内置渲染管线（Built-In Render Pipeline）已弃用，并将在未来版本中废止。在整个 Unity 6.7 LTS 生命周期内，它仍会获得支持，包括错误修复和维护。有关迁移的更多信息，请参阅 [[00-从内置渲染管线升级到 URP]] 和 [[02-渲染管线功能比较参考]]。

渲染路径是一系列操作，用于绘制和照亮摄像机看到的 GameObject。不同渲染路径的功能和性能特征各不相同。

Unity 支持前向（Forward）和延迟（Deferred）渲染路径。

## 前向

前向渲染路径是 Unity 项目中的默认渲染路径。其工作方式如下：

- Unity 依次照亮每个 GameObject。
- 光照存在限制，例如 Unity 为每个 GameObject 提供光照的频率或质量。这些限制因渲染管线而异。

通用渲染管线（URP）还有一个 [[04-URP 中的前向渲染路径|Forward+ 渲染路径]]，它类似于前向渲染路径，但不限制每个 GameObject 可使用的光源数量。

> **注意：**内置渲染管线还有一个 [[04-内置渲染管线中的旧版顶点光照渲染路径|Legacy Vertex Lit]] 渲染路径，它是前向渲染路径的子集。

## 延迟

延迟渲染路径的工作方式如下：

- Unity 首先创建几何缓冲区（G-buffer）。这是一组用于存储摄像机看到的几何体和材质数据的纹理。
- Unity 使用 G-buffer 中的数据一次性照亮所有 GameObject。
- 光照限制较少，因此 GameObject 和阴影可以呈现更多细节。例如，法线贴图和 Cookie 可与所有光源配合使用。

延迟渲染路径无法渲染透明对象，因此在渲染路径结束时，Unity 会使用前向渲染通道来渲染透明对象。

## 选择渲染路径

每种渲染路径都有优点和缺点。有关更多信息，请参阅以下内容：

- [[00-URP 中的渲染路径]]
- [[00-内置渲染管线中的渲染路径]]

## 其他资源

- [逐像素光照和逐顶点光照](https://docs.unity3d.com/6000.7/Documentation/Manual/PerPixelLights.html)

---

## 文档导航

- 上一页：[[04-更改或检测激活的渲染管线]]
- 目录：[[00-渲染管线]]
- 下一页：[[00-使用通用渲染管线]]
