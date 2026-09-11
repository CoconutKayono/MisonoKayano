# Conditional Formatter

> 原文：[Conditional Formatter](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/conditional-formatter.html)

根据 Placeholder 的类型和值从多个输出中选择一个。

Conditional Formatter 将格式拆分为多个 Choices，并根据 Placeholder 的值选出其中一个。可以使用名称 `cond` 显式应用；如果格式包含分隔字符，也可以省略名称隐式应用。它会根据值的类型使用不同规则处理数字、布尔值、字符串、日期和时间跨度。

使用分隔字符分开 Choices。默认分隔字符为 `|`，`,` 和 `~` 也有效。每个 Choice 本身都是一个格式，因此可以包含嵌套 Placeholder。空 Placeholder `{}` 会重新使用当前值。

## 数字

对于数字，值会选择对应索引处的 Choice。非整数会向下取整；负数或超出最后一个 Choice 的值会选择最后一个 Choice。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `{0:cond:Apple&#124;Pie&#124;Orange&#124;Banana&#124;No fruit}` | `0` | Apple |
| `{0:cond:Apple&#124;Pie&#124;Orange&#124;Banana&#124;No fruit}` | `3` | Banana |
| `{0:cond:Apple&#124;Pie&#124;Orange&#124;Banana&#124;No fruit}` | `-1` | No fruit |
| `{0:cond:zero&#124;one&#124;two&#124;three&#124;other}` | `4` | other |

### 复杂比较

使用 `?` 分隔比较条件和对应 Choice。最后一个没有比较条件的 Choice 会在没有任何条件匹配时作为回退。复杂比较语法只适用于可转换为数字的值。

| 操作符 | 描述 |
| --- | --- |
| `>=` | 大于或等于 |
| `>` | 大于 |
| `=` | 等于 |
| `<` | 小于 |
| `<=` | 小于或等于 |
| `!=` | 不等于 |

使用 `&` 组合 AND 条件，使用 `/` 组合 OR 条件。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `{0:cond:>10?Greater than 10&#124;=10?Equal to 10&#124;Less than 10}` | `5` | Less than 10 |
| `{0:cond:>=55?Senior&#124;>=30?Adult&#124;>=18?Young adult&#124;Child}` | `42` | Adult |

## 布尔值

对于布尔值，值为 `true` 时使用第一个 Choice，值为 `false` 时使用第二个 Choice。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `Enabled? {0:cond:Yes&#124;No}.` | `true` | Enabled? Yes. |
| `Enabled? {0:cond:Yes&#124;No}.` | `false` | Enabled? No. |

## 字符串

对于字符串，值不为 `null` 且不为空时使用第一个 Choice，否则使用第二个 Choice。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `The string is {0:cond:not empty&#124;empty}` | `"Some text"` | The string is not empty |
| `The string is {0:cond:not empty&#124;empty}` | `""` | The string is empty |
| `Text: {0:cond:{}&#124;No text}` | `"Hello World"` | Text: Hello World |
| `Text: {0:cond:{}&#124;No text}` | `""` | Text: No text |

## DateTime 和 DateTimeOffset

对于 `DateTime` 或 `DateTimeOffset`，会将值与当前 UTC 日期比较。使用三个 Choice 时，索引分别表示过去、今天和未来；使用两个 Choice 时，分别表示今天或过去、未来。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `My birthday {0:cond:was yesterday&#124;is today&#124;will be tomorrow}` | 过去的日期 | My birthday was yesterday |
| 同上 | 今天 | My birthday is today |
| 同上 | 将来的日期 | My birthday will be tomorrow |

## TimeSpan

对于 `TimeSpan`，会将值与 `TimeSpan.Zero` 比较。使用三个 Choice 时，索引分别表示负数、零和正数；使用两个 Choice 时，分别表示负数或零、正数。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `The event {0:cond:was {Hours} hours ago&#124;is now&#124;will start in {Hours} hours}` | 负持续时间 | The event was 2 hours ago |
| 同上 | `TimeSpan.Zero` | The event is now |
| 同上 | 正持续时间 | The event will start in 3 hours |

## 其他对象

对于其他类型，会将值与 `null` 比较：值不为 `null` 时使用第一个 Choice，为 `null` 时使用第二个 Choice。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `{0:cond:not null&#124;null}` | 对象 | not null |
| `{0:cond:not null&#124;null}` | `null` | null |

## 其他资源

- [[09-Choose Formatter]]
- [[11-Plural Formatter]]
- [[00-智能字符串]]

---

## 文档导航

- 上一页：[[09-Choose Formatter]]
- 目录：[[00-智能字符串]]
- 下一页：[[11-Plural Formatter]]
