# 预制件实例 Inspector 参考

> 原文：[Prefab instance Inspector reference](https://docs.unity3d.com/6000.7/Documentation/Manual/prefab-instance-inspector-reference.html)

当你[创建 Prefab 的实例](https://docs.unity3d.com/6000.7/Documentation/Manual/CreatingPrefabs.html#create-an-instance-of-a-prefab)时，Inspector 会显示特定的 Prefab 设置。你可以使用这些设置编辑 Prefab Instance 及其父 Prefab Asset。

![Prefab Instance 的 Inspector 窗口，其中选中了 Overrides 菜单。](Unity/Unity%20Manual%20中文文档/GameObjects/06-预制件/图片/prefab-instance-inspector.png)

Prefab Instance 的 Inspector 窗口，其中选中了 Overrides 菜单。

## Overrides

打开 **Overrides** 下拉窗口，其中会显示 Prefab Instance 的所有[覆盖项](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabInstanceOverrides.html)。可以使用此窗口将 Instance 上的覆盖应用到 Prefab Asset，或将 Instance 上的覆盖还原为 Prefab Asset 中的值。**Overrides** 窗口只适用于根 Prefab Instance，不适用于[嵌套 Prefab](https://docs.unity3d.com/6000.7/Documentation/Manual/NestedPrefabs.html)。

可以使用以下选项将所有更改应用到 Asset：

- **Revert All**：将 Prefab Instance 上的所有覆盖还原为父 Prefab Asset 的默认设置。
- **Apply All**：将 Prefab Instance 上的所有覆盖应用到父 Prefab Asset。

如果要应用或还原单独的更改，请在列表中选择对应覆盖，然后使用该覆盖上的 **Revert** 或 **Apply** 按钮。

有关 Prefab 覆盖的更多信息，请参阅[覆盖 Prefab Instance](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabInstanceOverrides.html)。

## Select

在 [Project 窗口](https://docs.unity3d.com/6000.7/Documentation/Manual/ProjectView.html)中选择 Prefab Instance 的父 Prefab Asset。

## Open

在 [Prefab 编辑模式](https://docs.unity3d.com/6000.7/Documentation/Manual/EditingInPrefabMode.html)中打开 Prefab Instance 的父 Prefab Asset。

## 其他资源

- [创建 Prefab](https://docs.unity3d.com/6000.7/Documentation/Manual/CreatingPrefabs.html)
- [覆盖 Prefab Instance](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabInstanceOverrides.html)
- [移除未使用的覆盖数据](https://docs.unity3d.com/6000.7/Documentation/Manual/UnusedOverrides.html)

---

## 文档导航

- 上一页：[[03-实例化投射物和爆炸]]
- 目录：[[00-预制件]]
- 下一页：[[00-相机]]
