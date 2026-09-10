# 使用 Quaternion 控制旋转

> 原文：[Controlling rotation with the Quaternion class](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Quaternion.html)

Unity 使用 [`Quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.html) 类存储 GameObject 的三维朝向，并描述从一个朝向到另一个朝向的相对旋转。在 Unity 中，可以使用 Euler 角和 Quaternion 表示旋转与朝向。这两种表示方式是等效的，但用途和限制不同。

通常，可以使用场景中的 [Transform 组件](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Transform.html)旋转对象，Transform 会将朝向显示为 Euler 角。不过，Unity 在内部使用 Quaternion 存储旋转和朝向。对于更复杂的运动，Quaternion 可以避免一些本来可能导致万向节锁的问题。

坐标系描述对象在三维空间中的位置。Unity 使用左手坐标系：正 x 轴指向右侧，正 y 轴指向上方，正 z 轴指向前方。这意味着沿正 z 轴观察时，从正 x 轴向正 y 轴旋转的方向是逆时针。

![Unity 左手坐标系与旋转方向](图片/unity-axis-with-rotation.png)

> [!NOTE]
> 上图展示了 Unity 左手坐标系的各个轴，以及沿正 z 轴观察时，从正 x 轴向正 y 轴旋转的逆时针方向。

## Euler 角

在 Transform 组件中，Unity 使用 Vector 属性 [`Transform.eulerAngles`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.eulerAngles.html) 的 X、Y 和 Z 显示旋转。与普通 Vector 不同，这些值表示绕 X、Y 和 Z 轴旋转的角度，单位是度。

Euler 角旋转会分别绕三个轴执行三次旋转。Unity 依次先绕 z 轴旋转，然后绕 x 轴旋转，最后绕 y 轴旋转。这种方法称为外旋（extrinsic rotation）；旋转发生时，原始坐标系不会改变。

要旋转 GameObject，可以在其 Transform 组件中输入每个轴要旋转的角度。要通过代码旋转 GameObject，请使用 [`Transform.eulerAngles`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.eulerAngles.html)。

如果将旋转转换为 Euler 角来进行计算和旋转，就可能遇到万向节锁问题。万向节锁是指三维空间中的对象失去一个自由度，只能在两个维度内旋转。当两个轴变得平行时，Euler 角可能发生万向节锁。如果脚本中不将旋转值转换为 Euler 角，使用 Quaternion 就可以避免万向节锁。

如果确实遇到万向节锁，可以使用 [`Transform.RotateAround`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.RotateAround.html) 执行旋转，从而避免使用 Euler 角。也可以在每个轴上使用 [`Quaternion.AngleAxis`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.AngleAxis.html)，再将它们相乘（Quaternion 乘法会依次应用各个旋转）。

## Quaternion

Quaternion 为三维空间中的空间朝向和旋转提供唯一表示的数学记法。Quaternion 使用四个数编码三维单位轴周围的旋转方向和角度。这四个值是复数，而不是角度或度数。

Unity 将旋转值转换为 Quaternion 进行存储，因为 Quaternion 旋转的计算高效且稳定。Unity Editor 不会将旋转显示为 Quaternion，因为单个 Quaternion 无法表示绕任意轴超过 360 度的旋转。

如果使用 [`Quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.html) 类，就可以直接使用 Quaternion。要通过代码控制旋转，可以使用 Quaternion 类及其函数创建和修改旋转值。可以将值作为 Euler 角应用到旋转中，但仍需要将其存储为 Quaternion，以避免出现问题。

## 在 Euler 角和 Quaternion 之间转换

可以使用以下方法在 Quaternion 和 Euler 角之间转换，以便从代码中查看和编辑旋转：

- 要将 Euler 角转换为 Quaternion，可以使用 [`Quaternion.Euler`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.Euler.html) 方法。
- 要将 Quaternion 转换为 Euler 角，可以使用 [`Quaternion.eulerAngles`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.eulerAngles.html) 方法。

在脚本中处理旋转时，应使用 `Quaternion` 类及其函数创建和修改旋转值。在某些情况下使用 Euler 角是合理的，但请注意：

- 使用处理 Euler 角的 Quaternion 类函数。
- 从旋转中获取、修改并重新应用 Euler 值，可能造成意外的副作用。

## 直接创建和操作 Quaternion

Unity 的 `Quaternion` 类提供了许多无需使用 Euler 角即可创建和操作旋转的函数，大多数情况下建议使用这些函数。

有关创建旋转的信息（包括代码示例），请参阅以下方法的 API 参考：

- [`Quaternion.LookRotation`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.LookRotation.html)
- [`Quaternion.Angle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.Angle.html)
- [`Quaternion.AngleAxis`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.AngleAxis.html)
- [`Quaternion.FromToRotation`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.FromToRotation.html)

有关操作旋转的信息（包括代码示例），请参阅以下方法的 API 参考：

- [`Quaternion.Slerp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.Slerp.html)
- [`Quaternion.Inverse`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.Inverse.html)
- [`Quaternion.RotateTowards`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.RotateTowards.html)

[`Transform`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html) 类也提供了处理 Quaternion 旋转的方法：

- [`Transform.Rotate`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.Rotate.html)
- [`Transform.RotateAround`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.RotateAround.html)

## 使用 Euler 角

在某些情况下，最好在脚本中使用 Euler 角。此时必须将角度保存在变量中，只将它们作为 Euler 角应用到旋转上，而旋转最终仍应存储为 `Quaternion`。虽然可以从 Quaternion 获取 Euler 角，但如果获取、修改并重新应用这些值，很可能会出现问题。有关这些问题的成因，请参阅 [`eulerAngles`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion-eulerAngles.html) 脚本参考页面。

下面的示例展示了如何在代码中正确使用 Euler 角：

```csharp
// Rotation scripting with Euler angles correctly.
// Store the Euler angle in a class variable, and only use it to
// apply it as an Euler angle, but never rely on reading the Euler back.
        
float x;
void Update () 
{
    x += Time.deltaTime * 10;
    transform.rotation = Quaternion.Euler(x,0,0);
}
```

## 其他资源

- [`Quaternion` API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.html)


---

## 文档导航

- 上一页：[[03-使用Random类生成随机数]]
- 目录：[[00-Unity Engine数学API]]
- 下一页：[[../03-Unity Mathematics API]]
