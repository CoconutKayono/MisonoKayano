# 配置 Smart Strings

> 原文：[Configure Smart Strings](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/configure-smart-strings.html)

设置项目范围的默认 Formatter，并在代码中自定义 Smart Strings 的格式化方式。

Smart String 由 [`SmartFormatter`](xref:Unity.SmartStrings.SmartFormatter) 进行格式化。它包含按顺序排列的 Source 和 Formatter 列表。可以在设置 Asset 中为整个项目配置一次 Formatter，也可以在代码中创建自定义 Formatter 并直接调用。

## 设置项目范围的默认 Formatter

创建 Smart Strings 设置 Asset，为项目定义默认 Formatter，并将其包含在 Player 构建中：

1. 打开 **Project Settings** > **Smart Strings**。
2. 选择 **Create**，并选择 Asset 的保存位置。
3. 在 Asset 上编辑 **Smart Formatter** 字段，添加、删除或重新排列 Source 和 Formatter。

该 Asset 是一个 [`SmartStringsSettings`](xref:Unity.SmartStrings.SmartStringsSettings) [`ScriptableObject`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html)。它的 `SmartFormatter` 属性通过 [`Smart.CreateDefaultSmartFormat()`](xref:Unity.SmartStrings.Smart.CreateDefaultSmartFormat) 初始化。活动 Asset 会作为 `EditorBuildSettings` 配置对象存储，并在构建时添加到 Player 的预加载 Asset 中，因此它会随 Player 一起发布，并在启动时自行注册。

有关 Asset 属性的详细信息，请参阅[[03-Smart Strings设置参考]]。

## 在代码中自定义 Formatter

[`Smart.Default`](xref:Unity.SmartStrings.Smart.Default) 是静态 [`Smart.Format`](xref:Unity.SmartStrings.Smart.Format) 方法使用的默认 `SmartFormatter`。它会在首次使用时通过 `Smart.CreateDefaultSmartFormat()` 创建，并注册所有核心 Source 和 Formatter。

`Smart.Default` 标记为 `[ThreadStatic]`，因此每个线程都有自己的实例。必须在每个使用它的线程上配置它。

要从已注册核心扩展的新 Formatter 开始，请调用 `Smart.CreateDefaultSmartFormat()`：

```csharp
var formatter = Smart.CreateDefaultSmartFormat();
```

### 添加、删除和重新排列扩展

Source 和 Formatter 会按列表顺序尝试，因此顺序会改变哪个扩展处理 Placeholder。可以使用以下方法配置 `SmartFormatter` 中的列表：

| 方法 | 描述 |
| --- | --- |
| `AddExtensions(params ISource[])` | 添加 Source 扩展。已知的 Source 会插入其推荐位置；其他 Source 会添加到末尾。已经存在的类型会被跳过。 |
| `AddExtensions(params IFormatter[])` | 添加 Formatter 扩展，插入和去重规则相同。 |
| `InsertExtension(int, ISource)` / `InsertExtension(int, IFormatter)` | 将单个扩展插入列表中的指定位置。 |
| `RemoveSourceExtension<T>()` / `RemoveFormatterExtension<T>()` | 删除类型为 `T` 的扩展。如果找到并删除扩展，则返回 `true`。 |
| `GetSourceExtension<T>()` / `GetFormatterExtension<T>()` | 返回类型为 `T` 的扩展；如果尚未注册，则返回 `null`。 |

有关 API 参考，请参阅 [`Smart.Format`](xref:Unity.SmartStrings.Smart.Format)。同时实现 [`ISource`](xref:Unity.SmartStrings.Core.Extensions.ISource) 和 [`IFormatter`](xref:Unity.SmartStrings.Core.Extensions.IFormatter) 的扩展会自动注册到两个列表中。`AddExtensions` 和 `InsertExtension` 方法返回同一个 `SmartFormatter`，因此可以链式调用。

```csharp
// Remove a source and a formatter.
formatter.RemoveSourceExtension<DictionarySource>();
formatter.RemoveFormatterExtension<PluralLocalizationFormatter>();

// Add a custom source at the front so it's tried first.
formatter.InsertExtension(0, new MySource());

// Look up an existing extension.
var properties = formatter.GetSourceExtension<PropertiesSource>();
```

## 格式化 Smart String

调用静态 `Smart.Format`，使用 `Smart.Default` 进行格式化。传入 [`IFormatProvider`](https://learn.microsoft.com/en-us/dotnet/api/system.iformatprovider)（例如 [`CultureInfo`](https://learn.microsoft.com/en-us/dotnet/api/system.globalization.cultureinfo)）可以控制依赖区域性的格式化：

```csharp
// "Total: 1,234.5"
Smart.Format("Total: {0}", 1234.5);

// Format with a specific culture.
Smart.Format(CultureInfo.GetCultureInfo("de-DE"), "Total: {0}", 1234.5);
```

[`SmartExtensions`](xref:Unity.SmartStrings.SmartExtensions) 类添加了与 `Smart.Format` 使用相同语义的便捷方法：

| 方法 | 描述 |
| --- | --- |
| `string.FormatSmart(params object[])` | 将字符串作为模板格式化，并返回结果。 |
| `StringBuilder.AppendSmart(string, params object[])` | 将格式化结果追加到 `StringBuilder`。 |
| `StringBuilder.AppendLineSmart(string, params object[])` | 将格式化结果及行终止符追加到 `StringBuilder`。 |
| `TextWriter.WriteSmart(string, params object[])` | 将格式化结果写入 `TextWriter`。 |
| `TextWriter.WriteLineSmart(string, params object[])` | 将格式化结果及行终止符写入 `TextWriter`。 |

```csharp
var result = "Hello {Name}.".FormatSmart(new Character { Name = "Lara" });

var sb = new StringBuilder();
sb.AppendSmart("Score: {0}", 42);
```

如果不想分配中间字符串，而是要直接写入 `StringBuilder` 或 `TextWriter`，请调用 [`SmartFormatter.FormatInto(IOutput, ...)`](xref:Unity.SmartStrings.SmartFormatter.FormatInto)。上面的便捷方法会自动为目标对象封装一个 [`IOutput`](xref:Unity.SmartStrings.Core.Output.IOutput)。

## 其他资源

- [[00-智能字符串]]
- [[03-Smart Strings设置参考]]
- [[14-创建自定义Formatter]]


---

## 文档导航

- 上一页：[[01-生成动态文本]]
- 目录：[[00-智能字符串]]
- 下一页：[[03-Smart Strings设置参考]]
