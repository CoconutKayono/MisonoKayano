# Unity 如何使用序列化

> 原文：[How Unity uses serialization](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-how-unity-uses.html)

## 保存和加载

Unity 使用序列化在设备内存中加载和保存 Scene、Asset 与 AssetBundle。这也包括保存在你自己的 scripting API 对象（例如 MonoBehaviour 组件和 ScriptableObject）中的数据。

Unity Editor 的许多功能都建立在核心序列化系统之上。序列化有两个尤其需要注意的方面：Inspector 窗口和热重载。

### Inspector 窗口

Inspector 窗口显示被检查对象的序列化字段值。当你在 Inspector 中更改值时，Inspector 会更新序列化数据，并触发反序列化来更新被检查对象。

这同时适用于内置 Unity 对象和继承自 MonoBehaviour 的 scripting 对象。

在 Inspector 窗口中查看或更改值时，Unity 不会调用任何 C# 属性 getter 和 setter，而是直接访问序列化的 backing field。

### 热重载

脚本代码的热重载是 Asset Database refresh 的一部分。它指 Editor 运行时直接重载并应用代码更改的过程，不必重启 Editor。详情请参阅 [Refreshing the Asset Database](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetDatabaseRefreshing.html) 及其 Hot reloading 部分。

**注意**：热重载是一种特殊的序列化情况。与其他序列化情况不同，Unity 在重载时默认序列化 private 字段，即使它们没有 `[SerializeField]` 属性。

Unity 重载脚本时：

1. Unity 序列化并存储所有已加载脚本中的所有变量。
2. Unity 将它们恢复为序列化前的原始值：
   - Unity 恢复所有满足序列化要求的变量，**包括 private 变量**，即使变量没有 `[SerializeField]` 属性。
   - Unity 永远不会恢复 static 变量。因此，不要使用 static 变量保存需要在 Unity 重载脚本后保留的状态，因为重载过程会丢弃它们。

### 阻止序列化和恢复

有时需要阻止 Unity 恢复 private 变量，例如希望脚本重载后某个引用为 null。此时请使用 `[NonSerialized]` 属性。

Unity 的恢复行为也适用于 C# 中存储 auto-implemented property 值的 private backing field。例如：

```csharp
public string MyProperty { get; set; }
```

C# 会向类中添加一个不可见的 private 字段来存储 `MyProperty` 的实际值。Unity 会在热重载期间序列化并恢复此值。若要阻止此行为，请在属性上使用 `[field: NonSerialized]`。

下面的示例分别使用 `[NonSerialized]` 和 `[field: NonSerialized]`，阻止普通字段和 auto-property backing field 被序列化及恢复：

```csharp
class Test
{
    // p will not be shown in the Inspector or serialized
    [System.NonSerialized]
    public int p = 5;

    // neverSerializeMe will never be serialized, even during an hot reload.
    [System.NonSerialized]
    private int neverSerializeMe;

    // The backing field for NeverSerializedProperty property will never be serialized,
    // even during a hot reload
    [field: System.NonSerialized]
    public int NeverSerializedProperty { get; set; }
}
```

## Prefabs

Prefab 是一个或多个 GameObject 或组件的序列化数据。Prefab 实例包含对 Prefab 源和一组修改的引用。Unity 需要这些修改，才能从 Prefab 源创建该特定的 Prefab 实例。

Prefab 实例只在 Unity Editor 中编辑项目时存在。Unity Editor 使用两组序列化数据实例化 GameObject：Prefab 源和 Prefab 实例的修改。

## 实例化

当你对 Scene 中存在的任何对象（例如 Prefab 或 GameObject）调用 `Instantiate` 时：

1. Unity 序列化该对象。这在运行时和 Editor 中都会发生。Unity 可以序列化所有继承自 `UnityEngine.Object` 的对象。
2. Unity 创建新的 GameObject，并将数据反序列化到新 GameObject 上。
3. Unity 以另一种变体运行相同的序列化代码，以报告它引用的其他 `UnityEngine.Object`。Unity 检查所有被引用的 `UnityEngine.Object`，确定它们是否属于 Unity 正在实例化的数据。如果引用指向外部对象（例如 Texture），Unity 保持该引用不变；如果引用指向内部对象（例如子 GameObject），Unity 会将引用修补为对应的副本。

## 卸载未使用的 Asset

`EditorUtility.UnloadUnusedAssetsImmediate` 是原生 Unity garbage collector，用途不同于标准 C# garbage collector。它在加载 Scene 后运行，检查不再被引用的对象（如 Texture），并安全地卸载它们。原生 Unity garbage collector 会在一种变体中运行 serializer，在该变体中对象会报告所有对外部 `UnityEngine.Object` 的引用。这就是某个 Scene 使用的 Texture 能被 garbage collector 在下一个 Scene 中卸载的原因。

