# 设置 LayerMask

> 原文：[Set a layerMask](https://docs.unity3d.com/6000.7/Documentation/Manual/layermask-set.html)

本页介绍如何正确设置 `LayerMask`，以便在使用序列化 `LayerMask` 属性的 API 调用中使用它。

## 使用序列化的 LayerMask 属性

在 Unity Editor 中设置 `LayerMask` 最简单的方法，是创建一个使用 Unity `LayerMask` 类的属性。如果该属性是 public，或使用 `SerializeField` Attribute，Unity 会在 Inspector 中提供一个界面，让你选择此 `LayerMask` 表示哪些 Layer。

```csharp
using UnityEngine;

public class LayerMaskExample : MonoBehaviour
{
    [SerializeField] private LayerMask layermask;
}
```

## 从 Layer 转换

如果希望在运行时通过脚本将 Layer 转换为 `LayerMask`，请使用二进制左移运算符，将 `1` 按 Layer 编号向左移动。结果是一个表示单个 Layer 的 `LayerMask`。

```csharp
using UnityEngine;

public class LayerExample : MonoBehaviour
{
    [SerializeField] private int layer = 10;
    private int layerAsLayerMask;

    private void Start()
    {
        layerAsLayerMask = (1 << layer);
    }
}
```

## 其他资源

- [[02-向LayerMask添加Layer|向 LayerMask 添加 Layer]]
- [[04-从LayerMask移除Layer|从 LayerMask 移除 Layer]]
- [[01-LayerMask简介|LayerMask 简介]]

---

## 文档导航

- 上一页：[[02-向LayerMask添加Layer]]
- 目录：[[../03-层与LayerMask]]
- 下一页：[[04-从LayerMask移除Layer]]
