> 原文：[Gizmos.DrawIcon](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawIcon.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawIcon

## Declaration

```csharp
public static void DrawIcon(Vector3 center,
    string name,
    bool allowScaling = true);

public static void DrawIcon(Vector3 center,
    string name,
    bool allowScaling = true,
    Color tint = Color(255,255,255,255));
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `center` | 图标在世界空间中的位置。 |
| `name` | 相对于 `Assets/Gizmos` 文件夹的图像文件名。 |
| `allowScaling` | 是否允许缩放图标。 |
| `tint` | 应用于图标的色调，可选。 |

## Description

在 Scene 视图中的指定位置绘制图标。

将图像文件放在 `Assets/Gizmos` 文件夹中。`DrawIcon` 可用于让游戏中的重要对象能够被快速选中。

```csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour
{
    void OnDrawGizmos()
    {
        // 在对象位置绘制灯泡图标。
        // 因为在 OnDrawGizmos 中绘制，所以图标也可以在 Scene 视图中被拾取。
        Gizmos.DrawIcon(transform.position, "Light Gizmo.tiff", true, Color.red);
    }
}
```

---

## 文档导航

- 上一页：[[08-DrawGUITexture]]
- 目录：[[00-Gizmos]]
- 下一页：[[10-DrawLine]]
