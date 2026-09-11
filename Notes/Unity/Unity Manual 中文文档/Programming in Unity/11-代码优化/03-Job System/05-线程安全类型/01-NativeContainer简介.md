# NativeContainer 简介

> 原文：[Introduction to NativeContainer](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-native-container.html)

`NativeContainer` 是一个用于包装原生内存的线程安全 C# 类型。`NativeContainer` 对象还允许 Job 访问与 [[01-Job System概览#多线程|Job System概览：多线程]] 中 Main Thread 共享的数据，而不是操作数据副本。

## NativeContainer 的类型

`Unity.Collections` 命名空间包含以下内置的 `NativeContainer` 对象：

- [`NativeArray`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.NativeArray_1.html)：一种非托管数组，向托管代码公开原生内存缓冲区。
- [`NativeSlice`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.NativeSlice_1.html)：从特定位置开始获取 `NativeArray` 的指定长度子集。

> **注意：** [Collections package](https://docs.unity3d.com/Packages/com.unity.collections@latest/) 包含其他 `NativeContainer`。如需查看其他类型的完整列表，请参阅 Collections 文档中的 [Collection types](https://docs.unity3d.com/Packages/com.unity.collections@latest/index.html?subfolder=/manual/collection-types.html)。

## 读写访问

默认情况下，当 Job 可以访问某个 `NativeContainer` 实例时，它同时拥有读写权限。这种配置可能会降低性能，因为 Job System 不允许调度一个对 `NativeContainer` 实例具有写入权限的 Job，同时调度另一个正在写入该实例的 Job。

但是，如果 Job 不需要写入 `NativeContainer` 实例，可以使用 `[ReadOnly]` Attribute 标记该 `NativeContainer`，如下所示：

```csharp
[ReadOnly]
public NativeArray<int> input;
```

在上面的示例中，你可以让该 Job 与其他同样只读访问第一个 `NativeArray` 的 Job 同时执行。

## 内存分配器

创建 `NativeContainer` 实例时，必须指定所需的内存分配类型。所使用的分配类型取决于你希望保留原生容器的时长。这样可以针对具体情况调整分配方式，以尽可能获得最佳性能。

`NativeContainer` 内存分配和释放有三种 [`Allocator`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.Allocator.html) 类型。实例化 `NativeContainer` 实例时，必须指定适当的类型：

- `Allocator.Temp`：速度最快的分配方式。用于生命周期为一帧或更短的分配。不能使用 `Temp` 将分配传递给存储在 Job 成员字段中的 `NativeContainer` 实例。
- `Allocator.TempJob`：比 `Temp` 慢，但比 `Persistent` 快。用于生命周期为四帧以内的线程安全分配。**重要：**必须在四帧以内对这种分配类型调用 `Dispose`，否则控制台会输出由原生代码生成的警告。大多数小型 Job 都使用这种分配类型。
- `Allocator.Persistent`：速度最慢的分配方式，但可以按需持续存在，必要时甚至可以贯穿应用程序的整个生命周期。它是对直接调用 [`malloc`](http://www.cplusplus.com/reference/cstdlib/malloc/) 的封装。较长时间运行的 Job 可以使用这种 NativeContainer 分配类型。在性能至关重要的场景中不要使用 `Persistent`。

例如：

```csharp
NativeArray<float> result = new NativeArray<float>(1, Allocator.TempJob);
```

> **注意：** 上例中的数字 1 表示 `NativeArray` 的大小。在本例中，它只有一个数组元素，因为它只存储结果中的一条数据。

## NativeContainer 安全系统

所有 `NativeContainer` 实例都内置了[安全系统](01-Job%20System概览.md#安全系统)。它会跟踪对任意 `NativeContainer` 实例的读写操作，并使用这些信息对 `NativeContainer` 的使用强制执行特定规则，使其在多个 Job 和线程之间以确定性的方式运行。

例如，如果两个彼此独立的已调度 Job 写入同一个 `NativeArray`，这是不安全的，因为你无法预测哪个 Job 会先执行。因此，你无法知道其中哪个 Job 会覆盖另一个 Job 写入的数据。当你调度第二个 Job 时，安全系统会抛出异常，并提供清晰的错误消息来解释原因和解决方法。

如果想要调度两个写入同一个 `NativeContainer` 实例的 Job，可以[[05-Job依赖|为这些 Job 设置依赖关系]]。第一个 Job 写入 `NativeContainer`；它执行完毕后，下一个 Job 才能安全地读取和写入同一个 `NativeContainer`。添加依赖关系可以保证 Job 始终按一致的顺序执行，并且 `NativeContainer` 中产生的数据是确定的。

安全系统允许多个 Job 并行读取同一份数据。

这些读写限制在从 Main Thread 访问数据时同样适用。例如，如果你在写入 `NativeContainer` 的 Job 完成之前尝试读取其内容，安全系统会抛出错误。同样，如果仍有读取或写入该 `NativeContainer` 的 Job 等待执行时，你尝试写入它，安全系统也会抛出错误。

此外，由于 NativeContainer 没有实现 [`ref return`](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/ref-returns)，因此不能直接更改 `NativeContainer` 的内容。例如，`nativeArray[0]++;` 等同于执行 `var temp = nativeArray[0]; temp++;`，后者不会更新 `nativeArray` 中的值。

相反，你必须将索引处的数据复制到本地临时副本，修改该副本，然后将其保存回去。例如：

```csharp
MyStruct temp = myNativeArray[i];
temp.memberVariable = 0;
myNativeArray[i] = temp;
```

## 其他资源

- [[03-实现自定义NativeContainer]]

---

## 文档导航

- 上一页：[[00-线程安全类型]]
- 目录：[[00-线程安全类型]]
- 下一页：[[03-实现自定义NativeContainer]]
