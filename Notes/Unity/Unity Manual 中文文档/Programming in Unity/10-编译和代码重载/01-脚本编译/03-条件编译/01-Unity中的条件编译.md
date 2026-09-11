# Unity 中的条件编译

> 原文：[Conditional compilation in Unity](https://docs.unity3d.com/6000.7/Documentation/Manual/platform-dependent-compilation.html)

Unity 对 C# 语言的支持包括使用**指令**。这些指令会根据是否定义了特定的**脚本符号**，选择性地将代码包含在编译中或从编译中排除。有关这些指令在 C# 中的工作方式，请参阅 Microsoft 文档中的 [C# 预处理器指令](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/preprocessor-directives)。

Unity 提供了一系列预定义符号，可以在脚本中使用它们，根据条件选择性地编译或排除代码片段。例如，Windows 独立平台项目构建中定义的符号是 `UNITY_STANDALONE_WIN`。可以使用一种特殊的 `if` 语句检查是否定义了该符号：

```csharp
#if UNITY_STANDALONE_WIN

  Debug.Log("Standalone Windows");

#endif
```

`#if` 和 `#endif` 前面的井号（`#`）表示这些语句是编译过程中处理的指令，而不是运行时处理的语句。在上一个示例中，只有在项目的 Windows 独立平台构建中，`Debug` 行才会参与编译。在 Unity Editor 或其他目标构建中，该行会被完全省略。这与使用普通的 [if 语句](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/selection-statements) 不同；普通 `if` 语句可能只是在运行时跳过某些代码片段的执行。

可以使用 `#elif` 和 `#else` 指令检查多个条件：

```csharp
#if UNITY_EDITOR

    Debug.Log("Unity Editor");

#elif UNITY_IOS

    Debug.Log("Unity iOS");

#else

    Debug.Log("Any other platform");

#endif
```

有许多预定义符号，可以根据所选的[[03-Unity脚本符号参考#平台符号|平台]]、[[03-Unity脚本符号参考#Unity Editor 版本符号|Editor 版本]]以及[[03-Unity脚本符号参考#其他符号|其他]]系统环境场景，选择性地编译或省略代码。Unity 预定义符号的完整列表请参阅[[03-Unity脚本符号参考]]。

也可以通过 Editor、脚本或资源文件定义自己的脚本符号。有关更多信息，请参阅[[02-自定义脚本符号]]。

> **注意：** **脚本符号**也称为定义符号、预处理器定义，或简称为定义。

## 指令的替代方案

预处理器指令并不总是条件性包含或排除代码的最合适或最可靠方式。以下列出了替代方法。

### `Conditional` 特性

可以使用 C# 的 `Conditional` 特性。它是移除函数时更简洁且不易出错的方式。有关更多信息，请参阅 [ConditionalAttribute 类](https://msdn.microsoft.com/en-us/library/system.diagnostics.conditionalattribute(v=vs.110).aspx)。常见的 Unity 回调（例如 `Start()`、`Update()`、`LateUpdate()`、`FixedUpdate()` 和 `Awake()`）不受此特性影响，因为它们由引擎直接调用；出于性能原因，引擎不会将此特性应用于这些回调。

### 程序集定义约束

高层级条件编译的推荐方式，是将脚本组织到带有相应[程序集定义文件](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-files.html)的程序集中。如果要有条件地包含或排除的代码位于某个程序集中，可以在程序集定义上配置 [Define Constraints](https://docs.unity3d.com/6000.7/Documentation/Manual/class-AssemblyDefinitionImporter.html#define-constraints)，例如仅当项目中存在指定版本的包时才编译该代码。

<a name="ConditionalExecution"></a>

### 条件执行

不要使用条件编译，而是可以使用标准的 `if` 语句，对已编译的代码执行条件控制。例如，Unity 的 `UNITY_64` 脚本符号并不能可靠地测试 64 位架构，因此更适合使用以下代码：

```csharp
if (IntPtr.Size == 4)
{
    // 32 bit code
}
else
{
    // 64-bit code
}
```

## 其他资源

- [如何在 Unity 中创建和使用脚本](https://docs.unity3d.com/6000.7/Documentation/Manual/creating-scripts.html)
- [[03-Unity脚本符号参考]]
- [[04-测试条件编译]]
- [[02-自定义脚本符号]]


---

## 文档导航

- 上一页：[[00-条件编译]]
- 目录：[[00-条件编译]]
- 下一页：[[03-Unity脚本符号参考]]
