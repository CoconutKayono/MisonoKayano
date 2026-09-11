# 7. PlayMode 测试

> 原文：[7. PlayMode tests](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/play-mode-tests.html)

## 学习目标

本练习将介绍 Play Mode 测试的概念，并教你：

- 何时使用 Play Mode 测试。
- 如何为 Play Mode 测试设置 assembly definition。
- 如何在 Play Mode 中运行测试。

## 简介与动机

Unity 中的 managed code 通常存在于两种不同模式：Edit Mode 和 Play Mode。Edit Mode 是在 Editor 内执行代码，包括 UI 及其底层逻辑。Play Mode 是游戏或 3D 应用运行时的状态，包括用户在 Editor 中点击播放按钮时，以及代码在 standalone player 中运行时。

我们为每种模式提供不同的 tests，因为测试的运行方式以及能够访问的内容不同。某个 API 的方法可能只在其中一种模式下可用。由于这种区别，Edit Mode 和 Play Mode tests 位于不同的 assemblies。

你可以按照 Test Runner UI 中 Play Mode 选项卡的说明创建 Play Mode test assembly。详细说明请参阅[开始使用](../../01-开始使用Unity Test Framework/02-创建测试程序集.md)。Edit Mode 与 Play Mode 的 assembly definition 区别在于它们启用的平台不同。Edit Mode test assembly 只对 Editor 平台启用。启用任何其他平台都会自动使其成为 Play Mode test assembly，因为 tests 现在可以在其他平台上运行。默认情况下，Play Mode tests 设置为在所有平台上运行。

## 练习

sample `7_PlayModeTests` 包含一个空项目。导入此 sample，并为 Play Mode tests 添加一个新 assembly。

然后添加一个 test，仅 assert `Application.isPlaying` 为 `true`。这个 flag 只有在 Play Mode 中才会为 `true`。

运行 test。注意，test 运行期间 Editor 会进入 Play Mode（相当于点击播放按钮），test 结束后会退出 Play Mode。

## 解决方案

包含 test 和 assembly 设置的完整解决方案位于 `7_PlayModeTests_Solution` sample 中。

## 其他资源

- [Edit Mode 和 Play Mode tests](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/edit-mode-vs-play-mode-tests.html)
- [[05-SetUp和TearDown]]
- [[07-Player中的PlayMode测试]]

---

## 文档导航

- 上一页：[[05-SetUp和TearDown]]
- 目录：[[00-Unity Test Framework通用简介]]
- 下一页：[[07-Player中的PlayMode测试]]
