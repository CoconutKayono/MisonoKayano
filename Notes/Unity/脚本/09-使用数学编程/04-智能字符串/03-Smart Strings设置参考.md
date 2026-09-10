# Smart Strings 设置参考

> 原文：[Smart Strings settings reference](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/smart-strings-settings.html)

自定义控制项目默认 Smart String Formatter 的设置，包括大小写敏感性、错误处理，以及当前启用的 Source 和 Formatter。

可以从主菜单（**Edit > Project Settings > Smart Strings**）打开这些设置，也可以在 **Project** 窗口中选择 Smart Strings Settings Asset。第一次打开该页面时，选择 **Create** 创建设置 Asset。这些设置定义默认的 [`SmartFormatter`](xref:Unity.SmartStrings.SmartFormatter)，运行时通过 [`Smart.Project`](xref:Unity.SmartStrings.Smart.Project) 获取；该 Asset 会包含在 Player 构建中。若要改为在代码中设置这些值，请参阅[[02-配置Smart Strings]]。

## Smart Strings 设置

Smart Strings 设置包含以下部分。

### 设置

| 设置 | 描述 |
| --- | --- |
| **Case Sensitivity** | 确定如何匹配 Selector 和 Formatter 名称。可选：**Case Sensitive**：精确匹配名称，这是默认值；**Case Insensitive**：匹配名称时忽略大小写。 |

#### Parser

| 设置 | 描述 |
| --- | --- |
| **Error Action** | 设置 Parser 对无效 Format 字符串的响应方式。可选：**Throw Error**：抛出异常，这是默认值；**Output Error In Result**：将错误消息写入输出；**Ignore**：跳过错误；**Maintain Tokens**：在输出中保持产生错误的 Placeholder 不变。详见[[04-处理格式化错误]]。 |
| **Convert Character String Literals** | 解析 Format 字符串中的字符转义，例如 `\n` 和 `\t`。默认启用。转义说明请参阅[[00-智能字符串]]。 |
| **Custom Selector Chars** | 列出除字母、数字、`_` 和 `-` 之外，允许出现在 Selector 中的额外字符。使用 **Add**（**+**）和 **Remove**（**−**）编辑列表。 |
| **Custom Operator Chars** | 列出除 `.` 和 `?.` 之外，被视为 Selector 运算符的额外字符。使用 **Add**（**+**）和 **Remove**（**−**）编辑列表。 |

#### Formatter

| 设置 | 描述 |
| --- | --- |
| **Error Action** | 设置 Formatter 无法格式化某个值时的响应方式。选项与 Parser 的 **Error Action** 相同，默认值为 **Throw Error**。详见[[04-处理格式化错误]]。 |
| **Alignment Fill Character** | 设置将值填充到对齐宽度时使用的字符，例如 `{value,10}`。默认使用空格。 |

### Sources

**Sources** 列表保存 Formatter 用于按顺序计算 Placeholder Selector 的 [Source](00-智能字符串.md#selector-和-source)。顺序很重要：系统从列表顶部开始尝试每个 Source，直到某个 Source 处理该 Selector。

- 选择 **Add**（**+**），从可用的 [`ISource`](xref:Unity.SmartStrings.Core.Extensions.ISource) 实现菜单中选择 Source 类型。
- 选择 **Remove**（**−**），删除选中的 Source。
- 拖动 Source 的操作柄，重新排列其顺序。

有关 Source，请参阅 [[05-Default Source]]、[[06-Properties Source]]、[[07-Dictionary Source]] 和 [[08-String Source]]。

### Formatters

**Formatters** 列表保存 Formatter 用于按顺序将值转换为文本的 Formatter。与 Source 一样，顺序会影响隐式应用的 Formatter。

- 选择 **Add**（**+**），从可用的 [`IFormatter`](xref:Unity.SmartStrings.Core.Extensions.IFormatter) 实现菜单中选择 Formatter 类型。
- 选择 **Remove**（**−**），删除选中的 Formatter。
- 拖动 Formatter 的操作柄，重新排列其顺序。

有关 Formatter，请参阅 [[09-Choose Formatter]]、[[11-Plural Formatter]]、[[12-List Formatter]] 和 [[10-Conditional Formatter]]。

## 其他资源

- [[02-配置Smart Strings]]
- [[04-处理格式化错误]]
- [[00-智能字符串]]


---

## 文档导航

- 上一页：[[02-配置Smart Strings]]
- 目录：[[00-智能字符串]]
- 下一页：[[04-处理格式化错误]]
