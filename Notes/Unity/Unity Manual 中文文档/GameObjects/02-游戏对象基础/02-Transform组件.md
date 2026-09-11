# Transform 组件

> 原文：[Transforms](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Transform.html)

`Transform` 存储 GameObject 的 Position、Rotation、Scale 和父子关系状态。每个 GameObject 都始终附加有一个 Transform Component：你无法移除 Transform，也无法创建不带 Transform Component 的 GameObject。

## Transform Component

Transform Component 决定 Scene 中每个 GameObject 的 Position、Rotation 和 Scale。每个 GameObject 都有一个 Transform。

![Transform Component](TransformExample4.png)

> [!TIP]
> 你可以更改 Transform 轴（以及其他 UI 元素）的颜色：打开 **Unity > Preferences**，然后选择 **Colors & keys** 面板。

## Properties

| Property | Function |
| --- | --- |
| **Position** | Transform 在 x、y 和 z 坐标中的位置。 |
| **Rotation** | Transform 绕 x 轴、y 轴和 z 轴的旋转角度，单位为度。 |
| **Scale** | Transform 在 x 轴、y 轴和 z 轴方向上的缩放值。值为 `1` 表示原始大小，也就是导入 GameObject 时的大小。 |
| **Enable Constrained Proportions** | 强制缩放保持当前比例，因此更改一个轴时会同时更改另外两个轴。默认禁用。 |

Unity 会根据 Transform 的父对象测量 Transform 的 Position、Rotation 和 Scale 值。如果 Transform 没有父对象，Unity 会在世界空间中测量这些属性。

## 编辑 Transform

在 2D 空间中，你只能在 x 轴或 y 轴上操作 Transform；在 3D 空间中，你可以在 x 轴、y 轴和 z 轴上操作 Transform。在 Unity 中，这些轴分别使用红色、绿色和蓝色表示。

![显示颜色编码坐标轴的 Transform](TransformExample2.png)

编辑 Transform 的属性主要有三种方式：

