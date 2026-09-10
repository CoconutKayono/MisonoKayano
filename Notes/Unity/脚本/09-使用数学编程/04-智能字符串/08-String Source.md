# String Source

> 原文：[String Source](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/string-source.html)

使用内置字符串操作在 Smart String 中转换字符串值。

String Source 处理 `string` 值，并将常用字符串操作公开为 Selector，因此可以直接在格式字符串中转换文本。例如，`{name.ToUpper}` 会以大写形式输出 `name` 的值。

| Selector | 描述 |
| --- | --- |
| `Length` | 字符串中的字符数量。 |
| `ToUpper`、`ToLower` | 使用当前 Culture 转换为大写或小写。 |
| `ToUpperInvariant`、`ToLowerInvariant` | 使用 invariant Culture 转换为大写或小写。 |
| `Trim`、`TrimStart`、`TrimEnd` | 移除首尾空白。 |
| `Capitalize` | 将第一个字符转换为大写。 |
| `CapitalizeWords` | 将每个单词的首字母转换为大写。 |
| `ToCharArray` | 将字符串转换为字符数组。 |
| `ToBase64`、`FromBase64` | 编码为 UTF-8 Base64 字符串，或从 UTF-8 Base64 字符串解码。 |

以下示例展示了 String Source 的一些常用字符串操作：

```csharp
Smart.Format("{0.ToUpper}", "hello");                // "HELLO"
Smart.Format("{0.Capitalize}", "hello");             // "Hello"
Smart.Format("{0.CapitalizeWords}", "hello world");  // "Hello World"
Smart.Format("Length: {0.Length}", "hello");         // "Length: 5"
```

- 除非在设置中启用区分大小写的匹配，否则 Selector 匹配不区分大小写。有关不同设置以及启用方式的信息，请参阅[[03-Smart Strings设置参考]]。
- 在 Source 上启用 **Use Invariant Culture**，即可始终使用 invariant Culture；否则大小写转换使用当前 Culture。

## 其他资源

- [[06-Properties Source]]
- [[00-智能字符串]]

---

## 文档导航

- 上一页：[[07-Dictionary Source]]
- 目录：[[00-智能字符串]]
- 下一页：[[09-Choose Formatter]]
