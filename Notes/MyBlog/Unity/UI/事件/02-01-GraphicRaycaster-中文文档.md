# Graphic Raycaster（图形射线投射器）

Graphic Raycaster 用于对 Canvas 执行射线投射。该射线投射器会检查 Canvas 上的所有 Graphic（图形），判断其中是否有被射线命中的图形。

你可以配置 Graphic Raycaster，使其忽略背面朝向（backfacing）的图形，并允许其被位于前方的 2D 或 3D 对象阻挡。

## 属性（Properties）

| 属性                                   | 功能                                   |
| ------------------------------------ | ------------------------------------ |
| **Ignore Reversed Graphics**（忽略反向图形） | 是否考虑背面朝向射线投射器的图形？                    |
| **Blocking Objects**（阻挡对象）           | 用于检查是否阻挡图形射线投射的对象类型。                 |
| **Blocking Mask**（阻挡遮罩）              | 通过 LayerMask 指定的对象类型，用于检查是否阻挡图形射线投射。 |

## 补充说明：Blocking Objects（阻挡对象）详解

**核心理解**：这个选项决定“哪种类型的物理碰撞体可以挡在射线前面，使射线无法命中它后方的 UI 图形”。它并不是让 2D/3D 对象“接收射线”。

| 选项 | 含义 |
| --- | --- |
| **None**（无） | 不启用阻挡。射线直接穿过所有 2D/3D 碰撞体，命中 Canvas 上的 UI。 |
| **Two Dimensional**（2D） | 只有 2D 碰撞体（Collider2D）能阻挡：射线在命中 UI 之前若先碰到 Collider2D，则该 UI 图形被判为被阻挡，不会响应这次点击。 |
| **Three Dimensional**（3D） | 只有 3D 碰撞体（Collider）能阻挡，规则同上。 |
| **All**（全部） | 2D 和 3D 碰撞体都能阻挡。 |

需要澄清的几点：

1. **选 2D ≠ 2D 对象接收射线**。阻挡只是“遮挡”行为：被挡住的 UI 收不到事件；那个 2D/3D 对象本身也不会因为这项设置而收到 UI 事件。如果想让 2D/3D 物体接收指针（Pointer）事件，需要另外在相机上挂 Physics 2D Raycaster / Physics Raycaster。
2. **阻挡是按距离比较的**。系统会比较 UI 图形与碰撞体到相机的距离：若碰撞体比 UI 图形更靠近相机，则该 UI 图形被阻挡（相当于点击落在碰撞体上，不会穿透到 UI）。
3. **必须有对应类型的 Collider**。只有带 Collider2D（选 2D/All 时）或 Collider（选 3D/All 时）的对象才会参与阻挡；纯 Sprite、Mesh 而没有碰撞体不会阻挡。
4. **Blocking Mask 是图层过滤器**。只有处于该 LayerMask 所选图层上的碰撞体才参与阻挡；默认是 Everything（所有图层）。典型用法：只想让“可点击的 3D 物体”阻挡 UI，就把阻挡遮罩只设到那个图层。
5. **默认值**：Blocking Objects 默认 None（不阻挡），Blocking Mask 默认 Everything。

示例：场景中有一个 UI 按钮，按钮前方有一个带 3D Collider 的立方体。

- Blocking Objects 设为 **Three Dimensional**：点击立方体所在区域时，按钮不会响应。
- Blocking Objects 设为 **None**：点击会穿透立方体，直接命中按钮。
