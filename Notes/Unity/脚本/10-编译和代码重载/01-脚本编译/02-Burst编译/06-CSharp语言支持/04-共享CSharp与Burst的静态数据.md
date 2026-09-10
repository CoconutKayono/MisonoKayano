# 在 C# 与 Burst 之间共享静态数据

> 原文：[Share static data between C# and Burst](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-shared-static.html)

Burst 基本支持访问静态只读数据。不过，如果要在 C# 与 HPC# 之间共享可变静态数据，请使用 `SharedStatic<T>` 结构体。

下面的示例展示如何访问一个 C# 与 HPC# 都可以修改的 `int` 静态字段：

```csharp
    public abstract class MutableStaticTest
    {
        public static readonly SharedStatic<int> IntField = SharedStatic<int>.GetOrCreate<MutableStaticTest, IntFieldKey>();

        // 定义用于标识 IntField 的 Key 类型
        private class IntFieldKey {}
    }
```

C# 和 HPC# 随后可以这样访问它：

```csharp
    // 写入共享静态数据
    MutableStaticTest.IntField.Data = 5;
    // 读取共享静态数据
    var value = 1 + MutableStaticTest.IntField.Data;
```

使用 `SharedStatic<T>` 时请注意以下事项：

- `SharedStatic<T>` 中的 `T` 定义数据类型。
- 要标识一个静态字段，需要为它提供上下文：为包含类型（例如上面示例中的 `MutableStaticTest`）和字段标识（例如上面示例中的 `IntFieldKey` 类）创建 Key，并将这些类作为 `SharedStatic<int>.GetOrCreate<MutableStaticTest, IntFieldKey>()` 的泛型参数传入。
- 始终先在 C# 的静态构造函数中初始化共享静态字段，再从 HPC# 访问它。如果访问前没有初始化数据，可能会导致未定义的初始化状态。

## 相关资源

- [调用 Burst 编译的代码](02-调用Burst编译代码.md)

---

## 文档导航

- 上一页：[[03-函数指针]]
- 目录：[[00-CSharp语言支持]]
- 下一页：[[05-静态只读字段和静态构造函数支持]]
