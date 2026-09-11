> 原文：[Gizmos.DrawRay](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawRay.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawRay

## Declaration

```csharp
public static void DrawRay(Ray r);

public static void DrawRay(Vector3 from,
    Vector3 direction);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `from` | 射线在世界空间中的起点。 |
| `direction` | 在世界空间中定义射线方向和长度的向量，其大小决定绘制射线的长度。 |
| `r` | 包含要绘制的射线起点和方向的 `Ray` 结构。 |

## Description

在 Scene 视图中从指定位置开始，沿给定方向绘制射线。

`DrawRay` 是 Unity Editor 中用于可视化调试的方法，可在 Scene 视图中绘制线段，用于可视化射线检测、方向或场景中的向量。

线使用当前的 Gizmo 颜色和矩阵绘制。通常应在 `MonoBehaviour.OnDrawGizmos`、`MonoBehaviour.OnDrawGizmosSelected` 或带有 `DrawGizmo` 属性的方法中调用。与所有 Gizmo 一样，它是仅限 Editor 的工具，不应当用于游戏功能；此方法在 GameView 或运行时没有效果。如果要在运行时绘制类似形状，请参阅 `Debug.DrawLine`。

线段遵循 Scene 的三维空间和透视关系，包括深度以及被其他对象遮挡的情况，也遵循 Gizmo 颜色的 alpha 通道和 `Gizmos.matrix` 的变换。

```csharp
using UnityEngine;

public class RayGizmoExample : MonoBehaviour
{
    public Vector3 direction = Vector3.forward;
    public float length = 5f;
    [Range(0f, 1f)]
    public float alpha = 0.75f;

    private void OnDrawGizmos()
    {
        // 使用自定义 alpha 设置颜色。
        Gizmos.color = new Color(0f, 1f, 0f, alpha); // 带自定义 alpha 的绿色

        // 绘制射线。
        Gizmos.DrawRay(transform.position, direction.normalized * length);

        // 在射线末端绘制球体。
        Gizmos.DrawSphere(transform.position + direction.normalized * length, 0.1f);
    }
}
```

另请参阅：`MonoBehaviour.OnDrawGizmos`、`MonoBehaviour.OnDrawGizmosSelected`、`DrawGizmo`、`Gizmos.color`、`Gizmos.matrix`。

---

## 文档导航

- 上一页：[[13-DrawMesh]]
- 目录：[[00-Gizmos]]
- 下一页：[[15-DrawSphere]]
