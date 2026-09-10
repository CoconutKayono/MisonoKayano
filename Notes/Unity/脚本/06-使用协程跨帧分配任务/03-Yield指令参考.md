# Yield 指令参考

> 原文：[Yield instruction reference](https://docs.unity3d.com/6000.7/Documentation/Manual/coroutines-yield-instructions.html)

Coroutine 会在 `yield return` 语句处暂停执行。`yield return null` 会将 Coroutine 的执行暂停到下一帧。不过，`yield return` 也可以返回一条指令，让 Unity Editor 或运行时在恢复 Coroutine 执行前等待指定时长，或等待某个条件满足。

## 运行时 Yield 指令

Unity 提供了一组派生自 [`UnityEngine.YieldInstruction`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/YieldInstruction.html) 的自定义 Yield 指令。可以使用这些指令，让 Coroutine 在指定时间后、指定条件满足时，或 Player Loop 中的特定时间点恢复执行。

| 指令 | 描述 |
| --- | --- |
| [`AsyncOperation`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AsyncOperation.html) | 暂停 Coroutine，并在异步操作完成时恢复，例如场景或资源加载完成时。 |
| [`WaitForEndOfFrame`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitForEndOfFrame.html) | 暂停 Coroutine，并在帧结束时恢复，此时所有渲染和 GUI 事件都已完成。**注意**：当 Editor 处于批处理模式时，即使脚本标记了 `[ExecuteInEditMode]` 或 `[ExecuteAlways]`，`WaitForEndOfFrame` 也不会在 Edit 模式下运行。 |
| [`WaitForFixedUpdate`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitForFixedUpdate.html) | 暂停 Coroutine，并在下一次物理更新结束、所有物理计算完成后恢复。 |
| [`WaitForSeconds`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitForSeconds.html) | 暂停 Coroutine，并在指定秒数后恢复，同时考虑 time scale。 |
| [`WaitForSecondsRealtime`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitForSecondsRealtime.html) | 暂停 Coroutine，并在指定秒数后恢复，不考虑 time scale。 |
| [`WaitUntil`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitUntil.html) | 暂停 Coroutine，并在传入的 delegate 求值为 `true` 时恢复。 |
| [`WaitWhile`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitWhile.html) | 暂停 Coroutine，并在传入的 delegate 求值为 `false` 时恢复。 |

如需了解这些 Yield 指令的更多信息和使用示例，请参阅对应的 API 参考页面。

如需直观了解不同 Coroutine 在 Player Loop 中的恢复位置，请参阅[事件函数的执行顺序](../04-管理更新和执行顺序/00-管理更新和执行顺序.md)中的示意图。

## UnityTest Yield 指令

标记了 `[UnityTest]` 属性的 Unity Test Framework 测试会以 Coroutine 的形式运行。Test Framework 软件包为测试提供了额外 Yield 指令，用于控制 Unity Editor，并支持定义自定义 Yield 指令。

| 指令 | 描述 |
| --- | --- |
| [`EnterPlayMode`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.EnterPlayMode.html) | 创建一个 Yield 指令，让 Unity Editor 进入 Play 模式。 |
| [`ExitPlayMode`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.ExitPlayMode.html) | 创建一个 Yield 指令，让 Unity Editor 退出 Play 模式。 |
| [`RecompileScripts`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.RecompileScripts.html) | 触发 Unity Editor 重新编译脚本。 |
| [`WaitForDomainReload`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.WaitForDomainReload.html) | 将脚本的执行延迟到即将发生的 domain reload 之后。 |

如需了解 Unity Test Framework 提供的 Yield 指令，请参阅[用于 Editor 的 Yield 指令](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-custom-yield-instructions.html)。

## Editor Yield 指令

Editor Coroutines 软件包为在 Unity Editor 的 Edit 模式下运行 Coroutine 提供支持。该软件包包含用于 Edit 模式 Coroutine 的额外 Yield 指令。

| 指令 | 描述 |
| --- | --- |
| [`EditorWaitForSeconds`](https://docs.unity3d.com/Packages/com.unity.editorcoroutines@latest/index.html?subfolder=/api/Unity.EditorCoroutines.Editor.EditorWaitForSeconds.html) | 在指定秒数后恢复 EditorCoroutine，同时考虑 time scale。 |

更多信息请参阅 [Editor Coroutines](https://docs.unity3d.com/Packages/com.unity.editorcoroutines@latest)。

## 批处理模式支持

在独立的 [Player 批处理模式](https://docs.unity3d.com/6000.7/Documentation/Manual/PlayerCommandLineArguments.html)中运行时，所有运行时 Coroutine Yield 指令都会正常运行。

如果在[批处理模式](https://docs.unity3d.com/6000.7/Documentation/Manual/EditorCommandLineArguments.html#batchmode)下运行 Editor，并且项目中的脚本标记了 [`[ExecuteInEditMode]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ExecuteInEditMode.html) 或 [`[ExecuteAlways]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ExecuteAlways.html)，从而也能在 Edit 模式下运行，那么这些脚本中的所有运行时 Coroutine 都会在 Edit 模式下运行，但 `WaitForEndOfFrame` 除外。这是因为 Unity 的某些子系统在 Edit 模式下不会像运行时那样定期更新。更多信息请参阅 [`[ExecuteAlways]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ExecuteAlways.html) API 参考。

## 其他资源

- [命令行参数](https://docs.unity3d.com/6000.7/Documentation/Manual/CommandLineArguments.html)
- [`[ExecuteAlways]` API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ExecuteAlways.html)


---

## 文档导航

- 上一页：[[02-分析Coroutine]]
- 目录：[[00-使用协程跨帧分配任务]]
- 下一页：[[../07-与Web服务器交互/00-与Web服务器交互]]
