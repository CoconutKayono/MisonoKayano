> 原文：[Object.DestroyImmediate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.DestroyImmediate.html)

# Object.DestroyImmediate

```csharp
public static void DestroyImmediate(Object obj,
    bool allowDestroyingAssets = false);
```

## 参数

| 参数 | 说明 |
| --- | --- |
| `obj` | 要销毁的对象。 |
| `allowDestroyingAssets` | 设置为 `true` 时允许销毁资源。 |

## 描述

立即销毁指定对象。应谨慎使用，并且只在编辑模式中使用。`DestroyImmediate` 主要用于编辑模式脚本；运行时应使用 `Object.Destroy`，它会在当前帧结束时销毁对象，更安全。若只是想停用 `GameObject`，请使用 `GameObject.SetActive`。

在物理触发器/接触事件、动画事件回调、渲染回调或 `MonoBehaviour.OnValidate` 中调用此方法会报错。

将 `allowDestroyingAssets` 设为 `true` 会永久移除资源文件中的对象，且不可撤销，但不会删除磁盘上的资源文件。要从磁盘删除资源文件，应使用 `AssetDatabase.DeleteAsset`。遍历数组或列表时从集合中销毁对象也可能跳过元素或导致越界。

```csharp
using UnityEngine;
using UnityEditor;

public class DestroyImmediateExample
{
    [MenuItem("Tools/Destroy Selected GameObjects Immediately")]
    static void DestroySelectedGameObjects()
    {
        var selected = Selection.gameObjects;
        if (selected.Length == 0)
        {
            Debug.LogWarning("No GameObjects selected!");
            return;
        }

        foreach (var go in selected)
            Object.DestroyImmediate(go);

        Debug.Log($"{selected.Length} GameObjects destroyed immediately.");
    }
}
```

---

## 文档导航

- 上一页：[[06-Destroy]]
- 目录：[[00-Object]]
- 下一页：[[08-DontDestroyOnLoad]]
