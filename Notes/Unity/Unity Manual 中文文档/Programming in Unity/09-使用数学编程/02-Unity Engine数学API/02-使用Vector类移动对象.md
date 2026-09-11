# 使用 Vector 类移动对象

> 原文：[Moving objects with the Vector classes](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-vectors.html)

Vector 是描述方向和大小的基础数学概念。在游戏和应用程序中，Vector 常用于表示角色的位置、对象的移动速度，或两个对象之间的距离等基本属性。

Vector 运算是图形、物理和动画等许多计算机编程领域的基础。深入理解 Vector，有助于充分利用 Unity 提供的数学功能。

Vector 可以用不同维度表示。Unity 提供 `Vector2`、`Vector3` 和 `Vector4` 类，分别用于 2D、3D 和 4D Vector。这三种 Vector 类共享许多函数，例如 `magnitude`，因此除非特别说明，本页内容适用于全部三种 Vector 类型。

本页概述 Vector 类及其在脚本中的常见用途。有关 Vector2、Vector3 和 Vector4 每个成员的完整信息，请参阅对应的 Scripting API 页面。

## 理解 Vector 运算

### 加法

两个 Vector 相加，结果相当于将原来的两个 Vector 依次当作“步长”。两个参数的顺序不影响结果。

如果将第一个 Vector 看作空间中的一个点，那么第二个 Vector 可以理解为从该位置出发的偏移或“跳跃”。例如，要找出地面上某个位置正上方 5 个单位的点，可以进行以下计算：

```csharp
var pointInAir = pointOnGround + new Vector2(0, 5);
```

如果 Vector 表示力，更直观的理解方式是方向和大小，其中大小表示力的强弱。将两个力 Vector 相加，会得到代表两个力合力的新 Vector。当多个独立力同时作用时，这个概念很有用；例如火箭向前推进时，还可能受到侧风影响。

下面的示例使用 2D Vector，但同样的概念也适用于 3D 和 4D Vector。

![Vector 加法示意图](VectorAdd.png)

### 减法

Vector 减法最常用于获取从一个对象指向另一个对象的方向和距离。与加法不同，减法中两个参数的顺序会影响结果：

```csharp
// Vector d 与 c 的大小相同，但方向相反。
var c = b - a;
var d = a - b;
```

和数字一样，加上一个 Vector 的负值等于减去这个 Vector 的正值：

```csharp
// 这两种写法的结果相同。
var c = a - b;
var c = a + -b;
```

Vector 的负值与原 Vector 大小相同，位于同一直线上，但方向完全相反。

![Vector 减法示意图](VectorSubtract.png)

## 获取两个对象之间的方向和距离

从一个空间点减去另一个空间点，结果就是一个从一个对象“指向”另一个对象的 Vector：

```csharp
// 获取从玩家位置指向目标位置的 Vector。
var heading = target.position - player.position;
```

这个 Vector 的方向指向目标对象，大小等于两个位置之间的距离。有时只需要指向目标的 normalized Vector，同时保持一个固定距离，例如为投射物确定发射方向。可以将 Vector 除以它自己的大小来进行归一化：

```csharp
var distance = heading.magnitude;
var direction = heading / distance;

// 这是归一化后的方向。
```

相比单独使用 `magnitude` 和 `normalized` 属性，这种写法更好，因为这两个属性都需要计算平方根，CPU 开销较高。

如果只需要比较距离，例如进行接近检测，则可以完全避免计算 `magnitude`。`sqrMagnitude` 返回大小的平方，其计算方式与 `magnitude` 类似，但不需要耗时的平方根运算。与已知距离的大小比较时，可以改为比较大小的平方：

```csharp
if (heading.sqrMagnitude < maxRange * maxRange)
{
    // 目标在范围内。
}
```

在比较中使用 `sqrMagnitude` 的效率高得多。

有时在 3D 场景中需要获取目标的“地面方向”。例如，玩家站在地面上，需要接近一个漂浮在空中的目标。直接用目标位置减去玩家位置，得到的 Vector 会向上指向目标，不适合用来设置玩家 Transform 的朝向，因为玩家也会跟着向上指。此时需要找到从玩家位置指向目标正下方地面位置的 Vector，可以将减法结果的 Y 坐标设置为零：

```csharp
var heading = target.position - player.position;
heading.y = 0;

// 这是地面方向。
```

## 数乘和数除

讨论 Vector 时，普通数字（例如 `float`）通常称为 scalar。Scalar 只有“大小”，而 Vector 同时具有大小和方向。

Vector 与 scalar 相乘后，结果 Vector 的方向与原 Vector 相同，但大小变为原大小乘以该 scalar。Scalar 除法同理，会将原 Vector 的大小除以该 scalar。

这些运算适合用于表示移动偏移或力的 Vector。它们可以改变 Vector 的大小，而不影响方向。

