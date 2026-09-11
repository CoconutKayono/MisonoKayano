# Jobs 概览

> 原文：[Jobs overview](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-jobs.html)

Job 是一个只完成一项特定任务的小型工作单元。Job 接收参数并操作数据，其行为类似于方法调用。Job 可以是自包含的，也可以依赖其他 Job 完成后才能运行。在 Unity 中，Job 指任何实现了 [IJob 接口](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJob.html)的 Struct。

只有 Main Thread 可以调度和完成 Job。Main Thread 无法访问任何正在运行的 Job 的内容，两个 Job 也不能同时访问某个 Job 的内容。为了确保 Job 高效运行，可以让 Job 彼此建立依赖关系。Unity Job System 允许创建复杂的依赖链，确保 Job 按正确顺序完成。

## Job 类型

- [`IJob`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJob.html)：在一个 Job Thread 上运行单个任务。
- [`IJobParallelFor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJobParallelFor.html)：并行运行任务。每个并行运行的 Worker Thread 都有一个独占索引，可以安全地访问 Worker Thread 之间共享的数据。
- [`IJobParallelForTransform`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Jobs.IJobParallelForTransform.html)：并行运行任务。每个并行运行的 Worker Thread 都有一个来自 Transform Hierarchy 的独占 Transform，可以对其进行操作。
- [`IJobFor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJobFor.html)：与 `IJobParallelFor` 相同，但允许你调度 Job，使其不并行运行。

## 其他资源

- [[03-创建和运行Job]]
- [[05-Job依赖]]
- [[04-并行Jobs]]

---

## 文档导航

- 上一页：[[01-Job System概览]]
- 目录：[[00-Job System]]
- 下一页：[[03-创建和运行Job]]
