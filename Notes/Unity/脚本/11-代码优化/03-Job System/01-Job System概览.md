# Job System 概览

> 原文：[Job system overview](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-overview.html)

Unity 的 Job System 让你能够创建多线程代码，使应用程序可以使用所有可用的 CPU 核心来执行代码。这样，应用程序可以更高效地利用运行设备上所有 CPU 核心的处理能力，而不是将所有代码都运行在一个 CPU 核心上，从而提升性能。

你可以单独使用 Job System，但为了获得更好的性能，还应该使用专门用于为 Unity Job System 编译 Job 的 [Burst Compiler](https://docs.unity3d.com/Packages/com.unity.burst@latest/)。Burst Compiler 改进了代码生成，从而提升性能并减少移动设备的电池消耗。

你还可以将 Job System 与 Unity 的 [Entity Component System](https://docs.unity3d.com/Packages/com.unity.entities@latest/) 结合使用，以创建高性能的面向数据代码。

## 多线程

Unity 使用自己的原生 Job System，通过多个 **Worker Thread** 处理 Unity 自身的原生代码；Worker Thread 的数量取决于应用程序运行设备上可用的 CPU 核心数量。通常，Unity 会在程序启动时默认运行代码的一个线程上执行代码，这个线程称为 **Main Thread**。不过，使用 Job System 时，Unity 会通过 Worker Thread 执行代码，这称为**多线程**。

多线程利用 CPU 跨多个核心同时处理大量线程的能力。任务或指令不再一个接一个地执行，而是同时运行。Worker Thread 会彼此并行运行，并在完成后将结果与 Main Thread 同步。

Job System 确保线程数量足以匹配 CPU 核心的处理能力，这意味着你可以根据需要调度任意数量的任务，而不必专门知道设备上有多少个 CPU 核心。这与依赖[线程池](https://en.wikipedia.org/wiki/Thread_pool)等技术的其他 Job System 不同；在线程池中，更容易低效地创建出多于 CPU 核心数量的线程。

## 工作窃取

Job System 将 Work Stealing 作为调度策略的一部分，用来均衡分配给 Worker Thread 的任务量。Worker Thread 处理任务的速度可能不同，因此某个 Worker Thread 完成自己的全部任务后，会查看其他 Worker Thread 的队列，然后处理分配给其他 Worker Thread 的任务。

## 安全系统

为了让多线程代码更容易编写，Job System 提供了 Safety System，可以检测所有潜在的竞态条件，并保护你免受这些竞态条件可能导致的 Bug 影响。竞态条件是指某个操作的输出取决于另一个它无法控制的进程的执行时机。

例如，如果 Job System 将 Main Thread 代码中的数据引用发送给一个 Job，它无法验证 Main Thread 是否正在读取数据，而 Job 同时正在写入数据。这种情况会产生竞态条件。

为了解决这个问题，Job System 会为每个 Job 发送一份该 Job 需要操作的数据副本，而不是 Main Thread 中数据的引用。这份副本将数据隔离开来，从而消除竞态条件。

Job System 复制数据的方式意味着 Job 只能访问 [Blittable 数据类型](https://en.wikipedia.org/wiki/Blittable_types)。这些类型在托管代码与原生代码之间传递时不需要转换。

Job System 使用 [`memcpy`](http://www.cplusplus.com/reference/cstring/memcpy/) 复制 Blittable 类型，并在 Unity 的托管部分与原生部分之间传输数据。调度 Job 时，它使用 `memcpy` 将数据放入原生内存；执行 Job 时，再让托管侧访问该副本。更多信息请参阅[[03-创建和运行Job#调度 Job]]。

## Collections package

除了 Unity 核心引擎提供的 Job System 之外，Collections package 还扩展了许多 [Job 类型](02-Jobs概览)和[Native Container](05-线程安全类型/00-线程安全类型)。更多信息请参阅 [Collections 文档](https://docs.unity3d.com/Packages/com.unity.collections@latest/)。

## 其他资源

- [[02-Jobs概览]]

---

## 文档导航

- 上一页：[[00-Job System]]
- 目录：[[00-Job System]]
- 下一页：[[02-Jobs概览]]
