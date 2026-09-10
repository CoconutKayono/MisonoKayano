# 创建并运行 Job

> 原文：[Create and run a job](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-creating-jobs.html)

要创建并成功运行 Job，必须完成以下操作：

- 创建 Job：实现 [`IJob`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJob.html) 接口。
- 调度 Job：调用 Job 的 [`Schedule`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJobExtensions.Schedule.html) 方法。
- 等待 Job 完成：该方法会在 Job 已经完成时立即返回；当你想要访问数据时，可以对 Job 调用 [`Complete`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.JobHandle.Complete.html) 方法。

## 创建 Job

要在 Unity 中创建 Job，请实现 [`IJob`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJob.html) 接口。你可以使用 `IJob` 的实现来调度一个 Job，使其与其他正在运行的 Job 并行运行。

`IJob` 有一个必需方法：[`Execute`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJob.Execute.html)。当 [[01-Job System概览#多线程]] 中的 Worker Thread 运行 Job 时，Unity 会调用这个方法。

创建 Job 时，还可以为它创建一个 [`JobHandle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.JobHandle.html)，其他方法需要使用它来引用该 Job。

> **重要：** Job 内部没有针对访问非只读或可变静态数据的保护。访问此类数据会绕过所有 Safety System，并可能导致应用程序或 Unity Editor 崩溃。

Unity 运行时，Job System 会复制已调度 Job 的数据，从而防止多个线程读取或写入相同数据。只有写入 `NativeContainer` 的数据可以在 Job 完成后访问。这是因为 Job 使用的 `NativeContainer` 副本和原始 `NativeContainer` 对象都指向同一块内存。更多信息请参阅 [[05-线程安全类型/00-线程安全类型]] 文档。

当 Job System 从 Job Queue 中取出一个 Job 时，会在一个线程上运行一次 `Execute` 方法。通常，Job System 会在后台线程上运行 Job，但如果 Main Thread 处于空闲状态，也可能选择 Main Thread。因此，应将 Job 设计为在一帧内完成。

## 调度 Job

<a id="schedule-a-job"></a>

要调度 Job，请调用 `Schedule`。这会将 Job 放入 Job Queue；Job System 会在该 Job 的所有 [[05-Job依赖]]（如果有）完成后开始执行 Job。Job 一旦调度，就无法中断。只有 Main Thread 可以调用 `Schedule`。

> **提示：** Job 提供了 [`Run`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJobExtensions.Run.html) 方法，可以用它替代 `Schedule`，立即在 Main Thread 上执行 Job。你可以将此方法用于调试。

## 完成 Job

调用 `Schedule` 且 Job System 执行完 Job 后，可以对 `JobHandle` 调用 [`Complete`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.JobHandle.Complete.html) 方法，以访问 Job 中的数据。最佳实践是尽可能晚地在代码中调用 `Complete`。调用 `Complete` 后，Main Thread 就可以安全地访问 Job 使用的 [[05-线程安全类型/00-线程安全类型]] 实例。调用 `Complete` 还会清理 Safety System 中的状态；如果不这样做，会造成内存泄漏。

## Job 示例

下面的示例展示了一个将两个浮点值相加的 Job。它实现了 [`IJob`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJob.html)，使用 `NativeArray` 获取 Job 的结果，并使用 `Execute` 方法在其中实现 Job：

```csharp
using UnityEngine;
using Unity.Collections;
using Unity.Jobs;

// Job adding two floating point values together
public struct MyJob : IJob
{
    public float a;
    public float b;
    public NativeArray<float> result;

    public void Execute()
    {
        result[0] = a + b;
    }
}
```

下面的示例基于 `MyJob`，在 Main Thread 上调度 Job：

```csharp
using UnityEngine;
using Unity.Collections;
using Unity.Jobs;

public class MyScheduledJob : MonoBehaviour
{
    // Create a native array of a single float to store the result. Using a
    // NativeArray is the only way you can get the results of the job, whether
    // you're getting one value or an array of values.
    NativeArray<float> result;
    // Create a JobHandle for the job
    JobHandle handle;

    // Set up the job
    public struct MyJob : IJob
    {
        public float a;
        public float b;
        public NativeArray<float> result;

        public void Execute()
        {
            result[0] = a + b;
        }
    }

    // Update is called once per frame
    void Update()
    {
        // Set up the job data
        result = new NativeArray<float>(1, Allocator.TempJob);

        MyJob jobData = new MyJob
        {
            a = 10,
            b = 10,
            result = result
        };

        // Schedule the job
        handle = jobData.Schedule();
    }

    private void LateUpdate()
    {
        // Sometime later in the frame, wait for the job to complete before accessing the results.
        handle.Complete();

        // All copies of the NativeArray point to the same memory, you can access the result in "your" copy of the NativeArray
        // float aPlusB = result[0];

        // Free the memory allocated by the result array
        result.Dispose();
    }


}
```

## 调度和完成的最佳实践

最佳实践是：一旦获得 Job 所需的数据，就立即对 Job 调用 `Schedule`；直到需要结果时，再对 Job 调用 `Complete`。

你可以在一帧中不会与更重要 Job 竞争的时间段调度不太重要的 Job。

例如，如果一帧结束与下一帧开始之间有一段时间没有 Job 正在运行，并且可以接受一帧延迟，那么可以在一帧接近结束时调度 Job，并在下一帧使用其结果。相反，如果应用程序在这个交接时间段已经被其他 Job 占满，而一帧中的其他位置存在利用不足的时间段，那么在该时间段调度 Job 会更高效。

你还可以使用 [Profiler](https://docs.unity3d.com/6000.7/Documentation/Manual/Profiler.html) 查看 Unity 在哪里等待 Job 完成。Main Thread 上的 `WaitForJobGroupID` 标记表示这一点。这个标记可能意味着你引入了某个应该解决的数据依赖关系。查找 `JobHandle.Complete`，以定位迫使 Main Thread 等待的数据依赖关系。

### 避免使用长时间运行的 Job

与线程不同，Job 不会让出执行权。Job 一旦开始运行，其 Worker Thread 就会负责完成该 Job，然后才运行其他 Job。因此，最佳实践是将长时间运行的 Job 拆分成多个彼此[依赖](05-Job依赖.md)的小 Job，而不是提交相对于系统中其他 Job 需要很长时间才能完成的 Job。

Job System 通常会运行多条 Job 依赖链，因此将长时间运行的任务拆分成多个部分后，多条 Job 链就有机会同时推进。如果 Job System 中填满长时间运行的 Job，它们可能会完全占用所有 Worker Thread，阻止独立 Job 执行。这可能会推迟 Main Thread 明确等待的重要 Job 的完成时间，导致原本不会出现的 Main Thread 停顿。

尤其是，长时间运行的 [`IJobParallelFor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJobParallelFor.html) Job 会对 Job System 产生负面影响，因为这类 Job 会根据 Job Batch Size，刻意尝试使用尽可能多的 Worker Thread。如果无法拆分长时间运行的并行 Job，可以考虑在调度时增大 Job 的 Batch Size，以限制获取该长时间运行 Job 的 Worker 数量。

```csharp
MyParallelJob jobData = new MyParallelJob();
jobData.Data = someData;  
jobData.Result = someArray;  

// Use half the available worker threads, clamped to a minimum of 1 worker thread
const int numBatches = Mathf.Max(1, JobsUtility.JobWorkerCount / 2); 
const int totalItems = someArray.Length;
const int batchSize = totalItems / numBatches;

// Schedule the job with one Execute per index in the results array and batchSize items per processing batch
JobHandle handle = jobData.Schedule(result.Length, totalItems, batchSize);
```

## 其他资源

- [[05-Job依赖]]
- [[05-线程安全类型/00-线程安全类型]]

---

## 文档导航

- 上一页：[[02-Jobs概览]]
- 目录：[[00-Job System]]
- 下一页：[[05-Job依赖]]
