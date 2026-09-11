# Link XML 格式参考

> 原文：[Link XML formatting reference](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-stripping-xml-formatting.html)

本参考介绍 `link.xml` 文件的正确格式，包括有效的 XML 元素、属性和用法示例。

> **注意**：Unity 的 `link.xml` 格式基于 .NET Linker 使用的 ILLink（Intermediate Language Linker）Descriptor 格式。有关该格式的权威参考，请参阅 [dotnet/runtime repository](https://github.com/dotnet/runtime/blob/main/docs/tools/illink/data-formats.md) 中的文档。

## 支持的 XML 元素

以下 XML 元素受 `link.xml` 文件支持：

| 元素 | 描述 |
| --- | --- |
| `<linker></linker>` | 所有 `link.xml` 文件都必须使用此元素作为包含其他所有元素的最外层元素。 |
| `<assembly></assembly>` | 声明特定于某个程序集的代码保留注释。 |
| `<type></type>` | 声明特定于某个类型的代码保留注释。 |
| `<field></field>` | 声明特定于某个字段的代码保留注释。 |
| `<method></method>` | 声明特定于某个方法的代码保留注释。 |
| `<property></property>` | 声明特定于某个属性的代码保留注释。 |
| `<event></event>` | 声明特定于某个事件的代码保留注释。 |

所有这些元素的用法示例，请参阅[[#usage-examples|用法示例]]。

## 支持的 XML 属性

| 属性 | 描述 |
| --- | --- |
| `accessors` | 应用于 `<property>` 元素，用于指定要保留该属性的哪些 accessor 方法。 |
| `feature` | 排除当前构建设置不支持的 feature 的保留内容。更多信息和用法示例请参阅[Feature 排除](#feature-exclusions)。 |
| `fullname` | 使用完全限定名标识代码元素。当单独使用 `name` 可能产生歧义时，使用 `fullname`。 |
| `ignoreIfMissing` | 应用于 `<assembly>` 元素，用于声明某个在所有 Player 构建期间并不存在的程序集的保留内容。用法示例请参阅[忽略缺失的程序集](#ignore-if-missing)。 |
| `ignoreIfUnreferenced` | 应用于 `<assembly>` 元素，仅当另一个程序集引用了该程序集的至少一个成员时，才保留其中的实体。用法示例请参阅[忽略未引用的程序集](#ignore-if-unreferenced)。 |
| `name` | 仅使用名称标识代码元素，不带父程序集作为前缀。如果已在父 XML 元素中使用 `fullname` 指定程序集名称，子 XML 元素可以只使用 `name` 标识代码元素。 |
| `preserve` | 指定要保留、防止被剥离的代码元素级别。有效值如下：<ul><li><code>all</code>：保留整个元素及其所有成员。</li><li><code>fields</code>：保留类型及其所有字段，但不保留方法。</li><li><code>methods</code>：保留类型及其所有方法，但不保留字段。</li><li><code>nothing</code>：保留类型的存在/元数据，但不保留其任何成员。</li></ul> |
| `signature` | 使用签名标识代码元素。方法签名由返回类型、名称和参数组成。字段、属性或事件签名由类型和名称组成。用法示例请参阅[用法示例](#usage-examples)。 |
| `windowsruntime` | 只要在 `link.xml` 文件中为 Windows Runtime Metadata（`.winmd`）程序集定义保留内容，就必须添加到 `<assembly>` 元素。用法示例请参阅[Windows Runtime Metadata 程序集](#windows-runtime)。 |

所有这些属性的用法示例，请参阅[[#usage-examples|用法示例]]。

<a id="usage-examples"></a>

## 用法示例

以下示例演示受支持 XML 元素和属性的有效用法。

<a id="different-root-declarations"></a>

### 声明程序集根类型的不同方式

以下示例说明如何使用 `link.xml` 文件，以不同方式声明项目程序集的根类型：

```xml
<linker>
  <!--Preserve types and members in an assembly-->
  <assembly fullname="AssemblyName">
    <!--Preserve an entire type-->
    <type fullname="Namespace.TypeName" preserve="all"/>

    <!--No "preserve" attribute and no members specified means preserve all members-->
    <type fullname="Namespace.TypeName"/>

    <!--Preserve all fields on a type-->
    <type fullname="Namespace.TypeName" preserve="fields"/>

    <!--Preserve all methods on a type-->
    <type fullname="Namespace.TypeName" preserve="methods"/>

    <!--Preserve the type only-->
    <type fullname="Namespace.TypeName" preserve="nothing"/>

    <!--Preserving only specific members of a type-->
    <type fullname="Namespace.TypeName">
        
      <!--Fields-->
      <field signature="System.Int32 FieldName" />

      <!--Preserve a field by name rather than signature-->
      <field name="FieldName" />
      
      <!--Methods-->
      <method signature="System.Void MethodName()" />

      <!--Preserve a method with parameters-->
      <method signature="System.Void MethodName(System.Int32,System.String)" />

      <!--Preserve a method by name rather than signature-->
      <method name="MethodName" />

      <!--Properties-->

      <!--Preserve a property, its backing field (if present), 
          getter, and setter methods-->
      <property signature="System.Int32 PropertyName" />

      <property signature="System.Int32 PropertyName" accessors="all" />

      <!--Preserve a property, its backing field (if present), and getter method-->
      <property signature="System.Int32 PropertyName" accessors="get" />

      <!--Preserve a property, its backing field (if present), and setter method-->
      <property signature="System.Int32 PropertyName" accessors="set" />

      <!--Preserve a property by name rather than signature-->
      <property name="PropertyName" />

      <!--Events-->

      <!--Preserve an event, its backing field (if present), add, and remove methods-->
      <event signature="System.EventHandler EventName" />

      <!--Preserve an event by name rather than signature-->
      <event name="EventName" />

    </type>
  </assembly>
</linker>
```

<a id="entire-assemblies"></a>

### 将完整程序集声明为根

以下示例展示如何声明完整程序集：

```xml
<!--Preserve an entire assembly-->
  <assembly fullname="AssemblyName" preserve="all"/>

  <!--No "preserve" attribute and no types specified means preserve all-->
  <assembly fullname="AssemblyName"/>

  <!--Fully qualified assembly name-->
  <assembly fullname="AssemblyName, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null">
    <type fullname="Namespace.Foo" preserve="all"/>
  </assembly>

  <!--Force an assembly to be processed for roots but don't explicitly preserve anything in particular. Useful when the assembly isn't referenced.-->
  <assembly fullname="AssemblyName" preserve="nothing"/>
```

<a id="nested-or-generic"></a>

### 保留嵌套类型或泛型类型

以下示例展示如何保留嵌套类型或泛型类型：

```xml
<!--Examples with generics-->
    <type fullname="Namespace.G`1">

      <!--Preserve a field with generics in the signature-->
      <field signature="System.Collections.Generic.List`1&lt;System.Int32&gt; FieldName" />

      <field signature="System.Collections.Generic.List`1&lt;T&gt; FieldName" />

      <!--Preserve a method with generics in the signature-->
      <method signature="System.Void MethodName(System.Collections.Generic.List`1&lt;System.Int32&gt;)" />

      <!--Preserve an event with generics in the signature-->
      <event signature="System.EventHandler`1&lt;System.EventArgs&gt; EventName" />

    </type>

    <!--Preserve a nested type-->
    <type fullname="Namespace.H/Nested" preserve="all"/>

    <!--Preserve all fields of a type if the type is used.  If the type isn't used, it will be removed-->
    <type fullname="Namespace.I" preserve="fields" required="0"/>

    <!--Preserve all methods of a type if the type is used. If the type isn't used, it will be removed-->
    <type fullname="Namespace.J" preserve="methods" required="0"/>

    <!--Preserve all types in a namespace-->
    <type fullname="Namespace.SomeNamespace*" preserve="all"/>

    <!--Preserve all types with a common prefix in their name-->
    <type fullname="Prefix*" preserve="all"/>
```

<a id="ignore-if-missing"></a>

### 忽略缺失的程序集

如果需要为某个在所有 Player 构建期间并不存在的程序集声明保留内容，请在 `<assembly>` 元素上使用 `ignoreIfMissing` 属性：

```xml
<linker>
  <assembly fullname="Foo" ignoreIfMissing="1">
    <type name="TypeName"/>
  </assembly>
</linker>
```

<a id="ignore-if-unreferenced"></a>

### 忽略未引用的程序集

在 `<assembly>` 元素上使用 `ignoreIfUnreferenced` 属性，仅当另一个程序集至少引用了一个类型时，才保留该程序集中的实体：

```xml
<linker>
  <assembly fullname="Bar" ignoreIfUnreferenced="1">
    <type name="TypeName"/>
  </assembly>
</linker>
```

<a id="windows-runtime"></a>

### Windows Runtime Metadata 程序集

只要在 `link.xml` 文件中为 Windows Runtime Metadata（`.winmd`）程序集定义保留内容，就必须在 `<assembly>` 元素上使用 `windowsruntime` 属性：

```xml
<linker>
  <assembly fullname="Windows" windowsruntime="true">
    <type name="TypeName"/>
 </assembly>
</linker>
```

<a id="feature-exclusions"></a>

### Feature 排除

嵌入 `mscorlib.dll` 的 `mscorlib.xml` 文件使用此属性，但在适当情况下，你也可以在任何 `link.xml` 文件中使用它。

在 **High** [[02-配置托管代码剥离|剥离级别]] 下，Unity Linker 会根据当前构建的设置，排除对不受支持 feature 的保留内容：

1. `remoting` — 以 IL2CPP scripting backend 为目标时排除。
2. `sre` — 以 IL2CPP scripting backend 为目标时排除。
3. `com` — 以不支持 COM 的平台为目标时排除。

例如，以下 `link.xml` 文件会在支持 COM 的平台上保留类型的一个方法，并在所有平台上保留另一个方法：

```xml
<linker>

    <assembly fullname="Foo">

        <type fullname="Type1">

            <!--Preserve FeatureOne on platforms that support COM-->

            <method signature="System.Void FeatureOne()" feature="com"/>

            <!--Preserve FeatureTwo on all platforms-->

            <method signature="System.Void FeatureTwo()"/>

        </type>

    </assembly>

</linker>
```

## 其他资源

- [[01-托管代码剥离和Unity Linker]]
- [[02-配置托管代码剥离]]
- [[04-使用注释保留代码]]
- [[06-Unity Linker标记规则参考]]
- [`IUnityLinkerProcessor.GenerateAdditionalLinkXmlFile`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Build.IUnityLinkerProcessor.GenerateAdditionalLinkXmlFile.html)

---

## 文档导航

- 上一页：[[04-使用注释保留代码]]
- 目录：[[00-托管代码剥离]]
- 下一页：[[06-Unity Linker标记规则参考]]
