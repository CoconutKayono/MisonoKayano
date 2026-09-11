> 原文：[Object.FindObjectsByType](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-FindObjectsByType.html)

# Object.FindObjectsByType

## 声明

```csharp
public static T[] FindObjectsByType<T>();
public static T[] FindObjectsByType<T>(FindObjectsInactive findObjectsInactive);
public static T[] FindObjectsByType<T>(FindObjectsInactive findObjectsInactive,
    FindObjectsSortMode sortMode);
public static Object[] FindObjectsByType(Type type);
public static Object[] FindObjectsByType(Type type,
    FindObjectsInactive findObjectsInactive);
public static Object[] FindObjectsByType(Type type,
    FindObjectsInactive findObjectsInactive, FindObjectsSortMode sortMode);
```

## 参数与返回值

`type` 是要查找的类型；`findObjectsInactive` 指定是否包含非活动 `GameObject` 上的组件；`sortMode` 指定返回数组的排序方式。返回匹配指定类型的对象数组；没有匹配项时返回空数组。

## 描述

获取指定类型的所有已加载对象。默认只返回活动对象，不返回资源（例如网格、纹理或预制件），也不返回设置了 `HideFlags.DontSave` 的对象。调用不带排序参数的重载时，Unity 不保证返回对象的顺序；如果不需要排序，使用该重载可以获得更好的性能。

带 `FindObjectsSortMode` 的旧重载已弃用，因为未来 `InstanceID` 将由 `EntityId` 替代，旧排序顺序无法保持。请改用不带 `sortMode` 的重载，或显式使用当前的排序需求。

```csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        // 查找场景中所有活动的 Rigidbody。
        Rigidbody[] bodies = Object.FindObjectsByType<Rigidbody>();
        foreach (Rigidbody body in bodies)
            Debug.Log(body.name);

        // 包含非活动对象。
        Rigidbody[] allBodies = Object.FindObjectsByType<Rigidbody>(
            FindObjectsInactive.Include);
    }
}
```

---

## 文档导航

- 上一页：[[09-FindAnyObjectByType]]
- 目录：[[00-Object]]
- 下一页：[[11-Instantiate]]
