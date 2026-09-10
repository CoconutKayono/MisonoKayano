# Unity Mathematics API

> 原文：[Unity Mathematics APIs](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-mathematics.html)

`Unity.Mathematics` Namespace 中的 API 是一个可由 [Burst](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html) 编译的 C# 数学库，提供 Vector 类型和数学函数，并使用类似 Shader 的语法，与 [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) 或 [HLSL](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl) 类似。

Unity Mathematics 是 Unity 标准 [[02-Unity Engine数学API/00-Unity Engine数学API|Unity Engine 数学 API]] 的可由 Burst 编译的替代方案。Unity Mathematics 实现了 [`float3`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float3.html)、[`quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.quaternion.html)、[`float3x3`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float3x3.html) 和 [`float4x4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float4x4.html) 等 Vector 和 Matrix 类型。它还包括 `min`、`max`、`fabs`、`sin`、`cos`、`sqrt`、`normalize`、`dot` 和 `cross` 等初等函数。

要使用 Unity Mathematics，请在代码中添加 `using Unity.Mathematics`。

在 Burst 编译的代码中，优先使用 Unity Mathematics API。对于未使用 Burst 编译的代码，优先使用 Unity Engine 数学 API。

## 命名约定

在 C# 中，`int` 和 `float` 是内置类型。Burst 编译器将内置类型扩展为还包括 Vector、Matrix 和 Quaternion。Burst 编译器已经实现了这些类型，相比自定义类型，可以利用它们生成更好的代码。

为了表示这些类型是内置类型，它们的类型名称全部使用小写字母。`Unity.Mathematics.math` 中这些内置类型的运算符也是 Intrinsic，并且始终使用小写形式。这个约定还让该库能够很好地兼容 Shader 代码，使两者之间更容易移植或共享代码。

## 4×4 Matrix

要创建 4×4 Transform Matrix，可以使用 [`float4x4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float4x4.html) 的构造函数为矩阵的所有元素赋值，或直接单独设置全部 16 个元素：

```csharp
// Unity Mathematics example
void Build4x4UnityMathematics()
{
   var c0 = new float4(1.0f, 0.0f, 0.0f, 0.0f);
   var c1 = new float4(0.0f, 1.0f, 0.0f, 0.0f);
   var c2 = new float4(0.0f, 0.0f, 1.0f, 0.0f);
   var c3 = new float4(0.0f, 0.0f, 0.0f, 1.0f);
   var m = new float4x4(c0, c1, c2, c3);
}
```

### 乘以 4×4 Matrix

`Unity.Mathematics` 和 `UnityEngine` API 对 `*` 运算符的定义不同。 [`float4x4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.float4x4.html) 的 `*` 运算符执行逐分量乘法。如果将元素全为 1 的 `float4x4` 与对角线为 0.5 的 Matrix 相乘，则会得到 Half Identity，因为矩阵的上三角和下三角会分别与 `f4x4_HalfIdentity` 中对应的零元素相乘：

```csharp
// Unity Mathematics example
void OperatorMultiply4x4UnityMathematics()
{
   float4x4 result = f4x4_Ones * f4x4_HalfIdentity;
   // result:
   // 0.5, 0.0, 0.0, 0.0,
   // 0.0, 0.5, 0.0, 0.0,
   // 0.0, 0.0, 0.5, 0.0,
   // 0.0, 0.0, 0.0, 0.5
}
```

### 乘以 4×4 Matrix 和 4D Vector

使用 [`math.mul`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.math-mul.html) 方法将 4×4 Matrix 与 4D Vector 相乘。如果将 `float4x4` 作为第一个参数，将 `float4` 作为第二个参数，则会执行 4×4 Matrix 与 4×1 列 Vector 的乘法，并以 `float4` 形式返回一个 4×1 列 Vector。

`math.mul` 也可以将 1×4 行 Vector 与 4×4 Matrix 相乘，生成 1×4 行 Vector：此时将 `float4` 作为第一个参数，将 `float4x4` 作为第二个参数。Unity Mathematics 使用 `float4` 存储行 Vector，不会将其视为单独的类型。

```csharp
// Unity Mathematics example
void Multiply4x4AndVector4UnityMathematics()
{
   float4 result1 = math.mul(f4x4, f4); // 4x4 * 4x1 = 4x1
   float4 result2 = math.mul(f4, f4x4); // 1x4 * 4x4 = 1x4
}
```

## Vector 乘法

要将 Vector 相乘，请使用 `*` 运算符：

```csharp
// Unity Mathematics example
void ComponentwiseVectorMultiplyUnityMathematics()
{
   var v0 = new float4(2.0f, 4.0f, 6.0f, 8.0f);
   var v1 = new float4(1.0f, -1.0f, 1.0f, -1.0f);
   var result = v0 * v1;
   // result == new float4(2.0f, -4.0f, 6.0f, -8.0f).
}
```

这是编写 [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) 代码的常见方式，即将一条指令应用于多个数据元素。加法、减法和除法等其他运算符的工作方式也相同。

## Quaternion 乘法

要旋转 Quaternion，请使用 [`AxisAngle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.quaternion.AxisAngle.html) 方法。需要依次指定旋转轴和旋转角度。所有角度都使用弧度，而不是度。`math.mul` 会像处理 Matrix 和 Vector 一样乘以 Quaternion。

```csharp
// Unity Mathematics example
void QuaternionMultiplicationUnityMathematics()
{
   var axis = new float3(0.0f, 1.0f, 0.0f);
   var q = quaternion.AxisAngle(axis,math.radians(45.0f));
   var orientation = quaternion.Euler(
       math.radians(45.0f),
       math.radians(90.0f),
       math.radians(180.0f));
   var result = math.mul(q, orientation);
}
```

## 随机数

要生成随机数，必须使用 [`Random`](https://docs.unity3d.com/Packages/com.unity.mathematics@latest/index.html?subfolder=/api/Unity.Mathematics.Random.html) 结构体自行创建和管理随机数生成器状态。可以显式控制随机数生成器状态，这在使用并行代码时很有用，也可以确保一个随机数来源使用的 Seed 与另一个来源不同。还可以根据需要创建任意数量的 `Random` 实例。

设置好状态后，使用 [`NextFloat`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Mathematics.Random.NextFloat.html) 获取随机浮点数。默认情况下，它会返回 `[0, 1)` 范围内的随机数，其中上界不包含在内：

```csharp
// Unity Mathematics example
void RandomNumberUnityMathematics()
{
   // Choose some non-zero seed and set up the random number generator state.
   uint seed = 1;
   Unity.Mathematics.Random rng = new Unity.Mathematics.Random(seed);

   // [0, 1) exclusive
   float randomFloat1 = rng.NextFloat();

   // [-5, 5) exclusive
   float randomFloat2 = rng.NextFloat(-5.0f, 5.0f);
}
```

## 其他资源

- [[02-Unity Engine数学API/01-使用Mathf进行常见数学运算]]
- [Burst 编译器](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html)


---

## 文档导航

- 上一页：[[02-Unity Engine数学API/04-使用Quaternion控制旋转]]
- 目录：[[00-使用数学编程]]
- 下一页：[[04-智能字符串/00-智能字符串]]
