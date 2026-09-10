# 在 URP 中导入包示例

> 原文：[Import a package sample in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/package-samples.html)

通用渲染管线 (URP) 附带一组示例，可帮助您入门。

示例是一组可以导入 Unity 项目的资源，您可以以此为基础构建项目，或学习如何使用某个功能。包示例可以包含从单个 C# 脚本到多个场景的任何内容。

## 导入包示例

导入 URP 包示例前，请注意这些示例要求项目与 URP 兼容。如果项目是从模板创建的，或在项目中手动安装并设置了 URP，则项目与 URP 兼容。如果项目与 URP 不兼容，导入包示例时可能会发生错误。

要导入包示例，请使用 Unity Package Manager 窗口：

1. 转到**窗口 (Window)** > **包管理 (Package Management)** > **包管理器 (Package Manager)**，然后在包列表视图中选择 **Universal RP**。
2. 在包详细信息视图中找到**示例 (Samples)** 部分。
3. 找到要导入的示例，然后单击其旁边的**导入 (Import)** 按钮。

Unity 会将 URP 包示例导入 `Assets/Samples/Universal RP/<package version>/<sample name>`。

## 打开包示例

要打开包示例，请执行以下操作：

1. 转到 `Assets/Samples/Universal RP/<package version>/`。其中有一个文件夹对应每个已导入的 URP 包示例。
2. 找到包含所需包示例的文件夹并打开它。该文件夹名称与 Unity Package Manager 窗口中的包示例名称相同。

---

## 文档导航

- 上一页：[[02-URP 中的场景模板]]
- 目录：[[00-创建 URP 项目]]
- 下一页：[[04-URP 的包示例参考]]
