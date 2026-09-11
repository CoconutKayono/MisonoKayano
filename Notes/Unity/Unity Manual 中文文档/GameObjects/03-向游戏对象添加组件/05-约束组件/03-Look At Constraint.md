# Look At Constraint

> 原文：[Look At Constraint component](https://docs.unity3d.com/6000.7/Documentation/Manual/class-LookAtConstraint.html)

Look At Constraint 会旋转 GameObject，使其朝向 Source GameObject。通常可以将 Look At Constraint 应用到 [Camera](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Camera.html)，让 Camera 跟随一个或多个 GameObject。导入带有 Target Camera 的文件时，Unity 也会创建一个使用目标对象作为 Source 的 Camera 和 Look At Constraint。

Look At 是 [Aim Constraint](https://docs.unity3d.com/6000.7/Documentation/Manual/class-AimConstraint.html) 的简化版本。Aim Constraint 允许你选择跟随约束 GameObject 的轴，而 Look At Constraint 始终跟随 Z 轴。

你可以将 Look At Constraint 的向上方向设置为另一个 GameObject 的 Y 轴，也可以指定 Roll，即围绕 Z 轴（瞄准轴）的旋转。

![Look At Constraint Component。](class-LookAtConstraint.png)

![Look At Constraint 中的 Source 影响示例。](class-LookAtConstraint_Example.png)

## Properties

| 属性 | 说明 |
| --- | --- |
| **Is Active** | 启用此选项后才会评估 Constraint。要应用 Constraint，请同时启用 **Lock** 属性。 |
| **Weight** | 设置 Constraint 的强度。有效范围为 `0` 到 `1`：`0` 表示 Constraint 没有影响，`1` 表示此 GameObject 以与其 Source GameObject 移动相同的速率旋转。此 Weight 会同等影响所有 Source GameObject，但也可以在 **Sources** 列表中单独修改每个 GameObject 的 Weight。 |
| **Use Up Object** | 启用此选项后，将此 GameObject 的 Up Vector 设置为 **World Up Object** 的 Y 轴。禁用后，Up Vector 使用 **Roll** 值。GameObject 的 Up Vector 用于确定哪个方向为向上。 |
| **Roll** | 设置用于此 GameObject Up Vector（向上方向）的 Z 轴旋转角度，单位为度。仅在禁用 **Use Up Object** 时可用。 |
| **World Up Object** | 设置要用作 Up Vector 参考的 GameObject。设置后，该 GameObject 的 Y 轴会成为受到约束的 GameObject 的向上方向。仅在启用 **Use Up Object** 时可用。 |

## Constraint Settings

| 属性 | 说明 |
| --- | --- |
| **Lock** | 启用此选项后，Constraint 可以旋转 GameObject，即应用 Constraint。禁用后，可以修改 GameObject 的旋转、**Rotation At Rest** 和 **Rotation Offset** 属性。完成修改后，启用 **Lock**，让 Constraint 控制此 GameObject。此属性在 Play Mode 中不起作用。 |
| **Rotation At Rest** | 设置受到约束的 GameObject 静止时在 X、Y、Z 轴上的方向。当包括所有 Source 的单独 Weight 在内的总 Weight 加起来为 `0` 时，GameObject 处于静止状态。要修改此属性，请禁用 **Lock**。 |
| **Rotation Offset** | 设置 X、Y、Z 轴上的偏移，使其偏离受到约束的方向，即 Constraint 计算出的旋转。要修改此属性，请禁用 **Lock**。 |

## Sources

这是约束此 GameObject 的 GameObject 列表。Unity 会按照 Source GameObject 在列表中的顺序对其进行评估。由于旋转会累积，顺序会影响此 Constraint 旋转受到约束的 GameObject 的方式。要得到预期结果，请拖动列表中的项目重新排列；不同顺序会产生不同结果。

列表中的每个条目都包含一个 GameObject Reference 及其 Weight，即该 Source 对 Constraint 的影响程度。Unity 会计算列表中 Source GameObject 的平均值，你可以通过修改每个 Source 的 Weight 来调整影响程度。例如，如果有两个 Source（一个 Cube 和一个 Sphere），并且希望 Camera 更偏向 Sphere，可以将 Sphere 的 Weight 设置为最大值 `1`，将 Cube 的 Weight 设置为 `0.5`。

---

## 文档导航

- 上一页：[[02-Aim Constraint]]
- 目录：[[00-约束组件]]
- 下一页：[[04-Parent Constraint]]
