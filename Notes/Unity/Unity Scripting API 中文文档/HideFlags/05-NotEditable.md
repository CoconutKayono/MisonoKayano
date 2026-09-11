> 原文：[HideFlags.NotEditable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/HideFlags.NotEditable.html)

# HideFlags.NotEditable

## 描述

对象无法在 Inspector 中编辑。

```csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        // 创建平面，并禁止在 Inspector 和 Scene 视图中修改它。
        GameObject createdGO =
            GameObject.CreatePrimitive(PrimitiveType.Plane);
        createdGO.hideFlags = HideFlags.NotEditable;
    }
}
```

---

## 文档导航

- 上一页：[[04-DontSaveInEditor]]
- 目录：[[00-HideFlags]]
- 下一页：[[06-DontSaveInBuild]]
