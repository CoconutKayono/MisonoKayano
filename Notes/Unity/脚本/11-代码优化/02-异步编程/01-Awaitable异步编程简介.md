# 使用 Awaitable 进行异步编程的简介

> 原文：[Introduction to asynchronous programming with Awaitable](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-introduction.html)

[`Awaitable`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.html) 类是 Unity 自定义的类型，可以在 C# 异步编程模型中被 await，并用作 `async` 返回类型。Unity 的大多数异步 API 都支持 `async` 和 `await` 模式，包括：

- Unity coroutine：[`NextFrameAsync`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.NextFrameAsync.html)、[`WaitForSecondsAsync`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.WaitForSecondsAsync.html)、[`EndOfFrameAsync`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.EndOfFrameAsync.html)、[`FixedUpdateAsync`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.FixedUpdateAsync.html)
- 切换到 Background Thread 或 Main Thread
- 所有继承自 [`AsyncOperation`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AsyncOperation.html) 的类型
- Unity Event
- Async GPU Readback

你可以在自己的代码中同时将 `Awaitable` 类与 `await` 运算符及 `async` 返回类型结合使用，如下所示：

```csharp
async Awaitable<List<Achievement>> GetAchievementsAsync()
{
    var apiResult = await SomeMethodReturningATask(); // or any await-compatible type
    List<Achievement> achievements = JsonConvert.DeserializeObject<List<Achievement>>(apiResult);
    return achievements;
}

async Awaitable ShowAchievementsView()
{
    ShowLoadingOverlay();
    List<Achievement> achievements = await GetAchievementsAsync();
    HideLoadingOverlay();
    ShowAchivementsList(achievements);
}
```

## Awaitable 与 .NET Task 的比较

`Awaitable` 的设计目标，是为 Unity 项目中的异步代码提供比 .NET `Task` 更高效的替代方案。与 `Task` 相比，`Awaitable` 的效率伴随着一些重要限制。

最重要的限制是：`Awaitable` 实例会被 pooled，以限制分配。请考虑以下示例：

```csharp
class SomeMonoBehaviorWithAwaitable : MonoBehaviour
{
    public async void Start()
    {
        while(true)
        {
            // do some work on each frame
            await Awaitable.NextFrameAsync();
        }
    }
}
```

如果没有 pooling，示例中的每个 `MonoBehaviour` 实例都会在每一帧分配一个 `Awaitable` 对象，从而增加 garbage collector 的工作量并降低性能。为缓解这一点，Unity 会在 `Awaitable` 对象被 await 后，将它返回到内部 `Awaitable` pool。

重要提示：`Awaitable` 实例的 pooling 意味着，对同一个 `Awaitable` 实例 await 多于一次永远不安全。这样做可能导致 exception 或 deadlock 等 undefined behavior。

## Awaitable 与 .NET ValueTask 的比较

