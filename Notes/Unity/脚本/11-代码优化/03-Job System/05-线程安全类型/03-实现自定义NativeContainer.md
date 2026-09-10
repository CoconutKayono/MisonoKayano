# 实现自定义 NativeContainer

> 原文：[Implement a custom native container](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-custom-nativecontainer.html)

要实现自定义原生容器，必须使用 [`NativeContainer`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.NativeContainerAttribute.html) Attribute 标注类型。还应了解原生容器如何与[安全系统](01-NativeContainer简介#NativeContainer 安全系统)集成。

实现自定义原生容器主要包含两个要素：

- **Usage tracking：** 让 Unity 能够跟踪使用某个 `NativeContainer` 实例的已调度 Job，从而检测并防止潜在冲突，例如两个 Job 同时写入同一个原生容器。
- **Leak tracking：** 检测 `NativeContainer` 是否未被正确释放。在这种情况下会发生内存泄漏：分配给 `NativeContainer` 的内存会在程序剩余的整个生命周期内变得不可用。

## 实现 Usage tracking

要在代码中访问 Usage tracking，请使用 [`AtomicSafetyHandle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.html) 类。`AtomicSafetyHandle` 持有 Safety System 为给定原生容器存储的中央信息的引用，是 `NativeContainer` 的方法与 Safety System 交互的主要方式。因此，每个 `NativeContainer` 实例都必须包含一个名为 `m_Safety` 的 `AtomicSafetyHandle` 字段。

每个 `AtomicSafetyHandle` 都存储一组标志，用于指示当前上下文中可以对原生容器执行哪些类型的操作。当 Job 包含一个 `NativeContainer` 实例时，Job System 会自动配置 `AtomicSafetyHandle` 中的标志，以反映该 Job 可以如何使用原生容器。

当 Job 尝试从 `NativeContainer` 实例读取数据时，Job System 会在读取之前调用 `CheckReadAndThrow` 方法，以确认 Job 对原生容器具有读取权限。同样，当 Job 尝试写入原生容器时，Job System 会在写入之前调用 `CheckWriteAndThrow`，检查 Job 是否具有写入权限。分配了同一个 `NativeContainer` 实例的两个 Job 各自拥有该原生容器的独立 `AtomicSafetyHandle` 对象。因此，虽然它们都引用同一组中央信息，但可以分别保存标志，指示各自对原生容器拥有的读写权限。

## 实现 Leak tracking

Unity 的原生代码主要实现 Leak tracking。它使用 [`UnsafeUtility.MallocTracked`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.UnsafeUtility.MallocTracked.html) 方法分配存储 `NativeContainer` 数据所需的内存，然后使用 [`UnsafeUtility.FreeTracked`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.UnsafeUtility.FreeTracked.html) 释放内存。

在 Unity 的早期版本中，[`DisposeSentinel`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.DisposeSentinel.html) 类提供 Leak tracking。当垃圾回收器回收 `DisposeSentinel` 对象时，Unity 会报告内存泄漏。要创建 `DisposeSentinel`，请使用 `Create` 方法，该方法同时初始化 `AtomicSafetyHandle`。使用此方法时，无需初始化 `AtomicSafetyHandle`。释放 `NativeContainer` 时，`Dispose` 方法会在一次调用中同时释放 `DisposeSentinel` 和 `AtomicSafetyHandle`。

要确定泄漏的 `NativeContainer` 是在哪里创建的，可以捕获最初分配内存的位置的堆栈跟踪。为此，请使用 [`NativeLeakDetection.Mode`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.NativeLeakDetection.Mode.html) 属性。也可以在 Editor 中访问此属性：转到 **Preferences** > **Jobs** > **Leak Detection Level**，然后选择所需的泄漏检测级别。

## 嵌套原生容器

Safety System 不支持 Job 中的嵌套原生容器，因为 Job System 无法正确配置较大 `NativeContainer` 实例内部每个 `NativeContainer` 的 `AtomicSafetyHandle`。

要阻止调度使用嵌套原生容器的 Job，请使用 `SetNestedContainer`。当 `NativeContainer` 包含其他 `NativeContainer` 实例时，该方法会将其标记为嵌套容器。

## Safety ID 和错误消息

当代码不遵守安全约束时，Safety System 会提供错误消息。为了让错误消息更清晰，可以向 Safety System 注册 `NativeContainer` 对象的名称。

要注册名称，请使用 [`NewStaticSafetyId`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.NewStaticSafetyId.html)，它会返回一个安全 ID，可将该 ID 传递给 [`SetStaticSafetyId`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.SetStaticSafetyId.html)。创建安全 ID 后，可以在该 `NativeContainer` 的所有实例中重复使用它，因此常见做法是将它存储在容器类的静态成员中。

还可以使用 [`SetCustomErrorMessage`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Collections.LowLevel.Unsafe.AtomicSafetyHandle.SetCustomErrorMessage.html) 覆盖特定安全约束违规的错误消息。

## 其他资源

- [[02-复制NativeContainer结构]]
- [[04-自定义NativeContainer示例]]

---

## 文档导航

- 上一页：[[01-NativeContainer简介]]
- 目录：[[00-线程安全类型]]
- 下一页：[[02-复制NativeContainer结构]]
