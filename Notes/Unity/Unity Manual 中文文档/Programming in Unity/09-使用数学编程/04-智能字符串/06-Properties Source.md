# Properties Source

> 原文：[Properties Source](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/properties-source.html)

通过 Unity.Properties 数据模型按名称从当前值读取成员。

Properties Source 使用 `Unity.Properties` 对当前对象求值命名 Selector。`Unity.Properties` 与 UI Toolkit 数据绑定使用相同的数据模型。Properties Source 将 Selector 与 Unity.Properties 暴露的成员匹配，并返回该成员的值。它适用于普通类和结构体，也适用于 `MonoBehaviour` 字段，不需要预先注册 Property Bag。

Properties Source 是按名称读取成员的默认方式，它只能解析 Unity.Properties 暴露的成员。如果 Selector 与已暴露的成员不匹配，Source 不返回结果，Formatter 中后续的 Source 会继续处理该 Selector。

匹配时，`string` 值由[[08-String Source]]处理，因此 Properties Source 会忽略它们。成员匹配区分大小写；当 Formatter 使用不区分大小写的匹配时，大小写不同的 Selector 仍无法通过此 Source 解析。

对当前值为 `null` 的情况，可以使用 nullable 操作符返回空结果而不是错误，例如 `{Address?.City}`。

| Smart String | 参数 | 结果 |
| --- | --- | --- |
| `{Name} reached level {Level}.` | `new PlayerData { Name = "Juan Pérez", Level = 12 }` | Juan Pérez reached level 12. |

```csharp
var player = new PlayerData { Name = "Juan Pérez", Level = 12 };

// "Juan Pérez reached level 12."
Smart.Format("{Name} reached level {Level}.", player);
class Enemy
{
    // A public field is visible with no attribute.
    public string Name = "Goblin";

    // A private field is visible when you mark it with [SerializeField].
    [SerializeField]
    int m_Health = 30;
    // A plain, non-attributed property is not visible.
    public int Score => 100;
}
var enemy = new Enemy();

// "Goblin has 30 health." m_Health resolves through [SerializeField].
Smart.Format("{Name} has {m_Health} health.", enemy);
```

## 标记成员，使 Properties Source 可以读取它们

Properties Source 暴露的成员遵循 Unity 的序列化规则：

- 公共字段。
- 使用 `[SerializeField]` 标记的私有或内部字段。
- 使用 `[CreateProperty]` 或 `[SerializeReference]` 标记的成员。

这包括带有这些特性的非公共成员。方法和普通的、未添加特性的属性不会被暴露，也无法通过此 Source 解析。若要读取这些成员，请编写自定义 Source。

```csharp
class Enemy
{
    // A public field is visible with no attribute.
    public string Name = "Goblin";

    // A private field is visible when you mark it with [SerializeField].
    [SerializeField]
    int m_Health = 30;

    // A plain, non-attributed property is not visible.
    public int Score => 100;
}
var enemy = new Enemy();

// "Goblin has 30 health." m_Health resolves through [SerializeField].
Smart.Format("{Name} has {m_Health} health.", enemy);
```

## 生成 Property Bag，避免反射

默认情况下，Unity.Properties 首次读取某个类型时，会通过反射为该类型创建 Property Bag。要避免反射，可以使用 `[GeneratePropertyBag]` 标记类型，并使用 `[assembly: GeneratePropertyBagsForAssembly]` 将程序集加入范围。此时 Source Generator 会在编译时生成 Property Bag。这可以提高性能；对于完全 AOT 编译的 Player 尤其重要，因为其中的反射回退能力有限。

```csharp
[GeneratePropertyBag]
public partial class Character
{
    public string Name;
}
```

## 其他资源

- [创建自定义 Source](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/create-a-custom-source.html)
- [[08-String Source]]
- [[00-智能字符串]]

---

## 文档导航

- 上一页：[[05-Default Source]]
- 目录：[[00-智能字符串]]
- 下一页：[[07-Dictionary Source]]
