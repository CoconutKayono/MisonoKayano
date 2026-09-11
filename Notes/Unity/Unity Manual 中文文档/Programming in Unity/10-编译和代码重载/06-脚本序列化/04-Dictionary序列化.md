# Dictionary 序列化

> 原文：[Dictionary serialization](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-dictionaries.html)

Unity 会直接序列化声明为 `Dictionary<TKey, TValue>` 的字段，因此可以在脚本中创建 Dictionary 数据，并在 **Inspector** 窗口中编辑，无需编写自定义序列化代码。声明的字段类型必须准确为 `Dictionary<TKey, TValue>`。

Dictionary serialization 是选择加入的功能：必须为每个希望 Unity 序列化的 Dictionary 字段应用 `[SerializeField]`。Unity 只支持[某些类型](#支持的键和值类型)作为 Dictionary 的键和值。序列化规则分析器会在编译时检测不支持的键和值类型，并指向解释限制的规则。Inspector 会渲染一个支持排序、重复键检测和列宽调整的两列键值编辑器。

Unity 按插入顺序将 Dictionary 序列化为一系列键值对。Inspector 中显示的顺序与序列化顺序相互独立。参阅[Inspector 中的排序顺序](#inspector-中的排序顺序)。

## 声明序列化的 Dictionary 字段

可以在 `MonoBehaviour`、`ScriptableObject` 或任意嵌套的 `[Serializable]` 类或结构体上序列化 Dictionary 字段。为 private 或 public Dictionary 字段应用 `[SerializeField]`，即可让 Unity 序列化该 Dictionary：

```csharp
using System.Collections.Generic;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    [SerializeField]
    private Dictionary<string, int> itemCounts = new Dictionary<string, int>();
}
```

Public Dictionary 字段不会自动序列化。没有 `[SerializeField]` 时，Unity 会跳过该字段，Dictionary 不会在 domain reload、Scene 保存或 Play mode 切换期间持久化。Dictionary 字段缺少 `[SerializeField]` 时，分析器会报告 [[07-序列化规则分析器参考#uac1015|UAC1015]]，这样你可以选择加入序列化，或使用 `[NonSerialized]` 标记该字段。

Dictionary 字段不能使用 `[SerializeReference]`，因为 Unity 将 Dictionary 序列化为内联的条目集合，而不是多态的单个引用。对 Dictionary 字段应用 `[SerializeReference]` 时，分析器会报告 [[07-序列化规则分析器参考#uac1014|UAC1014]]。

## 支持的键和值类型

`TKey` 和 `TValue` 都必须是 Unity 可以序列化的类型：

- 基本类型（`int`、`float`、`double`、`bool`、`string`）。
- Enum 类型（32 位或更小）。
- Unity 内置类型，例如 `Vector2`、`Vector3`、`Color`。
- 标记了 `[Serializable]` 的自定义类和结构体。
- 对继承自 `UnityEngine.Object` 的类型的引用。

不能将 interface 或 abstract 类型用作键或值（`UnityEngine.Object` 层次结构除外），也不能使用未标记 `[Serializable]` 的类型。分析器会分别报告 [[07-序列化规则分析器参考#uac1012|UAC1012]] 和 [[07-序列化规则分析器参考#uac1016|UAC1016]]。

集合可以作为值，但不能作为键：

- 作为**值**时，可以使用任意受支持的类型，或由受支持类型组成的集合，例如 `List<T>`、Array 或另一个 `Dictionary<TKey, TValue>`。例如 `Dictionary<int, List<int>>` 和 `Dictionary<int, Dictionary<string, int>>` 都有效。
- 作为**键**时，不能使用实现 `IEnumerable` 的类型——这是 `List<T>` 和 Array 等集合类型实现的接口。`string` 是例外。例如，Unity 不能序列化 `Dictionary<List<int>, int>` 字段，因为其键类型 `List<int>` 实现了 `IEnumerable`。分析器会报告 [[07-序列化规则分析器参考#uac1013|UAC1013]]。

Unity 也不会序列化直接嵌套在另一个集合中的 Dictionary。例如 `List<Dictionary<string, int>>` 和 `Dictionary<string, int>[]` 不受支持。请将 Dictionary 包装在可用作元素类型的 `[Serializable]` 类或结构体中。分析器会将此情况报告为 [[07-序列化规则分析器参考#uac1009|UAC1009]]。

包含 `[SerializeReference]` 字段的结构体和类——无论该字段直接存在，还是出现在字段图或继承链中的任意位置——都可以用作序列化 Dictionary 的键或值。

完整的分析器规则和用法示例请参阅[[07-序列化规则分析器参考]]。

### 自定义结构体和类键

如果使用自定义结构体或类作为 Dictionary 键，请重写 `GetHashCode` 和 `Equals`，让 Dictionary 能正确放置和查找条目：

- 没有重写方法的自定义类使用引用相等性。即使两个实例的字段值相同，也会被当作不同的键，从而破坏 Dictionary 查找。
- 没有重写方法的自定义结构体会回退到基于反射的哈希和相等性比较。Dictionary 仍然能正确工作，但速度较慢。添加重写可改善性能。
- 基本类型、`string`、Enum、`Vector3` 和 `Color` 等 Unity 内置类型，以及 `UnityEngine.Object` 子类，已经正确实现 `GetHashCode` 和 `Equals`，不需要重写。

对于值类型键，还应实现 `IEquatable<T>`，以避免键比较期间的 boxing allocation。`IEquatable<T>` 不是必需的，但可以改善运行时性能。

如果自定义的 `GetHashCode` 或 `Equals` 实现在 Unity 加载序列化 Dictionary 时抛出异常，Unity 会跳过受影响的条目，并向 Console 记录一条警告。

## 自定义键比较器

要控制序列化 Dictionary 比较和哈希键的方式，请在字段声明中将 `IEqualityComparer<TKey>` 接口的实现传给 Dictionary 构造函数：

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    [SerializeField]
    private Dictionary<string, int> itemCounts = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
}
```

Unity 不会将 comparer 写入 Scene、Prefab 或 Asset。只有在字段声明的构造函数中传入 comparer，加载后才会继续应用它。这是因为 Unity 会复用字段已有的 Dictionary，而不是创建新的 Dictionary：它会对该 Dictionary 调用 `Clear`，然后添加读取到的条目。`Clear` 不会重置 comparer。

字段包含哪个 Dictionary 取决于操作：

- 创建包含该 Dictionary 的对象时，会先执行字段声明，因此 Dictionary 使用声明的 comparer。这包括 domain reload、Scene load、Prefab load、Asset load，以及调用 `Object.Instantiate`。
- 反序列化到已经存在的对象时，会复用该时刻字段所包含的 Dictionary，不会再次执行字段声明。这包括 undo、redo、Prefab revert，以及调用 `SerializedObject.ApplyModifiedProperties`。除非脚本在 Unity 加载对象后替换 Dictionary 或将字段设为 `null`，否则声明的 comparer 仍然适用。如果字段为 `null`，Unity 会使用默认 comparer 创建新的 Dictionary，直到下次创建对象前不会再次应用声明的 comparer。

### 在字段声明中设置 comparer

序列化数据不包含 comparer，因此 Unity 无法恢复脚本只在运行时赋给 Dictionary 的 comparer。详情请参阅[Unity 无法保留的 comparer](#unity-无法保留的-comparer)。

例如，以下脚本在 Unity 下次创建对象（如 domain reload）时会丢失 comparer。`SetValues` 方法用带 comparer 的 Dictionary 替换字段，但字段声明没有设置 comparer，因此重载后的 Asset 会区分大小写地比较键：

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

public class ItemLookup : ScriptableObject
{
    [SerializeField]
    private Dictionary<string, int> values = new Dictionary<string, int>();

    public Dictionary<string, int> Values => values;

    // A caller supplies the comparer, for example:
    // lookup.SetValues(new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase));
    public void SetValues(Dictionary<string, int> newValues)
    {
        values = newValues;
    }
}
```

要保留 comparer，请在字段声明的构造函数中传入它：

```csharp
[SerializeField]
private Dictionary<string, int> values = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
```

使用此声明时，即使脚本在运行时替换了 Dictionary，下次 Unity 创建对象时该 Dictionary 仍会使用声明的 comparer。

在 Unity 再次创建对象之前，字段仍包含运行时赋给它的 Dictionary；例如 undo 这样的就地操作会使用该 Dictionary 的 comparer，而不是字段声明的 comparer。若要让两种情况下的行为一致，请让运行时赋给字段的任何 Dictionary 使用与字段声明相同的 comparer。

### 不要在 `Awake` 或 `OnEnable` 中替换 Dictionary

不要在 Unity 反序列化对象后调用的 MonoBehaviour 方法（例如 `Awake`、`OnEnable` 或 `Start`）中为字段赋予新的 Dictionary。新的 Dictionary 会丢弃 Unity 加载的条目。要设置 comparer，请在字段声明的构造函数中传入它，因为该构造函数在反序列化前运行。

### comparer 导致的重复键

一个 comparer 可能使两个不同的序列化键相等。例如，序列化数据中的 `Alpha` 和 `alpha` 是不同字符串，但 `StringComparer.OrdinalIgnoreCase` comparer 会将它们视为同一个键。

Unity 会将这报告为重复键：它将第一个条目添加到运行时 Dictionary，排除后面的条目，并在 Inspector 中标记每个被排除的行，以便你修正或删除。这与其他重复键的行为相同。详情请参阅[重复键](#重复键)。

### Unity 无法保留的 comparer

在以下情况下，Unity 无法恢复脚本设置在 Dictionary 上的 comparer：

- **运行时选择的 comparer**。字段声明在编译时固定，无法指定脚本运行时选择的 comparer，例如从加载值、项目设置或方法参数中选择的 comparer。Unity 无法从序列化数据中读回 comparer，因此不会恢复该选择。
- **Struct 中的 Dictionary**。C# 不允许在 Struct 字段上使用 field initializer，因此 Struct 声明无法创建 Dictionary 或设置 comparer。Unity 会在包含该 Struct 的对象内部就地读取序列化 Struct 的字段。
- **作为值使用的 Dictionary**。在 `Dictionary<string, Dictionary<string, int>>` 字段中，Unity 在读取条目时创建每个内部 Dictionary，因此内部 Dictionary 没有可以设置 comparer 的字段声明。外部 Dictionary 是字段，因此会保留为它设置的 comparer。

在这些情况下，Dictionary 使用字段声明中的 comparer；如果字段声明没有设置 comparer，则使用与 `EqualityComparer<TKey>.Default` 属性返回值行为相同的 comparer。

Dictionary 作为值时的限制只适用于值本身是 Dictionary 的情况。如果值是带有 Dictionary 字段的 `[Serializable]` 类，只要该类有无参数构造函数，该 Dictionary 就会保留其字段声明中的 comparer。Unity 使用该构造函数创建类，因此会执行类的字段声明。如果类只声明带参数的构造函数，Unity 会在不运行构造函数的情况下创建类，字段声明不会执行，Dictionary 会使用默认 comparer。

如果在这些情况之一需要自定义 comparer，请重构数据，使 Dictionary 成为其声明可以创建它的字段。例如，将 Dictionary 从 Struct 移到带无参数构造函数的 `[Serializable]` 类中，然后在该类的 Dictionary 字段声明中设置 comparer。

## 在 Inspector 中编辑 Dictionary

选择包含序列化 Dictionary 的 GameObject 或 Asset 时，Inspector 会将 Dictionary 渲染为两列列表，左侧是键，右侧是值。

![Inspector 将 Dictionary 字段显示为两列列表，左侧为键、右侧为值。](serialization-dictionary-inspector.png)

Inspector 提供以下功能：

- 使用列表底部的 **+** 和 **-** 按钮添加或删除条目。
- 更改列宽。宽度按 property path 和 Inspector 窗口持久化。
- 右键单击列标题更改布局。参阅[自定义 Dictionary 显示](#自定义-dictionary-显示)。
- 右键单击列标题并选择 **Reset Layout**，恢复默认布局、列分割和排序方向。
- 单击 **Key** 列标题切换排序方向。
- 右键单击列标题并选择 **Show Serialized Order (Global)**，按序列化顺序显示条目，而不是按键排序。此设置适用于所有 Dictionary，并在当前 Editor 会话中持久化，适合调试 Prefab override。参阅[Prefab 中的 Dictionary](#prefab-中的-dictionary)。

Dictionary 字段不支持多对象编辑。选择多个 GameObject 或 Asset 时，Inspector 会在 Dictionary editor 的位置显示 help box。

### Inspector 中的排序顺序

Inspector 只为显示而按键排序。排序不会改变序列化顺序，序列化顺序始终反映条目的添加顺序。单击 **Key** 列标题可以在升序和降序之间切换。

Inspector 直接从序列化数据读取每个键，并根据其 property type 比较字段。它不会调用键类型的 `IComparable<T>` 或 `CompareTo` 方法，因此不需要为 Inspector 排序实现它们。

下表说明各受支持键类型的排序行为：

| 键类型 | 排序行为 |
| --- | --- |
| `int`、`long`、`short`、`byte` 和其他整数类型 | 按数值顺序。 |
| `float`、`double` | 按数值顺序；`NaN` 值排在最后。 |
| `string` | 不区分大小写的自然顺序：数字连续段按数字比较，因此 `item2` 排在 `item10` 前面。 |
| `bool` | `false` 排在 `true` 前面。 |
| Enum 类型 | 按 Enum 值索引排序，该顺序与声明 Enum 成员的顺序一致。 |
| 对 `UnityEngine.Object` 子类的引用 | 按内部 entity identifier 排序。 |
| Struct 和 Class | 按字段声明顺序逐字段排序。参阅[复杂键的排序顺序](#复杂键的排序顺序)。 |

#### 复杂键的排序顺序

当 Dictionary 键是 Struct 或可序列化 Class 时，Inspector 按脚本中声明的顺序逐个字段比较条目。它会先比较每个键的第一个字段；如果值相等，再比较第二个字段，以此类推。要更改排序优先级，请重新排列类中的字段声明。

只有在 Inspector 中可见的字段会参与比较。标记了 `[HideInInspector]` 的字段会跳过。比较会递归进入嵌套 Struct 和 Class，最多 8 层。超过 8 层后，剩余嵌套字段会视为相等，Unity 会在 Console 中记录一次警告。

#### 排序顺序更新时机

Inspector 会在以下情况下重新排序显示的条目：

- 添加或删除条目时。
- 键字段更改并提交编辑后（例如离开字段或按 Enter）。
- 外部代码修改序列化属性时。

用户正在键字段中输入或拖动 slider 时，Inspector 会延后重新排序，以避免行在操作过程中移走。重复键标记会实时更新，因此仍能立即获得反馈。编辑完成后，Inspector 会重新排序，并在新顺序中保留当前选择。

### 自定义 Dictionary 显示

将 `[DictionaryDisplay]` 属性应用到 Dictionary 字段，可以设置列布局、列标签和初始列分割：

```csharp
using System.Collections.Generic;
using UnityEngine;

public class LootTable : MonoBehaviour
{
    [SerializeField]
    [DictionaryDisplay(keyLabel = "Item", valueLabel = "Drop chance", keyColumnFraction = 0.6f)]
    private Dictionary<string, float> drops = new Dictionary<string, float>();
}
```

`[DictionaryDisplay]` 的所有参数都是可选的：

- `keyLabel` 和 `valueLabel` 设置键和值列的标签。留空时，Unity 使用默认标签（**Key** 或 **Value**）。
- `keyColumnFraction` 设置分配给键列的可用宽度比例。有效值为 `0.01` 到 `0.99`，默认值为 `0.5`。
- `layout` 设置列布局。详情请参阅[选择布局](#选择布局)。

参数只设置初始显示方式。如果在 Inspector 中更改显示方式（例如拖动列分隔线，或从标题上下文菜单更改布局），Unity 会保存你的选择，后续绘制时忽略初始参数。要恢复属性设置的值，请右键单击列标题并选择 **Reset Layout**。

#### 选择布局

将 `layout` 参数设置为以下 `DictionaryLayout` 值之一，以决定 Inspector 如何排列键和值：

| 布局 | 说明 |
| --- | --- |
| `TwoColumns` | 在两个可调整大小的列中并排显示键和值。这是默认值。 |
| `OneColumnWithValueVisible` | 在单列中将每个值堆叠在其键下方，并以内联方式显示所有值。 |
| `OneColumnWithValueFoldout` | 在单列中将每个值堆叠在其键下方，并将每个值置于可折叠 foldout 后。 |

也可以从列标题的上下文菜单更改布局，这会覆盖属性设置的布局。

#### 按类型自定义 Dictionary

`[DictionaryDisplay]` 是字段属性，因此只配置应用它的单个字段。如果希望配置没有字段可装饰的 Dictionary（例如 `Dictionary<int, Dictionary<string, SkillLevel>>` 的内部 Dictionary，它是值而不是字段），或希望从单个声明为同一 Dictionary 类型的所有字段应用一致的显示方式，而不是重复添加 `[DictionaryDisplay]`，请改为将 `[DictionaryDisplayForType]` 作为 assembly-level 属性应用。

使用 `typeof` 指定准确的 Dictionary 类型。该属性会应用于该准确类型的每个 Dictionary，无论它出现在哪里：

```csharp
using System.Collections.Generic;
using UnityEngine;

// One declaration configures every Dictionary<string, SkillLevel> in the assembly: the nested
// dictionary in Character and the field in AbilityBook, without repeating [DictionaryDisplay].
// This assembly defines SkillLevel, which the attribute requires.
[assembly: DictionaryDisplayForType(typeof(Dictionary<string, SkillLevel>),
    layout = DictionaryLayout.OneColumnWithValueVisible,
    keyLabel = "Skill", valueLabel = "Level")]

[System.Serializable]
public struct SkillLevel
{
    public int rank;
    public float bonus;
}

public class Character : MonoBehaviour
{
    // Nested inner dictionary: a value, so it has no field to decorate.
    [SerializeField]
    private Dictionary<int, Dictionary<string, SkillLevel>> skillsPerTier = new();
}

public class AbilityBook : MonoBehaviour
{
    // A direct field of the same type, styled by the same declaration.
    [SerializeField]
    private Dictionary<string, SkillLevel> learnedSkills = new();
}
```

`[DictionaryDisplayForType]` 接受与 `[DictionaryDisplay]` 相同的参数，并全部应用。传给 `typeof` 的类型有两个要求：

- 必须是完全指定的 `Dictionary<TKey, TValue>`，例如 `Dictionary<string, SkillLevel>`。Unity 会忽略不是完全指定 Dictionary 类型的目标。分析器会报告 [[07-序列化规则分析器参考#uac1021|UAC1021]]。
- 必须使用与属性位于同一 assembly 中定义的类型：其键类型、值类型，或键/值内部嵌套的类型之一。例如，定义了 `SkillLevel` 的 assembly 可以指定 `Dictionary<string, SkillLevel>`、`Dictionary<int, SkillLevel[]>` 或 `Dictionary<int, List<SkillLevel>>`。如果目标只使用不在属性 assembly 中定义的类型（例如 `Dictionary<int, int>`），Unity 会忽略规则并在 Console 中记录警告。分析器会报告 [[07-序列化规则分析器参考#uac1022|UAC1022]]。

当 Dictionary 嵌套为另一个 Dictionary 的值时，Inspector 会使用 **Dictionary** 作为内部 Dictionary foldout 的标签，因为 Dictionary 值没有字段名。

#### 解析顺序

如果多个来源都能设置 Dictionary 的显示方式，Unity 按优先级从高到低使用第一个适用的来源：

1. 用户在 Editor 中的选择：标题上下文菜单中的布局和拖动分隔线设置的列宽。Unity 会按 property path 持久化这些选择，直到用户选择 **Reset Layout**。
2. Dictionary 字段上的字段级 `[DictionaryDisplay]` 设置布局、标签和宽度。
3. 准确 `Dictionary<TKey, TValue>` 上 assembly-level 的 `[DictionaryDisplayForType]` 设置布局、标签和宽度。
4. 内置默认值：`TwoColumns` 布局、**Key** 和 **Value** 标签，以及 `0.5` 的键列比例。

### 重复键

Dictionary 在运行时每个键只能包含一个值，但 Inspector 允许暂时创建重复键，以便逐步解决。Unity 会用图标和 tooltip 标记每个重复行，并在 Asset 中保留重复条目，直到你修正或删除它们。重复条目只在 Editor 中按宿主对象跟踪；Player 运行时始终强制键唯一。

当 Unity 加载包含重复键的序列化 Dictionary 的 Scene、Prefab 或 Asset，或实例化包含此类 Dictionary 的对象时，Editor 会在 Console 中写入警告。Unity 只将每个重复键的第一次出现添加到运行时 Dictionary。

如果要从自定义 Inspector 或其他工具读取重复索引，请使用 `SerializedProperty.GetDictionaryIgnoredEntries`，并读取其 `duplicateEntryIndices` 数组。

### Null 键

Dictionary 在运行时不能包含 null 键，但 Inspector 会保留键为 null 的行，以便你为它赋予有效键。使用 **+** 按钮添加条目但尚未设置键时，或 `UnityEngine.Object` 键未赋值或引用不再存在的对象时，行就具有 null 键。Unity 会用图标和 tooltip 标记每个 null-key 行，并在序列化数据中保留该行，以免丢失它或对应的值。

当 Unity 加载包含 null-key 行的序列化 Dictionary 的 Scene、Prefab 或 Asset，或实例化包含此类 Dictionary 的对象时，Editor 会在 Console 中写入警告，并将这些行排除在运行时 Dictionary 之外。Unity 会将每个 null-key 行作为独立占位符保留，而不会合并共享 null 键的行，因此不会丢失值。

如果 Dictionary 同时包含重复键和 null 键，Unity 会在一条 Console 警告中报告它们，而不是为每个问题分别报告警告。

如果要从自定义 Inspector 或其他工具读取 null-key 索引，请使用 `SerializedProperty.GetDictionaryIgnoredEntries`，并读取其 `nullKeyEntryIndices` 数组。

### Prefab 中的 Dictionary

可以在 Prefab 实例上覆盖序列化 Dictionary 的单个条目。Inspector 会像标记其他 property override 一样标记每个被覆盖的键或值，并允许分别应用或还原每个被覆盖的键或值。

Unity 使用条目的序列化位置记录 Dictionary override，就像记录 Array 和 List 字段的 override 一样。

Dictionary 给 Prefab override 增加了额外复杂性。Inspector 按排序顺序显示条目，而不是按添加或存储顺序显示，因此看到的行位置不对应条目的存储位置。在 Prefab Asset 中删除或添加条目后，请检查实例 override，确认它们仍应用于预期的条目。

为了更容易理解 override，可以右键单击列标题并选择 **Show Serialized Order (Global)**。Inspector 会按序列化顺序显示条目，此时每一行的位置与 Unity 用于记录 override 的存储索引一致。

有关此行为的逻辑和示例，请参阅 [Overrides on arrays, lists, and dictionaries](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabInstanceOverrides.html#collection-overrides)。

## 限制

- 不支持多对象编辑。选择多个目标时，Inspector 会显示 help box。
- Unity 使用序列化 Array index 记录 Dictionary override，因此在 Prefab Asset 上编辑 Dictionary 可能使现有实例 override 应用于不同条目。详情请参阅 [Overrides on arrays, lists, and dictionaries](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabInstanceOverrides.html#collection-overrides)。
- Inspector 排序不会改变序列化顺序，序列化顺序始终反映插入顺序。
- Unity 不会序列化 Dictionary 的 key comparer。只有在 Dictionary 字段声明的构造函数中传入 comparer，reload 后才会应用 comparer。参阅[自定义键比较器](#自定义键比较器)。

## 其他资源

- [[01-序列化规则]]
- [[07-序列化规则分析器参考]]
- [[05-自定义序列化]]
- [DictionaryDisplayAttribute](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryDisplayAttribute.html)
- [DictionaryDisplayForTypeAttribute](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryDisplayForTypeAttribute.html)
- [DictionaryLayout](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryLayout.html)
- [SerializedProperty.GetDictionaryIgnoredEntries](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializedProperty.GetDictionaryIgnoredEntries.html)
- [DictionaryIgnoredEntries](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryIgnoredEntries.html)

---

## 文档导航

- 上一页：[[03-序列化最佳实践]]
- 目录：[[00-脚本序列化]]
- 下一页：[[05-自定义序列化]]
﻿# Dictionary 序列化

> 原文：[Dictionary serialization](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-dictionaries.html)

Unity 会直接序列化声明为 [`Dictionary<TKey, TValue>`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.dictionary-2) 的 fields，因此你可以在 scripts 中编写 dictionary data，并在 **Inspector** window 中编辑它，无需编写 custom serialization code。声明的 field type 必须正好是 `Dictionary<TKey, TValue>`。

Dictionary serialization 是 opt-in 的：必须为希望 Unity 序列化的每个 dictionary field 应用 [`[SerializeField]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializeField.html)。Unity 只支持将[特定 types](#支持的-key-和值类型)作为 dictionary keys 和 values。[序列化规则分析器](07-序列化规则分析器参考.md)会在 compile time 检测不支持的 key 和 value types，并指向解释该限制的 rule。Inspector 会渲染一个两列的 key/value editor，支持 sort、duplicate-key detection 和 column resizing。

Unity 按 insertion order 将 dictionary 序列化为 key/value pairs 的 sequence。Inspector 中显示的 order 与 serialized order 独立。参阅[Inspector 中的排序顺序](#inspector-中的排序顺序)。

## 声明 serialized dictionary field

你可以在 `MonoBehaviour`、`ScriptableObject` 或任意 nested `[Serializable]` class 或 struct 上序列化 dictionary field。对 private 或 public dictionary field 应用 `[SerializeField]`，即可让 Unity 序列化 dictionary：

```csharp
using System.Collections.Generic;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    [SerializeField]
    private Dictionary<string, int> itemCounts = new Dictionary<string, int>();
}
```

Public dictionary fields 不会自动序列化。没有 `[SerializeField]` 时，Unity 会跳过该 field，dictionary 不会在 domain reloads、scene saves 或 Play mode transitions 之间持久化。若 public dictionary field 缺少 `[SerializeField]`，analyzer 会报告 [[07-序列化规则分析器参考#UAC1015|UAC1015]]，这样你可以决定 opt in，或将 field 标记为 [`[NonSerialized]`](https://learn.microsoft.com/en-us/dotnet/api/system.nonserializedattribute)。

[`[SerializeReference]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializeReference.html) 对 dictionary fields 无效，因为 Unity 将 dictionary 序列化为 entries 的 inline collection，而不是单个 polymorphic reference。如果在 dictionary field 上应用 `[SerializeReference]`，analyzer 会报告 [[07-序列化规则分析器参考#UAC1014|UAC1014]]。

## 支持的 key 和 value types

`TKey` 和 `TValue` 都必须是 Unity 可以序列化的 types：

- Primitive types（`int`、`float`、`double`、`bool`、`string`）。
- Enum types（32 bits 或更小）。
- Unity built-in types，例如 `Vector2`、`Vector3`、`Color`。
- 标记了 `[Serializable]` 的 custom classes 和 structs。
- 对派生自 [`UnityEngine.Object`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.html) 的 types 的 references。

不能将 interface、abstract type（`UnityEngine.Object` hierarchy 除外）或未标记 `[Serializable]` 的 type 用作 key 或 value。Analyzer 会分别报告 [[07-序列化规则分析器参考#UAC1012|UAC1012]] 和 [[07-序列化规则分析器参考#UAC1016|UAC1016]]。

Collections 可以作为 values，但不能作为 keys：

- 作为 **value**，可以使用任意 supported type，或 supported types 的 collection，例如 `List<T>`、array 或另一个 `Dictionary<TKey, TValue>`。例如，`Dictionary<int, List<int>>` 和 `Dictionary<int, Dictionary<string, int>>` 都有效。
- 作为 **key**，不能使用实现了 `IEnumerable` 的 type——这是 `List<T>` 和 arrays 等 collection types 实现的 interface。`string` 是例外，尽管它实现了 `IEnumerable`。例如，Unity 不能序列化 `Dictionary<List<int>, int>` field，因为其 key type `List<int>` 实现了 `IEnumerable`。Analyzer 会报告 [[07-序列化规则分析器参考#UAC1013|UAC1013]]。

Unity 也不会序列化直接嵌套在另一个 collection 中的 dictionary。例如，`List<Dictionary<string, int>>` 和 `Dictionary<string, int>[]` 不受支持。将 dictionary 包装在 `[Serializable]` class 或 struct 中，将其用作 element type。Analyzer 会将此情况报告为 [[07-序列化规则分析器参考#UAC1009|UAC1009]]。

直接或在其 field graph 或 inheritance chain 的任何位置包含 `[SerializeReference]` field 的 structs 和 classes，都可以作为 serialized dictionary 的 key 或 value。

完整的 analyzer rules 和 usage examples，请参阅 [[07-序列化规则分析器参考]]。

### Custom struct 和 class keys

如果使用 custom struct 或 class 作为 dictionary key，请重写 `GetHashCode` 和 `Equals`，让 dictionary 能正确放置和查找 entries：

- 没有 overrides 的 custom classes 使用 reference equality。两个 field values 相同的 instances 会被视为不同 keys，从而破坏 dictionary lookups。
- 没有 overrides 的 custom structs 会退回到基于 reflection 的 hashing 和 equality。Dictionary 可以正确工作，但速度较慢。添加 overrides 可改善 performance。
- Primitives、`string`、enums、Unity built-in types（例如 `Vector3` 和 `Color`）以及 `UnityEngine.Object` subclasses 已正确实现 `GetHashCode` 和 `Equals`，不需要重写。

对于 value-type keys，还应实现 [`IEquatable<T>`](https://learn.microsoft.com/en-us/dotnet/api/system.iequatable-1)，以避免 key comparisons 时的 boxing allocations。`IEquatable<T>` 不是必需的，但能改善 runtime performance。

如果 custom `GetHashCode` 或 `Equals` implementation 在 Unity 加载 serialized dictionary 时抛出 exception，Unity 会跳过受影响的 entries，并记录一条 Console warning。

## Custom key comparers

要控制 serialized dictionary 对 keys 的比较和 hashing，请在 field declaration 中将 [`IEqualityComparer<TKey>`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iequalitycomparer-1) interface 的 implementation 传给 dictionary constructor：

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    [SerializeField]
    private Dictionary<string, int> itemCounts = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
}
```

Unity 不会将 comparer 写入 scene、prefab 或 asset。只有在 field declaration 的 constructor 中传入 comparer，load 后 comparer 才会继续生效。这是因为 Unity 会复用 field 当前已有的 dictionary，而不是创建新的 dictionary：它会对该 dictionary 调用 `Clear`，然后添加读取到的 entries。`Clear` method 不会重置 comparer。

field 所包含的 dictionary 取决于 operation：

- 创建包含该 dictionary 的 object 的 operation 会先运行 field declaration，因此 dictionary 使用你声明的 comparer。这包括 domain reloads、scene loads、prefab loads、asset loads 以及调用 [`Object.Instantiate`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Instantiate.html) method。
- 对已经存在的 object 进行 deserialization 的 operation，会复用 field 在当时所包含的 dictionary，不会再次运行 field declaration。这包括 undo、redo、prefab revert 以及调用 [`SerializedObject.ApplyModifiedProperties`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializedObject.ApplyModifiedProperties.html) method。除非 script 在 Unity load object 后替换 dictionary 或将 field 设为 `null`，否则 declared comparer 仍然生效。如果 field 为 `null`，Unity 会用 default comparer 创建新 dictionary，直到下一次创建 object 时才会再次应用 declared comparer。

### 在 field declaration 中设置 comparer

Serialized data 不包含 comparer，因此 Unity 无法恢复只有 script 在 runtime 赋给 dictionary 的 comparer。更多信息请参阅[Unity 无法保留的 comparers](#unity-无法保留的-comparers)。

例如，以下 script 会在 Unity 下一次创建 object（例如 domain reload 后）时丢失 comparer。`SetValues` method 用带 comparer 的 dictionary 替换 field，但 field declaration 没有设置 comparer，因此 reloaded asset 会以 case-sensitive 方式比较 keys：

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

public class ItemLookup : ScriptableObject
{
    [SerializeField]
    private Dictionary<string, int> values = new Dictionary<string, int>();

    public Dictionary<string, int> Values => values;

    // A caller supplies the comparer, for example:
    // lookup.SetValues(new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase));
    public void SetValues(Dictionary<string, int> newValues)
    {
        values = newValues;
    }
}
```

要保留 comparer，请在 field declaration 的 constructor 中传入它：

```csharp
[SerializeField]
private Dictionary<string, int> values = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
```

采用此 declaration 后，下一次 Unity 创建 object 时 dictionary 会再次使用 declared comparer，即使 script 在 runtime 替换了 dictionary。

在 Unity 再次创建 object 之前，field 包含 runtime 赋值的 dictionary，而 in-place operation（例如 undo）会使用该 dictionary 的 comparer，而不是 declared comparer。要让两种情况下的行为一致，请为 runtime 赋值的任何 dictionary 使用与 field declaration 相同的 comparer。

### 不要在 `Awake` 或 `OnEnable` 中替换 dictionary

不要在 Unity 对 object 进行 deserialization 后调用的 `MonoBehaviour` method（例如 `Awake`、`OnEnable` 或 `Start`）中向 field 赋值新的 dictionary。新 dictionary 会丢弃 Unity 已加载的 entries。要设置 comparer，请在 field declaration 的 constructor 中传入它，该 declaration 会在 deserialization 之前运行。

### comparer 导致的 duplicate keys

Comparer 可能会让两个不同的 serialized keys 相等。例如，serialized data 中的 keys `Alpha` 和 `alpha` 是不同 strings，但 `StringComparer.OrdinalIgnoreCase` comparer 会将它们视为同一个 key。

Unity 会将此报告为 duplicate key：它把第一条 entry 加入 runtime dictionary，排除后续 entries，并在 Inspector 中标记每个被排除的 row，方便你修正或移除它。这与其他 duplicate key 的行为相同。更多信息请参阅[Duplicate keys](#duplicate-keys)。

### Unity 无法保留的 comparers

在以下情况下，Unity 无法恢复 script 设置在 dictionary 上的 comparer：

- **Runtime 选择的 comparer。** Field declaration 在 compile time 固定，因此无法指定 script 运行时选择的 comparer，例如从 loaded value、project setting 或 method argument 中选择的 comparer。Unity 无法从 serialized data 读回 comparer，因此不会恢复该选择。
- **Struct 内的 dictionary。** C# 不允许在 struct fields 上使用 field initializers，因此 struct declaration 无法创建 dictionary 或为它设置 comparer。Unity 会在包含该 struct 的 object 内就地读取 serialized struct 的 fields。
- **作为 value 使用的 dictionary。** 在 `Dictionary<string, Dictionary<string, int>>` field 中，Unity 读取 entries 时创建每个 inner dictionary，因此 inner dictionary 没有能设置 comparer 的 field declaration。Outer dictionary 是一个 field，因此会保留你为它设置的 comparer。

在这些情况中，dictionary 使用 field declaration 中的 comparer；如果 field declaration 没有设置 comparer，则使用与 [`EqualityComparer<TKey>.Default`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.equalitycomparer-1.default) property 返回值相同的 comparer。

作为 value 使用的 dictionary 的限制，仅在 value 本身是 dictionary 时适用。如果 value 是一个含有 dictionary field 的 `[Serializable]` class，只要该 class 有 parameterless constructor，该 dictionary 就会保留其 field declaration 中的 comparer。Unity 使用该 constructor 创建 class，因此 class 的 field declarations 会运行。如果 class 只声明了带 parameters 的 constructors，Unity 创建 class 时不会运行 constructor，field declarations 也不会运行，dictionary 会使用 default comparer。

如果在上述情况之一中需要 custom comparer，请重构 data，让 dictionary 成为一个其 declaration 可以创建它的 field。例如，将 dictionary 从 struct 移到带 parameterless constructor 的 `[Serializable]` class 中，然后在该 class 的 dictionary field declaration 中设置 comparer。

## 在 Inspector 中编辑 dictionary

当你选择包含 serialized dictionary 的 GameObject 或 asset 时，Inspector 会将 dictionary 渲染为两列 list，左侧是 keys，右侧是 values。

![Inspector 将 dictionary field 显示为两列 list，左侧为 keys，右侧为 values。](serialization-dictionary-inspector.png)

Inspector 提供以下功能：

- 使用 list 底部的 **+** 和 **-** buttons 添加或移除 entry。
- 更改 columns 的 width。Width 会按 property path 和 Inspector window 持久化。
- 右键点击 column header 更改 layout。参阅[自定义 dictionary display](#自定义-dictionary-display)。
- 右键点击 column header 并选择 **Reset Layout**，恢复 default layout、column split 和 sort direction。
- 点击 **Key** column header 切换 sort direction。
- 右键点击 column header 并选择 **Show Serialized Order (Global)**，按 serialized order 而不是按 key sort 显示 entries。此设置应用于每个 dictionary，并在当前 Editor session 中持久化。它对 debug prefab overrides 很有用。参阅[Prefabs 中的 dictionaries](#prefabs-中的-dictionaries)。

Dictionary fields 不支持 multi-object editing。当选择多个 GameObjects 或 assets 时，Inspector 会在 dictionary editor 的位置显示 help box。

### Inspector 中的排序顺序

Inspector 只为 display 按 key 对 entries 排序。排序不会改变 serialized order，serialized order 始终反映 entries 添加的顺序。点击 **Key** column header，在 ascending 和 descending order 之间切换。

Inspector 直接从 serialized data 读取每个 key，并根据 property type 比较 fields。它不会调用 comparison interface `IComparable<T>` 或 key type 上的 `CompareTo` method，因此不需要为 Inspector sorting 实现它们。

下表描述每种 supported key type 的 sort behavior：

| Key type | Sort behavior |
| --- | --- |
| `int`、`long`、`short`、`byte` 和其他 integer types | Numeric order。 |
| `float`、`double` | Numeric order。`NaN` values 排在最后。 |
| `string` | Case-insensitive natural order：digit runs 会按 numbers 比较，因此 `item2` 出现在 `item10` 之前。 |
| `bool` | `false` 在 `true` 之前。 |
| Enum types | 按 enum value index 排序，这与 enum members 的声明顺序一致。 |
| 对 `UnityEngine.Object` subclasses 的 references | 按 internal entity identifier 排序。 |
| Structs 和 classes | 按声明顺序逐 field 排序。参阅[复杂 key 的排序顺序](#复杂-key-的排序顺序)。 |

#### 复杂 key 的排序顺序

当 dictionary key 是 struct 或 serializable class 时，Inspector 按 script 中声明 fields 的顺序，一次比较一个 field。它会比较每个 key 的第一个 field；如果这些 values 相等，则继续比较第二个，以此类推。要改变 sort priority，请重新排列 class 中的 field declarations。

只有在 Inspector 中可见的 fields 才会参与 comparison。标记了 [`[HideInInspector]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/HideInInspector.html) 的 fields 会被跳过。Comparison 会递归进入 nested structs 和 classes，最多 8 层。超过此深度后，剩余 nested fields 会被视为相等，Unity 会记录一次性 Console warning。

#### Sort order 何时更新

Inspector 会在以下情况下重新 sort displayed entries：

- 添加或移除 entry 时。
- key field 改变并提交 edit 后（例如离开 field 或按 Enter）。
- external code 修改 serialized property 时。

当你正在 key field 中输入或拖动 slider 时，Inspector 会推迟 re-sort，避免 row 在你操作时移走。Duplicate-key markers 仍会实时更新，因此你仍能立即得到 feedback。完成 edit 后，Inspector 会重新 sort，并在新 order 中保留当前 selection。

### 自定义 dictionary display

将 [`[DictionaryDisplay]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryDisplayAttribute.html) attribute 应用到 dictionary field，可设置 column layout、column labels 和 initial column split：

```csharp
using System.Collections.Generic;
using UnityEngine;

public class LootTable : MonoBehaviour
{
    [SerializeField]
    [DictionaryDisplay(keyLabel = "Item", valueLabel = "Drop chance", keyColumnFraction = 0.6f)]
    private Dictionary<string, float> drops = new Dictionary<string, float>();
}
```

`[DictionaryDisplay]` 的以下 parameters 都是 optional：

- `keyLabel` 和 `valueLabel` 设置 key 和 value columns 的 labels。如果留空，Unity 使用 default label（**Key** 或 **Value**）。
- `keyColumnFraction` 设置分配给 key column 的 available width fraction。有效值为 `0.01` 到 `0.99`，default value 为 `0.5`。
- `layout` 设置 column layout。详情请参阅[选择 layout](#选择-layout)。

这些 parameters 只设置 initial presentation。如果你在 Inspector 中改变 presentation（例如拖动 column divider，或从 header context menu 更改 layout），Unity 会保存你的选择，并在后续 draws 中忽略 initial parameters。要恢复 attribute 设置的 values，请右键点击 column header 并选择 **Reset Layout**。

#### 选择 layout

要确定 Inspector 如何排列 keys 和 values，请将 `layout` parameter 设为以下 [`DictionaryLayout`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryLayout.html) values 之一：

| Layout | Description |
| --- | --- |
| `TwoColumns` | 在两个可调整大小的 columns 中并排显示 keys 和 values。这是 default value。 |
| `OneColumnWithValueVisible` | 在单个 column 中将每个 value 堆叠在其 key 下方，并 inline 显示每个 value。 |
| `OneColumnWithValueFoldout` | 在单个 column 中将每个 value 堆叠在其 key 下方，并将每个 value 放在可折叠 foldout 后。 |

也可以从 column header 的 context menu 更改 layout，这会覆盖 attribute 设置的 layout。

#### 按 type 自定义 dictionary

`[DictionaryDisplay]` attribute 是 field attribute，因此只配置附加它的单个 field。当希望执行以下操作时，请改为将 [`[DictionaryDisplayForType]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryDisplayForTypeAttribute.html) 作为 assembly-level attribute 应用：

- 配置没有可供 decorate 的 field 的 dictionary，例如 `Dictionary<int, Dictionary<string, SkillLevel>>` 的 inner dictionary，它是 value 而不是 field。
- 通过单个 declaration 为同一 dictionary type 的每个 field 应用一致的 presentation，而不是在每个 field 上重复 `[DictionaryDisplay]`。

使用 `typeof` 指定 exact dictionary type。该 attribute 会应用于任何位置出现的该 exact type 的每个 dictionary：

```csharp
using System.Collections.Generic;
using UnityEngine;

// One declaration configures every Dictionary<string, SkillLevel> in the assembly: the nested
// dictionary in Character and the field in AbilityBook, without repeating [DictionaryDisplay].
// This assembly defines SkillLevel, which the attribute requires.
[assembly: DictionaryDisplayForType(typeof(Dictionary<string, SkillLevel>),
    layout = DictionaryLayout.OneColumnWithValueVisible,
    keyLabel = "Skill", valueLabel = "Level")]

[System.Serializable]
public struct SkillLevel
{
    public int rank;
    public float bonus;
}

public class Character : MonoBehaviour
{
    // Nested inner dictionary: a value, so it has no field to decorate.
    [SerializeField]
    private Dictionary<int, Dictionary<string, SkillLevel>> skillsPerTier = new();
}

public class AbilityBook : MonoBehaviour
{
    // A direct field of the same type, styled by the same declaration.
    [SerializeField]
    private Dictionary<string, SkillLevel> learnedSkills = new();
}
```

`[DictionaryDisplayForType]` 接受与 `[DictionaryDisplay]` 相同的 parameters，并应用所有这些 parameters。传给 `typeof` 的 type 有两个要求：

- 必须是 fully specified 的 `Dictionary<TKey, TValue>`，例如 `Dictionary<string, SkillLevel>`。Unity 会忽略不是 fully specified dictionary type 的 target。Analyzer 会报告 [[07-序列化规则分析器参考#UAC1021|UAC1021]]。
- 必须使用与该 attribute 位于同一 assembly 中定义的 type：其 key type、value type，或两者中任一 type 内 nested 的 type。例如，定义 `SkillLevel` 的 assembly 可以 target `Dictionary<string, SkillLevel>`、`Dictionary<int, SkillLevel[]>` 或 `Dictionary<int, List<SkillLevel>>`。这样可以防止一个 assembly 中的 rule 修改完全由它未定义的 types 构成的 dictionary，例如 `Dictionary<int, int>`。如果 target 不使用该 attribute 所在 assembly 中的任何 type，Unity 会忽略 rule 并在 Console 中记录 warning。Analyzer 会报告 [[07-序列化规则分析器参考#UAC1022|UAC1022]]。

当 dictionary 作为另一个 dictionary 的 value nested 时，Inspector 会使用 **Dictionary** 作为 inner dictionary foldout 的 label，因为 dictionary value 没有 field name。

#### Resolution order

当多个 sources 都可以设置 dictionary 的 presentation 时，Unity 按从高到低的 precedence 使用第一个适用的 source：

1. User 自己在 Editor 中的 choices：来自 header context menu 的 layout 和拖动 divider 设置的 column width。Unity 按 property path 持久化这些 choices，直到 user 选择 **Reset Layout**。
2. Dictionary field 上 field-level 的 `[DictionaryDisplay]`，设置 layout、labels 和 width。
3. exact `Dictionary<TKey, TValue>` 上 assembly-level 的 `[DictionaryDisplayForType]`，设置 layout、labels 和 width。
4. Built-in defaults：`TwoColumns` layout、**Key** 和 **Value** labels，以及 `0.5` key-column fraction。

### Duplicate keys

Dictionary 在 runtime 中每个 key 只能包含一个 value，但 Inspector 允许临时创建 duplicate keys，让你可以逐步解决它们。Unity 会用 icon 和 tooltip 标记每个 duplicate row，并在你修正或移除它们之前，将 duplicate entries 保留在 asset 中。Duplicate entries 在 Editor 中仅按 host object 跟踪；Player runtime 始终强制要求 unique keys。

当 Unity 加载包含 serialized dictionary（其中有 duplicate keys）的 scene、prefab 或 asset，或实例化包含此类 dictionary 的 object 时，Editor 会在 Console 中写入 warning。Unity 只会将每个 duplicate key 的第一次出现加入 runtime dictionary。

如果需要从 custom Inspector 或其他 tooling 读取 duplicate indices，请使用 [`SerializedProperty.GetDictionaryIgnoredEntries`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializedProperty.GetDictionaryIgnoredEntries.html)，并读取其 [`duplicateEntryIndices`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryIgnoredEntries-duplicateEntryIndices.html) array。

### Null keys

Dictionary 在 runtime 中不能包含 null key，但 Inspector 会保留 key 为 null 的 row，让你可以为它赋予有效 key。以下情况会产生 null key row：使用 **+** button 添加 entry 但尚未设置 key，或 `UnityEngine.Object` key 未赋值，或指向已不存在的 object。Unity 会用 icon 和 tooltip 标记每个 null-key row，并将 row 保留在 serialized data 中，因此不会丢失它或它的 value。

当 Unity 加载包含 serialized dictionary（其中有 null-key rows）的 scene、prefab 或 asset，或实例化包含此类 dictionary 的 object 时，Editor 会在 Console 中写入 warning，并将这些 rows 排除在 runtime dictionary 之外。Unity 会将每个 null-key row 保留为独立 placeholder，而不会合并共享 null key 的 rows，因此不会丢失 value。

如果 dictionary 同时包含 duplicate keys 和 null keys，Unity 会在一条 Console warning 中报告它们，而不是为每个问题各写一条 warning。

如果需要从 custom Inspector 或其他 tooling 读取 null-key indices，请使用 [`SerializedProperty.GetDictionaryIgnoredEntries`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializedProperty.GetDictionaryIgnoredEntries.html)，并读取其 [`nullKeyEntryIndices`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryIgnoredEntries-nullKeyEntryIndices.html) array。

### Prefabs 中的 dictionaries

你可以在 [prefab instance](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabInstanceOverrides.html) 上 override serialized dictionary 的 individual entries。Inspector 会使用显示其他 property overrides 的相同方式，标示每个 overridden key 或 value；你可以独立 apply 或 revert 每个 overridden key 或 value。

Unity 使用 entry 的 serialized position 记录 dictionary overrides，这与记录 array 和 list fields 的 overrides 相同。

Dictionary 会为 prefab overrides 增加额外复杂性。Inspector 按 sorted order 显示 entries，而不是按它们添加或存储的 order 显示，因此你看到的 row position 与 entry 的 storage position 不对应。在 prefab asset 上删除或添加 entry 后，请检查 instance overrides，确认它们仍应用于你预期的 entries。

为了更容易理解 overrides，请右键点击 column header 并选择 **Show Serialized Order (Global)**。Inspector 随后会按 serialized order 显示 entries，因此每个 row 的 position 都与 Unity 用来记录 override 的 storage index 相匹配。

关于此行为背后的 logic 和示例，请参阅 [Overrides on arrays, lists, and dictionaries](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabInstanceOverrides.html#collection-overrides)。

## 限制

- 不支持 multi-object editing。选择多个 targets 时，Inspector 会显示 help box。
- Unity 使用 serialized array index 记录 dictionary overrides，因此在 prefab asset 上编辑 dictionary 可能会使现有 instance overrides 应用到另一个 entry。更多信息请参阅 [Overrides on arrays, lists, and dictionaries](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabInstanceOverrides.html#collection-overrides)。
- Inspector sort order 不会改变 serialized order，serialized order 始终反映 insertion order。
- Unity 不会序列化 dictionary 的 key comparer。只有在 dictionary field declaration 的 constructor 中传入 comparer，comparer 才会在 reload 后生效。参阅 [[04-Dictionary序列化#Custom key comparers|Custom key comparers]]。

## 其他资源

- [[01-序列化规则]]
- [[07-序列化规则分析器参考]]
- [[05-自定义序列化]]
- [`DictionaryDisplayAttribute`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryDisplayAttribute.html)
- [`DictionaryDisplayForTypeAttribute`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryDisplayForTypeAttribute.html)
- [`DictionaryLayout`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryLayout.html)
- [`SerializedProperty.GetDictionaryIgnoredEntries`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializedProperty.GetDictionaryIgnoredEntries.html)
- [`DictionaryIgnoredEntries`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/DictionaryIgnoredEntries.html)

---

## 文档导航

- 上一页：[[03-序列化最佳实践]]
- 目录：[[00-脚本序列化]]
- 下一页：[[05-自定义序列化]]
