# C#/.NET System 命名空间支持

> 原文：[C#/.NET System namespace support](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-system-support.html)

Burst 支持部分 `System` 命名空间，并在 Burst 编译器中将这些 API 转换为兼容 Burst 的变体。

## System.Math

Burst 支持 `System.Math` 声明的所有方法，但以下方法除外：

- `double IEEERemainder(double x, double y)` 仅在项目设置中的 API Compatibility Level 设为 `.NET Standard 2.1` 时支持。

## System.IntPtr

Burst 支持 `System.IntPtr`/`System.UIntPtr` 的所有方法，包括静态字段 `IntPtr.Zero` 和 `IntPtr.Size`。

## System.Threading.Interlocked

Burst 支持 `System.Threading.Interlocked` 提供的所有方法的原子内存 intrinsic，例如 `Interlocked.Increment`。

确保 interlocked 方法的源位置自然对齐。例如，指针对齐值是所指向类型大小的倍数：

```csharp
[StructLayout(LayoutKind.Explicit)]
struct Foo
{
    [FieldOffset(0)] public long a;
    [FieldOffset(5)] public long b;

    public long AtomicReadAndAdd()
    {
        return Interlocked.Read(ref a) + Interlocked.Read(ref b);
    }
}
```

如果指向结构体 `Foo` 的指针按 8 字节对齐，而这正是 `long` 值的自然对齐方式，那么 `a` 位于自然对齐的地址，`Interlocked.Read` 读取 `a` 会成功。但是，`b` 不会位于自然对齐地址，因此加载 `b` 时会发生未定义行为。

## System.Threading.Thread

Burst 支持 `System.Threading.Thread` 的 `MemoryBarrier` 方法。

## System.Threading.Volatile

Burst 支持 `System.Threading.Volatile` 提供的非泛型 `Read` 和 `Write` 变体。

## System.HashCode

Burst 支持 `HashCode` 的所有方法，但 `HashCode.Add<T>(T, IEqualityComparer<T>)` 除外。

但是，Burst 不保证结果与 .NET 实现兼容。因此，在 Burst 中运行时，`HashCode` 函数可能产生与 Mono 等其他运行时环境不同的结果。

例如，`HashCode.Combine` 产生的值在 Burst 与托管代码中不同，因为 Burst 无法访问托管实现使用的种子值。

## 相关资源

- [HPC# 概览](01-高性能CSharp简介.md)
- [字符串支持](06-字符串支持.md)
- [C#/.NET 类型支持](08-CSharp和.NET类型支持.md)

---

## 文档导航

- 上一页：[[06-字符串支持]]
- 目录：[[00-CSharp语言支持]]
- 下一页：[[08-CSharp和.NET类型支持]]
