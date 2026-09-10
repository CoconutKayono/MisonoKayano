# 使用低级 API 创建 Property Visitor

> 原文：[Create a property visitor with low-level APIs](https://docs.unity3d.com/6000.7/Documentation/Manual/property-visitors-low-level-api.html)

本示例演示如何使用低级 [`IPropertyBagVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IPropertyBagVisitor.html) 和 [`IPropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IPropertyVisitor.html) 接口创建 Property Visitor。它与[[05-使用PropertyVisitor类创建Property Visitor]]示例产生相同结果，但这里的 Visitor 实现这些接口，而不是继承 [`PropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.html)。

## 创建数据类和工具类

1. 创建与[[05-使用PropertyVisitor类创建Property Visitor]]示例中相同的 `Data` 和 `DebugUtilities` 类。
2. 修改 `DebugUtilities` 类，使用低级 Visitor 替代继承自 `PropertyVisitor` 的 Visitor：

   ```csharp
   public static class DebugUtilities
   {
       private static readonly LowLevelVisitor s_Visitor = new();

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

## 创建 Visitor

按以下方式创建低级 Visitor 类：

1. 创建一个名为 `LowLevelVisitor` 的类，实现 `IPropertyVisitor` 和 `IPropertyBagVisitor` 接口。
2. 向类中添加一个 [`StringBuilder`](https://learn.microsoft.com/en-us/dotnet/api/system.text.stringbuilder?view=net-7.0) 字段。可以使用它构建表示对象当前状态的字符串。
3. 添加一个 `Reset` 方法，用于清空 `StringBuilder` 并重置缩进级别。
4. 添加一个 `GetDump` 方法，返回表示对象当前状态的字符串。

此时，`LowLevelVisitor` 类如下所示：

```csharp
public class LowLevelVisitor
    : IPropertyBagVisitor
    , IPropertyVisitor
{
    private const int k_InitialIndent = 0;

    private readonly StringBuilder m_Builder = new StringBuilder();
    private int m_IndentLevel = k_InitialIndent;

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

## 获取属性

要使用 `this` 调用属性上的 [`Accept`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.Property_2.Accept.html) 方法，请实现 [`IPropertyVisitor`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IPropertyVisitor.html) 接口。此接口允许你指定访问属性时的行为，类似于 [`PropertyVisitor.VisitProperty`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyVisitor.VisitProperty.html) 方法。

1. 在 `LowLevelVisitor` 类中实现 `IPropertyBagVisitor.Visit` 和 `IPropertyVisitor.Visit` 方法：

   ```csharp
   void IPropertyBagVisitor.Visit<TContainer>(IPropertyBag<TContainer> propertyBag, ref TContainer container)
   {
       foreach (var property in propertyBag.GetProperties(ref container))
       {
           property.Accept(this, ref container);
       }
   }
           
   void IPropertyVisitor.Visit<TContainer, TValue>(Property<TContainer, TValue> property, ref TContainer container)
   {
       var value = property.GetValue(ref container);
       // Code goes here.
   }
   ```

2. 与 `PropertyVisitor` 基类一起使用的 `IVisitPropertyAdapter` Adapter 需要访问 Visitor 的内部状态，因此不能在该类之外使用。不过，可以定义包含必要信息的领域专用 Adapter。在与 `LowLevelVisitor` 类相同的文件中，定义 `IPrintValue`、`IPrintValue<in T>` 接口和 `PrintContext` 结构体，封装 Adapter 将属性值格式化为以下形式所需的信息：

   ```csharp
   // Create the following struct with methods to encapsulate the formatting of the message and display the value.
   public readonly struct PrintContext
   {
       private StringBuilder Builder { get; }
       private string Prefix { get; }
       public string PropertyName { get; }

       public void Print<T>(T value)
       {
           Builder.AppendLine($"{Prefix}- {PropertyName} = {{{TypeUtility.GetTypeDisplayName(value?.GetType() ?? typeof(T))}}} {value}");
       }
           
       public void Print(Type type, string value)
       {
           Builder.AppendLine($"{Prefix}- {PropertyName} = {{{TypeUtility.GetTypeDisplayName(type)}}} {value}");
       }

       public PrintContext(StringBuilder builder, string prefix, string propertyName)
       {
           Builder = builder;
           Prefix = prefix;
           PropertyName = propertyName;
       }
   }

   public interface IPrintValue
   {
   }

   public interface IPrintValue<in T> : IPrintValue
   {
       void PrintValue(in PrintContext context, T value);
   }
   ```

3. 在 `LowLevelVisitor` 类中实现 Adapter 接口方法，为 [`Vector2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html) 和 [`Color`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Color.html) 创建类型专用 Adapter，并更新 `IPropertyVisitor` 的实现，使其优先使用 Adapter：

   ```csharp
   public class LowLevelVisitor
       : IPropertyBagVisitor
       , IPropertyVisitor
       , IPrintValue<Vector2>
       , IPrintValue<Color>
   {
       public IPrintValue Adapter { get; set; }
           
       public LowLevelVisitor()
       {
           // For simplicity
           Adapter = this;
       }
       void IPropertyVisitor.Visit<TContainer, TValue>(Property<TContainer, TValue> property, ref TContainer container)
       {
           // Here, we need to manually extract the value.
           var value = property.GetValue(ref container);
           
           var propertyName = GetPropertyName(property);
           
           // We can still use adapters, but we must manually dispatch the calls. 
           if (Adapter is IPrintValue<TValue> adapter)
           {
               var context = new PrintContext(m_Builder, Indent, propertyName);
               adapter.PrintValue(context, value);
               return;
           }
               
           // Fallback behaviour here 
       }
           
       void IPrintValue<Vector2>.PrintValue(in PrintContext context, Vector2 value)
       {
           context.Print(value);
       }
       void IPrintValue<Color>.PrintValue(in PrintContext context, Color value)
       {
           const string format = "F3";
           var formatProvider = CultureInfo.InvariantCulture.NumberFormat;
           context.Print(typeof(Color), $"RGBA({value.r.ToString(format, formatProvider)}, {value.g.ToString(format, formatProvider)}, {value.b.ToString(format, formatProvider)}, {value.a.ToString(format, formatProvider)})");
       }
   }
   ```

## 完整的 Visitor 代码

低级 Visitor 类以及 `Color` 和 `Vector2` 自定义 Adapter 的完整代码如下：

```csharp
using UnityEngine;
using System.Globalization;
using System.Text;
using Unity.Properties;

public readonly struct PrintContext
{
    // A context struct to hold information about how to print the property.
    private StringBuilder Builder { get; }
    private string Prefix { get; }
    public string PropertyName { get; }

    // Method to print the value of type T with its associated property name.
    public void Print<T>(T value)
    {
        Builder.AppendLine($"{Prefix}- {PropertyName} = {{{TypeUtility.GetTypeDisplayName(value?.GetType() ?? typeof(T))}}} {value}");
    }

    // Method to print the value with a specified type and its associated property name.
    public void Print(System.Type type, string value)
    {
        Builder.AppendLine($"{Prefix}- {PropertyName} = {{{TypeUtility.GetTypeDisplayName(type)}}} {value}");
    }

    // Constructor to initialize the PrintContext.
    public PrintContext(StringBuilder builder, string prefix, string propertyName)
    {
        Builder = builder;
        Prefix = prefix;
        PropertyName = propertyName;
    }
}

// Generic interface IPrintValue that acts as a marker interface for all print value adapters.
public interface IPrintValue
{
}

// Generic interface IPrintValue<T> to define how to print values of type T.
// This interface is used as an adapter for specific types (Vector2 and Color in this case).
public interface IPrintValue<in T> : IPrintValue
{
    void PrintValue(in PrintContext context, T value);
}

// LowLevelVisitor class that implements various interfaces for property visiting and value printing.
public class LowLevelVisitor : IPropertyBagVisitor, IPropertyVisitor, IPrintValue<Vector2>, IPrintValue<Color>
{
    private const int k_InitialIndent = 0;

    private readonly StringBuilder m_Builder = new StringBuilder();
    private int m_IndentLevel = k_InitialIndent;

    public IPrintValue Adapter { get; set; }

    public LowLevelVisitor()
    {
        // The Adapter property is set to this instance of LowLevelVisitor.
        // This means the current LowLevelVisitor can be used as a print value adapter for Vector2 and Color.
        Adapter = this;
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
            // If it's a collection element property, display it with brackets.
            ICollectionElementProperty => $"[{property.Name}]",
            // For other property types, display the name as it is
            _ => property.Name
        };
    }

    // This method is called when visiting a property bag (a collection of properties)
    void IPropertyBagVisitor.Visit<TContainer>(IPropertyBag<TContainer> propertyBag, ref TContainer container)
    {
        foreach (var property in propertyBag.GetProperties(ref container))
        {
            // Call the Visit method of IPropertyVisitor to handle individual properties.
            property.Accept(this, ref container);
        }
    }

    // This method is called when visiting each individual property of an object.
    // It tries to find a suitable adapter (IPrintValue<T>) for the property value type (TValue) and uses it to print the value.
    // If no suitable adapter is found, it falls back to displaying the value using its type name.
    void IPropertyVisitor.Visit<TContainer, TValue>(Property<TContainer, TValue> property, ref TContainer container)
    {
        // Here, we need to manually extract the value.
        var value = property.GetValue(ref container);

        var propertyName = GetPropertyName(property);

        // We can still use adapters, but we must manually dispatch the calls.
        // Try to find an adapter for the current property value type (TValue).
        if (Adapter is IPrintValue<TValue> adapter)
        {
            // If an adapter is found, create a print context and call the PrintValue method of the adapter.
            var context = new PrintContext(m_Builder, m_IndentLevel.ToString(), propertyName);
            adapter.PrintValue(context, value);
            return;
        }

        // Fallback behavior here - if no adapter is found, handle printing based on type information.
        var type = value?.GetType() ?? property.DeclaredValueType();
        var typeName = TypeUtility.GetTypeDisplayName(type);

        if (TypeTraits.IsContainer(type))
            m_Builder.AppendLine($"{m_IndentLevel}- {propertyName} {{{typeName}}}");
        else
            m_Builder.AppendLine($"{m_IndentLevel}- {propertyName} = {{{typeName}}} {value}");

        // Recursively visit child properties (if any).
        ++m_IndentLevel;
        if (null != value)
            PropertyContainer.Accept(this, ref value);
        --m_IndentLevel;
    }

    // Method from IPrintValue<Vector2> used to print Vector2 values.
    void IPrintValue<Vector2>.PrintValue(in PrintContext context, Vector2 value)
    {
        // Simply use the Print method of PrintContext to print the Vector2 value.
        context.Print(value);
    }

    // Method from IPrintValue<Color> used to print Color values.
    void IPrintValue<Color>.PrintValue(in PrintContext context, Color value)
    {
        const string format = "F3";
        var formatProvider = CultureInfo.InvariantCulture.NumberFormat;

        // Format and print the Color value in RGBA format.
        context.Print(typeof(Color), $"RGBA({value.r.ToString(format, formatProvider)}, {value.g.ToString(format, formatProvider)}, {value.b.ToString(format, formatProvider)}, {value.a.ToString(format, formatProvider)})");
    }
}
```

将上述完整代码放入 `LowLevelVisitor.cs` 文件后，使用 `Data` 类实例调用 `DebugUtilities.PrintObjectDump` 方法，确认它产生的 Console 输出与[[05-使用PropertyVisitor类创建Property Visitor]]示例最后阶段的输出相同：

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

## 其他资源

- [[03-Property Visitor]]
- [[02-Property Bag]]
- [[04-Property Path]]
- [[05-使用PropertyVisitor类创建Property Visitor]]


---

## 文档导航

- 上一页：[[05-使用PropertyVisitor类创建Property Visitor]]
- 目录：[[00-使用Unity Properties处理类型数据]]
- 下一页：[[../09-使用数学编程/00-使用数学编程]]
