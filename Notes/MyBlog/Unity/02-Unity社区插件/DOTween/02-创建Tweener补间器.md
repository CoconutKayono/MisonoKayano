# 创建 Tweener（补间器）

> 本文翻译自 DOTween 官方文档「Creating a Tweener」，方法签名保留原文。

## 本文结构

- [[#一、创建方式]]
- [[#二、快捷方式速查]]
- [[#三、相关文档]]

---

## 一、创建方式

### 简介

Tweener 是 DOTween 的“工蚁”：它接管某个属性/字段，并将其向目标值做平滑过渡。

目前 DOTween 支持对以下类型执行补间：

- `float`、`double`、`int`、`uint`、`long`、`ulong`
- `Vector2` / `Vector3` / `Vector4`、`Quaternion`
- `Rect`、`RectOffset`、`Color`、`string`

（其中部分类型还支持特殊的补间方式。）

此外，你也可以编写自定义的 DOTween 插件，为自定义的值类型提供补间能力。

创建 Tweener 共有以下方式：

| 方式 | 说明 |
| --- | --- |
| [[#A. 泛型方式]] | 最灵活，几乎可以补间任何值 |
| [[#B. 快捷方式]] | 从已知对象（Transform、Material 等）直接启动 |
| [[#C. 其他泛型方式]] | 以特定方式补间数值（Punch、Shake、ToAlpha 等） |
| [[#虚拟补间（Virtual Tween）]] | 不绑定真实属性，通过 setter 驱动“虚拟值” |

### A. 泛型方式

泛型方式是最灵活的补间方式，几乎可以补间任何值——无论是公有还是私有属性、静态还是动态值（顺便一提，快捷方式在底层其实也是借助泛型方式实现的）。

与快捷方式一样，泛型方式也有对应的 FROM 变体。只需在 Tweener 上链式追加 `From`，就能把原本的“TO 补间”变成“FROM 补间”。

```cs
static DOTween.To(getter, setter, to, float duration)
```

将指定属性从当前值过渡到目标值。参数说明：

- **getter**：获取待补间属性值的委托，可写成 lambda：`()=> myValue`（`myValue` 为待补间属性的名称）。
- **setter**：设置待补间属性值的委托，可写成 lambda：`x=> myValue = x`（`myValue` 为待补间属性的名称）。
- **to**：需要到达的终点值。
- **duration**：补间时长。

示例：

```cs
// 在 1 秒内将 Vector3 类型的 myVector 过渡到 (3,4,8)
DOTween.To(()=> myVector, x=> myVector = x, new Vector3(3,4,8), 1);

// 在 1 秒内将 float 类型的 myFloat 过渡到 52
DOTween.To(()=> myFloat, x=> myFloat = x, 52, 1);

// 立刻将 float 类型的 myFloat 跳到 52，然后在 1 秒内将 52 过渡到当前值
DOTween.To(() => myFloat, x => myFloat = x, 52, 1).From();
```

### B. 快捷方式

DOTween 为一些常用的 Unity 对象内置了快捷方式，例如 `Transform`、`Rigidbody` 和 `Material`。你可以直接从这些对象的引用上启动补间（同时该对象也会被自动设为补间的目标）：

```cs
transform.DOMove(new Vector3(2,3,4), 1);
rigidbody.DOMove(new Vector3(2,3,4), 1);
material.DOColor(Color.green, 1);
```

除特别说明外，每个快捷方式也都有对应的 FROM 变体。只需在 Tweener 上链式追加 `From`，即可将“TO 补间”变成“FROM 补间”。

> [!IMPORTANT]
> 一旦给补间指定了 FROM，目标会立刻跳到 FROM 位置——这里的“立刻”指“写下行代码的那一刻”，而不是“补间启动的那一刻”。

```cs
transform.DOMove(new Vector3(2,3,4), 1).From();
rigidbody.DOMove(new Vector3(2,3,4), 1).From();
material.DOColor(Color.green, 1).From();
```

### C. 其他泛型方式

除泛型与快捷方式外，DOTween 还提供了一些以特定方式补间数值的泛型方法。它们同样支持 FROM 变体（除特别说明外）——只需在 Tweener 上链式追加 `From`，即可将“TO 补间”变为“FROM 补间”。

#### Punch（冲击）

```cs
static DOTween.Punch(getter, setter, Vector3 direction, float duration, int vibrato, float elasticity)
```

**无 FROM 变体。** 将 `Vector3` 沿指定方向冲击，再弹回起始位置，就像起始位置用弹性绳牵着它一样。

- **getter**：获取待补间属性值的委托，可写成 lambda：`()=> myValue`（`myValue` 为待补间属性的名称）。
- **setter**：设置待补间属性值的委托，可写成 lambda：`x=> myValue = x`。
- **direction**：冲击的方向与强度。
- **duration**：补间时长。
- **vibrato**：冲击的振动次数。
- **elasticity**：回弹时超出起始位置的程度（0~1）。1 表示在指定方向与相反的衰减方向之间完全振荡；0 则只在起始位置与衰减方向之间振荡。

```cs
// 在 1 秒内将名为 myVector 的 Vector3 向上冲击
DOTween.Punch(()=> myVector, x=> myVector = x, Vector3.up, 1);
```

#### Shake（晃动）

```cs
static DOTween.Shake(getter, setter, float duration, float/Vector3 strength, int vibrato, float randomness, bool ignoreZAxis)
```

**无 FROM 变体。** 以给定参数晃动一个 `Vector3` 的 X、Y 轴。

- **getter / setter**：同上。
- **duration**：补间时长。
- **strength**：晃动强度。使用 `Vector3` 代替 `float` 时，可以为每个轴单独设置强度。
- **vibrato**：晃动每秒振动的次数。
- **randomness**：晃动的随机程度（0~360——高于 90 的值效果不太好，慎用）。设为 0 时沿单一方向晃动，行为类似随机冲击。
- **ignoreZAxis**：若为 `TRUE` 只沿 X、Y 轴晃动（使用 `Vector3` 作为强度时不可用）。

```cs
// 在 1 秒内晃动名为 myVector 的 Vector3
DOTween.Shake(()=> myVector, x=> myVector = x, 1, 5, 10, 45, false);
```

#### ToAlpha（透明度补间）

```cs
static DOTween.ToAlpha(getter, setter, float to, float duration)
```

将 `Color` 的 alpha 从当前值补间到指定值。

- **to**：目标值。
- **duration**：补间时长。

```cs
// 在 1 秒内将名为 myColor 的颜色 alpha 补间到 0
DOTween.ToAlpha(()=> myColor, x=> myColor = x, 0, 1);
```

#### ToArray（分段补间）

```cs
static DOTween.ToArray(getter, setter, Vector3[] endValues, float[] durations)
```

**无 FROM 变体。** 将 `Vector3` 依次补间到给定的各段目标值。缓动（Ease）作用于每一段，而不是整体。（注：官方文档的签名行有笔误，实际参数为 `endValues` 与 `durations`，见下方示例。）

- **endValues**：每一段要到达的目标值数组，长度必须与 `durations` 相同。
- **durations**：每一段的时长数组，长度必须与 `endValues` 相同。

```cs
// 让 myVector 依次经过 3 个值，每段 1 秒
Vector3[] endValues = new[] { new Vector3(1,0,1), new Vector3(2,0,2), new Vector3(1,4,1) };
float[] durations = new[] { 1, 1, 1 };
DOTween.ToArray(()=> myVector, x=> myVector = x, endValues, durations);
```

#### ToAxis（单轴补间）

```cs
static DOTween.ToAxis(getter, setter, float to, float duration, AxisConstraint axis)
```

将 `Vector3` 的单个轴从当前值补间到指定值。

- **to**：目标值。
- **duration**：补间时长。
- **axis**：要补间的轴。

```cs
// 在 1 秒内将 myVector 的 X 补间到 3
DOTween.ToAxis(()=> myVector, x=> myVector = x, 3, 1);
// 同上，但改为补间 Y 轴
DOTween.ToAxis(()=> myVector, x=> myVector = x, 3, 1, AxisConstraint.Y);
```

### 虚拟补间（Virtual Tween）

```cs
static DOTween.To(setter, float startValue, float endValue, float duration)
```

从一个起始值到结束值补间一个“虚拟属性”，并通过 `setter` 将中间值交给外部方法或 lambda 使用。

- **setter**：对补间值执行的操作。
- **startValue**：起始值。
- **endValue**：目标值。
- **duration**：虚拟补间的时长。

```cs
DOTween.To(MyMethod, 0, 12, 0.5f);
// 其中 MyMethod 是一个接受 float 参数的函数
// （该参数即为虚拟补间产出的值）

// 或者使用 lambda
DOTween.To(x => someProperty = x, 0, 12, 0.5f);
```

---

## 二、快捷方式速查

> [!NOTE] 通用约定
>
> - 除特别标注外，所有快捷方式都有对应的 FROM 变体（链式追加 `From` 即可）。
> - 标注「无 FROM 变体」的方法例外，如 Punch、Shake、Path 系列。
> - `snapping` 参数：`TRUE` 时数值平滑吸附到整数（适合像素级移动）。
> - **Blendable 补间**：以可混合的方式补间——多个同类补间可在同一目标上协同工作，而不是像普通补间那样互相覆盖。

### Unity 基础组件

#### AudioMixer（Unity 5）

> [!NOTE] AudioMixer
> ```cs
> DOSetFloat(string floatName, float to, float duration)
> ```
> 将 `AudioMixer` 中已暴露的浮点参数补间到指定值。  
> 注意：你需要先在 `AudioMixerGroup` 中手动暴露一个浮点参数，之后才能通过 `AudioMixer` 对其进行补间。
> ```cs
> public class AudioFadeExample : MonoBehaviour
> {
>     [SerializeField] private AudioMixer mixer;          // 拖入你的 AudioMixer 资源
>     [SerializeField] private string exposedParam = "MasterVolume"; // 暴露的参数名
> 
>     void Start()
>     {
>         // 示例：2秒内将主音量渐变到 -20dB
>         mixer.DOSetFloat(exposedParam, -20f, 2f);
>         
>         // 也可链式加入回调，在淡出完成后执行操作
>         mixer.DOSetFloat(exposedParam, -80f, 1.5f)
>              .SetEase(Ease.InQuad)
>              .OnComplete(() => Debug.Log("静音完成"));
>     }
> }
> ```

#### AudioSource（音频源）

| 方法 | 说明 |
| --- | --- |
| `DOFade(float to, float duration)` | 将 `volume`（音量）补间到指定值。 |
| `DOPitch(float to, float duration)` | 将 `pitch`（音调）补间到指定值。 |

#### Camera（相机）

| 方法 | 说明 |
| --- | --- |
| `DOAspect(float to, float duration)` | 补间 `aspect`（宽高比）。 |
| `DOColor(Color to, float duration)` | 补间 `backgroundColor`（背景色）。 |
| `DOFarClipPlane(float to, float duration)` | 补间 `farClipPlane`（远裁剪面）。 |
| `DOFieldOfView(float to, float duration)` | 补间 `fieldOfView`（视野）。 |
| `DONearClipPlane(float to, float duration)` | 补间 `nearClipPlane`（近裁剪面）。 |
| `DOOrthoSize(float to, float duration)` | 补间 `orthographicSize`（正交尺寸）。 |
| `DOPixelRect(Rect to, float duration)` | 补间 `pixelRect`。 |
| `DORect(Rect to, float duration)` | 补间 `rect`。 |
| `DOShakePosition(float duration, float/Vector3 strength, int vibrato, float randomness, bool fadeOut, ShakeRandomnessMode randomnessMode)` | **无 FROM 变体。** 沿相对 X/Y 轴晃动 `localPosition`。 |
| `DOShakeRotation(float duration, float/Vector3 strength, int vibrato, float randomness, bool fadeOut, ShakeRandomnessMode randomnessMode)` | **无 FROM 变体。** 晃动 `localRotation`。 |

**Shake 系列参数说明：**

- `strength`：晃动强度；使用 `Vector3` 可为每个轴单独设置强度。
- `vibrato`：每秒振动次数。
- `randomness`：随机程度（0~180，高于 90 效果较差）；设为 0 时沿单一方向晃动。
- `fadeOut`（默认 `true`）：是否在补间时长内平滑衰减。
- `randomnessMode`（默认 `Full`）：随机类型，`Full`（完全随机）或 `Harmonic`（更均衡、观感更好）。
- 注意：用 `Vector3` 强度只晃动单轴旋转时，`randomness` 至少应保持 90。

#### Light（灯光）

| 方法 | 说明 |
| --- | --- |
| `DOColor(Color to, float duration)` | 将灯光颜色补间到指定值。 |
| `DOIntensity(float to, float duration)` | 将灯光强度补间到指定值。 |
| `DOShadowStrength(float to, float duration)` | 将灯光阴影强度补间到指定值。 |
| `DOBlendableColor(Color to, float duration)` | Blendable 补间：颜色可混合，多个补间可协同工作。 |

#### LineRenderer

| 方法 | 说明 |
| --- | --- |
| `DOColor(Color2 startValue, Color2 endValue, float duration)` | 将 LineRenderer 的颜色补间到指定值。 |

由于 LineRenderer 无法自行读取颜色，必须同时传入起始颜色与结束颜色。`Color2` 是 DOTween 的专用结构，可以在一个变量中存放两种颜色。

```cs
myLineRenderer.DOColor(new Color2(Color.white, Color.white), new Color2(Color.green, Color.black), 1);
```

#### Material（材质）

| 方法 | 说明 |
| --- | --- |
| `DOColor(...)`（3 个重载） | 补间材质整体颜色，或指定名称/ID 的颜色属性。 |
| `DOFade(...)`（3 个重载） | 淡入淡出 alpha（仅支持带 alpha 的材质），或指定名称/ID 的 alpha 属性。 |
| `DOFloat(...)`（2 个重载） | 补间指定名称/ID 的 float 属性。 |
| `DOGradientColor(...)`（3 个重载） | 通过渐变（Gradient）补间颜色，见下方注意点。 |
| `DOOffset(...)`（3 个重载） | 补间 `textureOffset`（纹理偏移）。 |
| `DOTiling(...)`（3 个重载） | 补间 `textureScale`（纹理缩放）。 |
| `DOVector(...)`（2 个重载） | 补间指定名称/ID 的 Vector 属性。 |
| `DOBlendableColor(...)`（3 个重载） | Blendable 补间：颜色可混合，多个补间可协同工作。 |

完整签名：

```cs
DOColor(Color to, float duration)
DOColor(Color to, string property, float duration)
DOColor(Color to, int propertyID, float duration)
DOFade(float to, float duration)
DOFade(float to, string property, float duration)
DOFade(float to, int propertyID, float duration)
DOFloat(float to, string property, float duration)
DOFloat(float to, int propertyID, float duration)
DOGradientColor(Gradient to, float duration)
DOGradientColor(Gradient to, string property, float duration)
DOGradientColor(Gradient to, int propertyID, float duration)
DOOffset(Vector2 to, float duration)
DOOffset(Vector2 to, string property, float duration)
DOOffset(Vector2 to, int propertyID, float duration)
DOTiling(Vector2 to, float duration)
DOTiling(Vector2 to, string property, float duration)
DOTiling(Vector2 to, int propertyID, float duration)
DOVector(Vector4 to, string property, float duration)
DOVector(Vector4 to, int propertyID, float duration)
DOBlendableColor(Color to, float duration)
DOBlendableColor(Color to, string property, float duration)
DOBlendableColor(Color to, int propertyID, float duration)
```

> [!NOTE] DOGradientColor 注意点
> - 只使用渐变的颜色，不使用 alpha。
> - 创建的是 **Sequence 而非 Tweener**。
> - 仅支持 Unity 4.3 及以上版本（Gradient 类此前不存在）。

通用参数：`property` 为属性名（如 `"_SpecColor"`），`propertyID` 为属性 ID。

```cs
// 补间材质的镜面颜色
myMaterial.DOColor(Color.green, "_SpecColor", 1);
myMaterial.DOGradientColor(myGradient, "_SpecColor", 1);
myMaterial.DOBlendableColor(Color.green, "_SpecColor", 1);
```

#### Rigidbody（刚体）

以下快捷方式在底层使用 rigidbody 的 `MovePosition` / `MoveRotation` 方法，以保证物理对象相关动画的正确性。

| 分组 | 方法 | 说明 |
| --- | --- | --- |
| 移动 | `DOMove(Vector3 to, float duration, bool snapping)` | 将刚体位置补间到指定值。 |
| 移动 | `DOMoveX/DOMoveY/DOMoveZ(float to, float duration, bool snapping)` | 仅补间所选轴（其他轴仍会被补间“锁定”）。 |
| 移动 | `DOJump(Vector3 endValue, float jumpPower, int numJumps, float duration, bool snapping)` | 沿 Y 轴跳跃。**返回 Sequence 而非 Tweener**，`SetSpeedBased` 无效。 |
| 旋转 | `DORotate(Vector3 to, float duration, RotateMode mode)` | 旋转到指定值（需 Vector3，mode 见下）。 |
| 旋转 | `DOLookAt(Vector3 towards, float duration, AxisConstraint axisConstraint = AxisConstraint.None, Vector3 up = Vector3.up)` | 旋转刚体使其朝向指定位置。 |
| 路径 | `DOPath(...)` / `DOLocalPath(...)` | 沿路径点补间位置（世界/本地）。**无 FROM 变体。** |
| 螺旋 | `DOSpiral(...)` | 螺旋轨迹移动。**仅限 PRO 版，无 FROM 变体。** |

> [!NOTE] DORotate 的 mode 参数
> - `Fast`（默认）：走最短路径，旋转不超过 360°。
> - `FastBeyond360`：旋转可超过 360°。
> - `WorldAxisAdd`：基于世界轴相加（类似 `transform.Rotate(Space.World)`），终值始终视为相对。
> - `LocalAxisAdd`：基于本地轴相加（类似 `transform.Rotate(Space.Self)`），终值始终视为相对。
> - `DORotate` 需要 Vector3 结束值；若想传 Quaternion，用 `myQuaternion.eulerAngles` 转换。

> [!NOTE] Path 系列参数（DOPath / DOLocalPath）
> - `pathType`：`Linear`（直线）/ `CatmullRom`（CatmullRom 曲线）/ `CubicBezier`（每个路径点带 2 个控制点的曲线）。
> - `pathMode`：决定 LookAt 的计算方式：`Ignore`（忽略）/ `3D` / 横版 2D / 俯视 2D。
> - `resolution`：路径分辨率（Linear 路径无效），越高曲线越精细但开销越大；默认 10，路径点之间没有大幅长曲线时 5 通常够用。
> - `gizmoColor`：路径颜色（运行且 Gizmos 开启时显示）。
> - 可通过 `SetOptions` 和 `SetLookAt` 附加选项。
> - **CubicBezier 规则**：路径点数量必须是 3 的倍数，每组 3 个依次为：路径点、IN 控制点（前一路径点的控制点）、OUT 控制点（新路径点的控制点）。第一个路径点总是自动添加，由目标当前位置决定，且没有控制点。

> [!NOTE] DOSpiral 参数（仅限 PRO 版）
> `axis`：螺旋绕其旋转的轴；`mode`：螺旋运动类型；`speed`：旋转速度；`frequency`：旋转频率，越低螺旋越宽；`depth`：沿螺旋轴移动的距离；`snapping`：`TRUE` 时平滑吸附整数。

```cs
transform.DOSpiral(3, Vector3.forward, SpiralMode.ExpandThenContract, 1, 10);
```

#### Rigidbody2D（2D 刚体）

以下快捷方式在底层使用 rigidbody2D 的 `MovePosition` / `MoveRotation` 方法，以保证物理对象相关动画的正确性。

| 分组 | 方法 | 说明 |
| --- | --- | --- |
| 移动 | `DOMove(Vector2 to, float duration, bool snapping)` | 将刚体位置补间到指定值。 |
| 移动 | `DOMoveX/DOMoveY(float to, float duration, bool snapping)` | 仅补间所选轴。 |
| 移动 | `DOJump(Vector2 endValue, float jumpPower, int numJumps, float duration, bool snapping)` | 沿 Y 轴跳跃。**返回 Sequence 而非 Tweener。** |
| 旋转 | `DORotate(float toAngle, float duration)` | 旋转到指定角度。 |
| 路径 | `DOPath(...)` / `DOLocalPath(...)` | 沿路径点补间位置。**无 FROM 变体。** |

#### SpriteRenderer

| 方法 | 说明 |
| --- | --- |
| `DOColor(Color to, float duration)` | 将颜色补间到指定值。 |
| `DOFade(float to, float duration)` | 将 alpha 淡入淡出到指定值。 |
| `DOGradientColor(Gradient to, float duration)` | 通过渐变补间颜色（只用颜色不用 alpha；创建的是 Sequence 而非 Tweener）。 |
| `DOBlendableColor(Color to, float duration)` | Blendable 补间：颜色可混合，多个补间可协同工作。 |

#### TrailRenderer（拖尾渲染器）

| 方法 | 说明 |
| --- | --- |
| `DOResize(float toStartWidth, float toEndWidth, float duration)` | 将 `startWidth` / `endWidth`（起止宽度）补间到指定值。 |
| `DOTime(float to, float duration)` | 将 `time` 补间到指定值。 |

#### Transform（变换）

| 分组 | 方法 | 说明 |
| --- | --- | --- |
| 移动 | `DOMove(Vector3 to, float duration, bool snapping)` | 将位置补间到指定值。 |
| 移动 | `DOMoveX/DOMoveY/DOMoveZ(float to, float duration, bool snapping)` | 仅补间所选轴。 |
| 移动 | `DOLocalMove(Vector3 to, float duration, bool snapping)` | 补间 `localPosition`（本地位置）。 |
| 移动 | `DOLocalMoveX/DOLocalMoveY/DOLocalMoveZ(float to, float duration, bool snapping)` | 本地位置，仅补间所选轴。 |
| 移动 | `DOJump(Vector3 endValue, float jumpPower, int numJumps, float duration, bool snapping)` | 沿 Y 轴跳跃。**返回 Sequence 而非 Tweener。** |
| 移动 | `DOLocalJump(Vector3 endValue, float jumpPower, int numJumps, float duration, bool snapping)` | 本地位置版本。**返回 Sequence 而非 Tweener。** |
| 旋转 | `DORotate(Vector3 to, float duration, RotateMode mode)` | 旋转到指定值（Vector3；mode 同 Rigidbody）。 |
| 旋转 | `DORotateQuaternion(Quaternion to, float duration)` | 纯四元数旋转，见下方注意点。 |
| 旋转 | `DOLocalRotate(Vector3 to, float duration, RotateMode mode)` | 补间 `localRotation`。 |
| 旋转 | `DOLocalRotateQuaternion(Quaternion to, float duration)` | 本地四元数旋转。 |
| 旋转 | `DOLookAt(Vector3 towards, float duration, AxisConstraint axisConstraint = AxisConstraint.None, Vector3 up = Vector3.up)` | 朝向指定位置（补间开始时计算一次）。 |
| 旋转 | `DODynamicLookAt(Vector3 towards, float duration, AxisConstraint axisConstraint = AxisConstraint.None, Vector3 up = Vector3.up)` | **实验性。** 每帧更新朝向。 |
| 缩放 | `DOScale(float/Vector3 to, float duration)` | 缩放 `localScale`；传 `float` 可等比例缩放。 |
| 缩放 | `DOScaleX/DOScaleY/DOScaleZ(float to, float duration)` | 仅补间指定轴。 |
| 冲击 | `DOPunchPosition(Vector3 punch, float duration, int vibrato, float elasticity, bool snapping)` | 冲击 `localPosition`。**无 FROM 变体。** |
| 冲击 | `DOPunchRotation(Vector3 punch, float duration, int vibrato, float elasticity)` | 冲击 `localRotation`。**无 FROM 变体。** |
| 冲击 | `DOPunchScale(Vector3 punch, float duration, int vibrato, float elasticity)` | 冲击 `localScale`。**无 FROM 变体。** |
| 震动 | `DOShakePosition(float duration, float/Vector3 strength, int vibrato, float randomness, bool snapping, bool fadeOut, ShakeRandomnessMode randomnessMode)` | 晃动 `localPosition`。**无 FROM 变体。** |
| 震动 | `DOShakeRotation(float duration, float/Vector3 strength, int vibrato, float randomness, bool fadeOut, ShakeRandomnessMode randomnessMode)` | 晃动 `localRotation`。**无 FROM 变体。** |
| 震动 | `DOShakeScale(float duration, float/Vector3 strength, int vibrato, float randomness, bool fadeOut, ShakeRandomnessMode randomnessMode)` | 晃动 `localScale`。**无 FROM 变体。** |
| 路径 | `DOPath(...)` / `DOLocalPath(...)` | 沿路径点补间位置（世界/本地）。**无 FROM 变体。** |
| 混合 | `DOBlendableMoveBy(Vector3 by, float duration, bool snapping)` | 相对方式补间位置（BY 值），可混合。 |
| 混合 | `DOBlendableLocalMoveBy(Vector3 by, float duration, bool snapping)` | 相对方式补间本地位置，可混合。 |
| 混合 | `DOBlendableRotateBy(Vector3 by, float duration, RotateMode mode)` | **实验性。** 相对方式补间旋转，可混合。 |
| 混合 | `DOBlendableLocalRotateBy(Vector3 by, float duration, RotateMode mode)` | **实验性。** 相对方式补间本地旋转，可混合。 |
| 混合 | `DOBlendableScaleBy(Vector3 by, float duration)` | 相对方式补间缩放，可混合。 |
| 螺旋 | `DOSpiral(...)` | 让 `localPosition` 沿螺旋轨迹补间。**仅限 PRO 版，无 FROM 变体。** |

> [!NOTE] Transform 注意事项
> - `DORotate` 仅沿 X 轴做小角度旋转时，某些边界情况下目标会抖动，遇到时请改用 `DORotateQuaternion`。
> - `DORotateQuaternion` / `DOLocalRotateQuaternion`：`DORotate`（Vector3 版本）是首选；此方法仅用于特殊场景，且不支持 `LoopType.Incremental` 循环（自身或所在 Sequence 均不支持）。
> - Shake 系列参数与 Camera 相同（`strength` / `vibrato` / `randomness` / `fadeOut` / `randomnessMode`）；用 Vector3 强度只晃动单轴旋转时，`randomness` 至少保持 90。
> - Path 系列参数同 Rigidbody。注意：`DOPath` 也有 Rigidbody 版本，但在 Windows Phone/Store 上不可用。
> - Punch 通用参数：`punch`：冲击方向与强度（叠加到当前值上）；`vibrato`：振动次数；`elasticity`（0~1）：回弹超出起始值的程度，1 = 在冲击值与相反值之间完全振荡，0 = 只在冲击值与起始值之间振荡。
> - Blendable 以相对方式（BY 值）补间，多个同类补间可在同一目标上协同工作而非互相覆盖。

```cs
// 让目标移动 3,3,0，同时混合另一个循环 3 次的 -3,0,0 移动
// （默认 OutQuad 缓动）
transform.DOBlendableMoveBy(new Vector3(3, 3, 0), 3);
transform.DOBlendableMoveBy(new Vector3(-3, 0, 0), 1f).SetLoops(3, LoopType.Yoyo);
```

```cs
transform.DOSpiral(3, Vector3.forward, SpiralMode.ExpandThenContract, 1, 10);
```

#### Tween

这些快捷方式补间的其实是**其他补间的属性**——没想到吧 :P

| 方法 | 说明 |
| --- | --- |
| `DOTimeScale(float toTimeScale, float duration)` | 将补间的 `timeScale` 补间到指定值。 |

### Unity UI（uGUI 4.6）

#### CanvasGroup

| 方法 | 说明 |
| --- | --- |
| `DOFade(float to, float duration)` | 将目标的 alpha 淡入淡出到指定值。 |

#### Graphic

| 方法 | 说明 |
| --- | --- |
| `DOColor(Color to, float duration)` | 将颜色补间到指定值。 |
| `DOFade(float to, float duration)` | 将 alpha 淡入淡出到指定值。 |
| `DOBlendableColor(Color to, float duration)` | Blendable 补间：颜色可混合，多个补间可协同工作。 |

#### Image

| 方法 | 说明 |
| --- | --- |
| `DOColor(Color to, float duration)` | 将颜色补间到指定值。 |
| `DOFade(float to, float duration)` | 将 alpha 淡入淡出到指定值。 |
| `DOFillAmount(float to, float duration)` | 将 `fillAmount`（填充量，0~1）补间到指定值。 |
| `DOGradientColor(Gradient to, float duration)` | 通过渐变补间颜色（只用颜色不用 alpha；创建的是 Sequence 而非 Tweener）。 |
| `DOBlendableColor(Color to, float duration)` | Blendable 补间：颜色可混合，多个补间可协同工作。 |

#### LayoutElement

| 方法 | 说明 |
| --- | --- |
| `DOFlexibleSize(Vector2 to, float duration, bool snapping)` | 补间 `flexibleWidth/Height`（弹性尺寸）。 |
| `DOMinSize(Vector2 to, float duration, bool snapping)` | 补间 `minWidth/Height`（最小尺寸）。 |
| `DOPreferredSize(Vector2 to, float duration, bool snapping)` | 补间 `preferredWidth/Height`（首选尺寸）。 |

#### Outline

| 方法 | 说明 |
| --- | --- |
| `DOColor(Color to, float duration)` | 将 Outline 的颜色补间到指定值。 |
| `DOFade(float to, float duration)` | 将 Outline 的 alpha 淡入淡出到指定值。 |

#### RectTransform

| 分组 | 方法 | 说明 |
| --- | --- | --- |
| 锚点 | `DOAnchorMax(Vector2 to, float duration, bool snapping)` | 补间 `anchorMax`（锚点最大值）。 |
| 锚点 | `DOAnchorMin(Vector2 to, float duration, bool snapping)` | 补间 `anchorMin`（锚点最小值）。 |
| 位置 | `DOAnchorPos(Vector2 to, float duration, bool snapping)` | 补间 `anchoredPosition`（锚点位置）。 |
| 位置 | `DOAnchorPosX/DOAnchorPosY(float to, float duration, bool snapping)` | 仅补间所选轴。 |
| 位置 | `DOAnchorPos3D(Vector3 to, float duration, bool snapping)` | 补间 `anchoredPosition3D`。 |
| 位置 | `DOAnchorPos3DX/DOAnchorPos3DY/DOAnchorPos3DZ(float to, float duration, bool snapping)` | 仅补间所选轴。 |
| 位置 | `DOJumpAnchorPos(Vector2 endValue, float jumpPower, int numJumps, float duration, bool snapping)` | 带 Y 轴跳跃补间 `anchoredPosition`。**返回 Sequence 而非 Tweener。** |
| 枢轴 | `DOPivot(Vector2 to, float duration)` | 补间 `pivot`（枢轴）。 |
| 枢轴 | `DOPivotX/DOPivotY(float to, float duration)` | 仅补间所选轴。 |
| 效果 | `DOPunchAnchorPos(Vector2 punch, float duration, int vibrato, float elasticity, bool snapping)` | 冲击 `anchoredPosition`。 |
| 效果 | `DOShakeAnchorPos(float duration, float/Vector3 strength, int vibrato, float randomness, bool snapping, bool fadeOut, ShakeRandomnessMode randomnessMode)` | 晃动 `anchoredPosition`。 |
| 尺寸 | `DOSizeDelta(Vector2 to, float duration, bool snapping)` | 补间 `sizeDelta`（尺寸增量）。 |
| 形状 | `DOShapeCircle(Vector2 center, float endValueDegrees, float duration, bool relativeCenter = false, bool snapping = false)` | 让 `anchoredPosition` 绕给定中心画圆。 |

> [!NOTE] RectTransform 注意点
> - `DOJumpAnchorPos`：`jumpPower` 为跳跃力度（最大跳跃高度 = jumpPower + 最终 Y 偏移）；`numJumps` 为跳跃总次数。
> - `DOPunchAnchorPos`：`punch` 为冲击方向与强度（叠加到当前位置）；`elasticity`（0~1）为回弹超出起始位置的程度，1 = 完全振荡，0 = 只在冲击与起始位置之间振荡。
> - `DOShakeAnchorPos`：参数与 Camera 的 Shake 相同。
> - `DOShapeCircle`：`center` 为旋转圆心/枢轴（UI anchoredPosition 坐标）；`endValueDegrees` 为目标角度（负值 = 逆时针）；`relativeCenter` 为 `TRUE` 时坐标相对目标当前 `anchoredPosition`。

#### ScrollRect

| 方法 | 说明 |
| --- | --- |
| `DONormalizedPos(Vector2 to, float duration, bool snapping)` | 同时补间 `horizontalNormalizedPosition` 和 `verticalNormalizedPosition`。 |
| `DOHorizontalNormalizedPos(float to, float duration, bool snapping)` | 补间 `horizontalNormalizedPosition`。 |
| `DOVerticalPos(float to, float duration, bool snapping)` | 补间 `verticalNormalizedPosition`。 |

> [!NOTE]
> 官方文档此处将 `DOVerticalNormalizedPos` 误写为 `DOVerticalPos`，实际方法名为前者。

#### Slider

| 方法 | 说明 |
| --- | --- |
| `DOValue(float to, float duration, bool snapping = false)` | 将 `value` 补间到指定值。 |

#### Text

| 方法 | 说明 |
| --- | --- |
| `DOColor(Color to, float duration)` | 将颜色补间到指定值。 |
| `DOFade(float to, float duration)` | 将 alpha 淡入淡出到指定值。 |
| `DOText(string to, float duration, bool richTextEnabled = true, ScrambleMode scrambleMode = ScrambleMode.None, string scrambleChars = null)` | 将文本补间到指定字符串，参数见下。 |
| `DOBlendableColor(Color to, float duration)` | Blendable 补间：颜色可混合，多个补间可协同工作。 |

> [!NOTE] DOText 参数
> - `richTextEnabled`：`TRUE`（默认）时动画过程中正确解析富文本；`FALSE` 时所有标签视为普通文本。
> - `scrambleMode`：乱序模式。若非 `None`，文本以字符随机翻滚的方式呈现；否则正常逐字拼出。
>   - `None`（默认）：不乱序。
>   - `All` / `Uppercase` / `Lowercase` / `Numerals`：乱序时使用的字符类型。
>   - `Custom`：使用 `scrambleChars` 中的自定义字符。
> - `scrambleChars`：自定义乱序字符集合，字符越多越好（至少 10 个）。

### Unity UI Toolkit

#### VisualElement

| 方法 | 说明 |
| --- | --- |
| `DOMove(Vector3 to, float duration, bool snapping)` | 将位置补间到指定值。 |
| `DOMoveX/DOMoveY/DOMoveZ(float to, float duration, bool snapping)` | 仅补间所选轴。 |
| `DORotate(float to, float duration)` | 将旋转补间到指定值。 |
| `DOScale(float/Vector2 to, float duration)` | 将缩放补间到指定值。 |
| `DOPunch(Vector2 punch, float duration, int vibrato, float elasticity, bool snapping)` | 冲击效果。**无 FROM 变体。** |
| `DOShake(float duration, float/Vector3 strength, int vibrato, float randomness, bool snapping, bool fadeOut, ShakeRandomnessMode randomnessMode)` | 晃动效果。**无 FROM 变体。** |

### 外部资源与 PRO 插件

#### Easy Performant Outline（EPO）

##### EPO ➨ Outlinable.OutlineProperties

| 方法 | 说明 |
| --- | --- |
| `DOBlurShift(float to, float duration, bool snapping = false)` | 补间模糊偏移。 |
| `DOColor(Color to, float duration)` | 补间颜色。 |
| `DODilateShift(float to, float duration, bool snapping = false)` | 补间膨胀偏移。 |
| `DOFade(float to, float duration)` | 淡入淡出。 |
| `DOFloat(float to, float duration)` | 补间 float 属性。 |
| `DOVector(Vector4 to, float duration)` | 补间 Vector 属性。 |

##### EPO ➨ Outliner

| 方法 | 说明 |
| --- | --- |
| `DOBlurShift(float to, float duration, bool snapping = false)` | 补间模糊偏移。 |
| `DODilateShift(float to, float duration, bool snapping = false)` | 补间膨胀偏移。 |
| `DOInfoRendererScale(float to, float duration, bool snapping = false)` | 补间信息渲染器缩放。 |
| `DOPrimaryRendererScale(float to, float duration, bool snapping = false)` | 补间主渲染器缩放。 |

##### EPO ➨ Serialized Pass

| 方法 | 说明 |
| --- | --- |
| `DOColor(string/int propertyName/id, Color to, float duration)` | 补间指定属性（名称或 ID）的颜色。 |
| `DOFade(string/int propertyName/id, float to, float duration)` | 补间指定属性的 alpha。 |
| `DOFloat(string/int propertyName/id, float to, float duration)` | 补间指定属性的 float 值。 |
| `DOVector(string/int propertyName/id, Vector4 to, float duration)` | 补间指定属性的 Vector 值。 |

#### 2D Toolkit（仅限 PRO 版）

##### tk2dBaseSprite

| 方法 | 说明 |
| --- | --- |
| `DOScale(Vector3 to, float duration)` | 补间缩放。 |
| `DOScaleX/Y/Z(float to, float duration)` | 仅补间所选轴。 |
| `DOColor(Color to, float duration)` | 补间颜色。 |
| `DOFade(float to, float duration)` | 淡入淡出 alpha。 |

##### tk2dSlicedSprite

| 方法 | 说明 |
| --- | --- |
| `DOScale(Vector2 to, float duration)` | 补间缩放。 |
| `DOScaleX/Y(float to, float duration)` | 仅补间所选轴。 |

##### tk2dTextMesh

| 方法 | 说明 |
| --- | --- |
| `DOColor(Color to, float duration)` | 补间颜色。 |
| `DOFade(float to, float duration)` | 淡入淡出 alpha。 |
| `DOText(string to, float duration, bool richTextEnabled = true, ScrambleMode scrambleMode = ScrambleMode.None, string scrambleChars = null)` | 文本补间，参数同 [[#Text]] 的 `DOText`。 |

#### TextMeshPro / TextMeshProUGUI（仅限 PRO 版）

##### 简单快捷方式一览

| 方法 | 作用 |
| --- | --- |
| `DOScale(float to, float duration)` | 将目标的 `scale` 等比例过渡到指定值。 |
| `DOColor(Color to, float duration)` | 将目标的颜色过渡到指定颜色。 |
| `DOFaceColor(Color to, float duration)` | 将目标的 `faceColor` 过渡到指定颜色。 |
| `DOFaceFade(float to, float duration)` | 将目标的 `faceColor` 淡入淡出到指定值。 |
| `DOFade(float to, float duration)` | 将目标的透明度（alpha）淡入淡出到指定值。 |
| `DOFontSize(float to, float duration)` | 将目标的 `fontSize` 过渡到指定值。 |
| `DOGlowColor(Color to, float duration)` | 将目标的 `glowColor` 过渡到指定颜色。 |
| `DOOutlineColor(Color to, float duration)` | 将目标的 `outlineColor` 过渡到指定颜色。 |

##### DOCounter（数字滚动）

```cs
DOCounter(int fromValue, int endValue, float duration, bool addThousandsSeparator = true, CultureInfo culture = null)
```

让文本从一个整数补间到另一个整数，支持千位分隔符与区域设置选项。

- **fromValue**：起始值。
- **endValue**：目标值。
- **duration**：补间时长。
- **addThousandsSeparator**：若为 `TRUE`（默认），同时添加千位分隔符。
- **culture**：使用的 `CultureInfo`（若为 `NULL`，默认使用 `InvariantCulture`）。

##### DOMaxVisibleCharacters（控制可见字符数）

```cs
DOMaxVisibleCharacters(int to, float duration)
```

将目标的 `maxVisibleCharacters` 过渡到指定值。

> [!NOTE]
> 如果在补间开始前没有设置过 `maxVisibleCharacters` 属性，TextMesh Pro 会自动将起始值设为 0（因为该属性只有首次使用时才会被激活）。

##### DOText（文本补间）

```cs
DOText(string to, float duration, bool richTextEnabled = true, ScrambleMode scrambleMode = ScrambleMode.None, string scrambleChars = null)
```

将目标的文本过渡到指定字符串。参数说明同 [[#Text]] 的 `DOText`。

##### TextMeshPro 逐字符动画

要对 TextMeshPro 对象（`TMP_Text`，包括世界空间与 UI 两种）逐字符做动画，首先需要创建一个 `DOTweenTMPAnimator` 包装器（`new DOTweenTMPAnimator(tmpText)`），DOTween 才能高效地跟踪所有变化并应用修改。之后，`DOTweenTMPAnimator` 引用上提供了各种 `DO[Shortcut]` 方法，可以按索引逐字符动画（偏移、缩放、旋转、颜色、淡入淡出——IntelliSense 会显示所有细节），并返回一个 `Tween`。你可以把它放进 `Sequence`，也可以像其他补间一样链式调用。

> [!IMPORTANT]
> 遍历 `TMP_Text` 对象的字符时，请务必使用 `animator.textInfo.characterCount`，并跳过不可见的元素（参见下方示例）。

```cs
// 示例 1：为单个字符制作缩放动画
DOTweenTMPAnimator animator = new DOTweenTMPAnimator(myTextMeshProTextField);
Tween tween = animator.DOScaleChar(characterIndex, scaleValue, duration)
    .SetEase(Ease.OutBack);

// 示例 2：让文本中所有字符从上方滑入，
// 并将所有补间加入一个 Sequence 以便统一控制
DOTweenTMPAnimator animator = new DOTweenTMPAnimator(myTextMeshProTextField);
Sequence sequence = DOTween.Sequence();
for (int i = 0; i < animator.textInfo.characterCount; ++i) {
    if (!animator.textInfo.characterInfo[i].isVisible) continue;
    Vector3 currCharOffset = animator.GetCharOffset(i);
    sequence.Join(animator.DOOffsetChar(i, currCharOffset + new Vector3(0, 30, 0), 1));
}
```

##### DOTweenTMPAnimator ➨ 设置方法（Setup Methods）

```cs
// Refresh()
// 刷新动画器的文本数据，并重置所有变换数据。
// 每次修改 TMP_Text 对象中的文本时都会自动调用。
Refresh();

// Reset()
// 重置所有变形。
Reset();
```

##### DOTweenTMPAnimator ➨ 逐字符补间（Per-character Tweens）

这些方法会逐字动画文本字符，并返回一个 `Tween`，可以放进 `Sequence`，也可以像普通补间一样继续链式调用。通用说明：`charIndex` 为字符索引，`duration` 为补间时长；若 `charIndex` 无效或字符不可见，方法返回 `NULL`。

```cs
DOFadeChar(int charIndex, float endValue, float duration)
// 将字符的 alpha 补间到指定值。
// endValue：目标值（0~1）

DOColorChar(int charIndex, Color endValue, float duration)
// 将字符的颜色补间到指定值。
// endValue：目标颜色

DOOffsetChar(int charIndex, Vector3 endValue, float duration)
// 将字符的偏移补间到指定值。
// endValue：目标偏移

DORotateChar(int charIndex, Vector3 endValue, float duration, RotateMode mode = RotateMode.Fast)
// 将字符的旋转补间到指定值。
// mode：旋转模式

DOScaleChar(int charIndex, float endValue, float duration)
// 将字符的缩放补间到指定值。
// endValue：目标缩放

DOPunchCharOffset(int charIndex, Vector3 punch, float duration, int vibrato = 10, float elasticity = 1)
// 将字符的偏移向指定方向冲击（punch），再弹回起始位置，
// 就像起始位置用一根弹性绳牵着它一样。
// punch：冲击强度
// vibrato：冲击每秒振动的次数
// elasticity：回弹时超出起始位置的程度（0~1）。
//   1 = 在冲击偏移与相反偏移之间完全振荡；0 = 只在冲击偏移与起始偏移之间振荡

DOPunchCharRotation(int charIndex, Vector3 punch, float duration, int vibrato = 10, float elasticity = 1)
// 同上，作用于字符的旋转。

DOPunchCharScale(int charIndex, Vector3/float punch, float duration, int vibrato = 10, float elasticity = 1)
// 同上，作用于字符的缩放。punch 可为 Vector3 或 float。

DOShakeCharOffset(int charIndex, float duration, Vector3/float strength, int vibrato = 10, float randomness = 90, bool fadeOut = true)
// 以给定参数晃动字符的偏移。
// strength：晃动强度
// vibrato：晃动每秒振动的次数
// randomness：晃动的随机程度（0~180，高于 90 的值效果不太好，慎用）；0 = 沿单一方向晃动
// fadeOut：TRUE = 晃动会在补间时长内平滑衰减；FALSE = 不会

DOShakeCharRotation(int charIndex, float duration, Vector3 strength, int vibrato = 10, float randomness = 90, bool fadeOut = true)
// 同上，作用于字符的旋转。

DOShakeCharScale(int charIndex, Vector3/float duration, Vector3/float strength, int vibrato = 10, float randomness = 90, bool fadeOut = true)
// 同上，作用于字符的缩放。
// 注：官方文档中该签名 duration 的参数类型疑似笔误，应为 float。
```

##### DOTweenTMPAnimator ➨ 额外逐词/片段方法（Extra per-word/span methods）

以下方法用于直接变形文本片段，不做动画。

```cs
SkewSpanX(int fromCharIndex, int toCharIndex, float skewFactor, bool skewTop = true)
// 沿 X 轴统一倾斜一段字符（类似图形软件中的常规倾斜）。
// fromCharIndex：片段起始字符索引
// toCharIndex：片段结束字符索引
// skewFactor：倾斜系数
// skewTop：TRUE = 倾斜片段顶部；FALSE = 倾斜底部

SkewSpanY(int fromCharIndex, int toCharIndex, float skewFactor, TMPSkewSpanMode mode = TMPSkewSpanMode.Default, bool skewRight = true)
// 沿 Y 轴统一倾斜一段字符。
// skewFactor：垂直倾斜系数
// mode：倾斜模式
// skewRight：TRUE = 倾斜片段右侧；FALSE = 倾斜左侧
```

##### DOTweenTMPAnimator ➨ 额外逐字符方法（Extra per-character methods）

以下方法用于直接变形或读取字符的信息，不做动画。通用说明：若 `charIndex` 无效或字符不可见，写操作将不做任何操作。

```cs
Color GetCharColor(int charIndex)
// 返回指定字符当前的颜色（若存在且可见）。

Vector3 GetCharOffset(int charIndex)
// 返回指定字符当前的偏移。

Vector3 GetCharRotation(int charIndex)
// 返回指定字符当前的旋转。

Vector3 GetCharScale(int charIndex)
// 返回指定字符当前的缩放。

ResetVerticesShift(int charIndex)
// 重置通过 ShiftCharVertices 应用到指定字符的顶点位移。

SetCharColor(int charIndex, Color color)
// 立即设置指定字符的颜色。

SetCharOffset(int charIndex, Vector3 offset)
// 立即设置指定字符的偏移。

SetCharRotation(int charIndex, Vector3 rotation)
// 立即设置指定字符的旋转。

SetCharScale(int charIndex, Vector3 scale)
// 立即设置指定字符的缩放。

ShiftCharVertices(int charIndex, Vector3 topLeftShift, Vector3 topRightShift, Vector3 bottomLeftShift, Vector3 bottomRightShift)
// 立即按给定偏移量移动指定字符的四个顶点。
// topLeftShift：左上角偏移
// topRightShift：右上角偏移
// bottomLeftShift：左下角偏移
// bottomRightShift：右下角偏移

SkewCharX(int charIndex, float skewFactor, bool skewTop = true)
// 沿 X 轴倾斜指定字符，并返回实际应用的倾斜量（基于字符尺寸计算）。
// skewFactor：倾斜量
// skewTop：TRUE = 倾斜字符顶部；FALSE = 倾斜底部

SkewCharY(int charIndex, float skewFactor, bool skewRight = true, bool fixedSkew = false)
// 沿 Y 轴倾斜指定字符（官方文档此处误写为 X 轴）。
// skewFactor：倾斜量
// skewRight：TRUE = 倾斜字符右侧；FALSE = 倾斜左侧
// fixedSkew：TRUE = 精确应用给定倾斜量；FALSE = 根据字符宽高比（aspectRatio）修正
```

---

## 三、相关文档

- [[00-DOTween术语]]
- [[01-DOTween.Init-初始化]]
- [[03-创建Sequence补间序列]]
- [[04-设置选项与回调-01-全局设置与默认值]]
- [[04-设置选项与回调-02-链式设置]]
- [[04-设置选项与回调-03-链式回调]]
- [[04-设置选项与回调-04-Tweener专用设置与选项]]
- [[05-控制补间]]
- [[06-获取补间数据]]
- [[07-协程与Task等待]]
- [[08-其他方法]]
