# 创建自定义 Formatter

> 原文：[Create a custom formatter](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/create-a-custom-formatter.html)

编写自己的 Formatter，在 Smart String 中将值转换为文本。

要编写自定义 Formatter，请创建继承 `FormatterBase` 的类（命名空间为 `Unity.SmartStrings.Core.Extensions`）。重写 `DefaultName` 属性，设置应用该 Formatter 时使用的名称；重写 `TryEvaluateFormat(IFormattingInfo)` 方法，实现自定义格式化逻辑。最后使用 `Smart.Default.AddExtensions(...)` 注册 Formatter，使 Smart Strings 可以使用它。

## 编写 Formatter

在自定义 Formatter 中继承 `FormatterBase`，重写 `TryEvaluateFormat`，并检查 `IFormattingInfo.CurrentValue`，判断该 Formatter 是否可以处理当前值。如果可以处理，使用 `IFormattingInfo.Write(...)` 写入输出并返回 `true`；如果不能处理，返回 `false`，这样就会尝试下一个 Formatter。

`CanAutoDetect` 默认值为 `false`，因此自定义 Formatter 只有在按名称应用时才会运行。可以重写此属性并将其设为 `true`，使 Formatter 在未提供名称时也能隐式运行。启用后，对于无法处理的值，`TryEvaluateFormat` 必须返回 `false`，以便后续 Formatter 获得处理机会。

如果自定义 Formatter 在使用前需要初始化（例如需要读取大小写敏感设置），可以实现 `IInitializer` 及其 `Initialize(SmartFormatter)` 方法。该方法会在 Formatter 注册时运行，并在设置 Asset 反序列化后再次运行。

下面的 `ByteFormatter` 示例将字节数转换为易读的大小。它处理 `long` 值，对其他类型返回 `false`，因此只有值为 `long` 时才会应用。

```csharp
public class ByteFormatter : FormatterBase
{
    public override string DefaultName => "byte";
    public override bool TryEvaluateFormat(IFormattingInfo formattingInfo)
    {
        if (formattingInfo.CurrentValue is long bytes)
        {
            // We are performing a Base 2 conversion here. 1024 bytes = 1 KB
            if (bytes < 512)
            {
                formattingInfo.Write($"{bytes} B");
                return true;
            }
            if (bytes < 512 * 1024)
            {
                var kb = bytes / 1024.0f;
                formattingInfo.Write($"{kb.ToString(\"0.00\")} KB");
                return true;
            }

            bytes /= 1024;
            if (bytes < 512 * 1024)
            {
                var mb = bytes / 1024.0f;
                formattingInfo.Write($"{mb.ToString(\"0.00\")} MB");
                return true;
            }
            bytes /= 1024;
            var gb = bytes / 1024.0f;
            formattingInfo.Write($"{gb.ToString(\"0.00\")} GB");
            return true;
        }

        return false;
    }
}
```

## 注册 Formatter

使用 `Smart.Default.AddExtensions(...)` 注册 Formatter，然后按名称应用：

```csharp
Smart.Default.AddExtensions(new ByteFormatter());

Smart.Format("The file size is {0:byte}", 1234L);  // "The file size is 1.21 KB"
```

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `The file size is {0:byte}` | `100` | The file size is 100 B |
| `The file size is {0:byte}` | `1000` | The file size is 0.98 KB |
| `The file size is {0:byte}` | `1234` | The file size is 1.21 KB |
| `The file size is {0:byte}` | `10000000` | The file size is 9.54 MB |
| `The file size is {0:byte}` | `2000000000` | The file size is 1.86 GB |

也可以不编写代码，直接将自定义 Formatter 添加到项目的默认 Formatter：在[[03-Smart Strings设置参考]]的 Formatters 列表中选择 **Add (+)**，然后从菜单中选择 Formatter。菜单会按名称列出所有可用的 Formatter 类型。要让 Formatter 能够通过设置添加并保存，请将类标记为 `[Serializable]`，并提供公共无参数构造函数。

## 提取字面量文本

如果 Formatter 像 Choose、Conditional 和 Null Formatter 一样在字面量文本分支之间进行选择，请实现 `IFormatterLiteralExtractor` 及其 `WriteAllLiterals(IFormattingInfo)` 方法。在该方法中写入 Formatter 可能输出的每一个字面量，而不仅是当前值匹配的分支。遍历 Smart String 字面量的工具会使用此方法，查找只存在于某些分支中的文本。

例如，工具可以对项目中的每个 Smart String 调用 `WriteAllLiterals`，收集这些字符串可能生成的所有不同字符，再生成只包含所需字形的 Font Atlas。如果没有实现它，扫描文本时未走到的分支就不会被提取，其字形可能缺失，导致运行时无法正确渲染。

## 其他资源

- [[09-Choose Formatter]]
- [Template Formatter](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/template-formatter.html)
- [[00-智能字符串]]

---

## 文档导航

- 上一页：[[13-Sub String Formatter]]
- 目录：[[00-智能字符串]]
- 下一页：[[../../10-编译和代码重载/00-编译和代码重载]]
