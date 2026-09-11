# Dictionary Source

> 原文：[Dictionary Source](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/dictionary-source.html)

通过将 Placeholder Selector 与字典的键匹配，从字典中提取值。

Dictionary Source 可以解析 `IDictionary`、泛型 `IDictionary<string, object>` 或动态 `ExpandoObject` 中的 Selector，并返回键与 Selector 匹配的值。如果字典键不是字符串，Source 会先使用 `ToString` 将其转换为字符串，再进行比较。

键比较使用 Formatter 的大小写敏感设置。

可以嵌套字典并使用点号表示法深入访问，例如 `{Numbers.One}`。使用 nullable 操作符（`{City?.Name}`）可以在键缺失或值为 `null` 时返回空结果，而不是产生错误。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `{SomeKey}` | `{ ["SomeKey"] = 999 }` | 999 |
| `Hello {Name} {Surname}` | `{ ["Name"] = "Gordon", ["Surname"] = "Freeman" }` | Hello Gordon Freeman |
| `{Numbers.One} {Letters.A}` | 嵌套字典 | 1 a |

```csharp
var args = new Dictionary<string, object>
{
    ["Name"] = "Gordon",
    ["Surname"] = "Freeman",
};

// "Hello Gordon Freeman"
Smart.Format("Hello {Name} {Surname}", args);
```

## 其他资源

- [[06-Properties Source]]
- [[05-Default Source]]
- [[00-智能字符串]]

---

## 文档导航

- 上一页：[[06-Properties Source]]
- 目录：[[00-智能字符串]]
- 下一页：[[08-String Source]]
