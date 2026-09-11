# 1. 设置 LostCrypt

> 原文：[1. Setting up LostCrypt](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/setting-up.html)

## 学习目标

在本练习中，你将设置一个简单的 Unity 2D 项目，并导入一个示例项目（LostCrypt）。

## 前置条件

1. **Unity 2020.3 LTS**：本培训推荐使用的 Unity 版本。
2. **C# IDE**（例如 [Rider](https://www.jetbrains.com/rider/download/) 或 [Visual Studio](https://visualstudio.microsoft.com)）：不是必需项，但强烈推荐。这样你可以使用调试器和可靠的语法自动补全等功能。

## 练习

1. 打开 **Unity Hub**，点击 **New Project**。选择一个空白的 2D（或 Core2D）项目。
2. 输入 **Project Name**，点击 **Create**。
3. 访问 [LostCrypt](https://assetstore.unity.com/packages/essentials/tutorial-projects/lost-crypt-2d-sample-project-158673) Asset 页面。点击 **Add to my Assets**，然后点击 **Open in Unity Editor**。
4. **Package Manager** 窗口会自动打开。找到 **Lost Crypt - 2D Sample Project**，点击 **Download**，然后点击 **Import**。
5. **Import Unity Package** 窗口会打开。点击 **Import**，将所有额外的 package 和 Asset 添加到新创建的项目中。
6. 如果需要，重启 Unity。

现在确认 LostCrypt 能够正常运行。

1. 在 **Project** 标签页中打开 `Scenes/Main`。
2. 点击 **Play** 按钮进入 Play Mode。
3. 你应当能够移动角色。

## 延伸阅读与资源

你可以在[我们的博客文章](https://blog.unity.com/technology/download-our-new-2d-sample-project-lost-crypt)中进一步了解 LostCrypt。

## 提示（可能遇到的问题）

- 可能会遇到依赖问题，请确保使用推荐的 Unity LTS 版本下载 LostCrypt。
- 确保 Package Manager 中的项目 package 都是最新版本。

---

## 文档导航

- 上一页：[[00-测试Lost Crypt]]
- 目录：[[00-测试Lost Crypt]]
- 下一页：[[02-在LostCrypt中运行测试]]
