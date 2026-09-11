# 设置和清理测试

> 原文：[Setting up and tearing down tests](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-unitysetup-and-unityteardown.html)

[`[UnitySetUp]`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnitySetUpAttribute.html) 和 [`[UnityTearDown]`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityTearDownAttribute.html) 特性等同于 NUnit 的 [`[SetUp]`](https://docs.nunit.org/articles/nunit/writing-tests/attributes/setup.html) 和 [`[TearDown]`](https://docs.nunit.org/articles/nunit/writing-tests/attributes/teardown.html) 特性，区别在于它们允许为 Unity Editor 使用[让步指令](03-用于Editor的Yield指令.md)。`[UnitySetUp]` 和 `[UnityTearDown]` 特性要求返回类型为 [IEnumerator](https://docs.microsoft.com/en-us/dotnet/api/system.collections.ienumerator?view=netframework-4.8)。

[`[UnityOneTimeSetUp]`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityOneTimeSetUpAttribute.html) 和 [`[UnityOneTimeTearDown]`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityOneTimeTearDownAttribute.html) 特性等同于 NUnit 的 [`[OneTimeSetUp]`](https://docs.nunit.org/articles/nunit/writing-tests/attributes/onetimesetup.html) 和 [`[OneTimeTearDown]`](https://docs.nunit.org/articles/nunit/writing-tests/attributes/onetimeteardown.html) 特性，区别在于它们允许为 Unity Editor 使用[让步指令](03-用于Editor的Yield指令.md)。`[UnityOneTimeSetUp]` 和 `[UnityOneTimeTearDown]` 特性要求返回类型为 [IEnumerator](https://docs.microsoft.com/en-us/dotnet/api/system.collections.ienumerator?view=netframework-4.8)。

如需了解更多信息和用法示例，请参阅以下特性的相应 API 参考：[ `[UnitySetUp]`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnitySetUpAttribute.html)、[`[UnityTearDown]`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityTearDownAttribute.html)、[`[UnityOneTimeSetUp]`](https://docs.unity3d.com/Packages/com.unity.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityOneTimeSetUpAttribute.html) 和 [`[UnityOneTimeTearDown]`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityOneTimeTearDownAttribute.html)。

## 执行顺序

`[UnitySetUp]` 和 `[UnityTearDown]` 可以与 `[Test]` 或 `[UnityTest]` 测试特性一起使用。在这两种情况下，Unity 和非 Unity 的 `[SetUp]` 与 `[TearDown]` 特性的相对执行顺序都相同。唯一的区别是，`[UnityTest]` 允许在测试期间使用让步指令，而这些指令可能导致域重载；在这种情况下，非 Unity 的 `[SetUp]` 方法会在继续执行测试的第二部分之前重新运行。

![设置和清理事件回调的执行顺序，其中区分了域重载时会重新运行和不会重新运行的操作。](execution-order-unitysetup-teardown.png)

*设置和清理事件回调的执行顺序，其中区分了域重载时会重新运行和不会重新运行的操作。*

## 基类和派生类

执行顺序中的 **base** 指测试类所继承的基类。`UnitySetUp` 和 `UnityTearDown` 在确定基类与派生类之间的执行顺序时，遵循与 NUnit 的 `SetUp` 和 `TearDown` 特性相同的模式。首先调用基类上的 `SetUp` 方法，然后调用派生类上的方法；首先调用派生类上的 `TearDown` 方法，然后调用基类上的方法。更多信息请参阅 [NUnit 文档](https://docs.nunit.org/articles/nunit/technical-notes/usage/SetUp-and-TearDown.html)。

以下示例演示基类和派生类。你可以通过控制台中打印的消息顺序验证执行顺序：

```csharp
    public class BaseClass
    {
        [OneTimeSetUp]
        public void OneTimeSetUp()
        {
            Debug.Log("OneTimeSetUp Base");
        }

        [SetUp]
        public void SetUp()
        {
            Debug.Log("SetUp Base");
        }

        [UnitySetUp]
        public IEnumerator UnitySetUp()
        {
            Debug.Log("UnitySetup Base");
            yield return null;
        }

        [TearDown]
        public void TearDown()
        {
            Debug.Log("TearDown Base");
        }

        [UnityTearDown]
        public IEnumerator UnityTearDown()
        {
            Debug.Log("UnityTearDown Base");
            yield return null;
        }
    }

    public class DerivedClass: BaseClass
    {
        [OneTimeSetUp]
        public new void OneTimeSetUp()
        {
            Debug.Log("OneTimeSetUp");
        }

        [SetUp]
        public new void SetUp()
        {
            Debug.Log("SetUp");
        }

        [UnitySetUp]
        public new IEnumerator UnitySetUp()
        {
            Debug.Log("UnitySetup");
            yield return null;
        }

        [Test]
        public void UnitTest()
        {
            Debug.Log("Test");
        }

        [UnityTest]
        public IEnumerator UnityTest()
        {
            Debug.Log("UnityTest before yield");
            yield return null;
            Debug.Log("UnityTest after yield");
        }

        [TearDown]
        public new void TearDown()
        {
            Debug.Log("TearDown");
        }

        [UnityTearDown]
        public new IEnumerator UnityTearDown()
        {
            Debug.Log("UnityTearDown");
            yield return null;
        }

        [OneTimeTearDown]
        public void OneTimeTearDown()
        {
            Debug.Log("OneTimeTearDown");
        }
    }
```

## 域重载

Edit mode 测试可以使用会导致域重载的[让步指令](03-用于Editor的Yield指令.md)。发生域重载时，所有非 Unity 操作（例如 `OneTimeSetup` 和 `Setup`）都会在继续执行触发域重载的代码之前重新运行。Unity 操作（例如 `UnitySetup`）不会重新运行。如果触发域重载的代码属于 Unity 操作，那么 `UnitySetup` 方法中的其余代码会在域重载后运行。

以下示例演示发生域重载时的基类和派生类：

```csharp
    public class BaseClass
    {
        [OneTimeSetUp]
        public void OneTimeSetUp()
        {
            Debug.Log("OneTimeSetUp Base");
        }

        [SetUp]
        public void SetUp()
        {
            Debug.Log("SetUp Base");
        }

        [UnitySetUp]
        public IEnumerator UnitySetUp()
        {
            Debug.Log("UnitySetup Base");
            yield return null;
        }

        [TearDown]
        public void TearDown()
        {
            Debug.Log("TearDown Base");
        }

        [UnityTearDown]
        public IEnumerator UnityTearDown()
        {
            Debug.Log("UnityTearDown Base");
            yield return null;
        }
    }

    public class DerivedClass: BaseClass
    {
        [OneTimeSetUp]
        public new void OneTimeSetUp()
        {
            Debug.Log("OneTimeSetUp");
        }

        [SetUp]
        public new void SetUp()
        {
            Debug.Log("SetUp");
        }

        [UnitySetUp]
        public new IEnumerator UnitySetUp()
        {
            Debug.Log("UnitySetup");
            yield return null;
        }

        [Test]
        public void UnitTest()
        {
            Debug.Log("Test");
        }

        [UnityTest]
        public IEnumerator UnityTest()
        {
            Debug.Log("UnityTest before yield");
            yield return new EnterPlayMode(); 
            //Domain reload happening
            yield return new ExitPlayMode();
            Debug.Log("UnityTest after yield");
        }

        [TearDown]
        public new void TearDown()
        {
            Debug.Log("TearDown");
        }

        [UnityTearDown]
        public new IEnumerator UnityTearDown()
        {
            Debug.Log("UnityTearDown");
            yield return null;
        }

        [OneTimeTearDown]
        public void OneTimeTearDown()
        {
            Debug.Log("OneTimeTearDown");
        }
    }
```

## 其他资源

- [[03-UnitySetUp和UnityTearDown]]
- [[01-测试操作执行顺序]]

---

## 文档导航

- 上一页：[[02-构建时设置和清理]]
- 目录：[[00-测试前后的操作]]
- 下一页：[[04-测试前后执行操作]]
