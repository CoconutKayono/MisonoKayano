> 原文：[ScriptableObject.CreateInstance](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.CreateInstance.html)

# [ScriptableObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html).CreateInstance

## 声明

```csharp
public static ScriptableObject CreateInstance(string className);
public static ScriptableObject CreateInstance(Type type);
public static T CreateInstance<T>() where T : ScriptableObject;
```

## 参数

| 参数 | 中文说明 |
| --- | --- |
| `className` | 要创建的 `ScriptableObject` 类型名称。 |
| `type` | 要创建的 `ScriptableObject` 类型，以 `System.Type` 实例表示。 |

## 返回值

创建的 `ScriptableObject`；泛型重载返回创建的 `T`。

## 描述

创建 `ScriptableObject` 的实例。

如果希望通过 Editor 用户界面轻松创建绑定到 `.asset` 文件的 `ScriptableObject` 实例，可以考虑使用 [`CreateAssetMenuAttribute`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/CreateAssetMenuAttribute.html)。

## 示例

```csharp
using UnityEngine;

public class MyData : ScriptableObject
{
    public int value;
}

public class CreateInstance : MonoBehaviour
{
    void Start()
    {
        ScriptableObject nonGenericInstance = ScriptableObject.CreateInstance(typeof(MyData));
        ((MyData)nonGenericInstance).value = 20;
        Debug.Log("Non-generic instance value: " + ((MyData)nonGenericInstance).value);
    }
}
```

```csharp
using UnityEngine;

public class MyData : ScriptableObject
{
    public int value;
}

public class CreateInstanceGeneric : MonoBehaviour
{
    void Start()
    {
        MyData genericInstance = ScriptableObject.CreateInstance<MyData>();
        genericInstance.value = 10;
        Debug.Log("Generic instance value: " + genericInstance.value);
    }
}
```

---

## 文档导航

- 上一页：[[00-ScriptableObject]]
- 目录：[[00-ScriptableObject]]
- 下一页：[[02-Awake]]
