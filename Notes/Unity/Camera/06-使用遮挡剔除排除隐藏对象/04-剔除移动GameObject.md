# 剔除移动 GameObject

> 原文：[Cull moving GameObjects](https://docs.unity3d.com/6000.7/Documentation/Manual/occlusion-culling-dynamic-gameobjects.html)

GameObject 可以是静态对象，也可以是动态对象（非静态对象）。静态 GameObject 和动态 GameObject 在 Unity 的 Occlusion Culling 系统中的行为不同：

- Unity 可以将静态 GameObject 烘焙到 Occlusion Culling 数据中，作为 Static Occluder 和/或 Static Occludee。
- Unity 无法将动态 GameObject 烘焙到 Occlusion Culling 数据中。动态 GameObject 可以在运行时作为 Occludee，但不能作为 Occluder。

要确定动态 GameObject 是否作为 Occludee，可以在任意类型的 Renderer 组件上设置 **Dynamic Occlusion** 属性。启用 Dynamic Occlusion 时，当 Static Occluder 阻挡动态 GameObject 从 Camera 看到的视线，Unity 会剔除该 Renderer。禁用 Dynamic Occlusion 时，即使 Static Occluder 阻挡该 Renderer，Unity 也不会剔除它。

Dynamic Occlusion 默认启用。为了实现特定效果，例如绘制墙后角色的轮廓，可能需要禁用 Dynamic Occlusion。

如果确定 Unity 永远不应对特定 GameObject 应用 Occlusion Culling，可以禁用 Dynamic Occlusion，以减少运行时计算和 CPU 使用。单个 GameObject 的计算开销非常小，但当对象数量足够多时，可能有助于改善性能。

使用 Umbra Occlusion 系统时，GPU Resident Drawer 会将所有对象视为启用了 Dynamic Occlusion，同时提供自己的基于 GPU 的 Occlusion Culling 机制。

---

## 文档导航
- 上一页：[[03-设置多个场景进行遮挡剔除]]
- 目录：[[00-使用遮挡剔除排除隐藏对象]]
- 下一页：[[05-创建高精度遮挡区域]]
