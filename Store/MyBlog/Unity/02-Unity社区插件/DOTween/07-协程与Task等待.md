# 协程与 Task 等待（WaitFor coroutines/Tasks）

## 协程（Coroutines）

补间提供了一组实用的 `YieldInstruction`，可以放进协程中，用来等待某件事发生。

所有方法都有一个可选的 `bool` 参数，可以改为返回 `CustomYieldInstruction`。

### WaitForCompletion

```cs
WaitForCompletion()
```

创建一个 yield 指令，等待补间被杀死或完成。

```cs
IEnumerator SomeCoroutine()
{
  Tween myTween = transform.DOMoveX(45, 1);
  yield return myTween.WaitForCompletion();
  // 这行日志会在补间完成后执行
  Debug.Log("Tween completed!");
}
```

### WaitForElapsedLoops

```cs
WaitForElapsedLoops(int elapsedLoops)
```

创建一个 yield 指令，等待补间被杀死或完成指定数量的循环。

```cs
IEnumerator SomeCoroutine()
{
  Tween myTween = transform.DOMoveX(45, 1).SetLoops(4);
  yield return myTween.WaitForElapsedLoops(2);
  // 这行日志会在第 2 次循环结束后执行
  Debug.Log("Tween has looped twice!");
}
```

### WaitForKill

```cs
WaitForKill()
```

创建一个 yield 指令，等待补间被杀死。

```cs
IEnumerator SomeCoroutine()
{
  Tween myTween = transform.DOMoveX(45, 1);
  yield return myTween.WaitForKill();
  // 这行日志会在补间被杀死后执行
  Debug.Log("Tween killed!");
}
```

### WaitForPosition

```cs
WaitForPosition(float position)
```

创建一个 yield 指令，等待补间被杀死或到达指定时间位置（含循环、不含延迟）。

```cs
IEnumerator SomeCoroutine()
{
  Tween myTween = transform.DOMoveX(45, 1);
  yield return myTween.WaitForPosition(0.3f);
  // 这行日志会在补间播放 0.3 秒后执行
  Debug.Log("Tween has played for 0.3 seconds!");
}
```

### WaitForRewind

```cs
WaitForRewind()
```

创建一个 yield 指令，等待补间被杀死或被倒回。

```cs
IEnumerator SomeCoroutine()
{
  Tween myTween = transform.DOMoveX(45, 1).SetAutoKill(false).OnComplete(myTween.Rewind);
  yield return myTween.WaitForRewind();
  // 这行日志会在补间被倒回时执行
  Debug.Log("Tween rewinded!");
}
```

### WaitForStart

```cs
WaitForStart()
```

创建一个 yield 指令，等待补间被杀死或开始（即首次进入播放状态，在任意延迟之后）。

```cs
IEnumerator SomeCoroutine()
{
  Tween myTween = transform.DOMoveX(45, 1);
  yield return myTween.WaitForStart();
  // 这行日志会在补间开始时执行
  Debug.Log("Tween started!");
}
```

## Task（异步等待）

要求：至少 Unity 2018.1，且 .NET Standard 2.0 或 4.6。

这些方法返回 `Task`，用于 async 操作中等待某件事发生。

### AsyncWaitForCompletion

```cs
AsyncWaitForCompletion()
```

返回一个等待补间被杀死或完成的 `Task`。

```cs
await myTween.AsyncWaitForCompletion();
```

### AsyncWaitForElapsedLoops

```cs
AsyncWaitForElapsedLoops(int elapsedLoops)
```

返回一个等待补间被杀死或完成指定数量循环的 `Task`。

```cs
await myTween.AsyncWaitForElapsedLoops(2);
```

### AsyncWaitForKill

```cs
AsyncWaitForKill()
```

返回一个等待补间被杀死的 `Task`。

```cs
await myTween.AsyncWaitForKill();
```

### AsyncWaitForPosition

```cs
AsyncWaitForPosition(float position)
```

返回一个等待补间被杀死或到达指定时间位置（含循环、不含延迟）的 `Task`。

```cs
await myTween.AsyncWaitForPosition(0.3f);
```

### AsyncWaitForRewind

```cs
AsyncWaitForRewind()
```

返回一个等待补间被杀死或被倒回的 `Task`。

```cs
await myTween.AsyncWaitForRewind();
```

### AsyncWaitForStart

```cs
AsyncWaitForStart()
```

返回一个等待补间被杀死或开始（首次进入播放状态，延迟之后）的 `Task`。

```cs
await myTween.AsyncWaitForStart();
```
