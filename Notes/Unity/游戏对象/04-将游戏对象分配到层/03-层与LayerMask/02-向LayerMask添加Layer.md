# 向 LayerMask 添加 Layer

> 原文：[Add a layer to a layerMask](https://docs.unity3d.com/6000.7/Documentation/Manual/layermask-add.html)

要向 `LayerMask` 添加 Layer，请对原始 `LayerMask` 和要添加的 Layer 使用逻辑 OR 运算符。先将 Layer 编号转换为对应的位，再与原始 `LayerMask` 合并，这样不会移除其中已经包含的其他 Layer。

```csharp
originalLayerMask |= (1 << layerToAdd);
```

## 其他资源

- [[03-设置LayerMask|设置 LayerMask]]
- [[04-从LayerMask移除Layer|从 LayerMask 移除 Layer]]

---

## 文档导航

- 上一页：[[01-LayerMask简介]]
- 目录：[[../03-层与LayerMask]]
- 下一页：[[03-设置LayerMask]]
