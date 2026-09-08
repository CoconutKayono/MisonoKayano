# 设置、选项与回调（四）：Tweener 专用设置与选项

以下设置仅适用于 **Tweener**，对 Sequence 无效。除 `SetEase` 外，在补间运行期间链式调用这些设置不会生效。

## From —— 变成 FROM 补间

```cs
From(bool isRelative = false)
```

将 Tweener 变为 FROM 补间（而不是普通的 TO 补间）：目标会立刻被送到指定值，然后再补间回它之前的值。

- 必须链式调用在任何其他设置之前（补间特定选项除外）。
- **isRelative**：`TRUE` = 设为相对补间（FROM 值按 `currentValue + endValue` 计算，而不是直接使用）。对 FROM 补间，请用这个参数而不是 `SetRelative`。

```cs
// 普通 TO 补间
transform.DOMoveX(2, 1);
// FROM 补间
transform.DOMoveX(2, 1).From();
// FROM 补间 + 相对 FROM 值
transform.DOMoveX(2, 1).From(true);
```

## From —— 直接指定起始值

```cs
From(T fromValue, bool setImmediately = true, bool isRelative = false)
```

直接设置补间的起始值，而不依赖补间开始时目标的当前值。

- 必须链式调用在任何其他设置之前（补间特定选项除外）。
- **fromValue**：补间开始的值。
- **setImmediately**：`TRUE` = 目标立即被设为 fromValue；`FALSE` = 等到补间开始。
- **isRelative**：`TRUE` = 设为相对补间（FROM 值按 `currentValue + fromValue` 计算）。

## SetDelay —— 延迟启动

```cs
SetDelay(float delay)
```

设置补间的延迟启动。若补间已经开始则无效。

链式挂接到 Sequence 上时，并不会添加真正的延迟，而只是在序列开头追加一段间隔（等同于 `PrependInterval`）。可用下方的重载改变这一行为。

```cs
transform.DOMoveX(4, 1).SetDelay(1);
```

```cs
SetDelay(float delay, bool asPrependedIntervalIfSequence)
```

设置延迟启动，并可在 Sequence 情况下选择延迟的应用方式。若补间已经开始则无效。

- **asPrependedIntervalIfSequence**：仅 Sequence 使用。`FALSE` = 延迟只发生一次（Tweener 默认此行为）；`TRUE` = 作为序列间隔，在每个循环周期开始时重复。

```cs
transform.DOMoveX(4, 1).SetDelay(1);
```

## SetSpeedBased —— 基于速度

```cs
SetSpeedBased(bool isSpeedBased = true)
```

`TRUE` = 将补间设为基于速度（duration 表示补间每秒移动的单位/角度数）。

> [!NOTE]
> 如果希望速度恒定，请同时把缓动设为 `Ease.Linear`。

若补间已经开始，或它是 Sequence（或 Sequence 内的嵌套补间），则无效。

```cs
transform.DOMoveX(4, 1).SetSpeedBased();
```

## SetOptions —— 补间专用选项

某些 Tweener 拥有特殊的专用选项，具体取决于你补间的对象类型。这一切都是自动的：如果某个 Tweener 有特殊选项，它就会有对应的 `SetOptions` 方法，否则就没有。

- 这些选项通常只有通过泛型方式创建补间时才可用；快捷方式已经在创建方法中内置了同样的选项。
- 重点：其他设置可以任意顺序链式调用，但 `SetOptions` 必须紧跟在创建补间的函数之后，否则就不再可用了。

### 泛型补间的专用选项

#### Color 补间

```cs
SetOptions(bool alphaOnly)
```

`alphaOnly`：`TRUE` = 只补间颜色的 alpha。

```cs
DOTween.To(()=> myColor, x=> myColor = x, new Color(1,1,1,0), 1).SetOptions(true);
```

#### float 补间

```cs
SetOptions(bool snapping)
```

`snapping`：`TRUE` = 数值平滑吸附到整数。

```cs
DOTween.To(()=> myFloat, x=> myFloat = x, 45, 1).SetOptions(true);
```

#### Quaternion 补间

```cs
SetOptions(bool useShortest360Route)
```

`useShortest360Route`：`TRUE`（默认）= 旋转走最短路径，不会超过 360°；`FALSE` = 完整计算旋转。若补间为相对模式，则始终为 `FALSE`。

```cs
DOTween.To(()=> myQuaternion, x=> myQuaternion = x, new Vector3(0,180,0), 1).SetOptions(true);
```

#### Rect 补间

```cs
SetOptions(bool snapping)
```

`snapping`：`TRUE` = 数值平滑吸附到整数。

