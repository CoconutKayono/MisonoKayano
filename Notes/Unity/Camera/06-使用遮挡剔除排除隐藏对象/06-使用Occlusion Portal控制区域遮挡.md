# 使用 Occlusion Portal 控制区域遮挡

> 原文：[Control occlusion in areas with Occlusion Portals](https://docs.unity3d.com/6000.7/Documentation/Manual/class-OcclusionPortal.html)

Occlusion Portal 可以处于打开或关闭状态。Occlusion Portal 关闭时，会遮挡其他 GameObject；打开时，不会遮挡其他 GameObject。

如果 Scene 中的 GameObject 具有打开和关闭两种状态（例如门），可以创建一个 Occlusion Portal，在 Occlusion Culling 系统中表示该 GameObject，然后根据 GameObject 的状态设置 Occlusion Portal 的打开状态。Occlusion Portal Component 不必添加到它所表示的 GameObject 上。

## 设置 Occlusion Portal

1. 在 Scene 中选择一个合适的 GameObject 作为 Occlusion Portal。门等中型到大型实体 GameObject 是良好候选对象。
2. 确保该 GameObject 未标记为 **Occluder Static** 或 **Occludee Static**。
3. 向该 GameObject 添加 **Occlusion Portal** Component。
4. 为 Scene 烘焙 Occlusion Culling 数据。
5. 确保 Occlusion Culling 窗口、Inspector 面板和 Scene view 都可见。
6. 在 Scene view 中移动 Camera，使其位于 Occlusion Portal 正前方。
7. 选择带有 Occlusion Portal Component 的 GameObject。
8. 在 Inspector 窗口中切换 Occlusion Portal Component 的 **Open** 属性，并在 Scene view 中观察 Occlusion Culling 的变化。

## 运行时控制

使用脚本将 Occlusion Portal 的 [`open`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/OcclusionPortal-open.html) 属性设置为所需状态。

```csharp
void OpenDoor()
{
    // 切换 Occlusion Portal 的打开状态，使 Unity 渲染其后的 GameObject。
    myOcclusionPortal.open = true;

    // 调用播放开门动画，或以其他方式隐藏 GameObject 的函数。
    // ...
}
```

## Occlusion Portal Component

| 属性 | 说明 |
| --- | --- |
| **Open** | 启用时，Occlusion Portal 打开，不会遮挡 Renderer；禁用时，Occlusion Portal 关闭，会遮挡 Renderer。 |
| **Center** | 设置 Occlusion Portal 的中心，默认值为 `(0, 0, 0)`。 |
| **Size** | 定义 Occlusion Portal 的大小。 |

---

## 文档导航
- 上一页：[[05-创建高精度遮挡区域]]
- 目录：[[00-使用遮挡剔除排除隐藏对象]]
- 下一页：[[07-Occlusion Culling窗口参考]]
