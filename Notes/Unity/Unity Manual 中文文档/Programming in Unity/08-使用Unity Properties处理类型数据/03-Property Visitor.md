# Property Visitor

> 原文：[Property visitors](https://docs.unity3d.com/6000.7/Documentation/Manual/property-visitors.html)

Property Visitor 定义了访问某个类型的 Property Bag 并对其属性执行操作时所使用的逻辑。如果某个类型已经通过 Property Bag 暴露其属性，就可以在不直接修改该类型的情况下，为它创建额外功能。

可以创建高度通用的 Visitor，同时定义访问算法本身和访问过程。这与经典的 Visitor Pattern 实现不同：它可以处理任意类型，而不仅是特定类型。因此，可以为运行时发现的类型实现序列化、类似 Inspector 的 UI 生成等功能。

访问的基本流程如下，该流程发生在 Property Bag 及其配套对象上：

1. 某个类型的实例接受一个 Visitor。
2. Visitor 访问该实例的 Property Bag。
3. Property Bag 遍历其属性，并让这些属性接受 Visitor。

## 创建 Property Visitor 获取属性

可以使用以下方式创建 Visitor 以获取属性：

- 派生自 [`Unity.Properties.PropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.html) 基类。示例请参阅[[05-使用PropertyVisitor类创建Property Visitor]]。
- 实现 [`IPropertyBagVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IPropertyBagVisitor.html) 和 [`IPropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IPropertyVisitor.html) 接口。示例请参阅[[06-使用低级API创建Property Visitor]]。

第一种方式最容易上手。不过，如果需要更广泛地自定义 Property Bag 和属性的访问行为，应使用第二种方式，因为它提供了更大的灵活性，并且有可能改善性能。

下面的示例使用 [`PropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.html) 类，创建一个简单的 Visitor，获取带有特定属性标记的给定类型的属性：

```csharp
public class BindableAttribute
    : Attribute
{
}

public class GatherBindablePropertiesVisitor
    : PropertyVisitor
{
    public List<PropertyPath> BindableProperties { get; set; }

    protected override void VisitProperty<TContainer, TValue>(Property<TContainer, TValue> property, ref TContainer container, ref TValue value)
    {
        if (property.HasAttribute<BindableAttribute>())
            BindableProperties.Add(PropertyPath.AppendProperty(default, property));
    }
}
```

下面是使用 `IPropertyBagVisitor` 接口创建等效 Visitor 的示例：

```csharp
public class BindableAttribute
    : Attribute
{
}

public class GatherBindablePropertiesVisitor
    : IPropertyBagVisitor
{
    public List<PropertyPath> BindableProperties { get; set; }

    void IPropertyBagVisitor.Visit<TContainer>(IPropertyBag<TContainer> propertyBag, ref TContainer container)
    {
        // Loop through the properties of the container object.
        foreach (var property in propertyBag.GetProperties(ref container))
        {
            if (property.HasAttribute<BindableAttribute>())
                BindableProperties.Add(PropertyPath.AppendProperty(default, property));
        }
    }
}
```

Low-Level Visitor 的性能更好，因为它不需要遍历 Property Bag 的所有属性并提取属性值。还可以使用 Low-Level Visitor 访问不属于 Property Bag 的属性。

## 性能注意事项

Property Bag、Property 和 Visitor 都使用泛型类型实现，以尽可能保持代码的强类型特征，并避免访问过程中产生 Boxing 分配。使用泛型类型的代价是，JIT 编译器会在某个方法第一次调用时为该方法生成[中间语言（IL）](https://learn.microsoft.com/en-us/dotnet/standard/managed-code)。这可能导致 Visitor 第一次被对象接受时执行速度较慢。

## 其他资源

- [[02-Property Bag]]
- [[04-Property Path]]
- [[05-使用PropertyVisitor类创建Property Visitor]]
- [[06-使用低级API创建Property Visitor]]


---

## 文档导航

- 上一页：[[02-Property Bag]]
- 目录：[[00-使用Unity Properties处理类型数据]]
- 下一页：[[04-Property Path]]
