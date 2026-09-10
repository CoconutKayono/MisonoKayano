# 在 Unity 项目中运行测试

> 原文：[1. Running a test in a Unity project](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/running-test.html)

## 学习目标

本练习将教你如何设置一个包含 test assembly 和 tests 的简单 Unity 项目。同时还会介绍基于 NUnit 的 unit test 结构。

## 简介与动机

在 Unity 中，我们测试内容的主要方式是使用 Unity Test Framework，它作为默认 package 随 Unity Editor 提供。了解如何设置一个包含 tests 的基础项目，可以帮助你开始使用 Unity Test Framework。

## 练习

从 Package Manager 窗口将 sample `1_RunningTest_Project` 导入 Unity Editor（版本 2019.2 或更高版本）。

> **注意：** 项目包含一个 `.cs` 文件（`MyMath.cs`），其中是一个简单的数学实现。本练习要求你为这个类创建 unit tests。

打开 Test Runner UI（**Window > General > TestRunner**），并在 `MyExercise` 文件夹旁边设置一个新的 EditMode test assembly。详细说明请参阅[[脚本/12-测试代码/01-开始使用Unity Test Framework/02-创建测试程序集|开始使用]]。

在新的 test assembly 文件夹（默认名称为 `Tests`）中创建一个新 test。你可以从 Test Runner UI 创建，也可以在 Project 窗口中右键点击并选择 **Create > Testing > C# test script**。开始编写 test 之前，还需要将 test assembly 与已有的 code assembly 连接起来。在 Project 窗口中点击创建的 test assembly，即可在 **Inspector** 中查看它（点击 **Tests 文件夹 > Tests**）。

在 **Assembly Definition References** 中，你会看到已经引用了 `UnityEngine.TestRunner`、`UnityEditor.TestRunner` 以及一个 NUnit assembly reference。点击 **Assembly Definition Reference** 区域中的 **+** 按钮，添加新的 reference。点击小圆圈，选择 `MyExercise`，然后点击 Inspector 底部的 **Apply**（可能需要向下滚动）。

用 IDE（Visual Studio 或 Rider）打开 C# solution，并打开刚才创建的 test 文件。可以删除带有 `[UnityTest]` 属性的方法，因为本练习不需要它。在带有 `[Test]` 属性的方法中加入 assert statement，验证 `MyMath.Add` 是否正确工作，例如使用 `Assert.AreEqual`。将方法重命名为更有描述性的名称。

良好的实践是让方法名描述被测试的内容。例如，类名可以是 `MyMathTests`，第一个 test 可以命名为 `AddsTwoPositiveIntegers`。如果愿意，还可以添加测试其他数字组合的方法。最佳实践是每个 test 只进行一次 check。

切回 Unity，打开 Test Runner UI。现在应该可以看到一棵树，其中包含 test assembly 名称、类名和方法名。这体现了 NUnit tests 的一般结构；Unity Test Framework 就构建在 NUnit 之上。每个类可以包含多个 tests，一个 namespace / assembly 中也可以有多个 test classes。双击 test 名称或其任意父节点即可运行 test。

test code 通过时会显示绿色勾号，test code 失败时会显示红色叉号。如果看不到任何 tests，请检查 Console log；任何 compile error 都会阻止所有 tests 显示。

现在可以回到 test code，为 `Subtract` 方法添加 tests。注意，你很可能会看到 tests 失败，因为示例中的 `Subtract` 方法存在 bug。在看到 test 以有意义的错误信息失败（例如 `Expected 2, but got 6`）后，可以打开 `MyMath.cs`，将返回值修正为：

```csharp
return a - b;
```

然后重新运行 test，验证错误已经修复。

## 提示

有时创建 test assembly 和第一个 test file 的 UI 可能不太容易使用。如果 Test Runner UI 没有识别你的 assembly，请尝试点击 Project 窗口中的文件夹，或者导航到包含 asmdef 的文件夹。

## 解决方案

本练习的解决方案位于 sample `1_RunningTest_Project_Solution` 中。解决方案包含一个带有 asmdef 文件的 `Tests` 文件夹，以及一个包含 tests 的 `.cs` 文件。

## 其他资源

- [将脚本组织到程序集](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-files.html)

---

## 文档导航

- 上一页：[[00-Unity Test Framework通用简介]]
- 目录：[[00-Unity Test Framework通用简介]]
- 下一页：[[02-Arrange Act Assert]]
