> 原文：[Gizmos.DrawLineStrip](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawLineStrip.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawLineStrip

## Declaration

```csharp
public static void DrawLineStrip(ReadOnlySpan<Vector3> points,
    bool looped);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `points` | 定义要绘制的线序列的点。函数在每个点与其后一个点之间绘制线。 |
| `looped` | 是否在最后一个点和第一个点之间额外绘制一条线。为 `true` 时，Unity 在 `points[points.Length - 1]` 和 `points[0]` 之间绘制额外的线；为 `false` 时，线在最后一个点处结束。 |

## Description

在给定 span 中的每个点之间绘制线。

与对每条线反复调用 `Gizmos.DrawLine` 相比，此函数提供了更高效的绘制多个线段的方式。

Unity 从 `points[0]` 绘制到 `points[1]`，再从 `points[1]` 绘制到 `points[2]`，以此类推。

```csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour
{
    Vector3[] points;

    void Start()
    {
        points = new Vector3[4]
        {
            new Vector3(-100, 0, 0),
            new Vector3(100, 0, 0),
            new Vector3(100, 100, 0),
            new Vector3(-100, 100, 0)
        };
    }

    void OnDrawGizmosSelected()
    {
        // 绘制四条线组成正方形。
        Gizmos.color = Color.blue;
        Gizmos.DrawLineStrip(points, true);
    }
}
```

另请参阅：`Gizmos.DrawLine`、`Gizmos.DrawLineList`。

---

## 文档导航

- 上一页：[[11-DrawLineList]]
- 目录：[[00-Gizmos]]
- 下一页：[[13-DrawMesh]]
