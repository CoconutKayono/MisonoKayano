> 原文：[Gizmos.DrawLineList](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawLineList.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawLineList

## Declaration

```csharp
public static void DrawLineList(ReadOnlySpan<Vector3> points);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `points` | 用作每条线起点和终点的点对。如果 `points` 包含奇数个元素，Unity 会抛出异常。 |

## Description

在多个点对之间绘制多条线。

与对每条线反复调用 `Gizmos.DrawLine` 相比，此函数提供了更高效的绘制多个线段的方式。

`points` span 中的每一对点表示一条线的起点和终点：Editor 从 `points[0]` 绘制到 `points[1]`，再从 `points[2]` 绘制到 `points[3]`，以此类推。span 必须包含偶数个点，否则会抛出异常。

此方法适合可视化场景中的连接、路径或边界。线使用当前的 Gizmo 颜色和矩阵绘制。通常应在 `MonoBehaviour.OnDrawGizmos`、`MonoBehaviour.OnDrawGizmosSelected` 或带有 `DrawGizmo` 属性的方法中调用。与所有 Gizmo 一样，它是仅限 Editor 的工具，不应当用于游戏功能；此方法在 Game 视图或运行时没有效果。

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
            new Vector3(-100, 100, 0),
            new Vector3(100, 100, 0)
        };
    }

    void OnDrawGizmosSelected()
    {
        // 绘制两条平行蓝线。
        Gizmos.color = Color.blue;
        Gizmos.DrawLineList(points);
    }
}
```

另请参阅：`Gizmos.DrawLine`、`Gizmos.DrawLineStrip`、`MonoBehaviour.OnDrawGizmos`、`MonoBehaviour.OnDrawGizmosSelected`、`DrawGizmo`、`Gizmos.color`、`Gizmos.matrix`。

---

## 文档导航

- 上一页：[[10-DrawLine]]
- 目录：[[00-Gizmos]]
- 下一页：[[12-DrawLineStrip]]
