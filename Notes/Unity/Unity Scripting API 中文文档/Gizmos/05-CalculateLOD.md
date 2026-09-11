> 原文：[Gizmos.CalculateLOD](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.CalculateLOD.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).CalculateLOD

## Declaration

```csharp
public static float CalculateLOD(Vector3 position,
    float radius);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `position` | Gizmo 在世界空间中的中心位置。 |
| `radius` | Gizmo 的最大范围。 |

## Returns

`float`：返回 0 到 1 之间的值，表示 Gizmo 的细节级别。

## Description

根据 Scene 视图中指定位置和半径的 Gizmo，确定适当的细节级别。

返回值为 0 表示 Gizmo 不可见。Gizmo 可能因为在屏幕上太小，或位于 Scene 视图摄像机视锥体之外而不可见。返回值会量化为八分之一，以减少生成的批次数量。还可以在 Gizmos 菜单中使用“Fade Gizmos”选项进一步控制此行为。

```csharp
using UnityEngine;

public class MyLODedComponent : MonoBehaviour
{
    // 在 Transform 位置绘制蓝色球体，距离越远越淡出。
    private void OnDrawGizmos()
    {
        float lod = Gizmos.CalculateLOD(transform.position, 1);

        // 剔除太小或位于屏幕外的 Gizmo。
        if (lod == 0.0f)
            return;

        // 淡出 Gizmo，避免在 Scene 中滚动时突然出现或消失。
        Gizmos.color = Color.blue * lod;
        Gizmos.DrawSphere(transform.position, 1);
    }
}
```

---

## 文档导航

- 上一页：[[04-probeSize]]
- 目录：[[00-Gizmos]]
- 下一页：[[06-DrawCube]]
