# 9. 使用 UnityTest 属性

> 原文：[9. Using the UnityTest Attribute](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/unitytest-attribute.html)

## 学习目标

本节将介绍自定义的 `[UnityTest]` 属性，它可以创建跨多个 frame 运行的 tests。

## 简介与动机

我们对 NUnit framework 做出的一项重要扩展，是引入 `[UnityTest]` 属性。这个属性允许创建能够暂停并在满足特定条件后恢复运行的 tests。因此，test 的返回类型必须是 `IEnumerator`。随后可以 yield 一个 yield instruction 或 `null`，例如：

```csharp
[UnityTest]
public IEnumerator MyTest()
{
    DoSomething();
    // Skip 1 frame.
    yield return null;
    DoSomethingElse();
}
```

上面的代码先调用 `DoSomething` 方法，然后跳过一帧，再调用 `DoSomethingElse` 方法。

有关 C# 中 `yield` 关键字的更多信息，请参阅 Microsoft 文档。

## 练习

在 sample `9_UnityTestAttribute` 中，有一个已经设置好的 Play Mode test assembly，其中包含一个 Play Mode test。这个 Play Mode test 还没有主体，但有一个名为 `PrepareCube()` 的函数，会创建一个施加了物理效果的 Cube。

任务是初始化 Cube，然后验证经过一帧后它已经移动。

## 解决方案

完整解决方案位于 `9_UnityTestAttribute_Solution` sample 中。

```csharp
[UnityTest]
public IEnumerator CubeMovesDown()
{
    var cubeUnderTest = PrepareCube();
    var initialPosition = cubeUnderTest.transform.position;

    yield return null;

    Assert.That(cubeUnderTest.transform.position, Is.Not.EqualTo(initialPosition));
}
```

## 其他资源

- [UnityTest 属性](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-unitytest-attribute.html)
- [[07-Player中的PlayMode测试]]
- [[09-长时间运行的测试]]

---

## 文档导航

- 上一页：[[07-Player中的PlayMode测试]]
- 目录：[[00-Unity Test Framework通用简介]]
- 下一页：[[09-长时间运行的测试]]
