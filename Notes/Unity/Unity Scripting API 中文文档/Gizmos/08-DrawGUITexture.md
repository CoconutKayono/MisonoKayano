> 原文：[Gizmos.DrawGUITexture](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.DrawGUITexture.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).DrawGUITexture

## Declaration

```csharp
public static void DrawGUITexture(Rect screenRect,
    Texture texture,
    Material mat = null);

public static void DrawGUITexture(Rect screenRect,
    Texture texture,
    int leftBorder,
    int rightBorder,
    int topBorder,
    int bottomBorder,
    Material mat = null);
```

## Parameters

| 参数 | 说明 |
| --- | --- |
| `screenRect` | 由 XY 平面定义的“屏幕”上纹理的大小和位置。 |
| `texture` | 要显示的纹理。 |
| `mat` | 可选的纹理材质。 |
| `leftBorder` | 从矩形左边缘向内的距离。 |
| `rightBorder` | 从矩形右边缘向内的距离。 |
| `topBorder` | 从矩形上边缘向内的距离。 |
| `bottomBorder` | 从矩形下边缘向内的距离。 |

## Description

在 Scene 中绘制纹理。

选定的纹理会在由 XY 平面定义的三维“屏幕”上绘制，也就是 Z 坐标为 0 的平面。纹理矩形的值使用 Scene 单位。可选的边框值指定 Scene 单位中从每条边向内的距离；纹理会绘制在内缩后的矩形中，边缘像素会向外重复。这是围绕主要纹理快速创建大面积背景区域的有用方法，尤其适用于边缘为单色的纹理。

此函数可以配合直接指向纹理的摄像机创建 GUI 背景。

```csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour
{
    public Texture myTexture;

    void OnDrawGizmosSelected()
    {
        // 在 Scene 的 XY 平面上绘制纹理矩形。
        Gizmos.DrawGUITexture(new Rect(10, 10, 20, 20), myTexture);
    }
}
```

---

## 文档导航

- 上一页：[[07-DrawFrustum]]
- 目录：[[00-Gizmos]]
- 下一页：[[09-DrawIcon]]
