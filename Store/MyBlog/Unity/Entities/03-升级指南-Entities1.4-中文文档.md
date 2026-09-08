# 升级指南：升级到 Entities 1.4（Upgrading to Entities 1.4）

> 来源：[Unity Package 官方文档 · Upgrade guide](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/upgrade-guide.html)

Entities 1.4 有一些更改可能会给项目带来警告。要修复这些警告，请执行以下操作：

- 更改 Entities.ForEach 代码
- 更改 Aspects 代码
- 更改 EntityCommandBuffer PlaybackPolicy 代码
- 将 PostLoadCommandBuffer 迁移到 RequestSceneLoaded.ImportEntity
- 如果你的项目使用基于 InstanceID 的 API，请参阅 EntityId API 迁移指南。

## 更改 Entities.ForEach 代码

为了整合 Entities API 并缩短迭代时间，`Entities.ForEach` 在 Entities 1.4 中已弃用，你应该改用 `IJobEntity` 或 `SystemAPI.Query`。

### IJobEntity

由于 `IJobEntity` 的 `Execute` 方法支持用 `ref` 和 `in` 参数表示只读/读写状态，你通常可以将 `Entities.ForEach` 的 lambda 直接复制到 `IJobEntity` 作业结构体的 `Execute` 方法中。此外，`IJobEntity` 支持 `Entities.ForEach` 支持的所有调度选项。

> **注意**：`IJobEntity` 默认不进行 Burst 编译，而且由于没有 lambda 主体，它无法捕获变量。请使用 `[BurstCompile]` 属性启用 Burst 编译，并将要捕获的变量写入作业结构体的字段中。

使用 Entities.ForEach 的代码示例：

```csharp
public partial class RotationSpeedSystemForEachISystem : SystemBase
{
    protected override void OnUpdate()
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        Entities
            .ForEach((ref LocalTransform transform, in RotationSpeed rotationSpeed) =>
            {
                transform.Rotation = math.mul(
                    math.normalize(transform.Rotation),
                    quaternion.AxisAngle(math.up(), rotationSpeed.RadiansPerSecond * deltaTime));
            })
            .ScheduleParallel();
    }
}
```

使用 IJobEntity 的代码示例：

```csharp
[BurstCompile]
public partial struct ASampleJob : IJobEntity
{
    public float DeltaTime;
    void Execute(ref LocalTransform transform, in RotationSpeed rotationSpeed)
    {
        transform.Rotation = math.mul(
            math.normalize(transform.Rotation),
            quaternion.AxisAngle(math.up(), rotationSpeed.RadiansPerSecond * DeltaTime));
    }
}

public partial class ASample : SystemBase
{
    protected override void OnUpdate()
    {
        var deltaTime = SystemAPI.Time.DeltaTime;
        new ASampleJob{ DeltaTime = deltaTime }.ScheduleParallel();
    }
}
```

有关 `IJobEntity` 的更多信息，请参阅「使用 IJobEntity 迭代组件数据」（Iterate over component data with IJobEntity）。

### SystemAPI.Query

对于不必在作业中执行（但仍可进行 Burst 编译）的实体迭代，`SystemAPI.Query` 可以提供更简单的选择，因为它使用 `RefRO` 和 `RefRW` 类型来包装分别以只读和读写方式访问的类型参数。Query 上还有其他构建器方法，用于指示 `WithAll`、`WithNone`、`WithAny` 等选项。

以下将之前的 Entities.ForEach 示例改为使用 SystemAPI.Query：

```csharp
public partial class ASample : SystemBase
{
    protected override void OnUpdate()
    {
        var deltaTime = SystemAPI.Time.DeltaTime;
        foreach (var (transform, rotationSpeed) in 
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<RotationSpeed>>())
        {
            transform.ValueRW.Rotation = math.mul(
                math.normalize(transform.ValueRO.Rotation),
                quaternion.AxisAngle(math.up(), rotationSpeed.ValueRO.RadiansPerSecond * deltaTime));
        }
    }
}
```

有关 `SystemAPI.Query` 的更多信息，请参阅「使用 SystemAPI.Query 迭代组件数据」（Iterate over component data with SystemAPI.Query）。

## 更改 Aspects 代码

