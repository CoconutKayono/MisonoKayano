# Unity 数学 API 简介

> 原文：[Introduction to Unity math APIs](https://docs.unity3d.com/6000.7/Documentation/Manual/programming-math-intro.html)

Unity 为 Unity 项目中常用的数学函数和结构提供了两组不同的数学 API：

- [[00-Unity Engine数学API]]：`UnityEngine` Namespace 中一组相互兼容的 API。其中包括用于常见数学函数的 [`Mathf`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.html) 类，支持三角函数、对数函数和其他运算；用于生成随机数的 [`UnityEngine.Random`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Random.html) 类；以及用于表示数据结构的 [`Vector2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html)、[`Vector3`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html)、[`Matrix4x4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Matrix4x4.html) 和 [`Quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.html) 等类。
- [[03-Unity Mathematics API]]：`Unity.Mathematics` Namespace 中一组相互兼容的 API，提供可由 [Burst](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html) 编译且支持 [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) 的 UnityEngine 数学 API 替代方案。其中包括用于常见数学函数的静态 `math` 类、用于生成随机数的 `Unity.Mathematics.Random` 类，以及 [`float2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float2.html)、[`float3`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float3.html)、[`float4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float4.html)、[`float4x4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float4x4.html) 和 [`quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.quaternion.html) 等数据结构。

## UnityEngine 数学 API 与 Unity Mathematics 的兼容性

`UnityEngine` 和 `Unity.Mathematics` API 在实现上存在重要差异。如果应用程序依赖其中一组 API 的特定行为，通常需要重新实现这些行为，才能在另一组 API 中获得等效结果。

可以在同一个项目中同时使用 `UnityEngine` 和 `Unity.Mathematics` API，但这可能影响应用程序性能，因为 `UnityEngine` 和 `Unity.Mathematics` 类型之间的转换（例如从 `Vector3` 转换为 `float3`）会产生较高的性能开销。

通常出于性能原因，建议遵循以下原则：

- 对于使用 [Mono Scripting Backend](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-mono.html) 进行即时编译（JIT）的代码：使用 `UnityEngine` 数学 API，而不是 `Unity.Mathematics`。
- 对于使用 [Burst](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html) 进行提前编译（AOT）的代码：默认使用 Unity Mathematics，仅在必要时使用 `UnityEngine` 数学 API。

## 在 UnityEngine 数学 API 与 Unity.Mathematics 之间转换

要在 `UnityEngine` 和 `Unity.Mathematics` API 之间迁移代码，必须执行以下操作：

- 将一组 API 中的类型替换为另一组 API 中的对应类型。例如，从 `UnityEngine` API 迁移到 `Unity.Mathematics` API 时，将 [`Vector4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html) 的用法替换为 [`float4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float4.html)，将 [`Quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.html) 替换为 [`quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.quaternion.html)。
- 更新矩阵或 Vector 中涉及的运算符。例如，`Matrix4x4` 的乘法运算符执行矩阵乘法，而 [`float4x4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float4xx4.html) 的乘法运算符执行逐分量乘法。
- 在适用的地方将角度从度转换为弧度。
- 更新代码中的随机数生成方式。[`Unity.Mathematics.Random`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.Random.html) 与 [`UnityEngine.Random`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Random.html) 的工作方式不同。可以使用 `Unity.Mathematics` 中的 `Random` 完全控制随机数生成；它是实例类型，而不是静态类型。此外，它的上界是排他的。如果要迁移对边界敏感的 `UnityEngine` 代码，这一点非常重要。更多信息请参阅 Unity Mathematics 编程参考。

下表概括了两组 API 中一些关键的等效类型和成员：

| 功能 | UnityEngine 数学 API | Unity Mathematics |
| --- | --- | --- |
| Namespace | `UnityEngine` | `Unity.Mathematics` |
| 标量数学类 | [`Mathf`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.html)（静态） | [`math`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math.html)（静态） |
| 标量类型 | `float` | `float` |
| 2D Vector | [`Vector2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html) | [`float2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float2.html) |
| 3D Vector | [`Vector3`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html) | [`float3`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float3.html) |
| 4D Vector | [`Vector4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html) | [`float4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float4.html) |
| 整数 | [`Vector2Int`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2Int.html)、[`Vector3Int`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3Int.html) | [`int2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.int2.html)、[`int3`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.int3.html)、[`int4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.int4.html) |
| Quaternion | [`Quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.html) | [`quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math-quaternion.html) |
| 矩阵 | [`Matrix4x4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Matrix4x4.html) | [`float4x4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math.float4x4.html)、[`float3x3`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math.float3x3.html)、[`float2x2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math.float2x2.html) |
| Random | [`UnityEngine.Random`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Random.html) | [`Unity.Mathematics.Random`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.Random.html) |
| Mod | [`Mathf.Repeat`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Repeat.html) 或 `%` | [`math.modf`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math-modf.html) |
| Epsilon | [`Mathf.Epsilon`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.Epsilon.html) | [`math.EPSILON`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math.EPSILON.html) |
| Dot product | [`Vector3.Dot`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Dot.html) | [`math.dot`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math-dot.html) |
| Cross product | [`Vector3.Cross`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Cross.html) | [`math.cross`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math-cross.html) |
| Lerp（Vector） | [`Vector3.Lerp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Lerp.html) | [`math.lerp(float3, float3, t)`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math-lerp.html) |
| Slerp（Quaternion） | [`Quaternion.Slerp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.Slerp.html) | [`math.slerp`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math-slerp.html) |
| 矩阵乘法 | `a * b` | [`math.mul(a, b)`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math-mul.html) |

如需查看等效函数和类型的完整列表，请参阅对应的 API 参考。

## 其他资源

- [[00-Unity Engine数学API]]
- [[03-Unity Mathematics API]]


---

## 文档导航

- 上一页：[[00-使用数学编程]]
- 目录：[[00-使用数学编程]]
- 下一页：[[00-Unity Engine数学API]]
