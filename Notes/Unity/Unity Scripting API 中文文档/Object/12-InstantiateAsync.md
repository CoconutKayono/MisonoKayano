> 原文：[Object.InstantiateAsync](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.InstantiateAsync.html)

# Object.InstantiateAsync

## 常用声明

```csharp
public static AsyncInstantiateOperation<T> InstantiateAsync<T>(T original);
public static AsyncInstantiateOperation<T> InstantiateAsync<T>(T original,
    Transform parent);
public static AsyncInstantiateOperation<T> InstantiateAsync<T>(T original,
    Transform parent, Vector3 position, Quaternion rotation);
public static AsyncInstantiateOperation<T> InstantiateAsync<T>(T original,
    Vector3 position, Quaternion rotation);
public static AsyncInstantiateOperation<T> InstantiateAsync<T>(T original,
    InstantiateParameters parameters, CancellationToken cancellationToken);
public static AsyncInstantiateOperation<T> InstantiateAsync<T>(T original,
    int count);
public static AsyncInstantiateOperation<T> InstantiateAsync<T>(T original,
    int count, Transform parent, Vector3 position, Quaternion rotation);
public static AsyncInstantiateOperation<T> InstantiateAsync<T>(T original,
    int count, Vector3 position, Quaternion rotation);
public static AsyncInstantiateOperation<T> InstantiateAsync<T>(T original,
    int count, ReadOnlySpan<Vector3> positions,
    ReadOnlySpan<Quaternion> rotations);
```

页面还提供组合 `count`、`parent`、每个实例的位置/旋转、`InstantiateParameters` 和 `CancellationToken` 的重载。

## 参数与返回值

`original` 是要复制的对象；`count` 是要创建的副本数量；`parent` 是父级；`position` 与 `rotation` 是位置和旋转；`positions` 与 `rotations` 允许为每个副本指定变换；`parameters` 指定父级、场景和世界/本地空间选项；`cancellationToken` 可在操作完成前取消它。返回包含生成对象的 `AsyncInstantiateOperation<T>`。

## 描述

捕获与另一个 `GameObject` 相关的原对象快照，并获取包含结果对象的 `AsyncInstantiateOperation`。操作主要异步执行，但最后的集成和 `Awake` 调用阶段在主线程上完成。可以取消操作，也可以通过 `allowSceneActivation` 延迟集成阶段。

可以对操作使用 `yield return`，或调用其 `WaitForCompletion()` 方法以同步完成。使用 `InstantiateParameters` 重载可以选择本地空间或世界空间，并指定对象要加入的目标场景。批量创建时，`positions` 或 `rotations` 的长度可以小于 `count`，Unity 会使用 `positions[i % positions.Length]` 或 `rotations[i % rotations.Length]`。

```csharp
using UnityEngine;

public class AsyncInstantiateExample : MonoBehaviour
{
    public GameObject prefab;

    async void Start()
    {
        AsyncInstantiateOperation<GameObject> operation =
            Object.InstantiateAsync(prefab, transform);
        await operation;

        GameObject[] instances = operation.Result;
        Debug.Log($"Created {instances.Length} instance(s).");
    }
}
```

---

## 文档导航

- 上一页：[[11-Instantiate]]
- 目录：[[00-Object]]
- 下一页：[[13-bool]]