.NET [`ValueTask<TResult>`](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask-1?view=net-8.0) 具有与 `Awaitable` 相同的一些关键优点和限制。`ValueTask` 的典型推荐用途，是预期大多数时候都能同步完成的异步 workload。更多信息请参阅[理解 ValueTask 的原因、方式和时机](https://devblogs.microsoft.com/dotnet/understanding-the-whys-whats-and-whens-of-valuetask/)。

## Awaitable、Task 和 ValueTask 总结

下表总结了 Unity `Awaitable` 类与 .NET `Task`、`ValueTask` 的功能比较：

| 功能 | `Task` | `ValueTask` | `UnityEngine.Awaitable` |
| --- | --- | --- | --- |
| 所需分配 | Many。<br>每次调用返回 `Task` 的方法都会分配，从而增加内存使用量和 garbage collector 工作量。 | As-needed。<br>可以通过 pooling 优化。 | Minimal as-needed。<br>调用返回 `Awaitable` 的方法通常不分配内存，因为 `Awaitable` 实例默认会被 pooled。 |
| 是否可以安全地 await 多次 | Yes。 | No。<br>必须使用 `ValueTask.AsTask` 转换为 `Task`。 | No。<br>必须使用自定义 `AsTask` extension method 转换为 `Task`；请参阅代码示例参考中的“多次 await”部分。 |
| Continuation 异步运行 | Yes。<br>默认使用 synchronization context，否则使用 ThreadPool。在 Unity 中的主线程上完成时，这会增加 latency，因为代码必须等到下一帧 Update 才能恢复。 | Yes。<br>针对 awaited task 同步完成的情况进行了优化。如果异步完成，continuation 行为等同于 `Task`。 | No。<br>当触发 completion 时，continuation 同步运行，这意味着代码会在触发 completion 的同一帧立即恢复。更多信息请参阅 [Awaitable completion and continuation](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-continuations.html)。 |
| Completion 可以由代码触发 | Yes。<br>使用 `TaskCompletionSource`。 | Not applicable in the typical use case，即 task 大多数时候同步完成。 | Yes。<br>使用 `AwaitableCompletionSource`。 |
| 可以返回值 | Yes。<br>使用 `Task<TResult>`。 | Yes。<br>使用 `ValueTask<TResult>`。 | Yes。<br>使用 `UnityEngine.Awaitable<T>`。 |
| 内置支持 `WaitAll` 和 `WaitAny` | Yes。 | No。<br>必须使用 `ValueTask.AsTask` 转换为 `Task`。 | No。<br>必须使用自定义 `AsTask` extension method 转换为 `Task`；请参阅代码示例参考中的“在 .NET Task 中包装 Awaitable”部分。 |
| Unity thread 和 update loop 感知的 execution scheduling | No。 | No。 | Yes。<br>可以使用 [`Awaitable.BackgroundThreadAsync`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.BackgroundThreadAsync.html) 和 [`Awaitable.MainThreadAsync`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.MainThreadAsync.html) 指定 `Awaitable` 恢复时所在的 thread。还可以使用 [`Awaitable.NextFrameAsync`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.NextFrameAsync.html) 和 [`Awaitable.FixedUpdateAsync`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.FixedUpdateAsync.html)，相对于 `Update` 或 `FixedUpdate` loop 调度工作。更多信息请参阅 [Awaitable completion and continuation](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-continuations.html)。 |

## 何时选择 Awaitable 而不是 Task 或 ValueTask

API 的选择取决于异步代码的性能 profile，但一般来说：

- 当你需要 await 多次，或需要由多个 consumer 并发 await 时，`Task` 是唯一选择。
- 如果你有大多数时候同步完成的高吞吐异步代码，`ValueTask` 是不错的选择。
- 在以下情况下，`Awaitable` 是不错的选择：
  - 不需要多次 await 你的方法，并且预计这些方法大多数会异步完成。
  - 希望异步 task 内置支持 Unity-specific concept，例如 Main Thread，以及 [`Update`](https://docs.unity3d.com/6000.7/Documentation/Manual/time-per-frame-updates.html) 和 [`FixedUpdate`](https://docs.unity3d.com/6000.7/Documentation/Manual/fixed-updates.html) loop。

## Awaitable 与基于 iterator 的 coroutine 比较

`Awaitable` coroutine 通常比基于 iterator 的 coroutine 更高效，尤其是在 iterator 返回 non-null value 的情况下，例如 [`WaitForFixedUpdate`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitForFixedUpdate.html)。

不过，当你并发运行许多 `Awaitable` coroutine 时，其性能优势会降低。例如，前面代码示例中在 `while` loop 里 await [`Awaitable.NextFrameAsync`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.NextFrameAsync.html) 的 `MonoBehaviour`，如果附加到大型项目中的每个 GameObject，很可能造成性能问题。

提示：你可以安全地从传统的基于 iterator 的 coroutine 中 `yield return` 一个 [`Awaitable`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.html)，但不能 `yield return` 一个 [`Awaitable<T0>`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable_1.html)。

## 其他资源

- [Awaitable completion and continuation](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-continuations.html)
- [Awaitable code example reference](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-examples.html)

---

## 文档导航

- 上一页：[[00-异步编程]]
- 目录：[[00-异步编程]]
- 下一页：[[02-Awaitable完成和Continuation]]
