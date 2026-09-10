# 使用非托管 API 执行 Transform 操作

> 原文：[Using unmanaged API for transform operations](https://docs.unity3d.com/6000.7/Documentation/Manual/transformhandle-landing.html)

[`TransformHandle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.html) API 是 [`Transform`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html) API 的替代方案。与 `Transform` 组件（托管类）不同，`TransformHandle` 是非托管 `struct`，因此与 [Burst](https://docs.unity3d.com/Packages/com.unity.burst@latest) 编译器完全兼容。

| 页面 | 说明 |
| --- | --- |
| [[01-TransformHandle API简介]] | 介绍 `TransformHandle` API，以及它与 `Transform` API 的主要差异。 |
| [[02-TransformHandle API代码示例]] | 展示 `Transform` 与 `TransformHandle` API 差异的代码示例。 |
| [[03-在Burst中使用TransformHandle]] | 介绍与 Burst 编译器兼容的 `TransformHandle` API，以及如何借此优化代码。 |

## 其他资源

- [Transforms](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Transform.html)

---

## 文档导航

- 上一页：[[../04-优化托管内存代码/01-优化数组]]
- 目录：[[00-使用非托管API执行Transform操作]]
- 下一页：[[01-TransformHandle API简介]]
