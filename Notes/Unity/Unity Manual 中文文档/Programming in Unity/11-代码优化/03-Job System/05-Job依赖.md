# Job 依赖

> 原文：[Job dependencies](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-job-dependencies.html)

通常，一个 Job 会依赖另一个 Job 的结果。例如，Job A 可能会写入一个由 Job B 用作输入的 `NativeArray`。调度有依赖关系的 Job 时，必须将这种依赖关系告知 Job System。Job System 不会运行依赖 Job，直到它所依赖的 Job 完成。一个 Job 可以依赖多个 Job。

你还可以创建 Job 链，其中每个 Job 都依赖前一个 Job。不过，依赖关系会延迟 Job 的执行，因为 Job 必须等待它的所有依赖完成后才能运行。完成一个有依赖关系的 Job 时，必须先完成它所依赖的 Job，以及这些依赖 Job 所依赖的所有 Job。

调用 Job 的 [`Schedule`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.IJobExtensions.Schedule.html) 方法时，该方法会返回一个 [`JobHandle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.JobHandle.html)。你可以将 `JobHandle` 用作其他 Job 的依赖。如果一个 Job 依赖另一个 Job 的结果，可以将第一个 Job 的 `JobHandle` 作为参数传递给第二个 Job 的 `Schedule` 方法，如下所示：

```csharp
JobHandle firstJobHandle = firstJob.Schedule();
secondJob.Schedule(firstJobHandle);
```

## 合并依赖

如果一个 Job 有很多依赖，可以使用 [`JobHandle.CombineDependencies`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Jobs.JobHandle.CombineDependencies.html) 方法将它们合并。`CombineDependencies` 允许你将这些依赖传递给 `Schedule` 方法。

```csharp
NativeArray<JobHandle> handles = new NativeArray<JobHandle>(numJobs, Allocator.TempJob);

// Populate `handles` with `JobHandles` from multiple scheduled jobs...

JobHandle jh = JobHandle.CombineDependencies(handles);
```

## 多个 Job 和依赖关系示例

下面是一个具有多个依赖关系的多个 Job 示例。最佳实践是将 Job 代码（`MyJob` 和 `AddOneJob`）放在与 `Update` 和 `LateUpdate` 代码分开的文件中，但为了清晰起见，本示例将它们放在同一个文件中：

```csharp
using UnityEngine;
using Unity.Collections;
using Unity.Jobs;

public class MyDependentJob : MonoBehaviour
{
    // Create a native array of a single float to store the result. This example waits for the job to complete.
    NativeArray<float> result;
    // Create a JobHandle to access the results
    JobHandle secondHandle;

    // Set up the first job
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

    // Set up the second job, which adds one to a value
    public struct AddOneJob : IJob
    {
        public NativeArray<float> result;

        public void Execute()
        {
            result[0] = result[0] + 1;
        }
    }

    // Update is called once per frame
    void Update()
    {
        // Set up the job data for the first job
        result = new NativeArray<float>(1, Allocator.TempJob);

        MyJob jobData = new MyJob
        {
            a = 10,
            b = 10,
            result = result
        };

        // Schedule the first job
        JobHandle firstHandle = jobData.Schedule();

        // Setup the data for the second job
        AddOneJob incJobData = new AddOneJob
        {
            result = result
        };

        // Schedule the second job
        secondHandle = incJobData.Schedule(firstHandle);
    }

    private void LateUpdate()
    {
        // Sometime later in the frame, wait for the job to complete before accessing the results.
        secondHandle.Complete();

        // All copies of the NativeArray point to the same memory, you can access the result in "your" copy of the NativeArray
        // float aPlusBPlusOne = result[0];

        // Free the memory allocated by the result array
        result.Dispose();
    }

}
```

## 其他资源

- [[04-并行Jobs]]

---

## 文档导航

- 上一页：[[03-创建和运行Job]]
- 目录：[[00-Job System]]
- 下一页：[[04-并行Jobs]]
