# JSON 序列化

> 原文：[JSON Serialization](https://docs.unity3d.com/6000.7/Documentation/Manual/json-serialization.html)

使用 `JsonUtility` class，可以在 Unity 对象与 JSON 格式之间转换。例如，可以使用 JSON Serialization 与 web service 交互，或轻松地将数据打包和解包为文本格式。

JSON Serialization 使用“structured JSON”的概念：创建一个 class 或 structure，描述希望存储在 JSON 数据中的变量。例如：

```csharp
[Serializable]
public class MyClass
{
    public int level;
    public float timeElapsed;
    public string playerName;
}
```

这定义了一个包含三个变量（`level`、`timeElapsed` 和 `playerName`）的普通 C# class，并用 `Serializable` attribute 标记它，使其能够与 JSON serializer 一起使用。可以按如下方式创建 class 的实例：

```csharp
MyClass myObject = new MyClass();
myObject.level = 1;
myObject.timeElapsed = 47.5f;
myObject.playerName = "Dr Charles Francis";
```

然后使用 `JsonUtility.ToJson` 方法将其序列化（转换）为 JSON 格式：

```csharp
string json = JsonUtility.ToJson(myObject);
// json now contains: '{"level":1,"timeElapsed":47.5,"playerName":"Dr Charles Francis"}'
```

要将 JSON 转换回对象，请使用 `JsonUtility.FromJson`：

```csharp
myObject = JsonUtility.FromJson<MyClass>(json);
```

这会创建 `MyClass` 的新实例，并使用 JSON 数据设置其值。如果 JSON 数据包含无法映射到 `MyClass` 字段的值，serializer 会忽略这些值。如果 JSON 数据缺少 `MyClass` 中的字段值，serializer 会让返回对象中这些字段保留构造后的值。

## 使用 JSON 覆盖对象

也可以在已有对象上反序列化 JSON 数据，从而覆盖已有数据：

```csharp
JsonUtility.FromJsonOverwrite(json, myObject);
```

如果 JSON 数据不包含某字段的值，serializer 不会改变该字段的值。此方法可以通过复用之前创建的对象，将 allocation 降到最低；也可以用只包含少量字段的 JSON 有意地“patch”对象。

**警告**：JSON Serializer API 支持 `MonoBehaviour` 和 `ScriptableObject` 子类，以及普通 struct 和 class。但是，将 JSON 反序列化到 `MonoBehaviour` 或 `ScriptableObject` 子类时，必须使用 `FromJsonOverwrite`。如果尝试使用 `FromJson`，Unity 会抛出 exception，因为不支持这种行为。

## 支持的类型

JSON Serializer API 支持任意 `MonoBehaviour` 子类、`ScriptableObject` 子类，或带有 `[Serializable]` attribute 的普通 class 或 struct。将对象传给标准 Unity serializer 处理时，Inspector 中相同的规则和限制也同样适用：Unity 只序列化字段，不序列化属性。

Unity 不支持直接将其他类型（例如基础类型或 array）传给该 API。如果需要转换这些类型，请将其包装在某种 class 或 struct 中。

仅在 Editor 中还有一个并行 API `EditorJsonUtility`，它允许对任何继承自 `UnityEngine.Object` 的对象进行 JSON 序列化和反序列化。生成的 JSON 包含与该对象 YAML 表示相同的数据。

`JsonUtility` 和 `EditorJsonUtility` 是使用 Unity serialization rules 将 Object 序列化为 JSON string，以及从 JSON string 反序列化回 Object 的 utility class。如果需要通过代码操作 JSON，或序列化 Unity serialization 不支持的数据结构，可以将通用 .NET JSON library 作为 `JsonUtility` API 的 companion 使用。

## 性能

Benchmark 测试表明，尽管 `JsonUtility` 在某些情况下功能较少，但它明显快于流行的 .NET JSON 解决方案。

Garbage collection（GC）的内存使用量最低：

- `ToJson` 只为返回的 string 分配 GC memory；
- `FromJson` 只为返回对象以及所需的子对象分配 GC memory（例如，反序列化包含 array 的对象时，Unity 会为该 array 分配 GC memory）；
- `FromJsonOverwrite` 只在必要时为被写入的字段分配 GC memory（例如 string 和 array）。这意味着，如果 JSON 覆盖的所有字段都是 value-typed，Unity 完全不会分配 GC memory。

可以从 background thread 使用 `JsonUtility` API。但和其他 multithreaded code 一样，要注意不要在一个线程序列化或反序列化对象的同时，从另一个线程访问或修改该对象。

## 控制 `ToJson()` 的输出

`ToJson` 方法支持对 JSON 输出进行 pretty-print。默认关闭，但将 `true` 作为第二个参数传入即可开启。

使用 `[NonSerialized]` attribute 可以从输出中省略字段。

## 使用 `FromJson()` 处理未知类型

如果事先不知道对象的 type，可以将 JSON 反序列化到包含“公共”字段的 class 或 struct 中，再用这些字段的值确定实际要使用的 type。然后再次将 JSON 反序列化为该 type。

---

## 文档导航

- 上一页：[[05-自定义序列化]]
- 目录：[[00-脚本序列化]]
- 下一页：[[07-序列化规则分析器参考]]
﻿# JSON 序列化

> 原文：[JSON Serialization](https://docs.unity3d.com/6000.7/Documentation/Manual/json-serialization.html)

使用 [JsonUtility](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.html) class，将 Unity objects 转换为 [JSON](http://www.json.org) format，或从 JSON format 转换回来。例如，可以使用 JSON Serialization 与 web services 交互，或轻松地将 data pack 和 unpack 为 text-based format。

JSON Serialization 使用一种“structured” JSON：创建一个 class 或 structure，描述希望存储在 JSON data 中的 variables。例如：

```csharp
[Serializable]
public class MyClass
{
    public int level;
    public float timeElapsed;
    public string playerName;
}
```

这定义了一个包含三个 variables（**level**、**timeElapsed** 和 **playerName**）的 plain C# class，并使用 `Serializable` attribute 标记它，使其可以与 JSON serializer 一起使用。要创建该 class 的 instance，可以使用类似以下的 code：

```csharp
MyClass myObject = new MyClass();
myObject.level = 1;
myObject.timeElapsed = 47.5f;
myObject.playerName = "Dr Charles Francis";
```

然后使用 [`JsonUtility.ToJson`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.ToJson.html) method 对其进行 serialization（转换为 JSON format）：

```csharp
string json = JsonUtility.ToJson(myObject);
// json now contains: '{"level":1,"timeElapsed":47.5,"playerName":"Dr Charles Francis"}'
```

要将 JSON 转换回 object，请使用 [`JsonUtility.FromJson`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.FromJson.html)：

```csharp
myObject = JsonUtility.FromJson<MyClass>(json);
```

这会创建一个新的 `MyClass` instance，并使用 JSON data 设置其 values。如果 JSON data 包含无法映射到 `MyClass` fields 的 values，serializer 会忽略这些 values。如果 JSON data 缺少 `MyClass` fields 的 values，serializer 会让 returned object 保留这些 fields 的 constructed values。

## 用 JSON 覆盖 objects

也可以在现有 object 上反序列化 JSON data，从而覆盖任何 existing data：

```csharp
JsonUtility.FromJsonOverwrite(json, myObject);
```

如果 JSON data 不包含某个 field 的 value，serializer 不会改变该 field 的 value。此 method 通过复用之前创建的 objects，可以将 allocations 保持在最低限度。它还允许你用只包含少量 fields 的 JSON 有意地“patch” objects。

**警告：** JSON Serializer API 支持 [`MonoBehaviour`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html) 和 [`ScriptableObject`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html) subclasses，以及 plain structs 和 classes。但是，当将 JSON 反序列化到 `MonoBehaviour` 或 `ScriptableObject` subclasses 时，必须使用 [`FromJsonOverwrite`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.FromJsonOverwrite.html) method。如果尝试使用 [`FromJson`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.FromJson.html)，Unity 会抛出 exception，因为不支持此行为。

## 支持的 types

JSON Serializer API 支持任意 `MonoBehaviour` subclass、`ScriptableObject` subclass，或带 `[Serializable]` attribute 的 plain class 或 struct。当将 object 传给标准 Unity serializer 处理时，使用与 Inspector 中相同的 rules 和 limitations：Unity 只序列化 fields，不序列化 properties。

Unity 不支持直接向 API 传入其他 types，例如 primitive types 或 arrays。如果需要转换这些 types，请将它们包装在某种 `class` 或 `struct` 中。

仅在 Editor 中存在一个 parallel API [`EditorJsonUtility`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/EditorJsonUtility.html)，允许将派生自 [`UnityEngine.Object`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.html) 的任何 object 序列化为 JSON，或从 JSON 反序列化。它产生的 JSON 包含与 object 的 YAML representation 相同的 data。

[`JsonUtility`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.html) 和 [`EditorJsonUtility`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/EditorJsonUtility.html) 是使用 [[01-序列化规则|Unity serialization rules]] 将 Objects 序列化为 JSON string format 或从中反序列化的 utility classes。如果需要通过 code 操作 JSON data，或序列化 Unity serialization 不支持的 data structures，可以使用 general-purpose .NET JSON library 作为 JsonUtility API 的 companion。

## Performance

Benchmark tests 表明，尽管 [`JsonUtility`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.html) 在某些情况下提供的 features 较少，但它明显快于常见的 .NET JSON solutions。

Garbage collection（GC）的 memory usage 最低：

- [`ToJson`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.ToJson.html) 只为 returned string 分配 GC memory。
- [`FromJson`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.FromJson.html) 只为 returned object 以及所需的 subobjects 分配 GC memory（例如，反序列化包含 array 的 object 时，Unity 会为 array 分配 GC memory）。
- [`FromJsonOverwrite`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.FromJsonOverwrite.html) 只在 written fields 需要时分配 GC memory（例如 strings 和 arrays）。这意味着，如果 JSON 覆盖的所有 fields 都是 value-typed，Unity 完全不会分配 GC memory。

可以从 background thread 使用 JsonUtility API。不过，与任何 multithreaded code 一样，要小心不要在一个 thread 序列化或反序列化 object 的同时，从另一个 thread 访问或修改该 object。

## 控制 `ToJson()` 的 output

[`ToJson`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/JsonUtility.ToJson.html) method 支持对 JSON output 进行 pretty-printing。默认关闭，但可以将 `true` 作为第二个 parameter 传入来开启。

可以使用 `[NonSerialized]` attribute 从 output 中省略 fields。

## 将 `FromJson()` 与 unknown types 一起使用

如果事先不知道 object 的 type，可以将 JSON 反序列化到包含“common” fields 的 class 或 struct 中，然后使用这些 fields 的 values 判断实际需要的 type。之后再将 JSON 第二次反序列化到该 type 中。

---

## 文档导航

- 上一页：[[05-自定义序列化]]
- 目录：[[00-脚本序列化]]
- 下一页：[[07-序列化规则分析器参考]]
