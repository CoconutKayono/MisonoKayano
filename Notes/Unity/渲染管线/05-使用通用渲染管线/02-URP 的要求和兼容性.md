# URP 的要求和兼容性

> 原文：[Requirements and compatibility for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/requirements.html)

本页介绍 Universal Render Pipeline（URP）包的系统要求和兼容性。

## Unity Editor 兼容性

URP 是一个 [core Unity package](https://docs.unity3d.com/6000.7/Documentation/Manual/pack-core.html)。对于 Unity 的每个 alpha、beta 或补丁版本，Unity 主安装程序都会包含该包的最新版本。

Package Manager 窗口只显示该包的主版本号和次版本号。例如，Unity 6.2.x 的所有版本都使用 17.2.0 版本。

您可以使用 Package Manager 从磁盘安装其他版本的图形包，也可以修改 `manifest.json` 文件来安装。

## 渲染管线兼容性

使用 URP 创建的项目与 High Definition Render Pipeline（HDRP）或 Built-in Render Pipeline 不兼容。在开始开发项目之前，必须决定使用哪一种渲染管线。有关如何选择渲染管线的信息，请参阅[[../03-选择渲染管线/02-渲染管线功能比较参考]]。

## Graphics API 兼容性

URP 支持以下 Graphics API：

- DirectX 11（feature level 11_0 及更高版本）
- DirectX 12
- Vulkan
- Metal
- OpenGL ES 3.0 及更高版本
- OpenGL Core
- WebGL2
- WebGPU

## Unity Player 系统要求

此包不会增加任何特定于平台的额外要求。Unity Player 的一般系统要求同样适用。有关 Unity 系统要求的更多信息，请查看 [Unity 的系统要求](https://docs.unity3d.com/6000.7/Documentation/Manual/system-requirements.html)。

## 其他资源

- [[../03-选择渲染管线/02-渲染管线功能比较参考]]
- [[../07-使用内置渲染管线/01-内置渲染管线的硬件要求]]

---

## 文档导航

- 上一页：[[01-通用渲染管线简介]]
- 目录：[[00-使用通用渲染管线]]
- 下一页：[[03-URP 17 (Unity 6) 中的新功能]]
