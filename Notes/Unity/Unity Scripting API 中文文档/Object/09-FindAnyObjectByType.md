> 原文：[Object.FindAnyObjectByType](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-FindAnyObjectByType.html)

# Object.FindAnyObjectByType

## 声明

```csharp
public static T FindAnyObjectByType<T>();
public static T FindAnyObjectByType<T>(FindObjectsInactive findObjectsInactive);
public static Object FindAnyObjectByType(Type type);
public static Object FindAnyObjectByType(Type type,
    FindObjectsInactive findObjectsInactive);
```

## 参数与返回值

`type` 是要查找的对象类型；`findObjectsInactive` 指定是否包含附加在非活动 `GameObject` 上的组件。返回匹配指定类型的任意已加载对象；找不到时返回 `null`。

## 描述

获取任意活动的已加载 `T` 类型对象。此方法不会返回资源（例如网格、纹理或预制件）、非活动对象，或设置了 `HideFlags.DontSave` 的对象。返回的对象不保证在多次调用间相同，但始终属于指定类型。如果不需要特定实例，此方法比 `Object.FindFirstObjectByType` 更快。

另请参阅：`Object.FindFirstObjectByType`、[[10-FindObjectsByType]]。

```csharp
using UnityEngine;

public class ExampleClass : MonoBehaviour
{
    void Start()
    {
        TextMesh textMesh = FindAnyObjectByType<TextMesh>();
        Debug.Log(textMesh ? "TextMesh object found: " + textMesh.name :
            "No TextMesh object could be found");

        CanvasRenderer canvas = FindAnyObjectByType<CanvasRenderer>();
        Debug.Log(canvas ? "CanvasRenderer object found: " + canvas.name :
            "No CanvasRenderer object could be found");
    }
}
```

---

## 文档导航

- 上一页：[[08-DontDestroyOnLoad]]
- 目录：[[00-Object]]
- 下一页：[[10-FindObjectsByType]]
