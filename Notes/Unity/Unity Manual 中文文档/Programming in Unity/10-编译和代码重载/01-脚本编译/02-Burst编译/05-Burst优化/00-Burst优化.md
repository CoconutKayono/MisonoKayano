# Burst 优化

> 原文：[Burst optimization](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/optimization-overview.html)

调试和分析 Burst 编译的代码以查找问题，并配置一系列选项来优化性能。

| 页面 | 说明 |
| --- | --- |
| [[10-调试和性能分析工具]] | 在 Editor 和 Player 构建中调试和分析 Burst 编译的代码。 |
| [[05-循环向量化]] | 了解 Burst 如何使用循环向量化优化代码。 |
| [[00-Burst内存别名]] | 使用内存别名告诉 Burst 代码如何使用数据。 |
| [[02-限制整数范围]] | 使用 `AssumeRange` 告诉 Burst 给定的标量整数位于受限范围内。 |
| [[04-添加优化提示]] | 使用 `Hint` intrinsic 向 Burst 提供更多数据相关信息。 |
| [[03-检查编译时约束]] | 使用 `IsConstantExpression` 检查表达式在编译时是否为常量。 |
| [[06-避免不必要的零初始化]] | 使用 `SkipLocalsInitAttribute` 告诉 Burst，方法中的栈分配不必初始化为零。 |

## 其他资源

- [[00-Burst Intrinsics]]

---

## 文档导航

- 上一页：[[06-编译警告参考]]
- 目录：[[00-Burst优化]]
- 下一页：[[00-Burst内存别名]]
