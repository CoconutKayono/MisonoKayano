> 原文：[Gizmos.DrawCube](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawCube.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawCube

## Declaration

```csharp
public static void DrawCube(Vector3 center,
    Vector3 size);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `center` | 要绘制的立方体中心点。 |
| `size` | 要绘制的立方体大小，决定立方体沿各轴的尺寸。 |

## Description

在 Scene 视图中以 `center` 为中心、以 `size` 为大小绘制实心盒，用于可视化和调试。

`DrawCube` 是 Unity Editor 中用于可视化调试的方法，可在 Scene 视图中渲染纯色立方体。它适合可视化边界框、触发区域或对象之间的空间关系。

立方体使用当前的 Gizmo 颜色绘制；可以在调用 `DrawCube` 前使用 `Gizmos.color` 设置颜色。立方体还使用当前的 Gizmo 矩阵绘制；可以在调用 `DrawCube` 前使用 `Gizmos.matrix` 设置矩阵。

通常应在 `MonoBehaviour` 脚本的 `MonoBehaviour.OnDrawGizmos` 或 `MonoBehaviour.OnDrawGizmosSelected` 函数中，或带有 `DrawGizmo` 属性的方法中调用此方法。与所有 Gizmo 一样，它是仅限 Editor 的工具，不应当用于游戏功能。此方法在 GameView 或运行时没有效果；如果要在运行时绘制类似形状，请参阅 `Debug.DrawLine`。

立方体遵循 Scene 的三维空间和透视关系，包括深度以及被其他对象遮挡的情况。它也遵循 Gizmo 颜色的 alpha 通道，因此可以绘制半透明立方体，并遵循 `Gizmos.matrix` 的变换。

```csharp
using UnityEngine;

public class CubeGizmoExample : MonoBehaviour
{
    public Vector3 size = Vector3.one;
    [Range(0f, 1f)]
    public float alpha = 0.5f;

    private void OnDrawGizmos()
    {
        // 使用自定义 alpha 设置颜色。
        Gizmos.color = new Color(0f, 1f, 0f, alpha); // 带自定义 alpha 的绿色

        // 绘制立方体。
        Gizmos.DrawCube(transform.position, size);

        // 绘制线框立方体轮廓。
        Gizmos.color = Color.white;
        Gizmos.DrawWireCube(transform.position, size);
    }
}
```

另请参阅：`MonoBehaviour.OnDrawGizmos`、`MonoBehaviour.OnDrawGizmosSelected`、`DrawGizmo`、`Gizmos.color`、`Gizmos.matrix`。

---

## 文档导航

- 上一页：[[05-CalculateLOD]]
- 目录：[[00-Gizmos]]
- 下一页：[[07-DrawFrustum]]
