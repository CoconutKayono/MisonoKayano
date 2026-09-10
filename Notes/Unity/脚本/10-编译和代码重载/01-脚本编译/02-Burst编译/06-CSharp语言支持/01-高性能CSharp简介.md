# 高性能 CSharp 简介

> 原文：[High Performance C# introduction](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-hpc-overview.html)

Burst 使用一个称为高性能 C#（HPC#）的高性能 C# 子集。

## HPC 中支持的 C# 功能

HPC# 支持 C# 中的大多数表达式和语句，具体包括：

| 支持的功能 | 说明 |
| --- | --- |
| 扩展方法。 | 不适用。 |
| 结构体的实例方法。 | 不适用。 |
| unsafe 代码和指针操作。 | 不适用。 |
| 从静态只读字段加载。 | 详见[静态只读字段和静态构造函数](05-静态只读字段和静态构造函数支持.md)。 |
| 常规 C# 控制流。 | `if`、`else`、`switch`、`case`、`for`、`while`、`break`、`continue`。 |
| `ref` 和 `out` 参数。 | 不适用。 |
| `fixed` 语句。 | 不适用。 |
| 部分 [IL opcode](https://docs.microsoft.com/en-us/dotnet/api/system.reflection.emit.opcodes?view=net-6.0)。 | `cpblk`、`initblk`、`sizeof`。 |
| `DLLImport` 和内部调用。 | 详见 [[09-Native Plug-in和内部调用支持]]。 |
| `try` 和 `finally` 关键字。Burst 也支持相关的 `IDisposable` 模式、`using` 和 `foreach`。 | 如果 Burst 中发生异常，其行为与 .NET 不同。在 .NET 中，如果 `try` 块内发生异常，控制流会进入 `finally` 块；但在 Burst 中，无论异常发生在 `try` 块内还是外部，都会像不存在 `finally` 块一样抛出异常。Burst 支持调用 `foreach`，但有一种 `foreach` 情况目前不支持，详见“Foreach 和 While”一节。 |
| 字符串和 `ProfilerMarker`。 | 详见[支持 Unity Profiler 标记](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/debugging-profiling-tools.html#profiler-markers)。 |
| `throw` 表达式。 | Burst 只支持简单的 `throw` 模式，例如 `throw new ArgumentException("Invalid argument")`。使用此类简单模式时，Burst 会提取静态字符串异常消息，并将其包含在生成的代码中。 |
| 字符串和 `Debug.Log`。 | 仅部分支持，详见[字符串支持和 `Debug.Log`](06-字符串支持.md)。 |

Burst 还为一些 HPC# 无法直接访问的 C# 构造提供替代方案：

- [函数指针](03-函数指针.md)，可替代 HPC# 中的委托。
- [Shared static](04-共享CSharp与Burst的静态数据.md)，用于从 C# 和 HPC# 访问可变静态数据。

### 异常表达式

Burst 支持使用 `throw` 表达式抛出异常。在 Editor 中抛出的异常可以由托管代码捕获，并报告到 Console 窗口。在 Player 构建中抛出的异常始终会导致应用程序终止。因此，使用 Burst 时只能将异常用于异常情况。

为了确保代码不会依赖异常实现常规控制流，Burst 会对未使用 `[Conditional("ENABLE_UNITY_COLLECTIONS_CHECKS")]` 标注的方法中尝试 `throw` 的代码发出以下警告：

```text
Burst warning BC1370: An exception was thrown from a function without the correct [Conditional("ENABLE_UNITY_COLLECTIONS_CHECKS")] guard. Exceptions only work in the editor and so should be protected by this guard
```

### Foreach 和 While

Burst 支持调用 `foreach` 和 `while`。但是，目前不支持一种边界情况：方法接受一个或多个泛型集合参数 `T: IEnumerable<U>`，并在方法体中对至少一个集合调用 `foreach` 或 `while`。以下示例说明了这一限制：

```csharp
public static void IterateThroughConcreteCollection(NativeArray<int> list)
{
    foreach (var element in list)
    {
        // 可以工作
    }
}

public static void IterateThroughGenericCollection<S>(S list) where S : struct, IEnumerable<int>
{
    foreach (var element in list)
    {
        // 无法工作
    }
}
```

上面的 `IterateThroughConcreteCollection()` 参数是具体集合类型，即 `NativeArray<int>`。由于类型具体，在方法内迭代它可以通过 Burst 编译。

而下面的 `IterateThroughGenericCollection()` 参数是泛型集合类型 `S`，因此在方法内迭代 `S` 无法通过 Burst 编译，而会产生以下错误：

```text
Can't call the method (method name) on the generic interface object type (object name). This may be because you are trying to do a foreach over a generic collection of type IEnumerable.
```

## HPC 中不支持的 C# 功能

HPC# 不支持以下 C# 功能：

- 在 `try/catch` 中捕获异常（`catch`）。
- 除通过 [Shared Static](04-共享CSharp与Burst的静态数据.md) 以外写入静态字段。
- 任何与托管对象有关的方法，例如字符串方法。

## 相关资源

- [静态只读字段和静态构造函数支持](05-静态只读字段和静态构造函数支持.md)
- [字符串支持](06-字符串支持.md)
- [C#/.NET 类型支持](08-CSharp和.NET类型支持.md)
- [C#/.NET System 命名空间支持](07-System命名空间支持.md)

---

## 文档导航

- 上一页：[[00-CSharp语言支持]]
- 目录：[[00-CSharp语言支持]]
- 下一页：[[02-调用Burst编译代码]]
