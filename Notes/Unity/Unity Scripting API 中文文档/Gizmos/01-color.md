> 原文：[Gizmos.color](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos-color.html)

# [Gizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Gizmos.html).color

```csharp
public static Color color;
```

## Description

设置接下来绘制的 Gizmo 的颜色。

可以为 Gizmo 应用任意颜色。将 `Color` 的 alpha 分量设置为小于 1 的值，可以使 Gizmo 透明。下面的示例展示了如何创建红色 Gizmo。

```csharp
using UnityEngine;

public class ExampleClass : MonoBehaviour
{
    void OnDrawGizmosSelected()
    {
        // 在对象前方绘制一条长度为 5 个单位的红线。
        Gizmos.color = Color.red;
        Vector3 direction = transform.TransformDirection(Vector3.forward) * 5;
        Gizmos.DrawRay(transform.position, direction);
    }
}
```

---

## 文档导航

- 上一页：[[00-Gizmos]]
- 目录：[[00-Gizmos]]
- 下一页：[[02-exposure]]
