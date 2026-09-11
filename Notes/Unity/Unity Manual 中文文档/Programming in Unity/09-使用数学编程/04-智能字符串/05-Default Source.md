# Default Source

> 原文：[Default Source](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/default-source.html)

根据数字索引选择参数，方式与 `String.Format` 相同。

Default Source 按索引提取参数，行为类似于 `String.Format`。它检查当前 Selector：如果 Selector 能解析为整数，并且该整数是传递给 `Smart.Format` 的参数的有效索引，就返回该索引处的参数。对于该 Placeholder，不会继续处理其他 Selector。

只有当索引是 Placeholder 中的第一个 Selector 且没有操作符时，Selector 才会解析为索引，这与 `String.Format` 处理 `{0}` 的方式一致。如果 Selector 无法解析为整数，或索引超出所提供的参数数量，Default Source 不会处理它，Formatter 会尝试下一个 Source。

例如，在 `{0.Name}` 中，Default Source 将 `0` 解析为第一个参数；然后由另一个 Source（例如[[06-Properties Source]]）针对该值解析 `Name`。

如果没有给出索引，例如 `{Name}`，其他 Source 会使用索引 `0` 处的参数。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `{0} {1} {2}` | `1, 2, 3` | 1 2 3 |
| `{1} {1} {2} {0}` | `1, 2, 3` | 2 2 3 1 |
| `Player {0} scored {1} points` | `"Potato"`, `155` | Player Potato scored 155 points |
| `Player {0.Name} scored {0.Points} points` | `new { Name = "One", Points = 100 }` | Player One scored 100 points |

```csharp
Smart.Format("{0} {1} {2}", 1, 2, 3);                          // "1 2 3"
Smart.Format("Player {0} scored {1} points", "Potato", 155);   // "Player Potato scored 155 points"
```

## 其他资源

- [[06-Properties Source]]
- [[07-Dictionary Source]]
- [[00-智能字符串]]

---

## 文档导航

- 上一页：[[04-处理格式化错误]]
- 目录：[[00-智能字符串]]
- 下一页：[[06-Properties Source]]