任何 Vector 除以自身大小后，结果都是大小为 1 的 Vector，称为 normalized Vector。将 normalized Vector 与 scalar 相乘，结果的大小就等于该 scalar。这适用于力的方向固定、但强度可调的情况，例如汽车车轮始终向前施力，但施力大小由驾驶员控制。

## Dot product

Dot product 接收两个 Vector，并返回一个 scalar。该 scalar 等于两个 Vector 的大小相乘，再乘以它们夹角的余弦值。当两个 Vector 都已归一化时，余弦值可以表示第一个 Vector 在第二个 Vector 方向上的延伸程度；反过来理解也一样，因为参数顺序不影响 Dot product 结果。

下图对比了不同角度的 Vector 与参考 Vector 进行 Dot product 后，返回的 `1` 到 `-1` 之间的值：

![不同角度的 Dot product 值](DotProduct.png)

![余弦值与 Vector 夹角的关系](CosineValues.png)

Dot product 的数学运算比计算余弦更简单，因此在某些情况下可以代替 `Mathf.Cos` 或 Vector 大小运算。它并不完全等价，但有时可以产生相同的效果。Dot product 的计算耗时要少得多，因此可以作为有效的优化手段。

如果需要计算一个 Vector 的大小中有多少部分位于另一个 Vector 的方向上，Dot product 很有用。

例如，汽车速度表通常通过测量车轮的旋转速度来工作。汽车可能并非正向移动，例如发生侧滑时，部分运动方向与车头方向不同，因此不会被速度表测量。物体 Rigidbody 的 `velocity` Vector 的大小表示总体运动方向上的速度；如果要单独得到车辆向前方向的速度，应使用 Dot product：

```csharp
var fwdSpeed = Vector3.Dot(rigidbody.velocity, transform.forward);
```

方向可以是任意方向，但用于此计算的方向 Vector 必须始终是 normalized Vector。这样不仅比直接使用速度大小更准确，也避免了计算大小时所需的平方根运算。

## Cross product

Cross product 只对 3D Vector 有意义。它接收两个 3D Vector，并返回另一个 3D Vector。

结果 Vector 垂直于两个输入 Vector。可以使用“左手螺旋规则”记住输入顺序如何决定输出方向：如果手指按照输入 Vector 的顺序弯曲，拇指所指的方向就是输出 Vector 的方向。如果反转参数顺序，结果 Vector 的方向会完全相反，但大小相同。

结果大小等于两个输入 Vector 的大小相乘，再乘以它们夹角的正弦值：

![正弦值与 Vector 夹角的关系](SineValues.png)

Cross product 的返回值同时包含多个有用信息，因此看起来可能比较复杂。不过和 Dot product 一样，它在数学上非常高效，可以用来优化原本依赖正弦、余弦等较慢超越函数的代码。

## 计算法线或垂直 Vector

在生成 Mesh 时，经常需要“法线”Vector，也就是垂直于平面的 Vector。路径跟随和其他场景中也会使用它。给定平面上的三个点，例如 Mesh 三角形的三个角点，可以按以下步骤计算法线：

1. 选择三个点中的一个。
2. 分别用另外两个点减去它，得到两个新 Vector，即 `Side 1` 和 `Side 2`。
3. 计算 `Side 1` 和 `Side 2` 的 Cross product。
4. Cross product 的结果是一个垂直于原三个点所在平面的新 Vector，也就是法线。

```csharp
Vector3 a;
Vector3 b;
Vector3 c;

Vector3 side1 = b - a;
Vector3 side2 = c - a;
Vector3 normal = Vector3.Cross(side1, side2);
```

![根据三角形三个点计算法线](CalculateNormal.png)

可以使用左手来判断计算 Cross product 时的输入顺序：食指和拇指彼此垂直伸展，中指伸向与它们所在平面垂直的第三个方向。食指和拇指分别代表 Cross product 的第一个和第二个输入 Vector，中指代表得到的法线。观察平面的上表面，也就是法线向外指的一面时，第一个 Vector 应沿顺时针方向转向第二个 Vector：

![使用左手规则确定 Cross product 输入顺序](LeftHandRuleDiagram.png)

如果反转两个输入 Vector 的顺序，结果会指向完全相反的方向。

对于 Mesh，法线 Vector 还必须归一化。可以使用 `normalized` 属性，也可以通过除以大小进行归一化：

```csharp
float perpLength = perp.magnitude;
perp /= perpLength;
```

另一个有用的结论是，三角形面积等于 `perpLength / 2`。如果需要计算整个 Mesh 的表面积，或者想根据三角形相对面积的概率随机选择三角形，这个结论会很有用。

---

## 其他资源

- Vector2 API 参考
- Vector3 API 参考
- Vector4 API 参考

---

## 文档导航

- 上一页：[[00-Unity Engine数学API]]
- 目录：[[00-Unity Engine数学API]]
- 下一页：[[01-使用Mathf进行常见数学运算]]
