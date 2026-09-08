# Unity Scene 视图中的 Center、Pivot、Local 和 Global

> 适用版本：Unity 6.5（6000.5），Unity 6.x 其他版本的基本行为相同  
> 官方文档：[Position GameObjects](https://docs.unity3d.com/6000.5/Documentation/Manual/PositioningGameObjects.html)  
> 官方文档：[Transforms](https://docs.unity3d.com/6000.5/Documentation/Manual/class-Transform.html)  
> 官方文档：[Customize the toolbar](https://docs.unity3d.com/6000.5/Documentation/Manual/Toolbar.html)  
> 整理日期：2026-09-07

在 Unity 的 Scene 视图中选中 GameObject 后，工具栏通常会显示两组容易混淆的选项：

```text
Position：Pivot / Center
Rotation：Local / Global / Grid
```

它们控制的是 Scene 视图中的 Transform 工具 Gizmo，而不是直接修改 GameObject 的 Transform 数据。

最简短的记忆方式是：

```text
Pivot / Center = Gizmo 放在哪里
Local / Global = Gizmo 朝哪个方向
```

## 一、先区分两个维度

| 选项 | 解决的问题 | 影响的内容 | 不会改变的内容 |
| --- | --- | --- | --- |
| **Pivot / Center** | 工具的参考点放在哪里 | Move、Rotate、Scale Gizmo 的位置 | GameObject 自己的 Pivot、Mesh Pivot、Transform 数值 |
| **Local / Global** | 工具的坐标轴朝向如何 | Rotate、Move、Scale Gizmo 的轴方向 | GameObject 的 Rotation 数值、父子关系和本地坐标数据 |

例如：

- 选择 **Center + Global**：Gizmo 放在选中对象的中心，轴方向与世界坐标轴一致；
- 选择 **Pivot + Local**：Gizmo 放在对象真实 Pivot，轴方向跟随对象自身旋转；
- 选择 **Pivot + Global**：Gizmo 放在对象真实 Pivot，但轴方向与世界坐标轴一致；
- 选择 **Center + Local**：Gizmo 放在选中对象的中心，但轴方向按照当前对象的 Local 方向显示。

## 二、什么是 Pivot

### Pivot 的含义

**Pivot** 是 GameObject 的实际参考点。Unity 官方对 Scene 工具中的 Pivot 定义是：Gizmo 位于 GameObject 的实际 Pivot 点，该点由 Transform 组件定义。

在 Scene 视图中选择 **Pivot** 后：

- Move 工具从对象的真实 Pivot 点开始移动；
- Rotate 工具围绕对象的真实 Pivot 点旋转；
- Scale 工具以对象的真实 Pivot 点作为缩放参考；
- 不会因为 Mesh 的几何中心改变而自动移动到几何中心。

### Pivot 从哪里来

不同类型对象的 Pivot 来源可能不同：

| 对象类型 | Pivot 通常来自哪里 |
| --- | --- |
| 普通 GameObject | Transform 的位置，通常表现为对象的原点。 |
| 3D 模型 | 建模软件导出的模型原点，也就是 Mesh 的导入 Pivot。 |
| 2D Sprite | Sprite Import Settings 中的 Pivot 设置。 |
| UI 元素 | RectTransform 的 Pivot 属性。 |
| 空 GameObject | 自己的 Transform 原点，因为它没有可见几何体。 |
| 多个对象组合 | 每个对象仍有自己的 Pivot；选择 Center 时才会显示一个整体参考中心。 |

需要注意：**Pivot 不是模型的包围盒中心**。例如，角色模型的原点可能位于脚底，而模型几何体的中心位于胸口。选择 Pivot 时，旋转轴会出现在脚底；选择 Center 时，Gizmo 可能显示在选中几何体或选中对象集合的中心附近。

### Pivot 会影响什么

Pivot 会影响围绕哪个点进行的操作：

```text
旋转对象       = 围绕 Pivot 旋转
缩放对象       = 以 Pivot 作为缩放参考
移动 Gizmo     = 从 Pivot 位置开始拖拽
```

如果希望角色围绕脚底旋转，角色模型的 Pivot 应该位于脚底。如果希望门围绕合页旋转，门的 Pivot 应该位于合页位置。

### Scene 工具中的 Pivot 不等于“修改 Pivot”

在工具栏中切换到 **Pivot**，只是告诉 Unity：“把 Gizmo 放到真实 Pivot”。它不会把 Pivot 移动到别的位置。

如果要真正修改模型或 Sprite 的 Pivot，需要在资源导入设置、Sprite Editor、建模软件或额外的父节点结构中处理。

## 三、什么是 Center

### Center 的含义

**Center** 会把 Gizmo 放在基于当前选中 GameObject 计算出的中心位置。Unity 6.5 手册将它描述为“根据选中 GameObject 得到的中心位置”。

Center 主要适用于同时选择多个对象时的整体操作：

```text
Object_A     Object_B     Object_C
     \          |          /
      \     Center        /
```

在多个对象同时选中时，Center 可以让你更容易围绕这一组选中对象的整体中心进行旋转或缩放。

### Center 不会创建新的父对象

选择 Center 后：

- 不会创建空的父 GameObject；
- 不会改变多个对象之间的父子关系；
- 不会让多个对象共享一个 Transform；
- 不会把各对象的 Pivot 改成同一个点；
- 只是临时改变 Scene 工具 Gizmo 的显示位置。

因此，如果你需要一个真正稳定的整体旋转中心，应该创建一个空父节点，而不是只依赖 Center：

```text
GroupRoot（Empty GameObject）
├── Statue_A
├── Statue_B
└── Statue_C
```

然后旋转 `GroupRoot`。这样旋转中心、层级关系和运行时行为都是明确的。

### 单选时 Center 和 Pivot 的区别

单选一个对象时，两者有时看起来接近，但不能把它们理解成完全相同：

- **Pivot** 使用对象实际的 Transform Pivot；
- **Center** 使用 Unity 根据选中对象计算出的中心；
- 对称模型、空节点或原点位于几何体中心的对象，两者可能重合；
- 原点位于脚底、合页或偏离模型中心的对象，两者通常不同。

## 四、什么是 Local

### Local 的含义

**Local** 表示 Gizmo 的方向跟随 GameObject 自身的局部坐标轴，也就是对象的 Local Rotation。

Unity Scene 视图中通常使用颜色表示轴：

```text
X 轴 = 红色
Y 轴 = 绿色
Z 轴 = 蓝色
```

选择 Local 后，如果对象发生旋转，Gizmo 的红、绿、蓝三条轴也会跟着旋转。

例如，一个角色绕 Y 轴旋转了 45 度：

```text
Global：X、Z 轴仍然对齐世界方向
Local ：X、Z 轴跟随角色旋转 45 度
```

### Local 适合什么场景

Local 适合沿着对象自身方向操作：

- 沿汽车自身的前方移动；
- 沿门的局部轴旋转；
- 沿斜放物体的自身边缘缩放；
- 调整已经旋转过的 UI、模型或道具；
- 在角色自身坐标中调整武器、骨骼或挂点。

## 五、什么是 Global

### Global 的含义

**Global** 表示 Gizmo 的方向固定在世界坐标系中，也就是对齐 Scene 世界的 X、Y、Z 轴。Unity 6.5 手册将它描述为将 Gizmo 限制在 World Space 的方向上。

选择 Global 后：

- 红色 X 轴沿世界 X 方向；
- 绿色 Y 轴沿世界 Y 方向；
- 蓝色 Z 轴沿世界 Z 方向；
- 对象自身旋转不会改变 Gizmo 的轴方向。

### Global 适合什么场景

Global 适合沿场景固定方向操作：

- 沿世界 Y 轴把对象抬高或降低；
- 把多个旋转角度不同的对象统一向世界 X 方向移动；
- 按场景地面方向摆放对象；
- 对齐建筑、道路、地图和关卡元素；
- 需要参考世界方向而不是对象自身方向时。

## 六、Local / Global 不等于 localPosition / position

这是最重要的区别之一。

### 工具栏中的 Local / Global

工具栏的 Local / Global 控制的是：

```text
Scene 视图中 Gizmo 的轴方向
```

它主要影响你如何拖拽 Move、Rotate、Scale 工具。

### C# 中的 localPosition / position

脚本中的 `localPosition` 和 `position` 代表的是不同坐标空间中的 Transform 数据：

```csharp
transform.localPosition  // 相对于父 Transform 的位置
transform.position       // 世界空间中的位置

transform.localRotation  // 相对于父 Transform 的旋转
transform.rotation       // 世界空间中的旋转

transform.localScale     // 相对于父 Transform 的缩放
```

Unity 官方 Transform 手册说明：有父节点时，Transform Inspector 中的 Position、Rotation 和 Scale 通常以父节点为参考；没有父节点时，它们就是世界空间中的值。

工具栏切换 Local / Global 不会把 `transform.localPosition` 自动改成 `transform.position`，也不会改变父子关系或重新计算对象的坐标数据。你只是改变了 Scene 视图中操作 Gizmo 的参考方向。

## 七、四种常用组合

### Pivot + Local

```text
位置：对象自己的真实 Pivot
方向：对象自己的 Local 轴
```

适合精确编辑单个对象，例如让门围绕合页旋转、沿角色自身方向移动、缩放一个已经旋转的道具。

### Pivot + Global

```text
位置：对象自己的真实 Pivot
方向：世界坐标轴
```

适合以对象原点为参考，但沿世界方向移动、旋转或缩放。例如把角色垂直向上移动，而不关心角色自身朝向。

### Center + Local

```text
位置：选中对象的中心
方向：Local 方向
```

适合对一组对象执行局部方向上的整体调整。需要完全可预测的整体旋转时，应使用公共父节点。

### Center + Global

```text
位置：选中对象的中心
方向：世界坐标轴
```

适合关卡编辑中对多个对象进行整体平移、旋转或缩放。

## 八、Move、Rotate、Scale 中的区别

### Move 工具

- Pivot / Center 决定移动 Gizmo 显示在哪里；
- Local / Global 决定轴的方向；
- 按住 Shift 拖动 Move Gizmo 中心，可以沿 Scene 视图相机所面对的平面移动；
- 点击红、绿、蓝小方块，可以锁定一个轴，在另两个轴组成的平面内移动。

### Rotate 工具

- Pivot / Center 决定围绕哪个点旋转；
- Local / Global 决定圆环对应的轴方向；
- Global 下旋转圆环与世界轴对齐；
- Local 下旋转圆环与对象自身轴对齐；
- 外层圆环通常用于沿 Scene 视图的屏幕空间方向旋转。

### Scale 工具

- Pivot / Center 决定缩放参考位置；
- Local / Global 决定轴向缩放手柄的方向；
- 缩放带有子对象的层级时要注意父节点缩放会影响子对象；
- 非均匀缩放可能导致子对象出现看似倾斜或剪切的效果。

## 九、实际例子：旋转一扇门

假设门的层级如下：

```text
DoorRoot
└── DoorMesh
```

### Pivot 正确位于合页

如果 `DoorRoot` 的 Pivot 位于合页位置：

1. 选择 `DoorRoot`；
2. 选择 **Pivot**；
3. 选择 **Local** 或 **Global**，取决于你希望沿门自身轴还是世界轴旋转；
4. 使用 Rotate 工具旋转。

门会围绕合页旋转，适合正常的开门效果。

### Pivot 位于门的几何中心

如果 Pivot 在门的中心，直接旋转会像一块板绕中心转动，而不是围绕合页转动。

推荐调整层级：

```text
DoorHinge（Empty GameObject，放在合页）
└── DoorMesh（局部位置偏移到合适位置）
```

运行时旋转 `DoorHinge`，不依赖临时切换 Center。Center 只能改变编辑器 Gizmo 的位置，不能为运行时创建真正的旋转中心。

## 十、实际例子：同时调整多个物体

假设场景中有三个箱子：

```text
Box_A
Box_B
Box_C
```

只想统一向世界上方移动时，可以使用：

```text
Pivot 或 Center + Global
```

拖动绿色 Y 轴，三个箱子会沿世界 Y 方向移动。

如果想围绕整体中心旋转，可以临时使用：

```text
Center + Global
```

但如果这个旋转中心需要在运行时继续存在，推荐创建：

```text
BoxesRoot
├── Box_A
├── Box_B
└── Box_C
```

并把 `BoxesRoot` 放在明确的旋转中心。这样比依靠编辑器的 Center 更可靠。

## 十一、UGUI 中的特殊情况

UGUI 使用的是 `RectTransform`，它除了 Position、Rotation、Scale 外，还包含：

- Anchors；
- Pivot；
- Anchored Position；
- Size Delta；
- Offset Min / Offset Max。

### UGUI 的 Pivot

UI 元素的 Pivot 决定 RectTransform 围绕哪个点旋转和缩放：

```text
Pivot = (0.5, 0.5)  // 中心
Pivot = (0, 0.5)    // 左侧中心
Pivot = (0.5, 1)    // 顶部中心
```

例如，UI 面板的 Pivot 设置为顶部中心后，面板进行缩放或展开动画时，可以让顶部边缘保持相对稳定。

### UGUI 的 Center

Scene 工具中的 Center 仍然只是 Gizmo 的临时显示位置，不会修改 UI 元素的 RectTransform Pivot。要真正改变 UI 的旋转或缩放中心，应修改 RectTransform 的 Pivot 属性。

### UGUI 的 Local / Global

对于 Screen Space UI，Local / Global 的视觉差异可能不明显，因为 UI 通常只在 XY 平面排列，并且大多数 UI 元素 Rotation 为零。对于 World Space Canvas、旋转后的 UI 面板或 3D UI，Local / Global 的区别会更加明显。

## 十二、推荐工作习惯

### 编辑单个模型

```text
Pivot + Local
```

优先使用真实 Pivot 和对象自身轴向，适合精确编辑。

### 调整场景中的高度和方向

```text
Pivot + Global
```

以对象自身原点为参考，但沿世界方向移动或旋转。

### 临时整体调整多个对象

```text
Center + Global
```

以选中对象的中心作为临时 Gizmo 位置，并沿世界轴操作。

### 制作长期存在的组合体

```text
创建 Empty GameObject 作为 Root
把对象放到 Root 下
调整 Root 的位置和 Pivot
运行时操作 Root
```

不要把 Center 当成运行时的父节点或旋转中心。

## 十三、常见误解

### 误解 1：切换 Pivot 会修改模型 Pivot

不会。它只切换 Gizmo 的显示位置。

### 误解 2：Center 就是把对象 Pivot 改到了中心

不是。Center 只是使用选中对象计算出来的中心放置 Gizmo。

### 误解 3：Local 会把 Transform 变成本地坐标

不会。Local 只控制 Gizmo 的方向。脚本中的 `localPosition`、`localRotation` 和 `localScale` 是另一组概念。

### 误解 4：Global 会把对象旋转重置为世界旋转

不会。Global 只让 Gizmo 轴对齐世界坐标，对象当前的 Rotation 不会因为切换选项而改变。

### 误解 5：多选后 Center 可以替代父节点

不能。Center 只在当前编辑操作中改变 Gizmo 位置，不能提供稳定的运行时层级和旋转中心。

## 十四、总结

```text
Pivot = GameObject 自己的真实参考点
Center = 当前选中对象集合的临时中心

Local = Gizmo 对齐对象自身坐标轴
Global = Gizmo 对齐世界坐标轴
```

再用一句话概括：

> `Pivot / Center` 决定“从哪里操作”，`Local / Global` 决定“沿哪个方向操作”。它们都是 Scene 视图工具的编辑选项，不会自动修改 GameObject 的 Pivot、父子关系或 Transform 坐标空间。
