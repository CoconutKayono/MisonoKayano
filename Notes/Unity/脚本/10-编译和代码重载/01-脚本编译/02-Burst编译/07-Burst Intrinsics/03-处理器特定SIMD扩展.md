# 处理器特定 SIMD 扩展

> 原文：[Processor specific SIMD extensions](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics-processors.html)

Burst 在 `Unity.Burst.Intrinsics.X86` 系列嵌套类中公开从 SSE 到 AVX2（包括 AVX2）的所有 Intel SIMD Intrinsics。`Unity.Burst.Intrinsics.Arm.Neon` 类提供 Armv7、Armv8 和 Armv8.2（RDMA、crypto、dotprod）的 Arm Neon Intrinsics。

## 整理代码

由于这些 Intrinsics 包含普通静态函数，应使用静态导入：

```csharp
using static Unity.Burst.Intrinsics.X86;
using static Unity.Burst.Intrinsics.X86.Sse;
using static Unity.Burst.Intrinsics.X86.Sse2;
using static Unity.Burst.Intrinsics.X86.Sse3;
using static Unity.Burst.Intrinsics.X86.Ssse3;
using static Unity.Burst.Intrinsics.X86.Sse4_1;
using static Unity.Burst.Intrinsics.X86.Sse4_2;
using static Unity.Burst.Intrinsics.X86.Popcnt;
using static Unity.Burst.Intrinsics.X86.Avx;
using static Unity.Burst.Intrinsics.X86.Avx2;
using static Unity.Burst.Intrinsics.X86.Fma;
using static Unity.Burst.Intrinsics.X86.F16C;
using static Unity.Burst.Intrinsics.X86.Bmi1;
using static Unity.Burst.Intrinsics.X86.Bmi2;
using static Unity.Burst.Intrinsics.Arm.Neon;
```

Burst CPU Intrinsics 会被转换为具体的 CPU 指令。不过，Burst 有一个特殊的编译器阶段，用于检查 Burst AOT 设置中的 CPU 目标集合是否与代码使用的 Intrinsics 兼容。这样可以确保不会调用不受支持的指令（例如在 Intel CPU 上调用 AArch64 Neon，或在 SSE4 CPU 上调用 AVX2 指令）；否则进程会因“Invalid instruction”异常而中止。如果检查失败，编译器会生成错误。

如果你想为不同 CPU 目标提供多条代码路径，或者希望确保 Intrinsics 代码兼容任意目标 CPU，可以使用以下属性检查包裹 Intrinsics 代码：

支持检查的属性包括：

- `IsNeonSupported`
- `IsNeonArmv82FeaturesSupported`
- `IsNeonCryptoSupported`
- `IsNeonDotProdSupported`
- `IsNeonRDMASupported`

例如：

```csharp
if (IsAvx2Supported)
{
    // Code path for AVX2 instructions
}
else if (IsSse42Supported)
{
    // Code path for SSE4.2 instructions
}
else if (IsNeonArmv82FeaturesSupported)
{
    // Code path for Armv8.2 Neon instructions
}
else if (IsNeonSupported)
{
    // Code path for Arm Neon instructions
}
else
{
    // Fallback path for everything else
}
```

这些分支不会影响性能。Burst 会在编译时计算 `IsXXXSupported` 属性，并将不支持的分支作为死代码移除；活动分支会保留下来，但不包含 `if` 检查。较新的功能级别会隐式包含之前的级别，因此应从最新级别到最旧级别组织检查。若使用了不属于当前编译目标的 Intrinsics，Burst 会发出编译时错误。Burst 不会用功能级别检查包围这些 Intrinsics，这有助于缩小功能检查的范围。

如果在未启用 Burst 的情况下于 .NET、Mono 或 IL2CPP 中运行应用，所有 `IsXXXSupported` 属性都会返回 `false`。不过，即使跳过检查，在 Mono 中仍可以运行大多数 Intrinsics 的参考实现（例外情况见下文），这对于使用托管调试器很有帮助。参考实现速度较慢，仅用于托管调试。

注意：Arm Neon Intrinsics 没有参考托管实现。因此，无法使用上一段所述技术在 Mono 中单步调试这些 Intrinsics。处理 double 的 FMA Intrinsics 没有软件回退实现，因为模拟融合 64 位浮点运算本身非常复杂。

Intrinsics 使用 `v64`（仅限 Arm）、`v128` 和 `v256` 类型，分别表示 64 位、128 位和 256 位向量。例如，给定一个 `NativeArray<float>` 和一个由 `v128` shuffle mask 组成的查找表，下面的代码片段会执行 lane 左打包，同时展示向量加载/存储重解释和直接调用 Intrinsics：

```csharp
v128 a = Input.ReinterpretLoad<v128>(i);
v128 mask = cmplt_ps(a, Limit);
int m = movemask_ps(a);
v128 packed = shuffle_epi8(a, Lut[m]);
Output.ReinterpretStore(outputIndex, packed);
outputIndex += popcnt_u32((uint)m);
```

## Intel Intrinsics

Intel Intrinsics API 与 C/C++ Intel Intrinsics API 对应，但有以下差异：

- 所有 128 位向量类型（`__m128`、`__m128i` 和 `__m128d`）都合并为 `v128`。
- 所有 256 位向量类型（`__m256`、`__m256i` 和 `__m256d`）都合并为 `v256`。
- 指令和宏中的所有 `_mm` 前缀都会被移除，因为 C# 使用命名空间。
- 所有位域常量（例如舍入模式选择）都替换为 C# 位标志枚举值。

## Arm Neon Intrinsics

Arm Neon Intrinsics API 与 Arm C 语言扩展对应，但有以下差异：

- 所有向量类型都合并为无类型的 `v64` 和 `v128`。这意味着调用 API 时，向量类型必须包含预期的元素类型和数量。
- 不支持 `*x2`、`*x3` 和 `*x4` 向量类型。
- 不支持 `poly*` 类型。
- 不支持 `reinterpret*` 函数（由于使用 `v64` 和 `v128` 向量类型，因此不需要这些函数）。
- Intrinsic 仅支持 Armv8（64 位）硬件。

Burst CPU Intrinsics 使用无类型向量。因此，Burst 不执行类型检查。例如，如果调用处理 4 个 int 的 Intrinsic，但传入的向量最初由 4 个 float 初始化，则不会产生编译器错误。向量类型的字段表示每一种元素类型，类似联合体的结构体使你可以按照最适合代码的方式使用这些 Intrinsics。

Arm Neon C Intrinsics（ACLE）使用有类型向量，例如 `int32x4_t`，并提供特殊 API（例如 `reinterpret_*`）将其转换为另一元素类型的向量。Burst CPU Intrinsics 向量没有类型，因此不需要这些 API。以下 API 提供等效功能：

- `v64`（仅限 Arm Neon）
- `v128`
- `v256`

有关 Burst 支持的 Arm Neon Intrinsics 分类索引，请参阅 [[02-Burst Arm Neon Intrinsics参考]]。

## 相关资源

- [[02-Burst Arm Neon Intrinsics参考]]

---

## 文档导航

- 上一页：[[01-跨平台Burst Intrinsics]]
- 目录：[[00-Burst Intrinsics]]
- 下一页：[[02-Burst Arm Neon Intrinsics参考]]
