# 使用 PropertyVisitor 类创建 Property Visitor

> 原文：[Create a property visitor with the PropertyVisitor class](https://docs.unity3d.com/6000.7/Documentation/Manual/property-visitors-PropertyVisitor.html)

本示例演示如何使用 [`PropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.html) 基类创建 Property Visitor。使用 [`IPropertyBagVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IPropertyBagVisitor.html) 和 [`IPropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IPropertyVisitor.html) 接口的等效示例，请参阅[[06-使用低级API创建Property Visitor]]。

## 创建数据类和工具类

创建一个简单的数据类，以及一个使用 Visitor 访问并打印其属性的工具类：

1. 创建下面名为 `Data` 的 C# 类，并添加可以被访问的属性：

   ```csharp
   using System.Collections.Generic;
   using UnityEngine;

   public class Data
   {
       public string Name = "Henry";
       public Vector2 Vec2 = Vector2.one;
       public List<Color> Colors = new List<Color> { Color.green, Color.red };
       public Dictionary<int, string> Dict = new Dictionary<int, string> { { 5, "zero" } };
   }
   ```

2. 创建下面名为 `DebugUtilities` 的工具类：

   ```csharp
   using UnityEngine;

   public static class DebugUtilities
   {
       public static void PrintObjectDump<T>(T value)
       {
       // Magic goes here.
       }
   }
   ```

## 创建 Visitor

按以下方式创建 Visitor 类：

1. 创建名为 `ObjectVisitor` 的类，并让它继承自 [`PropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.html)。
2. 向类中添加一个 [`StringBuilder`](https://learn.microsoft.com/en-us/dotnet/api/system.text.stringbuilder?view=net-7.0) 字段。可以使用它构建表示对象当前状态的字符串。
3. 添加一个 `Reset` 方法，用于清空 `StringBuilder` 并重置缩进级别。
4. 添加一个 `GetDump` 方法，返回表示对象当前状态的字符串。

此时，`ObjectVisitor` 类如下所示：

```csharp
// `PropertyVisitor` is an abstract class that you must derive from. 
public class ObjectVisitor: PropertyVisitor
{
    private const int k_InitialIndent = 0;
    private readonly StringBuilder m_Builder = new StringBuilder();
        
    private int m_IndentLevel = k_InitialIndent;
        
    private string Indent => new (' ', m_IndentLevel * 2);
        
    public void Reset()
    {
        m_Builder.Clear();
        m_IndentLevel = k_InitialIndent;
    }

    public string GetDump()
    {
        return m_Builder.ToString();
    }
}
```

## 获取顶层属性

在 `ObjectVisitor` 类中重写 [`VisitProperty`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.VisitProperty.html) 方法，访问对象的每个属性并记录属性名称。`PropertyVisitor` 不要求实现任何成员；默认情况下，它只访问每个属性而不执行任何操作。

1. 在 `ObjectVisitor` 类中添加以下 `VisitProperty` 重写方法：

   ```csharp
   protected override void VisitProperty<TContainer, TValue>(Property<TContainer, TValue> property, ref TContainer container, ref TValue value)
   {
       m_Builder.AppendLine($"- {property.Name}");
   }
   ```

2. 现在已经有了一个最小 Visitor，可以实现工具方法。更新 `DebugUtilities` 类中的 `PrintObjectDump` 方法，创建新的 `ObjectVisitor` 实例，并使用它访问给定对象的属性：

   ```csharp
   public static class DebugUtilities
   {
       private static readonly ObjectVisitor s_Visitor = new();
           
       public static void PrintObjectDump<T>(T value)
       {
           s_Visitor.Reset();
               
           // This is the main entry point to run a visitor.
           PropertyContainer.Accept(s_Visitor, ref value);
           Debug.Log(s_Visitor.GetDump());
       }
   }
   ```

3. 在代码中的适当位置调用 `PrintObjectDump` 方法，并将一个 `Data` 对象传给它。例如，在简单的 MonoBehaviour 组件中，可以这样调用：

   ```csharp
   using UnityEngine;

   public class MyMonoBehaviour : MonoBehaviour
   {
       
       void Start()
       {
       DebugUtilities.PrintObjectDump(new Data());
       }

   }
   ```

   这会在 Console 中打印以下输出：

   ```text
   - Name
   - Vec2
   - Colors
   - Dict
   ```

## 获取子属性

上一节的输出表明，重写 [`VisitProperty`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.VisitProperty.html) 方法时，不会自动访问对象的子属性。要获取子属性，请使用 [`PropertyContainer.Accept`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyContainer.Accept.html) 方法，让 Visitor 递归地访问每个值。

在 `ObjectVisitor` 类中，更新 `VisitProperty` 方法，使 Visitor 递归访问要嵌套的值：

```csharp
protected override void VisitProperty<TContainer, TValue>(Property<TContainer, TValue> property, ref TContainer container, ref TValue value)
{
    m_Builder.AppendLine($"{Indent}- {property.Name}");
        
    ++m_IndentLevel;
    // Apply this visitor recursively on the value to nest in.
    if (null != value)
        PropertyContainer.Accept(this, ref value);
    --m_IndentLevel;
}
```

此时，Console 输出如下：

```text
- Name
- Vec2
- x
- y
- Colors
- 0
    - r
    - g
    - b
    - a
- 1
    - r
    - g
    - b
    - a 
- Dict
- 5
    - Key
    - Value
```

## 显示每个属性的更多信息

为了进一步改进打印输出，可以获取集合元素的属性名称，以及每个属性的类型和值。某些属性具有特殊名称，在处理集合元素时尤其如此。属性名称遵循以下约定：

- 对于列表元素，名称对应其索引。
- 对于字典，名称来自键值的字符串形式。
- 对于集合，名称基于值的字符串形式。

为了更明确地区分这些情况，可以将属性名称放在方括号中。

1. 在 `ObjectVisitor` 类中添加以下方法：

   ```csharp
   private static string GetPropertyName(IProperty property)
   {
       return property switch
       {
           // You can also treat `IListElementProperty`, `IDictionaryElementProperty`, and `ISetElementProperty` separately.
           ICollectionElementProperty => $"[{property.Name}]",
           _ => property.Name
       };
   }
   ```

2. 更新 `VisitProperty` 方法，使用 [`TypeUtility.GetTypeDisplayName`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.TypeUtility.GetTypeDisplayName.html) 获取给定类型的显示名称：

   ```csharp
   protected override void VisitProperty<TContainer, TValue>(Property<TContainer, TValue> property, ref TContainer container, ref TValue value)
   {
       var propertyName = GetPropertyName(property);
           
       // Get the concrete type of the property or its declared type if value is null.
       var typeName = TypeUtility.GetTypeDisplayName(value?.GetType() ?? property.DeclaredValueType());
           
       m_Builder.AppendLine($"{Indent}- {propertyName} = {{{typeName}}} {value}");
           
       ++m_IndentLevel;
       if (null != value)
           PropertyContainer.Accept(this, ref value);
       --m_IndentLevel;
   }
   ```

   此时，Console 输出如下：

   ```text
   - Name = {string} Henry
   - Vec2 = {Vector2} (1.00, 1.00)
   - x = {float} 1
   - y = {float} 1
   - Colors = {List<Color>} System.Collections.Generic.List`1[UnityEngine.Color]
   - [1] = {Color} RGBA(0.000, 1.000, 0.000, 1.000)
       - r = {float} 0
       - g = {float} 1
       - b = {float} 0
       - a = {float} 1
   - [1] = {Color} RGBA(1.000, 0.000, 0.000, 1.000)
       - r = {float} 1
       - g = {float} 0
       - b = {float} 0
       - a = {float} 1
   - Dict = {Dictionary<int, string>} System.Collections.Generic.Dictionary`2[System.Int32,System.String]
   - [5] = {KeyValuePair<int, string>} [5, five]
       - Key = {int} 5
       - Value = {string} five
   ```

## 减少集合类型显示的信息

由于 `List<T>` 没有重写 `ToString` 方法，列表值会显示为 `System.Collections.Generic.List1[UnityEngine.Color]`。为了减少显示的信息，可以更新 `VisitProperty`，使用 [`TypeTraits.IsContainer`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.TypeTraits.IsContainer.html) 工具方法，只显示不包含子属性的类型值，例如基元类型、枚举和字符串。

在 `ObjectVisitor` 类中更新 `VisitProperty` 方法，使用 `TypeTraits.IsContainer` 判断值是否为容器类型。如果是容器，则不显示值，只显示类型名称；否则同时显示类型名称和值：

```csharp
protected override void VisitProperty<TContainer, TValue>(Property<TContainer, TValue> property, ref TContainer container, ref TValue value)
{
    var propertyName = GetPropertyName(property);

    var type = value?.GetType() ?? property.DeclaredValueType();
    var typeName = TypeUtility.GetTypeDisplayName(type);
    
    // Only display the values for primitives, enums and strings.
    if (TypeTraits.IsContainer(type))
        m_Builder.AppendLine($"{Indent}- {propertyName} {{{typeName}}}");
    else
        m_Builder.AppendLine($"{Indent}- {propertyName} = {{{typeName}}} {value}");
    
    ++m_IndentLevel;
    if (null != value)
        PropertyContainer.Accept(this, ref value);
    --m_IndentLevel;
}
```

此时，Console 输出如下：

```text
- Name = {string} Henry
- Vec2 {Vector2}
- x = {float} 1
- y = {float} 1
- Colors {List<Color>}
- [0] {Color}
    - r = {float} 0
    - g = {float} 1
    - b = {float} 0
    - a = {float} 1
- [1] {Color}
    - r = {float} 1
    - g = {float} 0
    - b = {float} 0
    - a = {float} 1
- Dict {Dictionary<int, string>}
- [5] {KeyValuePair<int, string>}
    - Key = {int} 5
    - Value = {string} five
```

> [!TIP]
> 为了减少显示的信息，也可以使用以下方法，为集合类型重写某个 `Visit` 特化方法：
>
> - [`PropertyVisitor.VisitCollection`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.VisitCollection.html)
> - [`PropertyVisitor.VisitList`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.VisitList.html)
> - [`PropertyVisitor.VisitDictionary`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.VisitDictionary.html)
> - [`PropertyVisitor.VisitSet`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.VisitSet.html)
>
> 这些方法与 [`VisitProperty`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.VisitProperty.html) 类似，但会暴露对应集合类型的泛型参数。

## 添加类型专用重写

添加类型专用重写，以更紧凑的形式显示 [`Vector2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/UnityEngine.Vector2.html) 和 [`Color`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/UnityEngine.Color.html) 类型。

使用 [`PropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.html) 和 [`IVisitPropertyAdapter`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IVisitPropertyAdapter.html)。当为特定类型注册 Adapter 后，如果访问过程中遇到目标类型，就会调用 Adapter，而不是调用 [`VisitProperty`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.VisitProperty.html) 方法。

在 `ObjectVisitor` 类中，为 `Vector2` 和 `Color` 添加 `IVisitPropertyAdapter`：

```csharp
public class DumpObjectVisitor
    : PropertyVisitor
    , IVisitPropertyAdapter<Vector2>
    , IVisitPropertyAdapter<Color>
{
    public DumpObjectVisitor()
    {
        AddAdapter(this);
    }
    
    void IVisitPropertyAdapter<Vector2>.Visit<TContainer>(in VisitContext<TContainer, Vector2> context, ref TContainer container, ref Vector2 value)
    {
        var propertyName = GetPropertyName(context.Property);
        m_Builder.AppendLine($"{Indent}- {propertyName} = {{{nameof(Vector2)}}} {value}");
    }

    void IVisitPropertyAdapter<Color>.Visit<TContainer>(in VisitContext<TContainer, Color> context, ref TContainer container, ref Color value)
    {
        var propertyName = GetPropertyName(context.Property);
        m_Builder.AppendLine($"{Indent}- {propertyName} = {{{nameof(Color)}}} {value}");
    }
}
```

## 从子属性开始访问

在数据上运行 Visitor 时，默认情况下会从顶层对象开始访问。对于任意 Property Visitor，如果要从对象的子属性开始访问，请将 [`PropertyPath`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyPath.html) 传给 [`PropertyContainer.Accept`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyContainer.Accept.html) 方法。

1. 更新 `DebugUtilities` 方法，使其接受可选的 `PropertyPath`：

   ```csharp
   public static class DebugUtilities
   {
       private static readonly ObjectVisitor s_Visitor = new();

       public static void PrintObjectDump<T>(T value, PropertyPath path = default)
       {
           s_Visitor.Reset();
           if (path.IsEmpty)
               PropertyContainer.Accept(s_Visitor, ref value);
           else
               PropertyContainer.Accept(s_Visitor, ref value, path);
           Debug.Log(s_Visitor.GetDump());
       }
   }
   ```

2. 使用 `Data` 对象调用 `PrintObjectDump` 方法。此时，Console 输出如下：

   ```text
   - Name {string} = Henry
   - Vec2 {Vector2} = (1.00, 1.00)
   - Colors {List<Color>}
     - [0] = {Color} RGBA(0.000, 1.000, 0.000, 1.000)
     - [1] = {Color} RGBA(1.000, 0.000, 0.000, 1.000)
   - Dict {Dictionary<int, string>}
     - [5] {KeyValuePair<int, string>}
       - Key {int} = 5
       - Value {string} = five
   ```

## 完整的 Visitor 代码

现在，Visitor 类的完整代码如下：

```csharp
using System.Text;
using Unity.Properties;
using UnityEngine;

public class ObjectVisitor
: PropertyVisitor
, IVisitPropertyAdapter<Vector2>
, IVisitPropertyAdapter<Color>
{
    private const int k_InitialIndent = 0;

    // StringBuilder to store the dumped object's properties and values.
    private readonly StringBuilder m_Builder = new StringBuilder();
    private int m_IndentLevel = k_InitialIndent;

    // Helper property to get the current indentation.
    private string Indent => new(' ', m_IndentLevel * 2);

    public ObjectVisitor()
    {
        // Constructor, it initializes the ObjectVisitor and adds itself as an adapter
        // to handle properties of type Vector2 and Color.
        AddAdapter(this);
    }

    // Reset the visitor, clearing the StringBuilder and setting indentation to initial level.
    public void Reset()
    {
        m_Builder.Clear();
        m_IndentLevel = k_InitialIndent;
    }

    // Get the string representation of the dumped object.
    public string GetDump()
    {
        return m_Builder.ToString();
    }

    // Helper method to get the property name, handling collections and other property types.
    private static string GetPropertyName(IProperty property)
    {
        return property switch
        {
            // If it's a collection element property, display it with brackets
            ICollectionElementProperty => $"[{property.Name}]",
            // For other property types, display the name as it is
            _ => property.Name
        };
    }

    // This method is called when visiting each property of an object.
    // It determines the type of the value and formats it accordingly for display.
    protected override void VisitProperty<TContainer, TValue>(Property<TContainer, TValue> property, ref TContainer container, ref TValue value)
    {
        var propertyName = GetPropertyName(property);

        // Get the type of the value or property.
        var type = value?.GetType() ?? property.DeclaredValueType();
        var typeName = TypeUtility.GetTypeDisplayName(type);

        // Only display the values for primitives, enums, and strings, and treat other types as containers.
        if (TypeTraits.IsContainer(type))
            m_Builder.AppendLine($"{Indent}- {propertyName} {{{typeName}}}");
        else
            m_Builder.AppendLine($"{Indent}- {propertyName} = {{{typeName}}} {value}");

        // Increase indentation level before visiting child properties (if any).
        ++m_IndentLevel;
        if (null != value)
            PropertyContainer.Accept(this, ref value);
        // Decrease indentation level after visiting child properties.
        --m_IndentLevel;
    }
    
    // This method is a specialized override for Vector2 properties.
    // It displays the property name and its value as a Vector2.
    void IVisitPropertyAdapter<Vector2>.Visit<TContainer>(in VisitContext<TContainer, Vector2> context, ref TContainer container, ref Vector2 value)
    {
        var propertyName = GetPropertyName(context.Property);
        m_Builder.AppendLine($"{Indent}- {propertyName} = {{{nameof(Vector2)}}} {value}");
    }

    // This method is a specialized override for Color properties.
    // It displays the property name and its value as a Color.
    void IVisitPropertyAdapter<Color>.Visit<TContainer>(in VisitContext<TContainer, Color> context, ref TContainer container, ref Color value)
    {
        var propertyName = GetPropertyName(context.Property);
        m_Builder.AppendLine($"{Indent}- {propertyName} = {{{nameof(Color)}}} {value}");
    }
   
}
```

## 其他资源

- [[03-Property Visitor]]
- [[02-Property Bag]]
- [[04-Property Path]]
- [[06-使用低级API创建Property Visitor]]


---

## 文档导航

- 上一页：[[04-Property Path]]
- 目录：[[00-使用Unity Properties处理类型数据]]
- 下一页：[[06-使用低级API创建Property Visitor]]
