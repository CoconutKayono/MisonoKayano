> 原文：[Gizmos.matrix](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos-matrix.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).matrix

```csharp
public static Matrix4x4 matrix;
```

## Description

设置 Unity Editor 用于绘制 Gizmo 的 `Matrix4x4`。

`Gizmos.matrix` 保存 Gizmo 的位置、旋转和缩放。默认情况下，Gizmos 始终使用世界坐标；默认的 `Gizmos.matrix` 使用单位矩阵变换世界坐标。`Transform.localToWorldMatrix` 可以将局部坐标空间转换为世界坐标空间。

`GameObject` 通常使用局部坐标。`Gizmos.matrix` 将这些局部坐标转换为世界坐标，使 Gizmo 能够使用它们。例如，旋转对象使用局部坐标，通过 `Gizmos.matrix` 可以将其转换到世界坐标。要可视化该对象，请使用 `Gizmos.DrawCube`。

要使用下面的示例绘制红色半透明立方体 Gizmo：

1. 将此示例脚本放在原点处的 Cylinder 上。
2. 在 Hierarchy 中选择 Cylinder，然后单击 Play 按钮。
3. 接着单击 Scene 按钮，Gizmo 应该会出现。

Cylinder 会在 Play 模式下旋转，并在 Scene 视图中显示旋转效果。

```csharp
using UnityEngine;

public class GizmosExample : MonoBehaviour
{
    public float rotationSpeed = 50.0f;

    void OnDrawGizmosSelected()
    {
        Gizmos.color = new Color(0.75f, 0.0f, 0.0f, 0.75f);

        // 将局部坐标值转换为世界坐标，供矩阵变换使用。
        Gizmos.matrix = transform.localToWorldMatrix;
        Gizmos.DrawCube(Vector3.zero, Vector3.one);
    }

    // 旋转立方体。
    void Update()
    {
        float zRot = rotationSpeed * Time.deltaTime;
        transform.Rotate(0.0f, 0.0f, zRot);
    }
}
```

---

## 文档导航

- 上一页：[[02-exposure]]
- 目录：[[00-Gizmos]]
- 下一页：[[04-probeSize]]
