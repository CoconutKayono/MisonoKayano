> 原文：[Gizmos.DrawSphere](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawSphere.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawSphere

## Declaration

```csharp
public static void DrawSphere(Vector3 center,
    float radius);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `center` | 要在世界空间中绘制的球体位置。 |
| `radius` | 要绘制的球体半径，使用世界空间单位。 |

## Description

在 Scene 视图中以指定中心和半径绘制实心球体。

`DrawSphere` 是 Unity Editor 中用于可视化调试的方法，可在 Scene 视图中渲染 icosphere，用于可视化碰撞区域、效果范围或场景中的重要位置。

球体使用当前的 Gizmo 颜色和矩阵绘制。通常应在 `MonoBehaviour.OnDrawGizmos`、`MonoBehaviour.OnDrawGizmosSelected` 或带有 `DrawGizmo` 属性的方法中调用。与所有 Gizmo 一样，它是仅限 Editor 的工具，不应当用于游戏功能；此方法在 GameView 或运行时没有效果。如果要在运行时绘制类似形状，请参阅 `Debug.DrawLine`。

球体遵循 Scene 的三维空间和透视关系，包括深度以及被其他对象遮挡的情况，也遵循 Gizmo 颜色的 alpha 通道和 `Gizmos.matrix` 的变换。

```csharp
using UnityEngine;

public class SphereGizmoExample : MonoBehaviour
{
    public float radius = 1f;
    [Range(0f, 1f)]
    public float alpha = 0.5f;

    private void OnDrawGizmos()
    {
        Gizmos.color = new Color(1f, 0f, 0f, alpha); // 带自定义 alpha 的红色
        Gizmos.DrawSphere(transform.position, radius);

        // 绘制线框球体轮廓。
        Gizmos.color = Color.white;
        Gizmos.DrawWireSphere(transform.position, radius);
    }
}
```

另请参阅：`MonoBehaviour.OnDrawGizmos`、`MonoBehaviour.OnDrawGizmosSelected`、`DrawGizmo`、`Gizmos.color`、`Gizmos.matrix`。

---

## 文档导航

- 上一页：[[14-DrawRay]]
- 目录：[[00-Gizmos]]
- 下一页：[[16-DrawWireCube]]
