# 2. Arrange、Act、Assert

> 原文：[2. Arrange, Act, Assert](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/arrange-act-assert.html)

## 学习目标

本练习将介绍单元测试的核心原则 AAA（Arrange、Act、Assert），帮助你组织 unit test。

## 简介与动机

Arrange、Act、Assert 是 unit testing 中的行业标准。它可以清晰地区分设置 test、执行 test 和评估结果的代码。使用这种结构可以让 test 对你自己和同事来说都更容易阅读。

在代码的第一部分，Arrange 所有 test 所需的元素；中间部分对被测试对象执行操作；最后一部分对 Act 阶段的结果进行 assert。通常使用空行分隔这三部分代码。

Arrange、Act、Assert 的示例：

```csharp
[Test]
public void StringWriterTest()
{
    // Arrange
    var stringWriterUnderTest = new StringWriter();
    stringWriterUnderTest.NewLine = "\\n";
    var testStringA = "I am testing";
    var testStringB = "with new line";

    // Act
    stringWriterUnderTest.WriteLine(testStringA);
    stringWriterUnderTest.WriteLine(testStringB);

    // Assert
    Assert.AreEqual("I am testing\\nwith new line\\n", stringWriterUnderTest.ToString());
}
```

为被测试的类使用 `XUnderTest` 作为变量名是一种良好实践。这样可以帮助 test 保持关注点清晰。

Act 部分的代码行数应尽可能少，以反映真正被测试的内容。理想情况下，Assert 部分应只包含 assert calls；但为了进行 assert，有时也必须加入一些逻辑代码。

## 练习

从 Package Manager 窗口将 sample `2_ActArrangeAssert` 导入 Unity Editor（版本 2019.2 或更高版本）。

在这个项目中有一个名为 `StringFormatter` 的类。它有两个需要关注的方法：

- `void Configure(string joinDelimiter)`
- `string Join(object[] args)`

本练习的目标是编写一个或多个 tests 来测试 `Join` 方法。例如，测试它是否可以使用 `;`（分号）作为 delimiter 进行连接。

## 提示

测试输入的设置，以及对 `Configure(";")` 的调用，都应该放在 test 的 Arrange 部分。

将 test 的三个部分（Arrange、Act 和 Assert）用空行分隔，是一种良好实践。

## 解决方案

本练习可以使用如下 test 解决：

```csharp
[Test]
public void JoinsObjectsWithSemiColon()
{
    // Arrange
    var formatterUnderTest = new StringFormatter();
    formatterUnderTest.Configure(";");
    var objects = new object[] {"a", "bc", 5, "d"};

    // Act
    var result = formatterUnderTest.Join(objects);

    // Assert
    Assert.AreEqual("a;bc;5;d", result);
}
```

包含解决方案的完整项目位于 sample `2_ActArrangeAssert_Solution` 中。

## 其他资源

- [安排测试](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/writing-tests.html)
- [[01-在Unity项目中运行测试]]
- [[17-语义测试断言]]

---

## 文档导航

- 上一页：[[01-在Unity项目中运行测试]]
- 目录：[[00-Unity Test Framework通用简介]]
- 下一页：[[03-自定义比较]]