## Editor 与运行时序列化的差异

大多数序列化发生在 Editor 中，而运行时主要关注反序列化。Unity 只在 Editor 中序列化某些功能，而其他功能在 Editor 和运行时都可以序列化：

| 功能 | Editor | 运行时 |
| --- | --- | --- |
| 二进制格式的 Asset | 支持读/写 | 支持读取 |
| YAML 格式的 Asset | 支持读/写 | 不支持 |
| 保存 Scene、Prefab 和其他 Asset | 支持，除非处于 Play mode | 不支持 |
| 使用 `JsonUtility` 序列化单个对象 | `JsonUtility` 支持读/写；`EditorJsonUtility` 支持其他类型对象 | `JsonUtility` 支持读/写 |
| `SerializeReference` | 支持 | 支持 |
| `ISerializationCallbackReceiver` | 支持 | 支持 |
| `FormerlySerializedAs` | 支持 | 不支持 |

对象可以包含只有 Editor 才会序列化的额外字段，例如在 `UNITY_EDITOR` scripting symbol 中声明字段：

```csharp
public class SerializeRules : MonoBehaviour
{
#if UNITY_EDITOR
public int m_intEditorOnly;
#endif
}
```

上例中的 `m_intEditorOnly` 只在 Editor 中序列化，不会包含在构建中。这样可以从构建中省略只在 Editor 中需要的数据，以节省内存。任何使用该字段的代码也必须有条件地编译，例如放在 `#if UNITY_EDITOR` 代码块中，使类能够在构建时编译。

Editor 不支持包含只在运行时序列化字段的对象（例如在 `UNITY_STANDALONE` 指令中声明字段）。

## 其他资源

- [[01-序列化规则]]
- [[06-JSON序列化]]
- [[03-序列化最佳实践]]

---

## 文档导航

- 上一页：[[01-序列化规则]]
- 目录：[[00-脚本序列化]]
- 下一页：[[03-序列化最佳实践]]
﻿# Unity 如何使用序列化

> 原文：[How Unity uses serialization](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-how-unity-uses.html)

## 保存和加载

