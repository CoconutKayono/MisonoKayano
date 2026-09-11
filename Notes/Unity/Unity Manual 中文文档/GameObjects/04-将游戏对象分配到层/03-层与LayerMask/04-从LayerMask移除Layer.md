# 从 LayerMask 移除 Layer

> 原文：[Remove a layer from a layerMask](https://docs.unity3d.com/6000.7/Documentation/Manual/layermask-remove.html)

要从 `LayerMask` 移除 Layer，请对原始 `LayerMask` 和要移除的 Layer 的按位补码使用逻辑 AND 运算符。

```csharp
originalLayerMask &= ~(1 << layerToRemove);
```

## 其他资源

- [[03-设置LayerMask|设置 LayerMask]]
- [[02-向LayerMask添加Layer|向 LayerMask 添加 Layer]]

---

## 文档导航

- 上一页：[[03-设置LayerMask]]
- 目录：[[03-层与LayerMask]]
- 下一页：[[05-将标签分配给游戏对象]]
