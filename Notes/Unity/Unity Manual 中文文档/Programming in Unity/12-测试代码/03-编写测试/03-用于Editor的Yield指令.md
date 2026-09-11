# 用于 Editor 的 Yield 指令

> 原文：[Yield instructions for the Editor](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-custom-yield-instructions.html)

与普通 NUnit `[Test]` 相比，`[UnityTest]` 的一项重要新增能力是可以在测试中向 Unity Editor 发送让步指令。通过 Unity 测试，你可以跳过帧，指示 Editor 进入或退出 Play Mode，重新编译脚本，或等待已计划的[域重载](https://docs.unity3d.com/6000.7/Documentation/Manual/domain-reloading.html)完成。

以下是预先定义的常用 Yield 指令：

- [EnterPlayMode](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.EnterPlayMode.html)
- [ExitPlayMode](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.ExitPlayMode.html)
- [RecompileScripts](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.RecompileScripts.html)
- [WaitForDomainReload](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.WaitForDomainReload.html)

你还可以为 Unity Editor 定义额外的自定义 Yield 指令，以便在 Edit Mode 测试中使用。有关如何执行此操作的信息（包括用法示例），请参阅 [IEditModeTestYieldInstruction](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.IEditModeTestYieldInstruction.html) 接口 API 说明。

有关在 C# 中使用 `yield` 语句的更多信息，请参阅 [yield 语句](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/yield)。

有关在 Unity 协程中使用向 Editor 返回的 `yield` 指令，请参阅[跨帧拆分任务](https://docs.unity3d.com/6000.7/Documentation/Manual/Coroutines.html)。

## 让 MonoBehaviour 产生让步以进行测试

[MonoBehaviourTest](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.MonoBehaviourTest-1.html) 是一个[协程](https://docs.unity3d.com/ScriptReference/Coroutine.html)，也是编写 [MonoBehaviour](https://docs.unity3d.com/ScriptReference/MonoBehaviour.html) 测试的辅助工具。

从 Unity 测试中返回一个 `MonoBehaviourTest`，即可实例化要测试的 `MonoBehaviour`，并等待其运行完成。在 `MonoBehaviour` 上实现 `IMonoBehaviourTest` 接口，以定义测试完成的时机。以下示例演示了这一过程：

```csharp
[UnityTest]
public IEnumerator MonoBehaviourTest_Works()
{
    yield return new MonoBehaviourTest<MyMonoBehaviourTest>();
}

public class MyMonoBehaviourTest : MonoBehaviour, IMonoBehaviourTest
{
    private int frameCount;
    public bool IsTestFinished
    {
        get { return frameCount > 10; }
    }

     void Update()
     {
        frameCount++;
     }
}
```

## 其他资源

- [[01-Edit Mode和Play Mode测试]]
- [Coroutine](https://docs.unity3d.com/ScriptReference/Coroutine.html)
- [YieldInstruction](https://docs.unity3d.com/ScriptReference/YieldInstruction.html)

---

## 文档导航

- 上一页：[[02-断言和比较]]
- 目录：[[00-编写测试]]
- 下一页：[[04-编写参数化测试]]
