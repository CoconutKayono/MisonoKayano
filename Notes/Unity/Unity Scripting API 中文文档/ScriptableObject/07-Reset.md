> 原文：[ScriptableObject.Reset](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.Reset.html)

# [ScriptableObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html).Reset

## 描述

重置为默认值。

当用户在 Inspector 的上下文菜单中点击 Reset 按钮，或首次添加组件时调用 `Reset`。此函数仅在编辑器模式下调用。通常使用 `Reset` 为 Inspector 中的字段提供良好的默认值。

```csharp
using UnityEngine;

public class Example : ScriptableObject
{
    public GameObject target;

    void Reset()
    {
        // 在控制台输出消息
        Debug.Log("Reset");
        if (!target)
            target = GameObject.FindWithTag("Player");
    }
}
```

---

## 文档导航

- 上一页：[[06-OnValidate]]
- 目录：[[00-ScriptableObject]]
- 下一页：无
