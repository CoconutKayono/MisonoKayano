# Layer 与 LayerMask

> 原文：[Layers and layerMasks](https://docs.unity3d.com/6000.7/Documentation/Manual/layers-and-layermasks.html)

Unity API 使用 `LayerMask` 以位掩码表示一个或多个 Layer。Camera 的 `cullingMask`、Physics 查询和许多过滤 API 都可以使用 LayerMask。

```csharp
[SerializeField] private LayerMask obstacleMask;

private bool IsBlocked(Vector3 origin, Vector3 direction, float distance)
{
    return Physics.Raycast(origin, direction, distance, obstacleMask);
}
```

Inspector 会把 LayerMask 显示为可多选的 Layer 列表。脚本中可以使用 `LayerMask.GetMask` 创建掩码，也可以使用位运算处理单个 Layer。

LayerMask 只是过滤信息，不会改变 GameObject 本身的 Layer。进行 Physics 查询时，还需要确认 Collider 所在 GameObject 的 Layer 是否正确。

---

## 文档导航

- 上一页：[[02-创建功能层]]
- 目录：[[00-将游戏对象分配到层]]
- 下一页：[[../05-将标签分配给游戏对象]]

