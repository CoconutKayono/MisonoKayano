# 配置 Burst 编译

> 原文：[Configure Burst compilation](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation.html)

使用 Burst 的自定义 C# attributes 定义由 Burst 编译的代码部分。这些 attributes 及其参数还可以配置一系列编译选项，以便在不同上下文中提升 Burst 性能。

| 页面 | 说明 |
| --- | --- |
| [[01-标记代码进行Burst编译]] | 使用 `[BurstCompile]` attribute 标记代码进行 Burst 编译；使用 attribute 参数自定义 Burst 编译的各个方面并提升性能。 |
| [[03-排除代码不进行Burst编译]] | 使用 `[BurstDiscard]` attribute 有选择地排除部分代码，使其不进行 Burst 编译。 |
| [[02-为程序集定义Burst选项]] | 在程序集级别应用 `[BurstCompile]` attribute，为整个程序集定义 Burst 编译选项。 |
| [[05-Play Mode中的Burst编译]] | Burst 提供在 Play mode 中异步或同步编译的选项；了解如何以及何时配置同步编译。 |
| [[04-泛型Job支持]] | 了解 Burst 对泛型 Job 和 function pointer 支持的重要限制。 |
| [[14-浮点精度和确定性]] | 使用相关 API 配置 Burst 浮点数计算的精度和确定性程度。 |
| [[06-编译警告参考]] | 修复常见的编译警告。 |

## 其他资源

- [[00-CSharp语言支持]]

---

## 文档导航

- 上一页：[[02-Burst入门]]
- 目录：[[00-配置Burst编译]]
- 下一页：[[01-标记代码进行Burst编译]]
