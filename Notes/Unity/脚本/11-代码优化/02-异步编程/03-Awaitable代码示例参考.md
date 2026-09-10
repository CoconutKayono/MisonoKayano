# Awaitable 代码示例参考

> 原文：[Awaitable code example reference](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-examples.html)

本参考中的示例展示了编写异步代码时常见场景对应的 `Awaitable` 解决方案。

## 异步测试

Unity 的 [Test Framework](https://docs.unity3d.com/Packages/com.unity.test-framework@latest) 不识别 `Awaitable` 作为有效的测试返回类型。不过，下面的示例展示了如何使用 `Awaitable` 对 `IEnumerator` 的实现来编写异步测试：

```csharp
[UnityTest]
public IEnumerator SomeAsyncTest(){
    async Awaitable TestImplementation(){
        // test something with async / await support here
    };
    return TestImplementation();
}
```

## 帧协程

你可以使用 `Awaitable` 类中与帧相关的异步方法，创建异步 Unity coroutine，作为基于 iterator 的 coroutine 的替代方案：

```csharp
async Awaitable SampleSchedulingJobsForNextFrame()
{
    // Wait until end of frame to avoid competing over resources with other Unity subsystems
    await Awaitable.EndOfFrameAsync();
    var jobHandle = ScheduleSomethingWithJobSystem();
    // Let the job execute while the next frame starts
    await Awaitable.NextFrameAsync();
    jobHandle.Complete();
    // Use results of computation
}

JobHandle ScheduleSomethingWithJobSystem()
{
    ...
}
```

### 条件等待

在基于 iterator 的 coroutine 中，[`WaitUntil`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitUntil.html) 会暂停 coroutine 的执行，直到 delegate 求值为 `true`。你可以让返回 `Awaitable` 的异步方法使用 cancellation token 等待 condition 改变，从而创建等效行为：

```csharp
public static async Awaitable AwaitableUntil(Func<bool> condition, CancellationToken cancellationToken)
{
    while(!condition()){
        cancellationToken.ThrowIfCancellationRequested();
        await Awaitable.NextFrameAsync();
    }
}
```

然后可以按如下方式传入 cancellation token：

```csharp
cancellationTokenSource = new CancellationTokenSource();
currentTask = AwaitableUntil(myCondition, cancellationTokenSource.Token);
```

## 异步加载资源

你可以 await 异步资源加载操作，使其不会阻塞主线程：

```csharp
public async Awaitable LoadResourcesAsync()
{
    // Load texture resource asynchronously
    var operation = Resources.LoadAsync("my-texture");
    // Return control to the main thread while the resource loads
    await operation;
    var texture = operation.asset as Texture2D;
}
```

## 组合

你可以在同一个方法中 await 多种不同的、兼容 `await` 的类型：

```csharp
public async Awaitable Bar()
{
    await CallSomeThirdPartyAPIReturningDotnetTask();
    await Awaitable.NextFrameAsync();
    await SceneManager.LoadSceneAsync("my-scene");
    await SomeUserCodeReturningAwaitable();
    ...
}
```

<a id="awaitable-as-task"></a>

## 在 .NET Task 中包装 Awaitable

为了绕过 `Awaitable` 的一些限制，你可以将它包装在 .NET `Task` 中。这样会产生一次分配成本，但可以使用 `Task` API 中的 `WhenAll` 和 `WhenAny` 等方法。可以编写自定义 `AsTask` extension method，如下所示：

```csharp
// Implement custom AsTask extension methods to wrap Awaitable in Task
public static class AwaitableExtensions
{
    public static async Task AsTask(this Awaitable a)
    {
        await a;
    }

    public static async Task<T> AsTask<T>(this Awaitable<T> a)
    {
        return await a;
    }
}
```

<a id="await-multiple-times"></a>

## 多次 Await 一个结果

`Awaitable` 和 `Task` 的一个重大区别是，`Awaitable` 对象会被 pooled 以减少分配。对于一个会返回 result 的方法，不能安全地多次 await 它返回的 `Awaitable`，因为原始 `Awaitable` 对象一旦返回，就会被返回到 pool。

### 不安全版本

下面的代码不安全，会导致 exception 和 deadlock：

```csharp
async Awaitable Bar(){
    var taskWithResult = SomeAwaitableReturningFunction();
    var awaitOnce = await taskWithResult;
    // Do something
    // The following will cause errors because at this point taskWithResult has already been pooled back
    var awaitTwice = await taskWithResult;
}
```

### 安全版本

这是可以在付出一次分配成本的情况下，将 `Awaitable` 包装在 `Task` 中的场景之一。之后可以安全地多次 await 这个 `Task`：

```csharp
// Implement custom AsTask extension methods to wrap Awaitable in Task
public static class AwaitableExtensions
{
    public static async Task AsTask(this Awaitable a)
    {
        await a;
    }

    public static async Task<T> AsTask<T>(this Awaitable<T> a)
    {
        return await a;
    }
}

async Awaitable Bar(){
    var taskWithResult = SomeAwaitableReturningFunction();
    // Wrap the returned Awaitable in a Task
    var taskWithResultAsTask = taskWithResult.AsTask();
    // The task can now be safely awaited multiple times, at the cost of allocating
    var awaitOnce = await taskWithResultAsTask;
    // Do something
    var awaitTwice = await taskWithResultAsTask;
}
```

## 其他资源

- [Comparing Unity Awaitable and .NET Task](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-introduction.html)
- [Async continuation and completion](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-continuations.html)
- [Awaitable API reference](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.html)

---

## 文档导航

- 上一页：[[02-Awaitable完成和Continuation]]
- 目录：[[00-异步编程]]
- 下一页：[[../03-Job System/00-Job System]]
