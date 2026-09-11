# Sub String Formatter

> 原文：[Sub String Formatter](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/substring-formatter.html)

在 Smart String 中输出字符串的一部分。

Sub String Formatter 根据起始索引和可选长度返回字符串值的一部分。如果值不是字符串，会先使用 `ToString` 转换为字符串。使用名称 `substr` 显式应用。

```text
{value:substr(start,length)}
```

![Sub String Formatter 语法结构](smart-strings-substring-formatter.svg)

`substr` Formatter 的第一个参数是起始索引，第二个可选参数是长度。负起始索引从字符串末尾反向计算，负长度也从末尾反向计算。

起始索引和长度使用分隔字符分开。有效分隔字符为 `,`（默认值）、`|` 和 `~`，可以通过 `SubStringFormatter.SplitChar` 配置。

当遇到 `null` 值时，Formatter 会写入 **Null Display String**，默认值为 `(null)`。可以通过 `SubStringFormatter.NullDisplayString` 配置。如果提供嵌套格式，嵌套格式会接收 `null`，并负责处理它。

提供的格式必须包含嵌套 Placeholder，否则 Formatter 会抛出 `FormattingException`。

`SubStringFormatter.OutOfRangeBehavior` 控制起始索引或长度超过字符串末尾时的行为：

- `ReturnEmptyString` 返回空字符串，这是默认值。
- `ReturnStartIndexToEndOfString` 返回从起始索引到字符串末尾的剩余内容。
- `ThrowException` 抛出 `FormattingException`。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `{0:substr(5)}` | `"Long John"` | John |
| `{0:substr(0,3)}` | `"New York"` | New |
| `{0:substr(-4)}` | `"Long John"` | John |
| `{0:substr(-4,2)}` | `"Long John"` | Jo |
| `{0:substr(-4,-1)}` | `"Long John"` | Joh |
| `Hello {name:substr(1)} {surname}` | `name = "Lara"`、`surname = "Croft"` | Hello ara Croft |

可以将结果传递给嵌套 Placeholder，继续进行格式化：

```csharp
Smart.Format("{0:substr(0,2):{ToLower}}", "ABC");  // "ab"
```

## 其他资源

- [[08-String Source]]
- [Template Formatter](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/template-formatter.html)
- [[00-智能字符串]]

---

## 文档导航

- 上一页：[[12-List Formatter]]
- 目录：[[00-智能字符串]]
- 下一页：[[14-创建自定义Formatter]]
