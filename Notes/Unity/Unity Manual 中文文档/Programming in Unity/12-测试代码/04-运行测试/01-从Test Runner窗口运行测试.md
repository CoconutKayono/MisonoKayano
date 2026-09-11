# 从 Test Runner 窗口运行测试

> 原文：[Run tests in the Test Runner window](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/workflow-run-test.html)

在 **Test Runner** 窗口中，可以通过以下几种方式运行测试：

- 双击测试或 Test Fixture 的名称。
- 使用窗口底部的 **Run All** 或 **Run Selected** 按钮。
- 右键测试树中的任意项目，在上下文菜单中选择 **Run**，运行该测试及其所有子测试。

运行测试后，测试状态图标会显示结果，窗口右上角的计数器也会更新：

![Test Runner 窗口显示测试树，以及右键单个测试时出现的 Run 上下文菜单。](Unity/Unity%20Manual%20中文文档/Programming%20in%20Unity/12-测试代码/04-运行测试/图片/run-tests.png)

## 筛选测试

如果测试数量较多，只想查看或运行其中一部分，可以通过以下几种方式筛选测试（参见上图）：

- 在左上角的搜索框中输入内容。
- 单击测试类或 Fixture，例如图中的 **NewTestScript**。
- 单击右上角的测试结果图标按钮。

## 从 Rider 运行测试

可以直接从 [JetBrains Rider](https://www.jetbrains.com/rider/) 运行 Unity Test Framework 测试。

有关更多信息，请参阅 [Run and Debug Unity Tests](https://www.jetbrains.com/help/rider/Running_and_Debugging_Unity_Tests.html)。

## 已知问题和限制

Test Runner 窗口显示的测试套件总持续时间不包含 OneTimeSetup、UnityOneTimeSetup、OneTimeTearDown 或 UnityOneTimeTearDown 方法的运行时间，而是显示该套件中所有测试持续时间的总和。

## 其他资源

- [[02-从命令行运行测试]]
- [[00-从代码运行测试]]


---

## 文档导航

- 上一页：[[00-运行测试]]
- 目录：[[00-运行测试]]
- 下一页：[[02-从命令行运行测试]]
