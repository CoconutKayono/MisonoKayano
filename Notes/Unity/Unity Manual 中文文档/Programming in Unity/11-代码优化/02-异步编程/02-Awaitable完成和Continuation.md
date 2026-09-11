# Awaitable 完成与 Continuation

> 原文：[Awaitable completion and continuation](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-continuations.html)

`await` 运算符会暂停外层 `async` 方法的执行，使调用线程可以在等待期间执行其他工作。被 await 的 `Task` 或 `Awaitable` 完成后，异步代码需要从暂停位置恢复并继续执行。异步代码的恢复方式，可能会对应用程序的功能和性能产生重要影响。

## .NET Task Continuation

代码开始 await 时所处状态的相关信息，被称为 synchronization context。.NET 平台提供 [`SynchronizationContext`](https://learn.microsoft.com/en-us/dotnet/api/system.threading.synchronizationcontext?view=net-8.0) 类来捕获这类信息。`Task` continuation 会在调用异步方法时所在的 synchronization context 中运行；如果没有设置 synchronization context，则通过 [thread pool](https://learn.microsoft.com/en-us/dotnet/api/system.threading.threadpool?view=net-8.0) 运行。

大多数 Unity API 不是 thread-safe，只能从主线程调用。因此，Unity 用自定义的 [`UnitySynchronizationContext`](https://github.com/Unity-Technologies/UnityCsReference/blob/master/Runtime/Export/Scripting/UnitySynchronizationContext.cs) 覆盖默认的 [`SynchronizationContext`](https://docs.microsoft.com/en-us/archive/msdn-magazine/2011/february/msdn-magazine-parallel-computing-it-s-all-about-the-synchronizationcontext)，确保在 Edit mode 和 Play mode 中，所有 .NET `Task` continuation 默认都在主线程运行。如果从 Unity 主线程调用返回 `Task` 的方法，continuation 会发布到 `UnitySynchronizationContext`，并在主线程下一帧的 `Update` tick 中运行。如果从后台线程调用，continuation 会在线程池线程上完成。

捕获 synchronization context 会增加应用程序的性能开销，而等待下一帧 `Update` 才能在主线程恢复，在规模较大时会引入 latency。使用 `Awaitable` 可以避免这两个问题。

## Awaitable Continuation

除非另有文档说明，Unity API 返回的所有 `Awaitable` 实例，以及任何用户定义的返回 `async Awaitable` 的方法，都具有以下 continuation 调度行为：

- 如果方法从主线程调用，它会在主线程恢复。
- 否则，它会在 .NET [`ThreadPool`](https://learn.microsoft.com/en-us/dotnet/api/system.threading.threadpool?view=net-8.0) 线程上恢复。

值得注意的例外情况是：

- `Awaitable.MainThreadAsync`：continuation 在主线程发生。
- `Awaitable.BackgroundThreadAsync`：continuation 在后台线程发生。

`Awaitable.MainThreadAsync` 和 `Awaitable.BackgroundThreadAsync` 的效果只作用于当前方法，例如：

```csharp
private async Awaitable<float> DoHeavyComputationInBackgroundAsync()
{
    await Awaitable.BackgroundThreadAsync();
    // here we are on a background thread
    // do some heavy math here
    return 42; // note: we don't need to explicitly get back to the main thread here, depending on the caller thread, DoHeavyComputationInBackgroundAsync will automatically complete on the correct one.
}

public async Awaitable Start()
{
    var computationResult = await DoHeavyComputationInBackgroundAsync();
    // although DoHeavyComputationInBackgroundAsync() internally switches to a background thread to avoid blocking,
    // because we await it from the main thread, we also resume execution on the main thread and can safely call "main thread only APIs" such as LoadSceneAsync()
    await SceneManager.LoadSceneAsync("my-scene"); // this will succeed as we resumed on main thread
}
```

提示：退出 Play mode 时，Unity 不会自动停止后台运行的代码。要在退出 Play mode 时取消后台操作，请使用 [`Application.exitCancellationToken`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Application-exitCancellationToken.html)。

## Thread switching 和性能

从主线程调用 `await Awaitable.MainThreadAsync()`，以及从后台线程调用 `await Awaitable.BackgroundThreadAsync()`，是最高效的方式，因为在每种情况下，代码都会在 completion 后立即恢复。如果使用 `MainThreadAsync` 从后台线程切回主线程，代码必须等到主线程的下一次 [frame update](https://docs.unity3d.com/6000.7/Documentation/Manual/time-per-frame-updates.html) 才能恢复。

如果从主线程调用返回 `Task` 的 API，且该 API 没有同步完成，则至少要等到下一次 `Update` tick（30fps 时为 33ms），continuation 才会运行。如果 network latency 是问题，建议在主线程之外执行这一操作，并使用自定义逻辑在主线程与 networking task 之间进行同步。

在 development build 中，如果你尝试在 multithreaded code 中使用 Unity API，Unity 会显示以下错误消息：

```text
UnityException: Internal_CreateGameObject can only be called from the main thread.
Constructors and field initializers will be executed from the loading thread when loading a scene.
Don't use this function in the constructor or field initializers, instead move initialization code to the Awake or Start function.
```

重要提示：出于性能原因，Unity 不会在 [non-development build](https://docs.unity3d.com/6000.7/Documentation/Manual/build-profiles-reference.html) 中检查 multithreaded behavior，也不会在 live build 中显示此错误。虽然 Unity 不会阻止这些 context 下的 multithreaded code 执行，但如果确实使用多个 thread，很可能发生 crash 和其他不可预测的错误。与其使用自己的 multithreading，不如使用 Unity 的 [job system](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system.html)，它能安全地使用多个 thread 并行执行 job，从而获得 multithreading 的性能优势。更多信息请参阅 [Job system overview](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-overview.html)。

### Awaitable 与 job system 比较

与 job system 相比，Unity 的 `Awaitable` 类更适合以下场景：

- 处理本质上是异步的操作时简化代码，例如以 non-blocking 方式操作文件或执行 web request。
- 将长期运行（>1 frame）的 task 转移到后台线程。
- Modernize 基于 iterator 的 coroutine。
- Await 多种类型的异步操作（frame event、Unity event、third-party asynchronous API、I/O）。

不过，不建议使用它处理生命周期较短的操作，例如并行化计算密集型算法。要充分利用多核 CPU 并行化算法，请改用 [job system](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system.html)。

## 从代码触发 Completion

[`AwaitableCompletionSource`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AwaitableCompletionSource.html) 和 [`AwaitableCompletionSource<T>`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AwaitableCompletionSource_1.html) 允许创建由用户代码触发 completion 的 `Awaitable` 实例。例如，可以用它实现 user prompt，而无需实现 state machine 来等待用户交互完成：

```csharp
public class UserNamePrompt : MonoBehaviour
{
    TextField _userNameTextField;
    AwaitableCompletionSource<string> _completionSource = new AwaitableCompletionSource<string>();

    public void Start()
    {
        var rootVisual = GetComponent<UIDocument>().rootVisualElement;
        var userNameField = rootVisual.Q<TextField>("userNameField");
        rootVisual.Q<Button>("OkButton").clicked += ()=>{
            _completionSource.SetResult(userNameField.text);
        }
    }

    public Awaitable<string> WaitForUsernameAsync() => _completionSource.Awaitable;
}

...

public class HighScoreRanks : MonoBehaviour
{
    ...

    public async Awaitable ReportCurrentUserScoreAsync(int score)
    {
        _userNameOverlayGameObject.SetActive(true);
        var prompt = _userNameOverlayGameObject.GetComponent<UserNamePrompt>();
        var userName = await prompt.WaitForUsernameAsync();
        _userNameOverlayGameObject.SetActive(false);
        await SomeAPICall(userName, score);
    }
}
```

## 其他资源

- [Awaitable code example reference](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-examples.html)

---

## 文档导航

- 上一页：[[01-Awaitable异步编程简介]]
- 目录：[[00-异步编程]]
- 下一页：[[03-Awaitable代码示例参考]]
