# Property Path

> 原文：[Property paths](https://docs.unity3d.com/6000.7/Documentation/Manual/property-paths.html)

Property Path 是描述容器对象中某个属性位置的字符串。

可以使用 Property Path 获取或设置对象在特定路径上的数据，或让对象的子属性接受 Visitor。

Property Path 由字符串构成，并从根对象解析出特定的属性实例。例如，路径 `foo.bar.baz[12]` 会解析出 `baz` 列表容器中的第 13 个元素。该列表嵌套在 `bar` 容器中，而 `bar` 又嵌套在 `foo` 容器中。

要创建和操作 Property Path，请使用 [`Unity.Properties.PropertyPath`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyPath.html) 类。

可以使用 Property Path 执行以下操作：

- 获取或设置对象在特定路径上的数据。
- 让对象的子属性接受 Visitor。

有关如何使用 Property Path 让对象的子属性接受 Visitor 的示例，请参阅[[05-使用PropertyVisitor类创建Property Visitor]]示例中的“访问子属性”部分。

## 性能注意事项

[`Unity.Properties.PropertyPath`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyPath.html) 是一种不可变的结构体类型。从字符串构造 Property Path 时，需要为提取子字符串分配内存。

下表列出了从字符串构造 Property Path 时的分配行为：

| 字符串 | 长度 | 分配行为 |
| --- | ---: | --- |
| `"Path"` | 1 | 不分配：整个路径是单个片段，直接引用原始字符串。 |
| `"Path.To"` | 2 | 两次分配：按 `.` 分隔符拆分后，为 `"Path"` 和 `"To"` 分配两个新的子字符串实例。 |
| `"Path.To[2]"` | 3 | 三次分配：为 `"Path"` 和 `"To"` 分配子字符串，并对索引 `"[2]"` 进行解析和提取。 |
| `"Path.To[2].My"` | 4 | 四次分配：为 `"Path"`、`"To"` 和 `"My"` 分配子字符串，并对索引 `"[2]"` 进行解析和提取。 |
| `"Path.To[2].My.Value"` | 5 | 六次分配：为 `"Path"`、`"To"`、`"My"` 和 `"Value"` 分配子字符串，对索引 `"[2]"` 进行解析和提取，并分配数组来保存展开后的片段。 |

Property Path 是由 [`PropertyPathPart`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.PropertyPathPart.html) 类型的片段组成的数组。在为额外片段分配数组之前，会将四个片段直接内联。下表列出了从片段构造 Property Path 时的分配行为：

| 构造方式 | 长度 | 分配行为 |
| --- | ---: | --- |
| `PropertyPath.FromName("Path")` | 1 | 不分配：使用第一个内联的 `PropertyPathPart`。 |
| `PropertyPath.AppendName(previous, "To")` | 2 | 不分配：使用第二个内联的 `PropertyPathPart`。 |
| `PropertyPath.AppendIndex(previous, 2)` | 3 | 不分配：使用第三个内联的 `PropertyPathPart`。 |
| `PropertyPath.AppendName(previous, "My")` | 4 | 不分配：使用第四个内联的 `PropertyPathPart`。 |
| `PropertyPath.AppendName(previous, "Value")` | 5 | 分配一次：分配一个新数组以保存额外的 Property Path 片段。 |

为了优化性能并避免内存分配：

- 在初始化例程中初始化并缓存 Property Path。
- 最多处理四个片段时，应组合或追加 Property Path 片段，而不是从字符串构造 Property Path。

## 其他资源

- [[02-Property Bag]]
- [[03-Property Visitor]]
- [[05-使用PropertyVisitor类创建Property Visitor]]
- [[06-使用低级API创建Property Visitor]]


---

## 文档导航

- 上一页：[[03-Property Visitor]]
- 目录：[[00-使用Unity Properties处理类型数据]]
- 下一页：[[05-使用PropertyVisitor类创建Property Visitor]]
