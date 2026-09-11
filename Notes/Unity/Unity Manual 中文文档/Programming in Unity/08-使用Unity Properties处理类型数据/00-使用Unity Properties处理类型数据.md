# 使用 Unity Properties 处理类型数据

> 原文：[Handle type data generically with Unity Properties](https://docs.unity3d.com/6000.7/Documentation/Manual/properties.html)

位于 `Unity.Properties` Namespace 中的 Unity Properties API 使用 [Visitor Design Pattern](https://en.wikipedia.org/wiki/Visitor_pattern)，在运行时访问 .NET 对象。访问对象可以发现和修改其属性，也可以在不修改现有对象结构的情况下，在运行时为其添加新操作。可以在 Visitor Pattern 的基础上构建多种功能，例如序列化、数据迁移、深度数据比较和数据绑定。

| 页面 | 说明 |
| --- | --- |
| [[01-Unity Properties简介]] | 了解 Unity Properties API 的基础和用途。 |
| [[02-Property Bag]] | 了解 Property Bag 的作用，以及使用它时需要考虑的性能因素。 |
| [[03-Property Visitor]] | 了解 Property Visitor 的作用，以及使用它时需要考虑的性能因素。 |
| [[04-Property Path]] | 了解 Property Path 的作用，以及使用它时需要考虑的性能因素。 |
| [[05-使用PropertyVisitor类创建Property Visitor]] | 通过示例了解如何使用 `PropertyVisitor` 基类创建 Property Visitor。 |
| [[06-使用低级API创建Property Visitor]] | 通过示例了解如何使用 `IPropertyBagVisitor` 和 `IPropertyVisitor` 接口创建 Property Visitor。 |

## 其他资源

- [Serialization](https://docs.unity3d.com/Packages/com.unity.serialization@latest)
- [运行时数据绑定](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-runtime-binding.html)


---

## 文档导航

- 上一页：[[03-Web Request低级API参考]]
- 目录：[[00-使用Unity Properties处理类型数据]]
- 下一页：[[01-Unity Properties简介]]
