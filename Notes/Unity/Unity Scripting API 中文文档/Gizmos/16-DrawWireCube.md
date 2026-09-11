> 原文：[Gizmos.DrawWireCube](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawWireCube.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawWireCube

## Declaration

```csharp
public static void DrawWireCube(Vector3 center,
    Vector3 size);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `center` | 要绘制的立方体中心点。 |
| `size` | 要绘制的立方体大小，决定立方体沿各轴的尺寸。 |

## Description

在 Scene 视图中以 `center` 为中心、以 `size` 为大小绘制线框盒，用于可视化和调试。

`DrawWireCube` 是 Unity Editor 中用于可视化调试的方法，会在 Scene 视图中渲染线框立方体，适合可视化边界框、触发区域或对象之间的空间关系。

立方体使用当前的 Gizmo 颜色和矩阵绘制。通常应在 `MonoBehaviour.OnDrawGizmos`、`MonoBehaviour.OnDrawGizmosSelected` 或带有 `DrawGizmo` 属性的方法中调用。与所有 Gizmo 一样，它是仅限 Editor 的工具，不应当用于游戏功能；此方法在 GameView 或运行时没有效果。如果要在运行时绘制类似形状，请参阅 `Debug.DrawLine`。

立方体遵循 Scene 的三维空间和透视关系，包括深度以及被其他对象遮挡的情况，也遵循 Gizmo 颜色的 alpha 通道和 `Gizmos.matrix` 的变换。

```csharp
using UnityEngine;

public class CubeGizmoExample : MonoBehaviour
{
    public Vector3 size = Vector3.one;
    [Range(0f, 1f)]
    public float alpha = 0.5f;

    private void OnDrawGizmos()
    {
        Gizmos.color = new Color(0f, 1f, 0f, alpha); // 带自定义 alpha 的绿色
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

- 上一页：[[15-DrawSphere]]
- 目录：[[00-Gizmos]]
- 下一页：[[17-DrawWireMesh]]
