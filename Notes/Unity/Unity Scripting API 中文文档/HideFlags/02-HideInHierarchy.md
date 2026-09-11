> 原文：[HideFlags.HideInHierarchy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/HideFlags.HideInHierarchy.html)

# HideFlags.HideInHierarchy

## 描述

对象不会出现在 Hierarchy 中。

```csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        // 创建 5 个平面，并在 Editor 的 Hierarchy 中隐藏它们。
        for (int i = 0; i < 5; i++)
        {
            GameObject createdGO =
                GameObject.CreatePrimitive(PrimitiveType.Plane);
            createdGO.hideFlags = HideFlags.HideInHierarchy;
        }
    }
}
```

---

## 文档导航

- 上一页：[[01-None]]
- 目录：[[00-HideFlags]]
- 下一页：[[03-HideInInspector]]
