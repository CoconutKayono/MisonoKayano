# 复制 NativeContainer 结构

> 原文：[Copying NativeContainer structures](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-copy-nativecontainer.html)

[NativeContainer](01-NativeContainer简介.md) 是 Value Type，这意味着将其赋值给变量时，Unity 会复制 `NativeContainer` 结构。该结构包含指向 NativeContainer 数据存储位置的指针，其中包括 [`AtomicSafetyHandle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.html)。Unity 不会复制整个 `NativeContainer` 的内容。

这意味着可能存在多个 `NativeContainer` 结构副本，它们都引用同一片内存区域，并且都包含引用同一中央记录的 `AtomicSafetyHandle` 对象。

![NativeContainer 对象副本的工作方式](Unity/Unity%20Manual%20中文文档/Programming%20in%20Unity/11-代码优化/03-Job%20System/05-线程安全类型/图片/native-container-diagram.png)

*NativeContainer 对象副本的工作方式*

上图展示了三个不同的 `NativeArray` 结构副本，它们都代表同一个实际容器。每个副本都指向与原始 `NativeArray` 相同的存储数据和安全数据。不过，每个 `NativeArray` 副本都有不同的标志，用来指示 Job 可以对该副本执行哪些操作。指向安全数据的指针与这些标志共同组成 `AtomicSafetyHandle`。

## 版本号

如果释放了 `NativeContainer`，所有 `NativeContainer` 结构副本都必须识别出原始 `NativeContainer` 已失效。释放原始 `NativeContainer` 意味着曾用于存储其数据的内存块已被释放。在这种情况下，每个 `NativeContainer` 副本中存储的指向数据的指针都已失效，使用它可能导致访问冲突。

`AtomicSafetyHandle` 也指向一个对于这些 `NativeContainer` 实例而言已失效的中央记录。不过，Safety System 永远不会释放中央记录所占用的内存，因此避免了访问冲突的风险。

相反，每条记录都包含一个版本号。每个引用该记录的 `AtomicSafetyHandle` 内部都存储着一份版本号副本。释放 NativeContainer 时，Unity 会调用 `Release()`，使中央记录中的版本号递增。之后，该记录可以重新用于其他 `NativeContainer` 实例。

每个剩余的 `AtomicSafetyHandle` 都会将其存储的版本号与中央记录中的版本号进行比较，以检查 `NativeContainer` 是否已被释放。Unity 会在调用 [`CheckReadAndThrow`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.CheckReadAndThrow.html) 和 [`CheckWriteAndThrow`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.CheckWriteAndThrow.html) 等方法时自动执行此检查。

## 动态 NativeContainer 的静态视图

动态 NativeContainer 是大小可变、可以继续向其中添加元素的容器，例如 [<code>NativeList<T></code>](https://docs.unity3d.com/Packages/com.unity.collections@latest/index.html?subfolder=/api/Unity.Collections.NativeList-1.html)（Collections package 中提供）。这与静态 NativeContainer 相反，例如 [`NativeArray<T>`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.NativeArray_1.html) 具有固定大小，不能更改。

使用动态 NativeContainer 时，还可以通过另一种称为视图（view）的接口直接访问其数据。视图可以为 `NativeContainer` 对象的数据创建别名，而不会复制或取得数据的所有权。视图的示例包括枚举器对象，你可以用它逐个访问 NativeContainer 中的元素；以及 [`NativeList<T>.AsArray`](https://docs.unity3d.com/Packages/com.unity.collections@latest/index.html?subfolder=/api/Unity.Collections.NativeList-1.html#Unity_Collections_NativeList_1_AsArray) 等方法，它可以让你像使用 `NativeArray` 一样使用 `NativeList`。

动态 NativeContainer 的大小发生变化时，视图通常不是线程安全的。这是因为 NativeContainer 大小发生变化时，Unity 会重新定位数据在内存中的存储位置，导致视图保存的指针失效。

### 次级版本号

为了支持动态 NativeContainer 大小发生变化的场景，Safety System 在 `AtomicSafetyHandle` 中加入了次级版本号机制。该机制与版本机制类似，但使用中央记录中独立于第一个版本号递增的第二个版本号。

若要使用次级版本号，可以使用 [`UseSecondaryVersion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.UseSecondaryVersion.html) 配置指向 `NativeContainer` 所存数据的视图。对于改变 NativeContainer 大小或以其他方式使现有视图失效的操作，应使用 [`CheckWriteAndBumpSecondaryVersion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.CheckWriteAndBumpSecondaryVersion.html) 代替 `CheckWriteAndThrow`。还需要在 `NativeContainer` 上设置 [`SetBumpSecondaryVersionOnScheduleWrite`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.SetBumpSecondaryVersionOnScheduleWrite.html)，以便每当调度写入 NativeContainer 的 Job 时自动使视图失效。

创建视图并将 `AtomicSafetyHandle` 复制到视图时，使用 [`CheckGetSecondaryDataPointerAndThrow`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.CheckGetSecondaryDataPointerAndThrow.html)，确认此时可以安全地将 NativeContainer 的内存指针复制到视图中。

## 特殊句柄

处理临时 NativeContainer 时，可以使用两个特殊句柄：

- [`GetTempMemoryHandle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.GetTempMemoryHandle.html)：返回一个 `AtomicSafetyHandle`，可用于使用 `Allocator.Temp` 分配的原生容器。当前临时内存作用域退出时，Unity 会自动使此句柄失效，因此无需手动释放。要测试某个 `AtomicSafetyHandle` 是否为 `GetTempMemoryHandle` 返回的句柄，请使用 `IsTempMemoryHandle`。
- [`GetTempUnsafePtrSliceHandle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.GetTempUnsafePtrSliceHandle.html)：返回一个全局句柄，可用于由不安全内存支持的临时原生容器，例如由栈内存构造的 `NativeSlice`。不能将使用此句柄的容器传递给 Job。

## 其他资源

- [[03-实现自定义NativeContainer]]
- [[04-自定义NativeContainer示例]]

---

## 文档导航

- 上一页：[[03-实现自定义NativeContainer]]
- 目录：[[00-线程安全类型]]
- 下一页：[[04-自定义NativeContainer示例]]
