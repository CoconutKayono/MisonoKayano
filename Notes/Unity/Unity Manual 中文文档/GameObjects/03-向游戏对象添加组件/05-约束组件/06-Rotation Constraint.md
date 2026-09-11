# Rotation Constraint

> 原文：[Rotation Constraint component](https://docs.unity3d.com/6000.7/Documentation/Manual/class-RotationConstraint.html)

Rotation Constraint Component 会旋转 GameObject，使其匹配 Source GameObject 的旋转。

![Rotation Constraint Component。](RotationConstraint.png)

## Properties

| 属性 | 说明 |
| --- | --- |
| **Activate** | 旋转受到约束的 GameObject 及其 Source GameObject 后，单击 **Activate** 保存这些信息。**Activate** 会将当前相对于 Source GameObject 的偏移保存到 **Rotation At Rest** 和 **Rotation Offset**，然后启用 **Is Active** 和 **Lock**。 |
| **Zero** | 将受到约束的 GameObject 的旋转设置为 Source GameObject 的旋转。**Zero** 会重置 **Rotation At Rest** 和 **Rotation Offset** 字段，然后启用 **Is Active** 和 **Lock**。 |
| **Is Active** | 切换是否评估 Constraint。要应用 Constraint，请同时确保 **Lock** 已启用。 |
| **Weight** | Constraint 的强度。Weight 为 `1` 时，Constraint 会使此 GameObject 以与 Source GameObject 相同的速率旋转；Weight 为 `0` 时，Constraint 完全不起作用。此 Weight 会影响所有 Source GameObject；**Sources** 列表中的每个 GameObject 也有独立的 Weight。 |

## Constraint Settings

| 属性 | 说明 |
| --- | --- |
| **Lock** | 启用后，Constraint 可以旋转 GameObject。禁用后，可以编辑此 GameObject 的旋转，也可以编辑 **Rotation At Rest** 和 **Rotation Offset** 属性。如果 **Is Active** 已启用，当你旋转 GameObject 或其 Source GameObject 时，Constraint 会为你更新 **Rotation At Rest** 或 **Rotation Offset** 属性。完成修改后，启用 **Lock**，让 Constraint 控制此 GameObject。此属性在 Play Mode 中不起作用。 |
| **Rotation At Rest** | 当 Weight 为 `0`，或对应的 **Freeze Rotation Axes** 未启用时使用的 X、Y、Z 值。要编辑这些字段，请禁用 **Lock**。 |
| **Rotation Offset** | Constraint 施加的 Transform 旋转偏移的 X、Y、Z 值。要编辑这些字段，请禁用 **Lock**。 |
| **Freeze Rotation Axes** | 启用 X、Y 或 Z 后，Constraint 可以控制对应的旋转轴；禁用某个轴后，Constraint 不再控制该轴，因此可以编辑、制作动画或通过脚本控制未冻结的轴。 |

## Sources

这是约束此 GameObject 的 GameObject 列表。Unity 会按照 Source GameObject 在列表中的顺序对其进行评估。此顺序会影响 Constraint 旋转受到约束的 GameObject 的方式。要得到预期结果，请拖动列表中的项目重新排列。每个 Source 的 Weight 范围为 `0` 到 `1`。

---

## 文档导航

- 上一页：[[05-Position Constraint]]
- 目录：[[00-约束组件]]
- 下一页：[[07-Scale Constraint]]
