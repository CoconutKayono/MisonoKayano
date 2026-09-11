# 在 Burst 中使用 TransformHandle

> 原文：[Using TransformHandle with Burst](https://docs.unity3d.com/6000.7/Documentation/Manual/transformhandle-burst.html)

`TransformHandle` API 与在主线程上运行的代码中的 [Burst](https://docs.unity3d.com/Packages/com.unity.burst@latest) 编译器兼容。这使你可以避免来回复制数据；当在 Burst 编译代码中使用托管的 `Transform` 组件时，通常需要进行这种复制。

本页通过示例展示了与 `Transform` API 相比，`TransformHandle` 如何简化 Burst 工作流。

## 在 Burst 中使用 TransformHandle 的优势

使用 Burst 编译代码时，`TransformHandle` 提供以下优势：

- **直接访问**：直接在 Burst 编译的方法中读写 Transform 的位置、旋转和其他属性。
- **兼容 NativeArray**：可以直接将 `TransformHandle` 实例存储在 `NativeArray` 和其他原生集合中。避免来回复制数据到 `NativeArray` 缓冲区的开销；使用 `Transform` API 时必须进行这种复制。示例请参阅[使用 TransformHandle API 与 Transform API 对比的示例实现](#examples)。
- **更简单的代码结构**：在单个主线程 Burst 编译过程中执行所有操作，而不是将逻辑拆分为独立的 Burst 兼容阶段和非 Burst 阶段。

## TransformHandle 与 Job System

`TransformHandle` struct 兼容 Burst，但不能安全地从 Worker Thread 访问。在实现了 `IJob`、`IJobParallelFor` 或 `IJobParallelForTransform` 的 Job 中读取或写入 `TransformHandle` 属性，或调用其方法，会抛出安全异常。本页的示例使用标记了 `[BurstCompile]` 属性的静态方法，这些方法在主线程上运行。

要跨 Worker Thread 并行读取和写入 Transform 值，请将 [`TransformAccessArray`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Jobs.TransformAccessArray.html) struct 与实现 [`IJobParallelForTransform`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Jobs.IJobParallelForTransform.html) 接口的 Job 配合使用。可以在调度 Job 之前，从 `NativeArray<TransformHandle>` 集合构造 `TransformAccessArray` 实例：

```csharp
NativeArray<TransformHandle> handles = ...;
TransformAccessArray accessArray = new TransformAccessArray(handles);
```

这种模式会将一个 `TransformAccess` struct 作为参数传递给 Job 的 `Execute` 方法。该 struct 只公开 Transform 值，不公开父句柄或子句柄，也不会使 `TransformHandle` 的方法（例如 `SetParent`）可以从 Job 中调用。

## 使用 TransformHandle API 与 Transform API 对比的示例实现

下面的示例展示了在使用 Burst 编译时，`TransformHandle` 与 `Transform` API 的差异。两个示例都会在每帧将 1000 个游戏对象向随机选择的目标移动。

### 使用 TransformHandle API 与 Burst 的实现

`TransformHandle` API 不需要中间缓冲区和独立的复制阶段。所有位置读取和写入都直接发生在 Burst 编译代码中，因此代码更简单，也更易维护。可以在单个 Burst 编译方法中执行所有必要操作。

```csharp
using Unity.Burst;
using Unity.Collections;
using Unity.Mathematics;
using UnityEngine;

public class TransformHandleMoveExample : MonoBehaviour
{
    public int SpawnCount = 1000;
    // TransformHandle can be stored in NativeArray and accessed from Burst-compiled code
    NativeArray<TransformHandle> SpawnedTransforms;
    public Unity.Mathematics.Random Random;

    void Start()
    {
        Random = Unity.Mathematics.Random.CreateFromIndex(0);

        // Allocate native array of handles (no separate float3 buffer needed)
        SpawnedTransforms = new NativeArray<TransformHandle>(SpawnCount, Allocator.Persistent);

        // Create transforms and assign random start positions
        for (int i = 0; i < SpawnedTransforms.Length; i++)
        {
            TransformHandle transformHandle = new GameObject($"Transform{i}").transformHandle;
            SpawnedTransforms[i] = transformHandle;
            transformHandle.position = Random.NextFloat3(new float3(-100f), new float3(100f));
        }
    }

    void OnDestroy()
    {
        if (SpawnedTransforms.IsCreated)
        {
            SpawnedTransforms.Dispose();
        }
    }

    void Update()
    {
        // Single Burst-compiled call: reads positions, computes movement, and writes new positions. No manual copying needed.
        TransformHandleMoveExampleUtils.ComputeAndApplyRandomMovements(ref SpawnedTransforms, ref Random, 1f * Time.deltaTime);
    }
}


[BurstCompile]
public static class TransformHandleMoveExampleUtils
{
    [BurstCompile]
    public static void ComputeAndApplyRandomMovements(ref NativeArray<TransformHandle> transforms,
        ref Unity.Mathematics.Random random, float movementMagnitude)
    {
        for (int i = 0; i < transforms.Length; i++)
        {
            // TransformHandle positions can be read and written directly in Burst-compiled code
            TransformHandle transformHandle = transforms[i];
            float3 movement = math.normalizesafe(transforms[random.NextInt(0, transforms.Length)]
                .position - transformHandle.position) * movementMagnitude;
            transformHandle.position = transformHandle.position + (Vector3)movement;
        }
    }
}
```

### 使用 Transform API 与 Burst 的实现

使用 `Transform` API 时，必须将操作拆分为三个阶段：

1. 将 Transform 组件的位置复制到 `NativeArray` 中（非 Burst 代码）。
2. 对复制的数据执行计算（Burst 编译代码）。
3. 将结果复制回 Transform 组件（非 Burst 代码）。

这种方式要求维护一个独立的 `NativeArray<float3>` 缓冲区，并且每帧执行两次复制操作，这会增加开销和代码复杂度。

```csharp
using Unity.Burst;
using Unity.Collections;
using Unity.Mathematics;
using UnityEngine;

public class TransformMoveExample : MonoBehaviour
{
    public int SpawnCount = 1000;
    // Transform API cannot be accessed from Burst-compiled code
    public Transform[] SpawnedTransforms;
    // Separate data buffer required to connect Transform and Burst
    NativeArray<float3> Positions;
    public Unity.Mathematics.Random Random;

    void Start()
    {
        Random = Unity.Mathematics.Random.CreateFromIndex(0);

        // Initialize managed Transform array and native float3 array
        // (extra overhead compared to TransformHandle)
        SpawnedTransforms = new Transform[SpawnCount];
        Positions = new NativeArray<float3>(SpawnCount, Allocator.Persistent);

        // Create transforms and assign random start positions
        for (int i = 0; i < SpawnedTransforms.Length; i++)
        {
            SpawnedTransforms[i] = new GameObject($"Transform{i}").transform;
            SpawnedTransforms[i].position = Random.NextFloat3(new float3(-100f), new float3(100f));
        }
    }

    void OnDestroy()
    {
        if (Positions.IsCreated)
        {
            Positions.Dispose();
        }
    }

    void Update()
    {
        // 1) Copy Transform positions into NativeArray (Transform cannot be accessed in Burst).
        for (int i = 0; i < SpawnedTransforms.Length; i++)
        {
            Positions[i] = SpawnedTransforms[i].position;
        }

        // 2) Burst-compiled compute on the copied data.
        TransformMoveExampleUtils.ComputeRandomMovements(ref Positions, ref Random, 1f * Time.deltaTime);

        // 3) Copy results back to each Transform to update scene state.
        for (int i = 0; i < SpawnedTransforms.Length; i++)
        {
            SpawnedTransforms[i].position = Positions[i];
        }
    }
}

[BurstCompile]
public static class TransformMoveExampleUtils
{
    [BurstCompile]
    public static void ComputeRandomMovements(ref NativeArray<float3> positions, ref Unity.Mathematics.Random random, float movementMagnitude)
    {
        for (int i = 0; i < positions.Length; i++)
        {
            // Calculate movement from copied position data
            float3 movement = math.normalizesafe(positions[random.NextInt(0, positions.Length)] - positions[i]) * movementMagnitude;
            // Updated positions will be copied back to Transforms
            positions[i] += movement;
        }
    }
}
```

## 其他资源

- [[04-TransformHandle类参考]]
- [[02-TransformHandle API代码示例]]
- [Burst 编译器文档](https://docs.unity3d.com/Packages/com.unity.burst@latest)

---

## 文档导航

- 上一页：[[02-TransformHandle API代码示例]]
- 目录：[[00-使用非托管API执行Transform操作]]
- 下一页：[[00-测试代码]]
