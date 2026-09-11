> 原文：[Gizmos.DrawFrustum](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawFrustum.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawFrustum

## Declaration

```csharp
public static void DrawFrustum(Vector3 center,
    float fov,
    float maxRange,
    float minRange,
    float aspect);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `center` | 截头棱锥的顶点。对于摄像机来说，这就是摄像机位置；它相对于当前设置的 `Gizmos.matrix` 是一个偏移量。 |
| `fov` | 垂直视野角，即顶点处的角度，单位为度而不是弧度。 |
| `maxRange` | 视锥体远裁剪面的距离。 |
| `minRange` | 视锥体近裁剪面的距离。 |
| `aspect` | 要绘制的视锥体宽高比，即视锥体宽度除以高度。 |

## Description

使用当前设置的 `Gizmos.matrix` 的位置和旋转绘制摄像机视锥体。

视锥体使用当前设置的 `Gizmos.color` 绘制。注意，`fov` 参数是垂直视野角，而不是水平视野角。

```csharp
using UnityEngine;

public class ExampleClass : MonoBehaviour
{
    void OnDrawGizmosSelected()
    {
        // 在世界原点绘制一个红色线框视锥体，使用 16:9 宽高比和 90 度水平视野角。
        Gizmos.color = Color.red;
        Gizmos.DrawFrustum(new Vector3(), 59f, 1000f, 3f, 16f / 9f);
        // 近裁剪面值故意设置得较大，用于展示其相对于视锥体中心的偏移。
    }
}
```

---

## 文档导航

- 上一页：[[06-DrawCube]]
- 目录：[[00-Gizmos]]
- 下一页：[[08-DrawGUITexture]]
