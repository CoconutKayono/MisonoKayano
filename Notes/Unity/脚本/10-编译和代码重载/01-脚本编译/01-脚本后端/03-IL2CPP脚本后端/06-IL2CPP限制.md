# IL2CPP 限制

> 原文：[IL2CPP limitations](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-restrictions.html)

IL2CPP 后端存在一些值得注意的限制，部分原因是提前编译（AOT）的固有特性，部分原因是特定于平台的限制。

## 线程

Web 平台不支持托管线程。`System.Threading` 命名空间中的大多数 API 要么执行后不产生效果，要么无法运行。部分 .NET 类库也隐式依赖线程。一个常见示例是 [`System.Timers.Timer`](https://learn.microsoft.com/en-us/dotnet/api/system.timers.timer?view=net-9.0) 类，它依赖线程支持。详细说明请参阅 [Web 平台上的 .NET API 支持](https://docs.unity3d.com/6000.7/Documentation/Manual/web-dotnet-api-support.html)。

## 反射

Unity 支持在 AOT 平台上使用反射。但是，如果编译器无法推断某段代码会通过反射使用，那么该代码在运行时可能不存在。详细信息请参阅[托管代码剥离](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-stripping.html)。

AOT 平台无法实现 [`System.Reflection.Emit`](https://learn.microsoft.com/en-us/dotnet/api/system.reflection.emit?view=net-9.0) 命名空间中的任何方法。

## 异常筛选器

IL2CPP 支持异常筛选器。不过，由于 IL2CPP 使用 C++ 异常实现托管异常，筛选器语句和 `catch` 代码块的执行顺序会有所不同。除非筛选器代码块向某个字段写入值，否则通常不会注意到这种差异。

在 Mono 上，字段写入发生在筛选器求值时，即进入 `catch` 代码块之前，并且相对于其他筛选器的顺序是确定的。在 IL2CPP 上，由于筛选器是模拟执行的，字段写入可能会在不同时间发生。这可能造成可观察的差异，例如：

- 相对于 `catch` 或 `finally` 代码块，字段更新早于或晚于预期。
- 存在多个筛选器时交错顺序不同，可能改变哪些更新先可见。
- 在少数情况下，依赖筛选器副作用来控制 `catch` 或 `finally` 行为的代码可能读到过期值，或观察到不同顺序的值。

最佳实践是避免在筛选器中产生副作用，将状态变更移到 `catch` 代码块中（或移到由 `catch` 调用的辅助函数中），从而确保 IL2CPP 和 Mono 之间的行为一致。

## 序列化

AOT 平台可能会因为序列化和反序列化使用反射而遇到问题。如果某个类型或方法只在序列化或反序列化过程中通过反射使用，AOT 编译器就无法检测到需要为该类型或方法生成代码。

## 泛型类型和方法

对于泛型类型和方法，编译器必须确定使用了哪些泛型实例，因为不同的泛型实例可能需要不同的代码。例如，`List<int>` 的代码与 `List<double>` 的代码不同。不过，IL2CPP 会为引用类型的用法共享代码，因此 `List<object>` 和 `List<string>` 使用相同的代码。

在以下情况下，可能会引用 IL2CPP 在编译时未找到的泛型类型和方法：

1. 在运行时创建新的泛型实例：`Activator.CreateInstance(typeof(SomeGenericType<>).MakeGenericType(someType));`
2. 调用泛型实例上的静态方法：`typeof(SomeGenericType<>).MakeGenericType(someType).GetMethod("AMethod").Invoke(null, null);`
3. 调用静态泛型方法：`typeof(SomeType).GetMethod("GenericMethod").MakeGenericMethod(someType).Invoke(null, null);`
4. 某些在编译时无法推断的泛型虚函数调用。
5. 使用深度嵌套的泛型值类型进行调用，例如 `Struct<Struct<Struct<...<Struct<int>>>>`。

为支持这些情况，IL2CPP 会生成适用于任意类型参数的泛型代码。不过，由于无法确定类型的大小，也无法确定类型是引用类型还是值类型，这种代码的速度会更慢。如果需要确保生成更快的泛型方法，请执行以下操作：

- 如果泛型参数始终是引用类型，请添加 `where: class` 约束。这样 IL2CPP 会使用引用类型共享生成回退方法，不会造成性能下降。
- 如果泛型参数始终是值类型，请添加 `where: struct` 约束。这可以启用一些优化，但由于值类型的大小可能不同，代码仍会较慢。
- 创建名为 `UsedOnlyForAOTCodeGeneration` 的方法，并在其中引用希望 IL2CPP 生成的泛型类型和方法。无需调用此方法。以下示例确保生成 `GenericType<MyStruct>` 的特化版本：

```csharp
public void UsedOnlyForAOTCodeGeneration()
{
    // Ensure that IL2CPP will create code for MyGenericStruct
    // using MyStruct as an argument.
    new GenericType<MyStruct>();

    // Ensure that IL2CPP will create code for SomeType.GenericMethod
    // using MyStruct as an argument.
    new SomeType().GenericMethod<MyStruct>();

    public void OnMessage<T>(T value)
    {
        Debug.LogFormat("Message value: {0}", value);
    }

    // Include an exception so we can be sure to know if this
    // method is ever called.
    throw new InvalidOperationException(
        "This method is used for AOT code generation only. " +
        "Do not call it at runtime.");
}
```

> **注意**：要只编译单个、完全可共享的泛型代码版本，请将 **IL2CPP Code Generation** [Player 设置](https://docs.unity3d.com/6000.7/Documentation/Manual/class-PlayerSettings.html)为 **Optimize for code size and build time**。这会减少生成的方法数量，从而减少编译时间和构建大小，但代价是运行时性能降低。

## 从原生代码调用托管方法

需要封送到 C 函数指针、以便从原生代码调用的托管方法，在 AOT 平台上有一些限制：

- 托管方法必须是静态方法。
- 托管方法必须具有 `[MonoPInvokeCallback]` Attribute。
- 如果托管方法是泛型方法，可能需要使用 `[MonoPInvokeCallback(Type)]` 重载，指定必须支持的泛型特化版本。此时，Type 必须是一个泛型实例，并且包含正确数量的泛型参数。一个方法可以有多个 `[MonoPInvokeCallback]` Attribute，如下所示：

```csharp
// Generates reverse P/Invoke wrappers for NameOf<long> and NameOf<int>
// Note that the types are only used to indicate the generic arguments.
[MonoPInvokeCallback(typeof(Action<long>))]
[MonoPInvokeCallback(typeof(Action<int>))]
private static string NameOfT<T>(T item)
{
    return typeof(T).Name;
}
```

## 不支持的 .NET API

IL2CPP 不支持以下 .NET API 和功能：

- [`MarshalAs`](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.marshalasattribute?view=net-9.0) 和 [`FieldOffset`](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.fieldoffsetattribute?view=net-9.0) Attribute 的反射。IL2CPP 支持在编译时使用这些 Attribute。你应使用它们来进行正确的[平台调用封送](https://docs.microsoft.com/en-us/dotnet/framework/interop/marshaling-data-with-platform-invoke)。
- C# [`dynamic`](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interop/using-type-dynamic) 关键字。此关键字需要 JIT 编译，而 IL2CPP 无法执行 JIT 编译。
- [`Marshal.Prelink`](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.marshal.prelink?view=net-9.0) 或 [`Marshal.PrelinkAll`](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.marshal.prelinkall?view=net-10.0) API 方法。
- [`System.Diagnostics.Process`](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.process?view=net-9.0) API 方法。

如果桌面平台需要这些 API，请使用 [[../02-Mono脚本后端]]。

## 其他资源

- [Unity .NET 功能](https://docs.unity3d.com/6000.7/Documentation/Manual/overview-of-dot-net-in-unity.html)


---

## 文档导航

- 上一页：[[05-Linux IL2CPP交叉编译器]]
- 目录：[[00-IL2CPP脚本后端]]
- 下一页：[CoreCLR 脚本后端（实验性）](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-coreclr.html)
