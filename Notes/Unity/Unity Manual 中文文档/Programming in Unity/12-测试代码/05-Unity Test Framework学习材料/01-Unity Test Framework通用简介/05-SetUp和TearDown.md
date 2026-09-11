# 6. SetUp 和 TearDown

> 原文：[6. SetUp and TearDown](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/setup-teardown.html)

## 学习目标

本练习将让你实际使用 NUnit 的 `[SetUp]` 和 `[TearDown]` 属性，以减少 test 中的代码重复。

## 简介与动机

让 test code 始终自行清理是一种良好实践；运行 test 前也经常需要完成一些设置。如果有多个 tests，就很容易产生大量重复代码。而且，如果没有将清理代码包在 `try` 和 `finally` blocks 中，test 失败时甚至可能不会执行清理。

NUnit 提供了 `[SetUp]` 和 `[TearDown]` 属性作为解决方案。带有这些属性的方法，会分别在类中每个 test 之前和之后运行。如果一次运行类中的多个 tests，TearDown 和 SetUp 会在每个 test 之间运行。

```csharp
public class TestClass
{
    [SetUp]
    public void MySetUp() { ... }

    [Test]
    public void MyFirstTest() { ... }

    [Test]
    public void MySecondTest() { ... }

    [TearDown]
    public void MyTearDown() { ... }
}
```

## 练习

导入 sample `6_SetUpTearDown`。

这个项目中有一个 `FileCreator` 类，它有两个方法：

- `CreateEmptyFile(fileName)`：在 `OutputFiles` 目录中创建一个空文件。
- `CreateFile(string fileName, string content)`：在 `OutputFiles` 目录中创建一个包含指定内容的文件。

关键问题在于：如果当前目录中没有名为 `OutputFiles` 的目录，它就会抛出 `DirectoryNotFoundException`。你需要在 `SetUp` 方法中创建这个目录，并在之后使用 `TearDown` 将其删除。这样，test 就可以假定自己从一个空目录开始，从而简化 assert。

## 提示

- 可以使用 `Directory.CreateDirectory` 创建目录。
- 可以将 `Directory.Delete` 的 recursive flag（第二个参数）设为 `true`，以便连同目录中的所有 files 一起删除。
- 可以使用 `Directory.GetFiles` 获取指定目录中的 files。
- `Path.Combine` 适合用来组合路径的各个部分，例如目录名和文件名。

## 解决方案

本练习可以使用如下 test 解决：

```csharp
[SetUp]
public void Setup()
{
    Directory.CreateDirectory(FileCreator.k_Directory);
}

[Test]
public void CreatesEmptyFile()
{
    var fileCreatorUnderTest = new FileCreator();
    var expectedFileName = "MyEmptyFile.txt";

    fileCreatorUnderTest.CreateEmptyFile(expectedFileName);

    var files = Directory.GetFiles(FileCreator.k_Directory);
    Assert.That(files.Length, Is.EqualTo(1), "Expected one file.");
    var expectedFilePath = Path.Combine(FileCreator.k_Directory, expectedFileName);
    Assert.That(files[0], Is.EqualTo(expectedFilePath));
}

[Test]
public void CreatesFile()
{
    var fileCreatorUnderTest = new FileCreator();
    var expectedFileName = "MyFile.txt";
    var expectedContent = "TheFileContent";

    fileCreatorUnderTest.CreateFile(expectedFileName, expectedContent);

    var files = Directory.GetFiles(FileCreator.k_Directory);
    Assert.That(files.Length, Is.EqualTo(1), "Expected one file.");
    var expectedFilePath = Path.Combine(FileCreator.k_Directory, expectedFileName);
    Assert.That(files[0], Is.EqualTo(expectedFilePath));
    var content = File.ReadAllText(expectedFilePath);
    Assert.That(content, Is.EqualTo(expectedContent));
}

[TearDown]
public void Teardown()
{
    Directory.Delete(FileCreator.k_Directory, true);
}
```

包含解决方案的完整项目位于 sample `6_SetUpTearDown` 中。

## 其他资源

- [SetUp 和 TearDown](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-setup-and-cleanup.html)
- [[04-断言和预期日志]]
- [[06-PlayMode测试]]

---

## 文档导航

- 上一页：[[04-断言和预期日志]]
- 目录：[[00-Unity Test Framework通用简介]]
- 下一页：[[06-PlayMode测试]]