Aspects 从 Entities 1.4 起弃用，并且没有直接的替代品。你必须用显式代码替换该抽象：查询正确的组件集合，并对它们执行预期操作。以下代码提供了一个简单示例，说明如何将 aspect 及其用法转换为显式 `EntityQuery` 和一个用于执行操作的辅助方法。

使用 Aspects 的代码示例：

```csharp
public partial struct RotationSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        var deltaTime = SystemAPI.Time.DeltaTime;
        var elapsedTime = SystemAPI.Time.ElapsedTime;

        foreach (var movement in SystemAPI.Query<VerticalMovementAspect>())
        {
            movement.Move(elapsedTime);
        }
    }
}

readonly partial struct VerticalMovementAspect : IAspect
{
    readonly RefRW<LocalTransform> m_Transform;
    readonly RefRO<RotationSpeed> m_Speed;

    public void Move(double elapsedTime)
    {
        m_Transform.ValueRW.Position.y = (float)math.sin(elapsedTime * m_Speed.ValueRO.RadiansPerSecond);
    }
}
```

使用 EntityQuery 的代码示例：

```csharp
public partial struct RotationSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        var elapsedTime = SystemAPI.Time.ElapsedTime;

        foreach (var (transform, speed) in SystemAPI.Query<RefRW<LocalTransform>, RefRO<RotationSpeed>>())
        {
            VerticalMovementHelper.Move(elapsedTime, transform, speed);
        }
    }
}

static class VerticalMovementHelper
{
    public static void Move(double elapsedTime, RefRW<LocalTransform> transform, RefRO<RotationSpeed> speed)
    {
        transform.ValueRW.Position.y = (float)math.sin(elapsedTime * speed.ValueRO.RadiansPerSecond);
    }
}
```

## 更改 EntityCommandBuffer PlaybackPolicy 代码

`PlaybackPolicy` 枚举整体弃用，将在未来版本中移除。这包括 `PlaybackPolicy.SinglePlayback` 和 `PlaybackPolicy.MultiPlayback`，以及任何接受 `PlaybackPolicy` 参数的 `EntityCommandBuffer` 构造函数重载。

今后，`SinglePlayback` 是唯一受支持的行为，也是默认行为：一个 `EntityCommandBuffer` 只能播放（playback）一次。创建 `EntityCommandBuffer` 时不要指定 `PlaybackPolicy`。如果你需要多次应用同一组命令，请为每次播放将命令重新记录到新的 `EntityCommandBuffer` 中。

## 将 PostLoadCommandBuffer 迁移到 RequestSceneLoaded.ImportEntity

托管类型的 `PostLoadCommandBuffer` IComponentData 已弃用，将在未来版本中移除。请将其替换为 `RequestSceneLoaded.ImportEntity`，它会在 `ProcessAfterLoadGroup` 运行之前，将常规主世界实体（及其所有组件）传送到分段的流式世界（streaming world）中。

要迁移：

1. 在主世界中的常规实体上构建每个实例的数据，直接添加你之前记录到 `EntityCommandBuffer` 中的组件。
2. 将该实体作为 `ImportEntity` 传递给 `SceneSystem.LoadParameters`，用于 `SceneSystem.LoadSceneAsync`（或在场景/分段元实体上写入 `RequestSceneLoaded { ImportEntity = dataEntity }`）。
3. 你现有的 `ProcessAfterLoad` 系统像以前一样精确查询导入的组件；载体实体（carrier entity）会出现在流式世界中。如果你不希望它在加载后继续存在于主世界中，请在该系统内销毁它。
4. 你拥有主世界中的源实体：请保持它存活直到加载完成，并在不再需要时自行销毁。

## 将托管组件转换为非托管组件

托管组件（IComponentData）和托管共享组件（ISharedComponentData）已弃用，将在未来版本中移除。如果组件或共享组件是类，或是包含托管（引用类型）字段（如 `string` 或其他类）的结构体，则该组件属于托管组件。请将这些转换为非托管组件：使用只包含非托管字段的结构体，并使用 `UnityObjectRef<T>` 引用 UnityEngine.Object 实例。更多信息，请参阅「在代码中引用 Unity 对象」（Reference Unity objects in your code）。
