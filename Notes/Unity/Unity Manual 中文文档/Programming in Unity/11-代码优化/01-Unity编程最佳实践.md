# Unity 编程最佳实践

> 原文：[Unity programming best practices](https://docs.unity3d.com/6000.7/Documentation/Manual/programming-best-practices.html)

与标准的 C#/.NET 项目相比，Unity 的编程环境有一些独特特性，编写代码时需要额外考虑。下面总结了为 Unity 应用程序编写代码时需要注意的关键问题，以及帮助你避免常见陷阱的最佳实践。

## Unity Object 生命周期和引用

在 Unity 中编写 C# 时，将对象与其他对象或 `null` 比较时要谨慎。对于继承自 [UnityEngine.Object](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Object.html) 的类型，Unity 使用自定义版本的 C# [相等和不等运算符](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/equality-operators)。这意味着，即使 `myGameObject` 在技术上仍持有有效的 C# 对象引用，`myGameObject == null` 这个 null 检查也可能求值为 `true`（反过来，`myGameObject != null` 也可能求值为 `false`）。有关此行为细节，请参阅[自定义相等运算符](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Object.html#custom-equality-comparers)。

Unity 的自定义相等行为和对象生命周期会对代码产生以下影响：

- 如果检查的目的，是确保排除已销毁的对象，请务必对 Unity 对象使用 `if (obj == null)`，不要使用 `ReferenceEquals`。
- 如果要检查真正的 C# null 引用，请使用 `ReferenceEquals`，或先将对象转换为 `System.Object`。
- 比较两个 Unity 对象是否相等时，请注意：如果其中一个或两个对象已销毁并重新创建（例如通过 [Undo](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Undo.html)），`obj1 == obj2` 即使面对两个不同的 C# 对象引用，也可能返回 `true`。
- 自定义相等运算符比标准 C# 运算符慢。通常这不是问题，但在大量使用以及 hot path 中要留意这一点。
- 不要跨场景卸载缓存组件而不加保护，因为组件可能已经销毁，却仍作为没有 unmanaged counterpart 的 C# wrapper 对象存在。
- 不要在 static field 中持有大型资源的 strong reference，因为它们会跨场景持久存在并阻止资源卸载。
- 销毁对象时，[`Object.DestroyImmediate`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.DestroyImmediate.html) 只能在 Editor 中使用；运行时请使用 [`Object.Destroy`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Destroy.html)，让 Unity 调度销毁操作。

## 避免使用 C# finalizer

不要在运行时代码中使用 [C# finalizer](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/finalizers)，原因如下：

- 它们在单独的 finalizer thread 上运行，而 Unity API 通常要求在主线程上运行。
- 它们以非确定方式运行，会导致不可预测的行为。
- 除非应用程序执行垃圾回收并等待，否则它们可能根本不会运行。
- 如果没有特别处理，从 finalizer 抛出的异常可能导致应用程序停止。
- 它们仅仅因为存在，就会增加 garbage collector 的开销。

## Garbage collector 开销和分配

Unity 应用程序需要注意的最重要性能风险之一，是运行时分配内存并增加 garbage collector 开销的代码，尤其是 hot path 中的代码。

为避免这一点，请采用以下编码实践：

- 通过[缓存和复用列表](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-reusable-code.html)，并在可用时使用 non-allocating 版本的方法，避免逐帧分配。这也包括在使用 [coroutine](https://docs.unity3d.com/6000.7/Documentation/Manual/Coroutines.html) 时缓存 [`WaitForSeconds`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitForSeconds.html) 和其他 [yield instruction](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/YieldInstruction.html)。
- 尽可能使用 non-allocating 版本的方法，并在 [`Awake`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.Awake.html) 中执行 [`GameObject.GetComponent`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponent.html) 等昂贵操作，缓存返回对象的引用，而不是在 [`Update`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.Update.html) 中重复调用。
- 避免在运行时代码中使用 [LINQ](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)，尤其不要在逐帧执行的 `Update` 或 `FixedUpdate` 以及其他 hot path 中使用。`System.Linq` 命名空间中的方法可能造成不必要的分配，并涉及 boxing 和 closure。
- 避免[重复的字符串操作](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-reference-types.html)，例如字符串拼接。
- 找出并避免使用 reflection。有关更多信息，请参阅[避免 C# reflection 开销](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-gc-avoid-reflection.html)。

有关这些问题的更详细指导和示例，请参阅[优化代码以使用 managed memory](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-optimizing-code-managed-memory.html)。

有关追踪和降低 garbage collector 开销的信息，请参阅[Managed memory](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-managed-memory.html)。

## MonoBehaviour Update loop 优化

许多 Unity 项目采用这样的传统模式：使用 `MonoBehaviour` script component，通过 [`MonoBehaviour.Update`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.Update.html)、[`MonoBehaviour.FixedUpdate`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.FixedUpdate.html) 和 [`MonoBehaviour.LateUpdate`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.LateUpdate.html) 等内置 callback 定期更新游戏状态；这些 callback 通常每秒运行许多次。

在适当使用时，这仍然是一个简单且有效的模型，但它有一些常见的性能风险，缺乏经验的开发者很容易忽视：

- Unity 对逐帧或其他定期 event function 的默认实现扩展性可能较差。每个 `Update` function 都会因 Unity 的内部管理以及与 native layer 的交互而产生少量开销。当这类 `MonoBehaviour` script 很多时，累计开销可能会显著影响性能。
- 内置 update 运行非常频繁，因此属于 hot code path；放入其中的低效、耗内存操作的影响会被放大。缺乏经验的用户常见的不良模式，是创建许多包含 `Update` function 的 `MonoBehaviour` script，而这些 function 大部分时间都不必要地运行，或运行时不必要地消耗大量内存。

为降低这些风险，可以考虑以下选项：

- 考虑使用 Unity 的 [Entity Component System (ECS)](https://docs.unity3d.com/Packages/com.unity.entities@latest) 将项目转换为 data-oriented architecture，以便在实体数量多时获得更好的扩展性。
- 如果使用基于 `MonoBehaviour` 的 architecture：
  - 为确保 hot path 对 managed memory 的影响最小，请参阅[优化代码以使用 managed memory](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-optimizing-code-managed-memory.html)。
  - 使用 centralized update manager 或 custom Player loop，减少 active `Update` function 的数量。有关更多信息，请参阅[使用 custom update manager](https://docs.unity3d.com/6000.7/Documentation/Manual/events-per-frame-optimization.html)和[自定义 Player loop](https://docs.unity3d.com/6000.7/Documentation/Manual/player-loop-customizing.html)。
  - 请记住，即使项目基于 `MonoBehaviour`，也经常可以使用 Unity data-oriented system 的特定功能。可以使用 [Jobs](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system.html)，对代码的部分区域进行 [Burst-compile](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html)，在性能关键部分使用更高效的数据结构（例如 [`NativeArray`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.NativeArray_1.html)），并为 managed API 选择 unmanaged alternative，例如用于 transform operation 的[这些 API](https://docs.unity3d.com/6000.7/Documentation/Manual/transformhandle-landing.html)。

## Thread safety

虽然 Unity 具备 multithreaded 能力，但其 core runtime 是 single-threaded 的，并且 `UnityEngine` 和 `UnityEditor` 命名空间中的大多数 API 只能从主线程调用。不要从后台线程引用 GameObject、Transform、Component 或 asset API。永远不要在主线程上对 `Task` 使用 `await` 配合 `Task.Result` 或 `Task.Wait`，因为这会导致 deadlock。

处理本质上异步且长期运行的操作时，Unity 提供 [`Awaitable`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Awaitable.html) 类作为 .NET `Task` 的 Unity-specific alternative。`Awaitable` 使用 object pooling 减少分配，并且了解 `Update`、`FixedUpdate` 等 Unity-specific concept，因此可以 `await` task，并安排它们在 Player loop 的特定时刻恢复。更多信息请参阅[使用 Awaitable 类进行异步编程](https://docs.unity3d.com/6000.7/Documentation/Manual/async-await-support.html)。

对于生命周期较短但计算量更大的并行工作，Unity 提供可以 [Burst compile](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html) 的 [job system](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system.html)。更多信息请参阅[使用 job system 编写 multithreaded code](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system.html)。

## Compilation considerations

为了获得最佳性能，不仅要考虑如何编写代码，还要考虑代码如何编译。未经思考地编译代码，而不是主动定义每个 source file 或代码区域适用的 context，会带来以下成本：

- 如果包含不必要的代码，build size 会增大。
- 为应用变更而进行编译和重新编译会耗费时间。这尤其会影响在 Editor 中的 iteration time。
- 如果对某个平台或 context 包含了不适用的代码，可能在运行时产生错误。

Unity 提供了多种机制，帮助你控制代码的哪些部分针对不同平台和 context 进行编译：

- 可以使用 Assembly Definition 将 source file 分组到 assembly 中，使它们能够分别编译。这样可以将 Editor-only code 与 runtime code 隔离，也可以将 platform-specific code 与 cross-platform code 隔离。更多信息请参阅[将 script 组织到 assembly 中](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-files.html)。
- 可以将 `#if` directive 与 [scripting symbol](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-symbol-reference.html) 一起使用，根据目标平台或 context 排除特定代码区域的编译。例如，将 Editor-only code 放在 `#if UNITY_EDITOR` directive 后面，以便从 runtime build 中排除。有关 Unity 提供的条件性包含或排除代码的多种方法，请参阅[条件编译](https://docs.unity3d.com/6000.7/Documentation/Manual/platform-dependent-compilation.html)。
- [Mono scripting backend](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-mono.html) 特有的一个关键概念是 [domain reload](https://docs.unity3d.com/6000.7/Documentation/Manual/configurable-enter-play-mode.html)：重新编译 script 时会自动发生，如果选择启用它，进入 Play mode 时也会发生。Domain reload 耗时，并且会影响在 Editor 中编写和测试代码时的 iteration time。Domain reload 还与 Mono scripting backend 相关，而该 backend 将在未来的 Unity 版本中移除。基于这些原因，进入 Play mode 时的 domain reload 默认关闭；建议保持关闭，并使用其他方式重置 static state。更多信息请参阅[不进行 domain reload 进入 Play mode](https://docs.unity3d.com/6000.7/Documentation/Manual/domain-reloading.html)。

## Unity 的 analysis tool

Unity 提供多种工具，帮助你找出瓶颈并编写性能更好的代码。[Project Auditor](https://docs.unity3d.com/6000.7/Documentation/Manual/project-auditor/project-auditor.html) 可以分析项目代码，找出常见性能问题并建议修复方法。[Profiler](https://docs.unity3d.com/6000.7/Documentation/Manual/Profiler.html) 可以通过提供 CPU 和 GPU 使用情况、内存分配等详细信息，帮助你找出代码中的 runtime performance bottleneck。你还可以创建 [Roslyn analyzer](https://learn.microsoft.com/en-us/visualstudio/code-quality/roslyn-analyzers-overview?view=visualstudio)，在项目中强制执行 coding standard，并找出特定于项目的性能问题。

有关创建 custom Roslyn analyzer 和 source generator 的更多信息，请参阅[Roslyn analyzer 和 source generator](https://docs.unity3d.com/6000.7/Documentation/Manual/roslyn-analyzers.html)。

有关 Unity analysis tool 套件的更多信息，请参阅[优化](https://docs.unity3d.com/6000.7/Documentation/Manual/analysis.html)。

## 其他资源

- [Unity 中的内存](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-memory.html)
- [优化代码以使用 managed memory](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-optimizing-code-managed-memory.html)
- [调试和诊断](https://docs.unity3d.com/6000.7/Documentation/Manual/debugging-and-diagnostics.html)

---

## 文档导航

- 上一页：[[00-代码优化]]
- 目录：[[00-代码优化]]
- 下一页：[[00-异步编程]]
