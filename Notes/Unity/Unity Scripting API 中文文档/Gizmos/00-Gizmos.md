> 原文：[Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html)

# Gizmos

## Description

Gizmos 用于在 Scene 视图中提供可视化调试或设置辅助。

脚本中的所有 Gizmo 绘制都必须在 `MonoBehaviour.OnDrawGizmos` 或 `MonoBehaviour.OnDrawGizmosSelected` 函数中完成。Scene 视图或 Game 视图重绘时会调用 `MonoBehaviour.OnDrawGizmos`，在其中渲染的所有 Gizmo 都可以被拾取。只有当附加脚本的对象被选中时，才会调用 `MonoBehaviour.OnDrawGizmosSelected`。

另请参阅：`GizmoUtility`。

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

大多数 Gizmo 绘制方法还接受位置和旋转等额外变换参数。这些变换会叠加到当前设置的 `Gizmos.matrix` 上。

## 静态属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-color]] | `color` | 设置接下来绘制的 Gizmo 的颜色。 |
| [[02-exposure]] | `exposure` | 设置包含 LightProbe Gizmo 曝光校正的纹理，采样纹理中心的红色通道。 |
| [[03-matrix]] | `matrix` | 设置 Unity Editor 用于绘制 Gizmo 的 `Matrix4x4`。 |
| [[04-probeSize]] | `probeSize` | 设置 Light Probe Gizmo 的缩放，用于渲染球谐预览球体。 |

## 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[05-CalculateLOD]] | `CalculateLOD` | 确定 Scene 视图中指定位置和半径的 Gizmo 的适当细节级别。 |
| [[06-DrawCube]] | `DrawCube` | 在 Scene 视图中以 `center` 为中心、以 `size` 为大小绘制实心盒，用于可视化和调试。 |
| [[07-DrawFrustum]] | `DrawFrustum` | 使用当前设置的 `Gizmos.matrix` 的位置和旋转绘制摄像机视锥体。 |
| [[08-DrawGUITexture]] | `DrawGUITexture` | 在 Scene 中绘制纹理。 |
| [[09-DrawIcon]] | `DrawIcon` | 在 Scene 视图中的指定位置绘制图标。 |
| [[10-DrawLine]] | `DrawLine` | 在 Scene 视图中绘制连接两个点的线。 |
| [[11-DrawLineList]] | `DrawLineList` | 在多个点对之间绘制多条线。 |
| [[12-DrawLineStrip]] | `DrawLineStrip` | 在给定 span 中的每个点之间绘制线。 |
| [[13-DrawMesh]] | `DrawMesh` | 在指定变换处绘制网格 Gizmo。 |
| [[14-DrawRay]] | `DrawRay` | 在 Scene 视图中从指定位置开始，沿给定方向绘制射线。 |
| [[15-DrawSphere]] | `DrawSphere` | 在 Scene 视图中以指定中心和半径绘制实心球体。 |
| [[16-DrawWireCube]] | `DrawWireCube` | 在 Scene 视图中以 `center` 为中心、以 `size` 为大小绘制线框盒。 |
| [[17-DrawWireMesh]] | `DrawWireMesh` | 在指定变换处绘制网格线框。 |
| [[18-DrawWireSphere]] | `DrawWireSphere` | 在 Scene 视图中以指定中心和半径绘制线框球体。 |

---

## 文档导航

- 上一页：无
- 目录：[[00-Gizmos]]
- 下一页：[[01-color]]
