# TransformHandle API 简介

> 原文：[Introduction to TransformHandle API](https://docs.unity3d.com/6000.7/Documentation/Manual/class-TransformHandle.html)

[`TransformHandle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.html) API 是 [`Transform`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html) API 的替代方案。与 `Transform` 组件（托管类）不同，`TransformHandle` 是非托管 `struct`，因此与在主线程上运行的代码中的 [Burst](https://docs.unity3d.com/Packages/com.unity.burst@latest) 编译器兼容。

虽然 `TransformHandle` API 与 `Transform` API 覆盖相同的核心操作，但其设计带来了本页所述的若干主要差异。`TransformHandle` API 确保了与未来 Entity 和 `GameObject` 交互的兼容性。

## 与 Transform API 的差异

`TransformHandle` API 的功能与 `Transform` API 等效，主要差异在于访问方式和实现细节。`TransformHandle` API 可以在 Unity 6 中与 `Transform` API 并行使用。

| Transform API（Unity 6.2 及更早版本） | TransformHandle API（Unity 6.3 及更高版本） |
| --- | --- |
| 通过 `GameObject.transform` 属性访问 Transform。 | 通过 `gameObject.transformHandle` 或 `transform.GetTransformHandle` 访问 Transform，其中 `transform` 是 `Transform` 组件。 |
| 返回 `Transform` 组件引用（托管类型）。 | 返回 `TransformHandle` struct（非托管类型）。 |
| API 是托管的，与 [Burst](https://docs.unity3d.com/Packages/com.unity.burst@latest) 编译器不兼容。 | 与在主线程上运行的 Burst 编译代码中的 [Burst](https://docs.unity3d.com/Packages/com.unity.burst@latest) 编译器兼容。`TransformHandle` struct 不是线程安全的；如果从实现了 `IJobParallelForTransform` 等接口的 Job 中访问它，会抛出安全异常。要从 Job 中读取或写入 Transform 值，请使用 [`TransformAccessArray`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Jobs.TransformAccessArray.html) struct；可以从 `NativeArray<TransformHandle>` 集合构造该 struct。更多信息，请参阅 [[03-在Burst中使用TransformHandle]]。 |
| Editor 和运行时 API。 | 仅运行时 API。 |

## TransformHandle API 中不可用的 Transform API

以下 `Transform` API 中的方法和属性在 `TransformHandle` API 中不可用：

- `GetSiblingIndex` / `SetSiblingIndex`
- `Find`
- `hasChanged` 属性

## TransformHandle API 中没有对应 Transform API 的功能

以下 `TransformHandle` API 元素在 `Transform` API 中没有对应功能：

- [`TransformHandle.DirectChildrenEnumerable`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.DirectChildrenEnumerable.html)：表示一个 TransformHandle 直接子节点的可枚举对象；枚举该对象时会返回 `DirectChildrenEnumerator`。
- [`TransformHandle.DirectChildrenEnumerator`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.DirectChildrenEnumerator.html)：遍历 Transform 直接子节点的枚举器。
- [`TransformHandle.DirectChildren`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.DirectChildren.html)：返回此 Transform 的 `DirectChildrenEnumerable`，可以使用 `foreach` 循环遍历直接子节点。
- [`TransformHandle.GetDirectChildrenEnumerator`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.GetDirectChildrenEnumerator.html)：返回此 Transform 的 `DirectChildrenEnumerator`，可以使用它手动遍历直接子节点。
- [`TransformHandle.SubhierarchyEnumerable`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.SubhierarchyEnumerable.html)：表示一个 `TransformHandle` 实例及其所有后代的可枚举对象；枚举该对象时会返回一个 `TransformHandle.SubhierarchyEnumerator` 实例。
- [`TransformHandle.SubhierarchyEnumerator`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.SubhierarchyEnumerator.html)：产生一个 `TransformHandle` 实例及其所有后代。它首先产生 `TransformHandle` 实例本身，然后按深度优先顺序产生其后代。
- [`TransformHandle.Subhierarchy`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.Subhierarchy.html)：返回一个 `TransformHandle.SubhierarchyEnumerable` 实例，可以使用 `foreach` 循环遍历此 `TransformHandle` 实例及其所有后代。
- [`TransformHandle.GetSubhierarchyEnumerator`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TransformHandle.GetSubhierarchyEnumerator.html)：返回一个 `TransformHandle.SubhierarchyEnumerator` 实例，可以使用它手动遍历此 `TransformHandle` 实例及其所有后代。

## 常见操作的差异

以下常见操作在 `TransformHandle` API 中具有不同的实现方式。

检查 Transform 是否有效：

- **Transform**：`transform != null`
- **TransformHandle**：`TransformHandle.IsValid`

遍历 Transform 的直接子节点：

- **Transform**：`foreach (Transform t in transform)`
- **TransformHandle**：`foreach (TransformHandle t in handle.DirectChildren)`

将 Transform 的父级设置为 `None`：

- **Transform**：`transform.SetParent(null)`
- **TransformHandle**：`transformHandle.SetParent(TransformHandle.None)`

替代写法：

```csharp
TransformHandle h = transformHandle;
h.parent = TransformHandle.None;
```

有关如何使用该 API 的具体示例，请参阅 [[02-TransformHandle API代码示例]]。

## 参数或返回类型不同的方法

以下方法在功能上等效，但参数类型或返回类型不同；具体类型取决于调用它们的 API 是 `Transform` 还是 `TransformHandle`。

参数类型不同的方法：

- `IsChildOf`
- `LookAt`
- `SetParent`
- `Translate`（重载）

返回类型不同的方法或属性：

- `GetChild`
- `parent`
- `root`

## 其他资源

- [[02-TransformHandle API代码示例]]
- [[03-在Burst中使用TransformHandle]]

---

## 文档导航

- 上一页：[[00-使用非托管API执行Transform操作]]
- 目录：[[00-使用非托管API执行Transform操作]]
- 下一页：[[02-TransformHandle API代码示例]]
