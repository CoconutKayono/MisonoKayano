# 编写和运行 Coroutine

> 原文：[Write and run coroutines](https://docs.unity3d.com/6000.7/Documentation/Manual/Coroutines.html)

Coroutine 是一种可以暂停执行，并在稍后恢复执行的方法。在 Unity 应用中，Coroutine 可以在某一帧开始运行，在另一帧继续运行，从而将任务分摊到多帧完成。

普通的非 Coroutine 方法会在将控制权交还给调用者前执行完毕；在 Unity Runtime 中，这意味着它的操作会在单个帧更新内完成。如果希望一个方法的工作跨越多帧生效（例如逐渐淡出），可以使用 Coroutine。Coroutine 也适合处理等待 HTTP 传输、Asset 加载或文件 I/O 完成等较长的异步操作。

> [!IMPORTANT]
> 不要把 Coroutine 与 Thread 混淆。Coroutine 中执行的同步操作仍然运行在主线程上。如果要减少主线程消耗的 CPU 时间，就必须像处理其他脚本代码一样，避免在 Coroutine 中执行阻塞操作。如果需要在 Unity 中编写多线程代码，可以使用：
>
> - [Job System](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system.html)。
> - [.NET `async` / `await` 和 Unity 自定义的 `Awaitable` 支持](https://docs.unity3d.com/6000.7/Documentation/Manual/async-await-support.html)。

## 编写 Coroutine

考虑逐渐降低对象的 alpha（不透明度），直到对象完全不可见。为了让淡出效果可见，不透明度必须在连续多帧中降低。如果直接编写 `Fade` 方法，可能会写成这样：

```csharp
void Fade()
{
    Color c = renderer.material.color;

    for (float alpha = 1f; alpha >= 0; alpha -= 0.1f)
    {
        c.a = alpha;
        renderer.material.color = c;
    }
}
```

这不是 Coroutine，因此 `for` 循环的每次迭代都会在同一帧更新中执行，对象会立即消失，而不是看起来逐渐淡出。一种解决方案是在 `Update` 中添加代码，让淡出效果按帧执行；但使用 Coroutine 通常更方便。

Coroutine 是返回 [`IEnumerator`](https://docs.microsoft.com/en-us/dotnet/api/system.collections.ienumerator) 类型，并且在方法体的某处包含 [`yield return`](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/yield) 语句的方法。`yield return` 是暂停执行的位置。上面的 `Fade` 方法可以改写为：

```csharp
IEnumerator Fade()
{
    Color c = renderer.material.color;

    for (float alpha = 1f; alpha >= 0; alpha -= 0.1f)
    {
        c.a = alpha;
        renderer.material.color = c;
        yield return null;
    }
}
```

这个版本会先执行一次 `for` 循环，然后在 `yield return null` 处暂停。下一帧恢复执行后，再执行一次循环，如此反复，渐变淡出效果就能显示出来。`Fade` 中的循环计数器会在 Coroutine 的生命周期内保持正确的值，变量和参数也会在多个 `yield` 语句之间保留。

## 启动和停止 Coroutine

使用 `StartCoroutine` 方法启动 Coroutine：

```csharp
void Update()
{
    if (Input.GetKeyDown("f"))
    {
        StartCoroutine(Fade());
    }
}
```

可以使用 [`StopCoroutine`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.StopCoroutine.html) 和 [`StopAllCoroutines`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.StopAllCoroutines.html) 停止 Coroutine。以下情况也会停止 Coroutine：

- 脚本附加的 `GameObject` 的 [`activeSelf`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-activeSelf.html) 变为 `false`。
- 通过 [`Destroy`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Destroy.html) 销毁 `MonoBehaviour` 脚本。

> [!NOTE]
> 将 `MonoBehaviour` 脚本的 `enabled` 设置为 `false` 不会停止 Coroutine。

## 恢复 Coroutine

暂停的 Coroutine 何时恢复，取决于 `yield return` 语句提供的 Yield Instruction。`yield return null` 会在下一帧恢复。Unity 提供了自定义 Yield Instruction，可以在指定时间之后、满足指定条件时或 Player Loop 的特定位置恢复执行。相关内容请参阅 [[03-Yield指令参考]]。

在淡出示例中，如果希望淡出速度低于帧率并且更加稳定，可以使用 `WaitForSeconds`，在 `Fade` 的循环迭代之间加入固定时间延迟：

```csharp
IEnumerator Fade()
{
    Color c = renderer.material.color;

    for (float alpha = 1f; alpha >= 0; alpha -= 0.1f)
    {
        c.a = alpha;
        renderer.material.color = c;

        // 等待 0.1 秒后再进行下一次迭代。
        yield return new WaitForSeconds(0.1f);
    }
}
```

也可以在 Coroutine 中 `yield return` 一个 Unity [`Awaitable`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.html)。如果要将 Coroutine 与使用 `async` 和 `await` 的异步代码集成，这会很有用。例如，可以使用 `yield return Awaitable.WaitForSecondsAsync(0.1f)` 代替 `yield return new WaitForSeconds(0.1f)`，实现相同的效果。

> [!IMPORTANT]
> 不支持从 Coroutine 中 `yield return` 泛型 `Awaitable<T0>`。

## Edit Mode 中的 Coroutine

Coroutine 主要是 Runtime 功能。相关的 Runtime Yield Instruction 位于 `UnityEngine` Namespace 中，可以在 Editor 的 Play Mode 或独立平台 Player 中运行。如果脚本使用 `[ExecuteInEditMode]` 或 `[ExecuteAlways]` Attribute，Coroutine 也可以在 Edit Mode 中运行，但 Edit Mode 的更新循环不像 Player Loop 那样固定和规律。

如果要专门为 Edit Mode 编写 Coroutine，请使用 Editor Coroutine Package。

## 测试中的 Coroutine

带有 `[UnityTest]` Attribute 的 Unity Test Framework Play Mode 测试会作为 Coroutine 运行，因此可以在测试中向 Unity Editor `yield` 自定义指令。相关内容请参阅用于 Editor 的 Yield Instruction 文档。

## Coroutine 性能

误用 Coroutine 可能产生隐藏的内存分配和 Garbage Collector 峰值。每个 Coroutine 都会创建一个 `IEnumerator` 状态机。频繁启动 Coroutine（例如每帧启动一次）会产生分配并增加开销。`yield return null` 不会分配内存，但 `new WaitForSeconds` 等 Yield Instruction 会分配内存。缓存经常复用的 Yield Instruction，并避免在 `WaitUntil` 和 `WaitWhile` 中使用 Lambda，以防止 Delegate 和闭包捕获分配。

与其反复启动新的 Coroutine，不如优先使用长生命周期、通过 `yield return null` 循环的 Coroutine。对于固定时长，缓存或池化 `WaitForSeconds`。Coroutine 会保留对其所有者和捕获变量的引用；为避免泄漏，应确保它们结束，或通过 `MonoBehaviour.StopCoroutine` 停止。

始终使用 Profiler，尤其是在资源受限的平台上，以确认并定位内存分配。更多信息请参阅 Coroutine 分析文档。

## 其他资源

- [Coroutine API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Coroutine.html)
- [`MonoBehaviour.StartCoroutine`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.StartCoroutine.html)

---

## 文档导航

- 上一页：[[00-使用协程跨帧分配任务]]
- 目录：[[00-使用协程跨帧分配任务]]
- 下一页：[[02-分析Coroutine]]
