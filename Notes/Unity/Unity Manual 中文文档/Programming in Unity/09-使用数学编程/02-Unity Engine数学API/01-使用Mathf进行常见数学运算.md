# 使用 Mathf 进行常见数学运算

> 原文：[Common math functions with the Mathf class](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Mathf.html)

Unity 的 [`Mathf`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.html) 类提供了一组常见数学函数，包括 Unity 项目中经常需要的三角函数、对数函数和其他函数。它是 Unity 针对 .NET [`System.MathF`](https://learn.microsoft.com/en-us/dotnet/api/system.mathf?view=net-10.0) 类提供的专用替代方案。

下面的章节介绍 `Mathf` 类的一些主要功能。有关该类所有成员的完整参考，请参阅 [`Mathf` API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.html)。

## 三角函数

Unity 的所有三角函数都使用弧度：

- [`Sin`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Sin.html)
- [`Cos`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Cos.html)
- [`Tan`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Tan.html)
- [`Asin`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Asin.html)
- [`Acos`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Acos.html)
- [`Atan`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Atan.html)
- [`Atan2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Atan2.html)

[`PI`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.PI.html) 以常量形式提供。可以乘以静态值 [`Rad2Deg`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Rad2Deg.html) 或 [`Deg2Rad`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Deg2Rad.html)，在弧度和角度之间进行转换。

## 幂和平方根

`Mathf` 类包含以下常见幂和平方根函数：

- [`Pow`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Pow.html)
- [`Sqrt`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Sqrt.html)
- [`Exp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Exp.html)

它还提供与 2 的幂相关的函数。这些函数在处理常见的二进制数据大小时很有用，因为这类数据通常受限于 2 的幂，或针对 2 的幂进行优化，例如 Texture 尺寸：

- [`ClosestPowerOfTwo`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.ClosestPowerOfTwo.html)
- [`NextPowerOfTwo`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.NextPowerOfTwo.html)
- [`IsPowerOfTwo`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.IsPowerOfTwo.html)

## 插值

`Mathf` 插值函数可以计算两个给定点之间某个位置的值。每个函数的行为不同，适用于不同场景。更多信息请参阅每个方法 API 参考中的示例：

- [`Lerp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Lerp.html)
- [`LerpAngle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.LerpAngle.html)
- [`LerpUnclamped`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.LerpUnclamped.html)
- [`InverseLerp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.InverseLerp.html)
- [`MoveTowards`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.MoveTowards.html)
- [`MoveTowardsAngle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.MoveTowardsAngle.html)
- [`SmoothDamp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.SmoothDamp.html)
- [`SmoothDampAngle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.SmoothDampAngle.html)
- [`SmoothStep`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.SmoothStep.html)

[[02-使用Vector类移动对象]]和[[04-使用Quaternion控制旋转]]类也有自己的插值函数（例如 [`Quaternion.Lerp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.Lerp.html)），用于在多个维度上插值位置、方向和旋转。

## 限制和重复值

下面的辅助函数在游戏或应用中经常有用：当需要将值限制在某个范围内，或让值在范围内重复时，它们可以节省时间：

- [`Max`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Max.html) 和 [`Min`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Min.html)
- [`Repeat`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Repeat.html) 和 [`PingPong`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.PingPong.html)
- [`Clamp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Clamp.html) 和 [`Clamp01`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Clamp01.html)
- [`Ceil`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Ceil.html) 和 [`Floor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Floor.html)

## 对数函数

[`Log`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Log.html) 函数可以计算指定数值的对数，既可以计算自然对数，也可以指定对数的底数。此外，[`Log10`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Log10.html) 函数会返回指定数值的以 10 为底的对数。

## 其他资源

- [`Mathf` API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.html)
- [[03-Unity Mathematics API]]


---

## 文档导航

- 上一页：[[00-Unity Engine数学API]]
- 目录：[[00-Unity Engine数学API]]
- 下一页：[[02-使用Vector类移动对象]]
