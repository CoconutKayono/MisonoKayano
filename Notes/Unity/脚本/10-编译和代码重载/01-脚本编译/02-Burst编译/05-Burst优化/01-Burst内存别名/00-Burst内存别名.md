# Burst 内存别名

> 原文：[Burst memory aliasing](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/memory-aliasing.html)

使用内存别名向 Burst 提供代码如何使用数据的信息，Burst 可以利用这些信息创建运行时优化。

| 页面 | 说明 |
| --- | --- |
| [[01-内存别名简介]] | 了解内存别名的工作方式，以及如何让 Burst 生成更高效的运行时代码。 |
| [[03-声明无别名指针和结构体]] | 使用 `[NoAlias]` attribute 向 Burst 提供指针和 struct 别名情况的额外信息。 |
| [[02-别名与Job System]] | 了解 Job 中别名适用的特殊限制。 |

## 其他资源

- [[../00-Burst优化]]

---

## 文档导航

- 上一页：[[../00-Burst优化]]
- 目录：[[00-Burst内存别名]]
- 下一页：[[01-内存别名简介]]
