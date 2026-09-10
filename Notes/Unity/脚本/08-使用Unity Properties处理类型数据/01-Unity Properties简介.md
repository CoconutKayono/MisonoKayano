# Unity Properties 简介

> 原文：[Introduction to Unity Properties](https://docs.unity3d.com/6000.7/Documentation/Manual/properties-intro.html)

Unity Properties 是一个系统，允许你在运行时探索和修改 C# 类型的属性。它使用 Visitor 风格的 API，以可预测且可控的方式遍历对象图中的属性。

可以使用 Unity Properties 以通用方式读取或写入 C# 类型，只需进行极少的类型专用处理。这样就能处理自定义的用户定义 C# 类型，例如验证这些类型，或在不同表示形式之间转换它们。

Unity Properties 可以避免或减少对 [reflection](https://learn.microsoft.com/en-us/dotnet/fundamentals/reflection/reflection) 的依赖。Reflection 的速度相对较慢，会分配内存（增加 Garbage Collector 的开销），并且支持范围有限，尤其是在需要使用提前编译（AOT）的平台上使用 [IL2CPP](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-il2cpp.html) 时更加明显。

Unity Properties 适用于以下常见场景：

- 数据验证和处理：
  - 遍历对象图，验证范围、空值和引用，或强制执行约束条件。
  - 计算属性之间的差异、Hash，或检测属性是否发生变化。
- 复制、克隆和应用补丁：
  - 通过访问并复制特定属性，深度复制容器或应用补丁。
- 从创作数据转换为运行时数据：
  - 例如，通过属性遍历将 ScriptableObject 配置数据转换为运行时结构体。

## 基础功能

Unity Properties 框架包含以下基础功能，可以用通用方式处理 C# 类型数据：

- [[02-Property Bag]]：[`IPropertyBag<T>`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IPropertyBag_1.html) 描述类型 `T` 的字段和属性。Unity 会生成 Property Bag，使系统能够枚举类型的属性。
- [[03-Property Visitor]]：实现带有 [`Visit<TContainer, TValue>`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Properties.IPropertyVisitor.Visit.html) 等回调的 Visitor。框架会遍历容器的属性，并针对每个属性调用你的逻辑。
- Adapter：用于自定义特定类型的访问或转换方式的 Hook，例如对 `Vector3`、枚举和集合进行特殊处理。
- [[04-Property Path]]：支持嵌套容器、数组、字典，并支持通过路径访问值，同时可以控制遍历深度和选项。

如需查看将这些功能结合使用的更详细示例，请参阅[[05-使用PropertyVisitor类创建Property Visitor]]和[[06-使用低级API创建Property Visitor]]。

## 其他资源

- [[02-Property Bag]]
- [[03-Property Visitor]]
- [[04-Property Path]]
- [[05-使用PropertyVisitor类创建Property Visitor]]
- [[06-使用低级API创建Property Visitor]]


---

## 文档导航

- 上一页：[[00-使用Unity Properties处理类型数据]]
- 目录：[[00-使用Unity Properties处理类型数据]]
- 下一页：[[02-Property Bag]]
