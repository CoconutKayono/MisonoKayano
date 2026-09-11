> 原文：[Gizmos.DrawLine](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawLine.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawLine

## Declaration

```csharp
public static void DrawLine(Vector3 from,
    Vector3 to);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `from` | 要绘制的线在世界空间中的起点。 |
| `to` | 要绘制的线在世界空间中的终点。 |

## Description

在 Scene 视图中绘制连接两个点的线。

`DrawLine` 是 Unity Editor 中用于可视化调试的方法，可以在 Scene 视图中绘制线段，用于可视化连接、路径或边界。

线使用当前的 Gizmo 颜色绘制，可在调用 `DrawLine` 前通过 `Gizmos.color` 设置；也使用当前的 Gizmo 矩阵绘制，可通过 `Gizmos.matrix` 设置。

通常应在 `MonoBehaviour` 脚本的 `MonoBehaviour.OnDrawGizmos` 或 `MonoBehaviour.OnDrawGizmosSelected` 函数中，或带有 `DrawGizmo` 属性的方法中调用此方法。与所有 Gizmo 一样，它是仅限 Editor 的工具，不应当用于游戏功能。此方法在 Game 视图或运行时没有效果；如果要在运行时绘制类似形状，请参阅 `Debug.DrawLine`。

线段遵循 Scene 的三维空间和透视关系，包括深度以及被其他对象遮挡的情况。它也遵循 Gizmo 颜色的 alpha 通道，因此可以绘制半透明线段，并遵循 `Gizmos.matrix` 的变换。

如果需要绘制大量线段，请考虑使用 `Gizmos.DrawLineList` 或 `Gizmos.DrawLineStrip`，它们比重复调用此方法逐条绘制更快。

```csharp
using UnityEngine;

public class LineGizmoExample : MonoBehaviour
{
    public Transform endPoint;
    [Range(0f, 1f)]
    public float alpha = 0.75f;

    private void OnDrawGizmos()
    {
        if (endPoint == null) return;

        Gizmos.color = new Color(1f, 1f, 0f, alpha); // 带自定义 alpha 的黄色
        Gizmos.DrawLine(transform.position, endPoint.position);

        Gizmos.DrawSphere(transform.position, 0.1f);
        Gizmos.DrawSphere(endPoint.position, 0.1f);

        Vector3 midpoint = (transform.position + endPoint.position) / 2f;
        Gizmos.color = Color.red;
        Gizmos.DrawSphere(midpoint, 0.15f);

        float distance = Vector3.Distance(transform.position, endPoint.position);
        UnityEditor.Handles.Label(midpoint, $"Distance: {distance:F2}");
    }
}
```

另请参阅：`Gizmos.DrawLineList`、`Gizmos.DrawLineStrip`、`MonoBehaviour.OnDrawGizmos`、`MonoBehaviour.OnDrawGizmosSelected`、`DrawGizmo`、`Gizmos.color`、`Gizmos.matrix`。

---

## 文档导航

- 上一页：[[09-DrawIcon]]
- 目录：[[00-Gizmos]]
- 下一页：[[11-DrawLineList]]
