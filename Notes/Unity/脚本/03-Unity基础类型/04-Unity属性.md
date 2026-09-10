# Unity Attribute

> 原文：[Unity attributes](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-attributes.html)

Attribute 是放置在类、属性或方法声明上方的 C# 元数据标记，用来指示特殊行为。

.NET 类库中定义了许多 Attribute，Unity 也提供了许多自定义的 Unity 专用 Attribute。例如，可以在属性声明上方添加 `HideInInspector` Attribute，即使属性是 public，也可以阻止 Inspector 显示它。Attribute 使用方括号写在声明上方：

```csharp
[HideInInspector]
public float strength;
```

完整的 `UnityEngine` Attribute 列表，请参阅 Scripting API 中 **UnityEngine > Attributes** 下的列表，该列表从 `AddComponentMenu` 开始。

完整的 `UnityEditor` Attribute 列表，请参阅 Scripting API 中 **UnityEditor > Attributes** 下的列表，该列表从 `AssetPostprocessorStaticVariableIgnoreAttribute` 开始。

> [!NOTE]
> 不要使用 .NET 的 `ThreadStatic` Attribute，因为将它添加到 Unity 脚本后会导致崩溃。

## 其他资源

- Unity Learn：[Attributes](https://learn.unity.com/tutorial/attributes)
- [[../01-开始使用Unity编程/04-检查脚本]]
- [[../10-编译和代码重载/06-脚本序列化/01-序列化规则]]

---

## 文档导航

- 上一页：[[03-ScriptableObject类]]
- 目录：[[00-Unity基础类型]]
- 下一页：[[05-从InstanceID迁移到EntityId]]
