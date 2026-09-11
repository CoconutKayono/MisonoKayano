# C#/.NET 类型支持

> 原文：[C#/.NET type support](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-type-support.html)

Burst 基于 .NET 的一个子集运行，该子集不允许代码使用任何托管对象或引用类型（C# 中的类）。

下面各节详细介绍 Burst 支持的构造及其限制：

- [内置类型](#内置类型)
- [数组类型](#数组类型)
- [结构体类型](#结构体类型)
- [泛型类型](#泛型类型)
- [向量类型](#向量类型)
- [枚举类型](#枚举类型)
- [指针类型](#指针类型)
- [Span 类型](#span-类型)
- [元组类型](#元组类型)

## 内置类型

### 支持的内置类型

Burst 支持以下内置类型：

- `bool`
- `byte`/`sbyte`
- `double`
- `float`
- `int`/`uint`
- `long`/`ulong`
- `short`/`ushort`

### 不支持的内置类型

Burst 不支持以下内置类型：

- `char`
- `decimal`
- `string`，因为它是托管类型。

## 数组类型

### 支持的数组类型

Burst 支持从静态只读字段加载的只读托管数组：

```csharp
[BurstCompile]
public struct MyJob : IJob {
    private static readonly int[] _preComputeTable = new int[] { 1, 2, 3, 4 };

    public int Index { get; set; }

    public void Execute()
    {
        int x = _preComputeTable[0];
        int z = _preComputeTable[Index];
    }
}
```

访问静态只读托管数组有以下限制：

- 只能直接使用静态只读托管数组，不能将其传递出去，例如作为方法参数传递。
- 不使用 Job 的 C# 代码不应修改只读静态数组的元素，因为 Burst 编译器会在编译时制作一份数据只读副本。
- 不支持多维数组。

如果使用了不支持的静态构造函数，Burst 会产生 `BC1361` 错误。

有关 Burst 如何初始化数组的更多信息，请参阅[静态只读字段和静态构造函数](05-静态只读字段和静态构造函数支持.md)。

### 不支持的数组类型

Burst 不支持托管数组。请改用 `NativeArray<T>` 等 Native 容器。

## 结构体类型

### 支持的结构体

Burst 支持以下结构体：

- 所有字段均为受支持类型的普通结构体。
- 带有固定数组字段的结构体。

**注意**：显式布局的结构体可能生成非最优的原生代码。

### 支持的结构体布局

Burst 支持以下结构体布局：

- `LayoutKind.Sequential`
- `LayoutKind.Explicit`
- `StructLayoutAttribute.Pack`
- `StructLayoutAttribute.Size`

Burst 原生支持 `System.IntPtr` 和 `System.UIntPtr`，将它们作为直接表示指针的 intrinsic 结构体处理。

## 泛型类型

Burst 支持用于结构体的泛型类型。对于带有接口约束的泛型类型，它支持泛型调用的完整实例化，例如带有泛型参数的结构体需要实现接口时。

**注意**：使用[泛型 Job](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-generic-jobs.html)时存在限制。

## 向量类型

Burst 可以将来自 [`Unity.Mathematics`](https://docs.unity3d.com/Packages/com.unity.mathematics@latest) 的向量类型转换为原生 SIMD 向量类型，并对以下类型提供一等优化支持：

- `bool2`/`bool3`/`bool4`
- `uint2`/`uint3`/`uint4`
- `int2`/`int3`/`int4`
- `float2`/`float3`/`float4`

**提示**：出于性能原因，优先使用 4 宽类型（`bool4`、`uint4`、`float4`、`int4`），而不是其他宽度的类型。

## 枚举类型

### 支持的枚举类型

Burst 支持所有枚举，包括指定存储类型的枚举，例如 `public enum MyEnum : short`。

### 不支持的枚举

Burst 不支持 `Enum` 方法，例如 `Enum.HasFlag`。

## 指针类型

Burst 支持指向任何受支持 Burst 类型的指针类型。

## Span 类型

在支持这些类型的 Unity Editor 中，Burst 支持 `Span<T>` 和 `ReadOnlySpan<T>` 类型。

只能在 Burst Job 或函数指针内部使用 Span 类型，不能将其跨过与它们的接口传递。这是因为 C# 的 Span 类型实现支持将 Span 指向托管数据类型（例如托管数组）。例如，以下代码无效：

```csharp
[BurstCompile]
public static void SomeFunctionPointer(Span<int> span) {}
```

这是因为 `Span` 被用在托管与 Burst 的边界上。在 Burst 中，Span 类型遵守安全检查设置，并且只有启用安全检查时才执行性能开销较大的检查。

## 元组类型

Burst 支持在 Burst 编译的 Job 或静态方法中使用值元组 `ValueTuple<T1,T2>`，但不能将其跨过与它们的接口传递。这是因为值元组使用 `LayoutKind.Auto` 结构体布局。Burst 不支持 `LayoutKind.Auto`；有关 Burst 支持的结构体布局，请参阅[结构体类型](#结构体类型)一节。

可以使用普通结构体模拟元组：

```csharp
[BurstCompile]
private struct MyTuple
{
    public int item1;
    public float item2;
}
```

## 相关资源

- [HPC# 概览](01-高性能CSharp简介.md)
- [字符串支持](06-字符串支持.md)
- [C#/.NET System 命名空间支持](07-System命名空间支持.md)

---

## 文档导航

- 上一页：[[07-System命名空间支持]]
- 目录：[[00-CSharp语言支持]]
- 下一页：[[09-Native Plug-in和内部调用支持]]
