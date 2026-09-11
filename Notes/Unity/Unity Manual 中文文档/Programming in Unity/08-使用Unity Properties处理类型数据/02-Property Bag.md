# Property Bag

> 原文：[Property bags](https://docs.unity3d.com/6000.7/Documentation/Manual/property-bags.html)

Property Bag 是特定 .NET 对象类型的配套对象。该 Bag 包含其对应类型的属性集合。可以使用 Property Bag 高效地遍历、访问和修改对应类型对象实例中的数据。

## 生成 Property Bag

Unity 使用以下方式之一为类型生成 Property Bag：

- **Reflection**：默认情况下，Unity 使用 Reflection 为类型生成 Property Bag。Reflection 使用方便，并且采用[延迟初始化](https://learn.microsoft.com/en-us/dotnet/framework/performance/lazy-initialization)：只有在尚未注册某个类型的 Property Bag 时，才会为该类型生成一次。
- **代码生成**：为了提高性能，可以选择使用代码生成。要通过代码生成 Property Bag，必须：
  - 使用 [`[Unity.Properties.GeneratePropertyBag]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.GeneratePropertyBagAttribute.html) 属性标记类型。
  - 使用 [`[assembly: Unity.Properties.GeneratePropertyBagsForAssembly]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.GeneratePropertyBagsForAssemblyAttribute.html) 属性标记程序集。代码生成的 Property Bag 会在 Domain 加载时自动注册。

## 包含的成员

无论使用哪种方式生成 Property Bag，都会为以下类型成员生成属性：

- Public 字段。
- 使用 [`[SerializeField]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializeField.html)、[`[SerializeReference]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializeReference.html) 或 [`[CreateProperty]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.CreatePropertyAttribute.html) 标记的 Private 或 Internal 字段。
- 使用 [`[Unity.Properties.CreateProperty]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.CreatePropertyAttribute.html) 标记的 Public、Private 或 Internal 属性。

将 [`[DontCreateProperty]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.DontCreatePropertyAttribute.html) 属性添加到 Public、Private 或 Internal 字段，可以将其排除在 Property Bag 之外。

如果字段是只读的，或属性只有 getter，那么生成的属性就是只读的。也可以使用 [`[Unity.Properties.CreateProperty(ReadOnly = true)]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.DontCreatePropertyAttribute.html) 将生成的属性设为只读。

下面的示例将 Unity Serialization 系统与 Unity Properties 系统结合使用：

```csharp
using UnityEngine;
using Unity.Properties;

public class PropertyBagExample : MonoBehaviour
{
    // Serialization go through the field. 
    [SerializeField, DontCreateProperty] 
    private int m_Value;
    
    // Bindings go through the property rather than the field. 
    // This allows you to do validation, notify changes, and more.
    [CreateProperty] 
    public int value
    {
        get => m_Value;
        set => m_Value = value;
    }
    
    // This is a similar example, but for the backing field of an auto-property. 
    // Note that the name of the auto-property is postfixed with k_BackingField.
    [field: SerializeField, DontCreateProperty]
    [CreateProperty]
    public float floatValue { get; set; }
}
```

为了方便而使用 Serialization 属性在 Property Bag 中创建属性，并不总是首选方案。[Unity Serialization 系统](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization.html)只能处理字段和自动属性，这使得有效验证或传播更改变得困难。

与 Unity Serialization 系统不同，Property Bag 中的属性不会因为带有 [`[SerializeField]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializeField.html) 而被视为值类型。相反，结构体类型会被识别为值类型，而类类型会被识别为引用。

在 Unity Serialization 中，虽然支持多态，但必须使用 [`[SerializeReference]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializeReference.html) 属性显式启用多态。否则，实例会被序列化为值类型。请注意，`UnityEngine.Object` 类型是这一规则的例外，会自动被序列化为引用类型。

## 性能注意事项

通过 Reflection 生成 Property Bag 时，第一次为某个容器类型请求 Property Bag 可能会产生性能开销。通过 Reflection 为字段成员创建属性，可能会分配内存，并在 IL2CPP 构建中增加 Garbage Collector 的开销。

为了避免 Reflection 并提高性能，可以改为[通过代码生成 Property Bag](#生成-property-bag)。但是请注意，这种运行时优化可能会延长编译时间。若要让 Property Bag 访问 Internal 和 Private 字段及属性，请将类型声明为 `partial`。

## 其他资源

- [[03-Property Visitor]]
- [[04-Property Path]]
- [[05-使用PropertyVisitor类创建Property Visitor]]
- [[06-使用低级API创建Property Visitor]]


---

## 文档导航

- 上一页：[[01-Unity Properties简介]]
- 目录：[[00-使用Unity Properties处理类型数据]]
- 下一页：[[03-Property Visitor]]
