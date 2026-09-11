# Aim Constraint

> 原文：[Aim Constraint component](https://docs.unity3d.com/6000.7/Documentation/Manual/class-AimConstraint.html)

Aim Constraint 会旋转 GameObject，使其朝向 Source GameObject。它还可以保持另一个轴的一致方向。例如，可以向 Camera 添加 Aim Constraint。为了让 Camera 在 Constraint 使其朝向目标时保持直立，请指定 Camera 的上方向轴以及与之对齐的上方向。

使用 **Up Vector** 指定受到约束的 GameObject 的上方向轴。使用 **World Up Vector** 指定向上的方向。当 Aim Constraint 旋转 GameObject 使其朝向 Source GameObject 时，Constraint 也会将受到约束的 GameObject 的上方向轴与向上的方向对齐。

![Aim Constraint Component。](AimConstraint.png)

### Properties

| 属性 | 说明 |
| --- | --- |
| **Activate** | 在旋转受到约束的 GameObject 并移动其 Source GameObject 后，单击 **Activate** 保存这些信息。**Activate** 会将当前相对于 Source GameObject 的偏移保存到 **Rotation At Rest** 和 **Rotation Offset**，然后启用 **Is Active** 和 **Lock**。 |
| **Zero** | 将受到约束的 GameObject 的旋转设置为 Source GameObject 的旋转。**Zero** 会重置 **Rotation At Rest** 和 **Rotation Offset** 字段，然后启用 **Is Active** 和 **Lock**。 |
| **Is Active** | 启用后才会评估 Constraint。要应用 Constraint，请同时确保 **Lock** 已启用。 |
| **Weight** | Constraint 的强度。Weight 为 `1` 时，Constraint 会使 GameObject 以与 Source GameObject 移动相同的速率旋转；Weight 为 `0` 时，Constraint 完全不起作用。此 Weight 会影响所有 Source GameObject；**Sources** 列表中的每个 GameObject 也有独立的 Weight。 |
| **Aim Vector** | 指定面向 Source GameObject 方向的轴。例如，要让 GameObject 仅使用正 Z 轴朝向 Source GameObject，请将 X、Y、Z 轴的 **Aim Vector** 分别设置为 `0, 0, 1`。 |
| **Up Vector** | 指定此 GameObject 的上方向轴。例如，要让 GameObject 的正 Y 轴保持向上，请将 X、Y、Z 轴的 **Up Vector** 分别设置为 `0, 1, 0`。 |
| **World Up Type** | 指定向上方向所使用的轴。Aim Constraint 使用此向量将 GameObject 的上方向轴与向上的方向对齐。可选值包括：**Scene Up** 使用 Scene 的 Y 轴；**Object Up** 使用 **World Up Object** 所引用 GameObject 的 Y 轴；**Object Up Rotation** 使用 **World Up Object** 所引用 GameObject 的 **World Up Vector** 指定的轴；**Vector** 使用 **World Up Vector** 作为向上方向；**None** 不使用 World Up 向量。 |
| **World Up Vector** | 指定 **World Up Type** 选择 **Object Up Rotation** 或 **Vector** 时使用的向量。 |
| **World Up Object** | 指定 **World Up Type** 选择 **Object Up** 或 **Object Up Rotation** 时使用的 GameObject。 |

### Constraint settings

包含 Aim Constraint 的其他设置。

| 属性 | 说明 |
| --- | --- |
| **Lock** | 启用后，Constraint 可以旋转 GameObject。禁用后，可以编辑此 GameObject 的旋转，也可以编辑 **Rotation At Rest** 和 **Rotation Offset** 属性。如果 **Is Active** 已启用，当你旋转 GameObject 或其 Source GameObject 时，Constraint 会为你更新 **Rotation At Rest** 或 **Rotation Offset** 属性。在完成修改后，启用 **Lock**，让 Constraint 控制此 GameObject。此属性在 Play Mode 中不起作用。 |
| **Rotation At Rest** | 当 Weight 为 `0`，或对应的 **Freeze Rotation Axes** 未启用时使用的 X、Y、Z 值。要编辑这些字段，请禁用 **Lock**。 |
| **Rotation Offset** | Constraint 计算出的旋转与实际旋转之间的 X、Y、Z 偏移值。要编辑这些字段，请禁用 **Lock**。 |
| **Freeze Rotation Axes** | 启用 X、Y 或 Z 后，Constraint 可以控制对应轴；禁用某个轴后，Constraint 不再控制该轴。这样可以编辑、制作动画或通过脚本控制未冻结的轴。 |

### Sources

用于约束此 GameObject 的 GameObject 列表。Unity 会按照 Source GameObject 在此列表中的顺序对其进行评估。此顺序会影响 Constraint 旋转受到约束的 GameObject 的方式。要得到预期结果，请拖动列表中的项目重新排列。每个 Source 的 Weight 范围为 `0` 到 `1`。

---

## 文档导航

- 上一页：[[01-约束组件简介]]
- 目录：[[00-约束组件]]
- 下一页：[[03-Look At Constraint]]
