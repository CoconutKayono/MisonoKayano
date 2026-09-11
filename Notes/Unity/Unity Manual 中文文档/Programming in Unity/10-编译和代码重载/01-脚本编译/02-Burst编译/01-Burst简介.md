# Burst 简介

> 原文：[Introduction to Burst](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/introduction-to-burst.html)

Burst 是一种编译器，可以处理 Unity 语境中称为 High-Performance C#（HPC#）的 C# 子集。Burst 使用 LLVM，将 .NET Intermediate Language（IL）转换为针对目标 CPU 架构优化的代码。

Burst 最初是为 Unity 的 Job System 设计的。Job 是实现 `IJob` 接口的 struct，代表可以并行运行的小型工作单元，从而充分利用所有可用的 CPU 核心。设计或重构项目，将工作拆分为由 Burst 编译的 Job，可以显著提升 CPU-bound 代码的性能。

除 Job 外，只要静态方法内部的代码属于受支持的 C# 子集，Burst 也可以编译静态方法。有关 High-Performance C# 中包含哪些内容，请参阅 [[01-高性能CSharp简介]]。

Burst 是 Unity Entity Component System（ECS）技术的核心。ECS 包含一系列相互依赖、协同生成高性能代码的 Package。不过，Burst 可以独立于 ECS 使用，也可以集成到任何使用受支持 C# 功能的 Unity 项目中。

## Burst 在编译流程中的作用

Burst 不是完整的 scripting backend，因为它只支持 C# 的一个子集。它不能替代 Unity 中使用的 Mono scripting backend 或 IL2CPP，而是作为二者之一的补充。

scripting backend 默认编译代码，而 Burst 编译其中标记为 Burst 编译的、与 Burst 兼容的部分。

C# 脚本照常编译为 Intermediate Language（IL）。对于标记为 Burst 的方法，Burst 会进一步将 IL 编译为 native code。Burst 在 Unity Editor 的 Play mode 中进行 just-in-time（JIT）编译，在 Player 构建中进行 ahead-of-time（AOT）编译。

Burst 支持的 C# 子集不支持 managed object。Unity 提供了用于常见类型和数据结构的 Burst 兼容库。Collections Package 提供数组和列表等 Burst 兼容集合，Unity Mathematics API 提供 Burst 兼容的数学函数。

## 使用 Burst 编译

代码满足以下条件时会由 Burst 编译：

- 代码与 Burst 兼容。
- 已启用 Burst 编译：Player 构建通过 Burst AOT Settings 启用，Unity Editor 代码则通过 Burst 菜单启用。
- 代码显式使用 `[BurstCompile]` attribute 标记，或从已标记的代码中引用。

可以使用脚本符号 `ENABLE_BURST_AOT`，仅在启用 Burst AOT 编译设置时对代码的部分内容进行条件编译。

更多信息请参阅 [[00-配置Burst编译]]。

## 其他资源

- [[00-Job System]]

---

## 文档导航

- 上一页：[[00-Burst编译]]
- 目录：[[00-Burst编译]]
- 下一页：[[02-Burst入门]]