- 在 [Scene 视图](https://docs.unity3d.com/6000.7/Documentation/Manual/UsingTheSceneView.html)中编辑。
- 在 [Inspector 窗口](https://docs.unity3d.com/6000.7/Documentation/Manual/UsingTheInspector.html)中编辑。
- 在 C# 脚本中编辑。

### Scene 视图

在 Scene 视图中，你可以使用 Move、Rotate 和 Scale 工具修改 Transform。这些工具位于 Unity Editor 的左上角。

![Hand、Move、Rotate 和 Scale 工具](Transform-Tools.png)

你可以对 Scene 中的任意 GameObject 使用 Transform 工具。选择 GameObject 时，Transform 内会显示工具 Gizmo。Gizmo 的外观取决于你选择的工具。

![带有键盘快捷键提示的 Transform Gizmo](TransformGizmo35.png)

点击并拖动三个 Gizmo 轴中的一个时，该轴的颜色会变为黄色。拖动鼠标时，GameObject 会沿选中的轴移动、旋转或缩放。释放鼠标按钮后，该轴仍保持选中状态。

移动 GameObject 时，你可以将移动锁定到某个平面，也就是更改其中两个轴并保持第三个轴不变。要激活某个平面的锁定，请选择 Move Gizmo 中心周围的三个小彩色方块。颜色对应选择方块时被锁定的轴；例如，选择蓝色方块会锁定 z 轴。

### Inspector 窗口

在 Inspector 窗口中，你可以使用 Transform Component 编辑选中 GameObject 的 Transform 属性。编辑 Component 中的 Transform 属性值有两种方式：

- 手动在属性值字段中输入数值。这适用于非常精确的调整。
- 点击某个值字段并上下拖动，以增大或减小数值。这适用于不需要精确数值的调整。

### From code

在 C# 代码中使用 Transform 类，可以修改 GameObject 的位置、旋转、缩放，以及它与父子 GameObject 的层级关系。完整的 Transform 类成员参考和使用示例，请参阅 [Transform API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html)。

## 对 GameObject 分组

在 Unity 中，你可以将 GameObject 组织成父子层级：

- 父 GameObject 连接着其他 GameObject，这些子对象会继承它的 Transform 属性。
- 子 GameObject 连接到另一个 GameObject，并继承该对象的 Transform 属性。

在 Hierarchy 窗口中，子 GameObject 会直接显示在父 GameObject 下方，并在列表中缩进。你可以选择折叠按钮来隐藏或显示父 GameObject 的子 GameObject。

子 GameObject 会完全按照父 GameObject 的方式移动、旋转和缩放。子 GameObject 还可以拥有自己的子 GameObject。一个 GameObject 可以有多个子 GameObject，但只能有一个父 GameObject。

这些多层父子关系构成 Transform hierarchy。层级顶部的 GameObject，也就是层级中唯一没有父对象的 GameObject，称为 root GameObject。

要创建父 GameObject，请在 Hierarchy 窗口中将一个 GameObject 拖到另一个 GameObject 上。这会在两个 GameObject 之间建立父子关系。

![Hierarchy 窗口中的父子 GameObject：Child 1 和 Child 2 属于 Parent，Child 3 属于 Child 2 并且是 Parent 的后代](parenting-in-hierarchy-window.png)

## 编辑父子 GameObject 的 Transform

你可以将 GameObject 组织成父子层级。

任何子 GameObject 的 Transform 值都会相对于父 GameObject 的 Transform 值显示。这些值称为 local coordinates。对于 Scene 构建，使用子 GameObject 的 local coordinates 通常就足够了。在 Gameplay 中，通常需要获取它们的 global coordinates 或者它们在世界空间中的精确位置。Transform Component 的 Scripting API 为 local 和 global 的 Position、Rotation、Scale 提供了独立属性，并且允许你在 local 和 global coordinates 之间转换。

> [!TIP]
> 为 Transform 设置父对象时，最好在添加子 Transform 之前将父对象的位置设为 `<0,0,0>`。这样子 Transform 的 local coordinates 就会与 global coordinates 相同，更容易确保子对象处于正确位置。

## Transform 和 Scale

Transform 的 Scale 决定建模应用程序中的 Mesh 大小与该 Mesh 在 Unity 中的大小之间的差异。Mesh 在 Unity 中的大小（因此 Transform 的 Scale）尤其会影响 Physics Simulation。默认情况下，Physics Engine 假设世界空间中的一个单位对应一米。如果 GameObject 非常大，它看起来可能会以“慢动作”下落；但模拟是正确的，因为你看到的是一个非常大的 GameObject 下落很长的距离。

GameObject 的 Scale 受以下三个因素影响：

- 3D 建模应用程序中的 Mesh 大小。
- GameObject Import Settings 中的 **Mesh Scale Factor** 设置。
- Transform Component 的 Scale 值。

不要在 Transform Component 中调整 GameObject 的 Scale。如果你按照现实世界的比例创建模型，就不需要更改 Transform 的 Scale。你也可以在导入设置中调整 Mesh 的导入比例，因为一些优化会根据导入大小执行。对具有调整后 Scale 值的 GameObject 进行实例化可能会降低性能。

绝不要在 Transform Component 中将任何 Scale 轴设为 `0`。这样做可能导致数学计算出现未定义结果，例如在渲染中产生 NaN（Not a Number）值，并在屏幕上造成错误的图形伪影。

更改 Scale 会影响子 Transform 的位置。例如，将父 Transform 缩放为 `(0,0,0)` 会使所有子 Transform 相对于父 Transform 的位置变为 `(0,0,0)`。

## Non-uniform scaling

当 Transform 的 Scale 在 x、y 和 z 方向使用不同值时，就是非均匀缩放（Non-uniform scaling），例如 `(2, 4, 2)`。相反，x、y 和 z 使用相同值（例如 `(3, 3, 3)`）时是均匀缩放。非均匀缩放在某些特定情况下很有用，但它的行为与均匀缩放不同：

- 有些 Components 不完全支持非均匀缩放。例如，Sphere Collider、Capsule Collider、Light 和 Audio Source 等 Components 可能通过 Radius 属性定义圆形或球形元素。这意味着在非均匀缩放下，圆形仍保持圆形，而不是变成椭圆形。
- 如果子 GameObject 的父 GameObject 使用了非均匀缩放，并且子 GameObject 相对于父对象发生旋转，它可能会出现扭曲或“剪切”。有些 Components 支持简单的非均匀缩放，但在这种剪切状态下不能正确工作。例如，剪切后的 Box Collider 可能无法准确匹配渲染 Mesh 的形状。
- 非均匀缩放父 GameObject 的子 GameObject 在旋转时不会自动更新其 Scale。因此，当你之后更新 Scale 时，子 GameObject 的形状可能会突然改变，例如将子 GameObject 从父对象中分离时。

## 其他资源

- [定位 GameObject](https://docs.unity3d.com/6000.7/Documentation/Manual/PositioningGameObjects.html)
- [网格吸附](https://docs.unity3d.com/6000.7/Documentation/Manual/GridSnapping.html)
- [Transform API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html)

---

## 文档导航

- 上一篇：[[01-GameObject类]]
- 所属目录：[[00-游戏对象基础]]
- 下一篇：[[03-静态游戏对象]]
