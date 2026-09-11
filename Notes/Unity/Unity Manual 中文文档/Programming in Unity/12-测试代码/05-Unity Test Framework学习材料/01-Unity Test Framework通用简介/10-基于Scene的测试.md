# 11. 基于 Scene 的测试

> 原文：[11. Scene-based tests](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/scene-based-tests.html)

## 学习目标

在本练习中，你将学习如何测试存储在 Scene 中的内容。

## 简介与动机

对 Unity 用户来说，一个很有用的场景是使用 Test Framework 验证 Scene 的内容，例如检查其中是否存在特定的 GameObject 和 MonoBehaviour。

[EditorSceneManager](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SceneManagement.EditorSceneManager.html) 可以加载和保存 Scene。将它与 Test Framework 结合，就可以实现验证 Scene 的测试。

在测试中执行会改变 Editor 状态的操作（例如加载 Scene）时，最好在操作结束后清理状态。可以将清理逻辑放在带有 `[TearDown]` 属性的方法中。

## 练习

导入 [sample](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/test-framework-general-introduction.html#import-samples) `11_SceneBasedTests`。该 sample 包含一个名为 `MyGameScene` 的 Scene，以及一个用于 Edit Mode 测试的 Assembly。

任务是创建一个测试，打开该 Scene，并验证其中包含名为 `GameObjectToTestFor` 的 GameObject。

清理时，测试应打开一个新的空 Scene；这是 Edit Mode 测试的默认状态。建议将这部分逻辑放入 `[TearDown]` 方法中，这样即使测试失败，也能执行清理代码。

## 提示

- `EditorSceneManager.OpenScene("Assets\\MyGameScene.unity");` 用于加载 Scene。
- `EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);` 通过切换回空 Scene 完成清理。

## 解决方案

完整解决方案位于 sample `11_SceneBasedTests_Solution` 中。

测试实现可以如下所示：

```csharp
public class SceneTests
{
    [SetUp]
    public void Setup()
    {
        EditorSceneManager.OpenScene("Assets\\MyGameScene.unity");
    }

    [Test]
    public void VerifyScene()
    {
        var gameObject = GameObject.Find("GameObjectToTestFor");

        Assert.That(gameObject, Is.Not.Null);
    }

    [TearDown]
    public void Teardown()
    {
        EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
    }
}
```

## 其他资源

- [EditorSceneManager API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SceneManagement.EditorSceneManager.html)

---

## 文档导航

- 上一页：[[09-长时间运行的测试]]
- 目录：[[00-Unity Test Framework通用简介]]
- 下一页：[[11-构建时设置和清理]]