```cs
DOTween.To(()=> myRect, x=> myRect = x, new Rect(0,0,10,10), 1).SetOptions(true);
```

#### String 补间

```cs
SetOptions(bool richTextEnabled, ScrambleMode scrambleMode = ScrambleMode.None, string scrambleChars = null)
```

- **richTextEnabled**：`TRUE`（默认）= 动画时正确解析富文本；`FALSE` = 所有标签视为普通文本。
- **scrambleMode**：乱序模式。若非 `None`，字符串将以随机字符动画呈现；否则正常逐字拼出。
  - `None`（默认）：不乱序。
  - `All` / `Uppercase` / `Lowercase` / `Numerals`：乱序时使用的字符类型。
  - `Custom`：使用 `scrambleChars` 中的自定义字符。
- **scrambleChars**：自定义乱序字符集合。字符越多越好（至少 10 个），因为 DOTween 使用快速乱序模式，字符越多效果越好。

```cs
DOTween.To(()=> myString, x=> myString = x, "hello world", 1).SetOptions(true, ScrambleMode.All);
```

#### Vector2/3/4 补间

```cs
SetOptions(AxisConstraint constraint, bool snapping)
```

- **constraint**：只动画指定的轴。
- **snapping**：`TRUE` = 数值平滑吸附到整数（很适合像素级移动）。

```cs
DOTween.To(()=> myVector, x=> myVector = x, new Vector3(2,2,2), 1).SetOptions(AxisConstraint.Y, true);
```

#### Vector3Array 补间

```cs
SetOptions(bool snapping)
```

`snapping`：`TRUE` = 数值平滑吸附到整数（很适合像素级移动）。

```cs
DOTween.ToArray(()=> myVector, x=> myVector = x, myEndValues, myDurations).SetOptions(true);
```

### DOPath 专用选项

#### Path 补间 SetOptions

```cs
SetOptions(bool closePath, AxisConstraint lockPosition = AxisConstraint.None, AxisConstraint lockRotation = AxisConstraint.None)
```

- **closePath**：`TRUE` = 自动闭合路径。
- **lockPosition**：要锁定的移动轴，多轴用 `|` 分隔，如 `AxisConstraint.X | AxisConstraint.Y`。
- **lockRotation**：要锁定的旋转轴，写法同上。

```cs
transform.DOPath(path, 4f).SetOptions(true, AxisConstraint.X);
```

#### Path 补间 SetLookAt

```cs
SetLookAt(Vector3 lookAtPosition/lookAtTarget/lookAhead, Vector3 forwardDirection, Vector3 up, bool stableZRotation)
```

路径补间的附加 LookAt 选项。根据所选重载：

- a) 让目标朝向指定位置；
- b) 让目标朝向指定 Transform；
- c) 按给定 lookAhead 让目标沿路径向前看。

必须直接链式调用在补间创建方法或 `SetOptions` 方法之后。

- **lookAtPosition**：要朝向的位置。
- **lookAtTarget**：要朝向的目标。
- **lookAhead**：沿路径朝向的提前量百分比（0 到 1）。
- **forwardDirection**（可选重载）：视为"前方"的方向，默认是 Transform 的常规前方。
- **up**（可选重载）：定义"上"方向的向量，默认 `Vector3.up`。
- **stableZRotation**（可选重载）：`TRUE` = 不沿 Z 轴旋转目标。

```cs
transform.DOPath(path, 4f).SetLookAt(new Vector3(2,1,3));
transform.DOPath(path, 4f).SetLookAt(someOtherTransform);
transform.DOPath(path, 4f).SetLookAt(0.01f);
```

## TweenParams —— 参数包

如果你用过 HOTween，应该认识 `TweenParms`（现在叫 `TweenParams`）：它用来存储设置，以便应用到多个补间。与 HOTween 不同的是，它现在完全不是必需的——因为设置可以直接链式调用在补间上，它只是作为一个额外的工具类存在。

用法：创建一个新的 `TweenParams` 实例（或 `Clear()` 一个已有的），然后像普通链式调用一样添加设置，最后用 `SetAs` 应用到补间上。

```cs
// 存储一个"无限循环 + 弹性缓动"的设置
TweenParams tParms = new TweenParams().SetLoops(-1).SetEase(Ease.OutElastic);
// 应用到几个补间上
transformA.DOMoveX(15, 1).SetAs(tParms);
transformB.DOMoveY(10, 1).SetAs(tParms);
```

## 更多链式写法

不必一次只链一个设置，可以这样写：

```cs
transform.DOMoveX(45, 1).SetDelay(2).SetEase(Ease.OutQuad).OnComplete(MyCallback);
```