Unity 使用 serialization 在 device memory 与 scenes、Assets 和 AssetBundles 之间加载、保存数据。这也包括保存在你自己的 scripting API objects 中的数据，例如 [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html) components 和 [ScriptableObjects](https://docs.unity3d.com/6000.7/Documentation/Manual/class-ScriptableObject.html)。

Unity Editor 中的许多功能都构建在 core serialization system 之上。使用 serialization 时尤其需要注意两点：Inspector window 和 hot reloading。

### Inspector window

Inspector window 显示被检查 objects 的 serialized fields 的值。当你在 Inspector 中修改某个值时，Inspector 会更新 serialized data，并触发一次 deserialization 来更新被检查的 object。

这同时适用于 built-in Unity objects 和 scripting objects（例如派生自 MonoBehaviour 的 classes）。

当你在 Inspector window 中查看或修改值时，Unity 不会调用任何 C# property getters 和 setters，而是直接访问 serialized backing field。

### 热重载

Script code 的 hot reloading 作为 asset database refresh 的一部分执行。它指的是 Editor 运行时直接重载并应用 code changes 的过程，无需重启 Editor。更多信息请参阅 [Refreshing the Asset Database](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetDatabaseRefreshing.html) 和 [Hot reloading](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetDatabaseRefreshing.html#hotreloading)。

**注意**：Hot reloading 是一种特殊的 serialization case。与其他 serialization cases 不同，Unity 在 reload 时默认序列化 private fields，即使它们没有 [`[SerializeField]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializeField.html) attribute。

当 Unity reload scripts 时：

1. Unity 序列化并存储所有已加载 scripts 中的所有 variables。
2. Unity 将它们恢复为 serialization 前的原始值：

   - Unity 会恢复所有满足 serialization 要求的 variables，**包括 private variables**，即使 variable 没有 `[SerializeField]` attribute。
   - Unity 从不恢复 static variables。因此，不要使用 static variables 保存需要在 Unity reload script 后保留的 states，因为 reload process 会丢弃它们。

### 阻止 serialization 和 restoration

有时你需要阻止 Unity 恢复 private variables，例如希望某个 reference 在 script reload 后为 null。此时请使用 [`[NonSerialized]`](https://learn.microsoft.com/en-us/dotnet/api/system.nonserializedattribute) attribute。

Unity 的 restore behavior 同样适用于 C# 中存储 automatically implemented properties 值的 private backing fields。例如，考虑以下 automatically implemented property：

```csharp
public string MyProperty { get; set; }
```

在此情况下，C# 会向 class 添加一个 invisible private field，用于存储 `MyProperty` 的实际值。Unity 会在 hot reload 期间序列化并恢复这个值。要阻止此行为，请在 property 上使用 `[field: NonSerialized]`。

以下示例展示如何分别使用 `[NonSerialized]` 和 `[field: NonSerialized]`，阻止普通 fields 和 auto-property backing field 的 serialization 与 restoration：

```csharp
class Test
{
    // p will not be shown in the Inspector or serialized
    [System.NonSerialized]
    public int p = 5;

    // neverSerializeMe will never be serialized, even during an hot reload.
    [System.NonSerialized]
    private int neverSerializeMe;

    // The backing field for NeverSerializedProperty property will never be serialized,
    // even during a hot reload
    [field: System.NonSerialized]
    public int NeverSerializedProperty { get; set; }
}
```

## Prefabs

Prefab 是一个或多个 GameObjects 或 components 的 serialized data。Prefab instance 同时包含对 prefab source 的 reference 以及一组 modifications。Modifications 是 Unity 根据 prefab source 创建特定 prefab instance 所需的数据。

Prefab instance 只在 Unity Editor 中编辑项目时存在。Unity Editor 使用两组 serialization data（prefab source 和 prefab instance 的 modifications）实例化 GameObject。

## 实例化

当你对 scene 中存在的任何 object（例如 prefab 或 GameObject）调用 [`Instantiate`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Instantiate.html) 时：

1. Unity 序列化它。这在 runtime 和 Editor 中都会发生。Unity 可以序列化所有派生自 `UnityEngine.Object` 的 objects。
2. Unity 创建一个新的 GameObject，并将 data 反序列化到新的 GameObject 上。
3. Unity 以另一种 variant 运行相同的 serialization code，报告它引用的其他 `UnityEngine.Objects`。Unity 检查所有被引用的 `UnityEngine.Objects`，确定它们是否属于 Unity 正在实例化的数据。如果 reference 指向外部 object（例如 Texture），Unity 保持该 reference 不变。如果 reference 指向内部 object（例如 child GameObject），Unity 会将 reference 修补为对应的副本。

## 卸载未使用的 Assets

`EditorUtility.UnloadUnusedAssetsImmediate` 是 native Unity garbage collector，其用途不同于标准 C# garbage collector。它在加载 scene 后运行，检查不再被引用的 objects（例如 Textures），并安全地卸载它们。Native Unity garbage collector 会以一种 variant 运行 serializer，让 objects 报告它们对外部 `UnityEngine.Objects` 的所有 references。这就是某个 scene 使用的 Textures 会在下一个 scene 中被 garbage collector 卸载的原因。

## Editor 与 runtime serialization 的差异

大多数 serialization 发生在 Editor，而 runtime 主要进行 deserialization。Unity 只在 Editor 中序列化某些 features，而其他 features 在 Editor 和 runtime 中都可以序列化：

| Feature | Editor | Runtime |
| --- | --- | --- |
| **Assets in Binary Format** | 支持读/写 | 支持读 |
| **Assets in YAML format** | 支持读/写 | 不支持 |
| **Saving scenes, prefabs and other assets** | 支持，除非处于 Play mode | 不支持 |
| **使用 `JsonUtility` 序列化 individual objects** | `JsonUtility` 支持读/写；`EditorJsonUtility` 支持 additional object types | `JsonUtility` 支持读/写 |
| [`SerializeReference`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SerializeReference.html) | 支持 | 支持 |
| [`ISerializationCallbackReceiver`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ISerializationCallbackReceiver.html) | 支持 | 支持 |
| [`FormerlySerializedAs`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Serialization.FormerlySerializedAsAttribute.html) | 支持 | 不支持 |

当你在 `UNITY_EDITOR` [scripting symbol](https://docs.unity3d.com/6000.7/Documentation/Manual/platform-dependent-compilation.html) 中声明 fields 时，objects 可以拥有仅由 Editor 序列化的 additional fields：

```csharp
public class SerializeRules : MonoBehaviour
{
#if UNITY_EDITOR
public int m_intEditorOnly;
#endif
}
```

在前面的示例中，`m_intEditorOnly` field 只在 Editor 中序列化，不会包含在 build 中。这让你可以从 build 中省略只在 Editor 中需要的数据，从而节省 memory。任何使用该 field 的 code 也必须进行 conditional compilation，例如放在 `#if UNITY_EDITOR` blocks 中，使 class 能在 build time 编译。

Editor 不支持带有 Unity 只在 runtime 序列化的 fields 的 objects（例如在 `UNITY_STANDALONE` directive 中声明 fields 的情况）。

## 其他资源

- [[01-序列化规则]]
- [[06-JSON序列化]]
- [[03-序列化最佳实践]]

---

## 文档导航

- 上一页：[[01-序列化规则]]
- 目录：[[00-脚本序列化]]
- 下一页：[[03-序列化最佳实践]]
