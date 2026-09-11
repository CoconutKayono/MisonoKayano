> 原文：[Gizmos.DrawWireMesh](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawWireMesh.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawWireMesh

## Declaration

```csharp
public static void DrawWireMesh(Mesh mesh,
    Vector3 position = Vector3.zero,
    Quaternion rotation = Quaternion.identity,
    Vector3 scale = Vector3.one);

public static void DrawWireMesh(Mesh mesh,
    int submeshIndex,
    Vector3 position = Vector3.zero,
    Quaternion rotation = Quaternion.identity,
    Vector3 scale = Vector3.one);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `mesh` | 要绘制线框 Gizmo 的 `Mesh`。可以创建和管理网格对象，也可以通过 `MeshFilter` 组件获取。 |
| `position` | 网格在世界空间中的位置，默认位置为零。 |
| `rotation` | 网格在世界空间中的方向，默认为单位四元数。 |
| `scale` | 网格在世界空间中的缩放，默认缩放为 1。 |
| `submeshIndex` | 要绘制的子网格，默认值为 -1，表示绘制整个网格。 |

## Description

在指定变换处绘制网格线框。

线框网格 Gizmo 使用当前设置的 `Gizmos.color` 绘制。

另请参阅：`Gizmos.DrawMesh`。

```csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour
{
    Mesh mesh = null;

    void OnDrawGizmosSelected()
    {
        // 在对象位置绘制一个绕 Y 轴旋转 45 度的红色 Cube 线框。
        if (mesh is null)
            mesh = Resources.GetBuiltinResource<Mesh>("Cube.fbx");
        Gizmos.color = Color.red;
        Gizmos.DrawWireMesh(mesh, transform.position,
            Quaternion.Euler(0f, 45f, 0f));
    }
}
```

---

## 文档导航

- 上一页：[[16-DrawWireCube]]
- 目录：[[00-Gizmos]]
- 下一页：[[18-DrawWireSphere]]
