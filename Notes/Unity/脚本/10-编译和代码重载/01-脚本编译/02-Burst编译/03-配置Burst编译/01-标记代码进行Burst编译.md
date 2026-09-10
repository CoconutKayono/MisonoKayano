# 标记代码进行 Burst 编译

> 原文：[Marking code for Burst compilation](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-burstcompile.html)

对希望由 Burst 编译的代码应用 `[BurstCompile]` attribute。可以将 `[BurstCompile]` attribute 应用到以下对象：

- **Job**：将 `[BurstCompile]` 应用到 Job 定义时，Burst 会编译 Job 内部的所有内容。有关 Job 的信息，请参阅 [[../../../../11-代码优化/03-Job System/00-Job System]]。
- **Class**：如果 class 包含同样标记了 `[BurstCompile]` 的静态方法，则对 class 定义应用 `[BurstCompile]`。Burst 不能编译 class 本身，只能编译其成员方法。
- **Struct**：如果普通（非 Job）struct 定义包含同样标记了 `[BurstCompile]` 的静态方法，则对 struct 定义应用 `[BurstCompile]`。
- **Static method**：对方法及其父类型应用 `[BurstCompile]`。要使用根据其他数据状态处理数据的动态函数，请参阅 [[../06-CSharp语言支持/03-函数指针]]。
- **Assembly**：对 assembly 应用 `[BurstCompile]`，为 assembly 中的所有 Burst Job 和 function pointer 设置选项。更多信息请参阅 [[02-为程序集定义Burst选项]]。

**注意**：并不总是需要在方法上标记 `[BurstCompile]`，Burst 也能编译它。程序执行从 managed code 切换到 Burst 编译代码的位置称为 **Burst entry point**。如果静态 entry point 方法标记了 `[BurstCompile]`，Burst 还会编译它调用的、即使没有标记 `[BurstCompile]` 的方法（前提是这些方法属于 Burst 支持范围）。

## 使用参数配置 Burst 编译

可以向 `[BurstCompile]` attribute 提供参数，以修改编译的各个方面并提升 Burst 性能。attribute 参数可以用于：

- 为数学函数（例如 `sin`、`cos`）使用不同的精度。
- 放宽数学计算的顺序，使 Burst 可以重新排列浮点计算。
- 强制 Job 同步编译（仅用于 just-in-time 编译）。

例如，可以使用 `[BurstCompile]` attribute 更改 Burst 的 floating point 精度和 float mode：

```csharp
[BurstCompile(FloatPrecision.Medium, FloatMode.Fast)]
```

有关配置浮点计算的精度和确定性的信息，请参阅 [[../14-浮点精度和确定性]]。

## 其他资源

- [`[BurstCompile]` attribute API reference](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Burst.BurstCompileAttribute.html)
- [[02-为程序集定义Burst选项]]

---

## 文档导航

- 上一页：[[00-配置Burst编译]]
- 目录：[[00-配置Burst编译]]
- 下一页：[[02-为程序集定义Burst选项]]
