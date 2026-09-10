# Analyzer 范围和规则集文件

> 原文：[Analyzer scope and rule set files](https://docs.unity3d.com/6000.7/Documentation/Manual/analyzer-scope-and-diagnostics.html)

默认情况下，位于 `Assets` 文件夹根目录中的 Analyzer 会应用于项目中的所有[预定义程序集](https://docs.unity3d.com/6000.7/Documentation/Manual/script-compile-order-folders.html)。也就是说，它会分析 `Assets` 文件夹或其子文件夹中的脚本，但这些脚本不能属于使用 [Assembly Definition 文件](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definitions-creating.html) 定义的自定义程序集。

如果 Analyzer 位于包含 Assembly Definition 文件的文件夹或其子文件夹中，它只会应用于该程序集，以及引用该程序集的其他程序集。

例如，Package 可以借助 Assembly Definition 提供只分析与该 Package 相关代码的 Analyzer，从而帮助 Package 用户正确使用 Package API。

## 规则集文件

你可以使用 `.ruleset` 文件，进一步自定义代码 Analyzer 的诊断信息在不同程序集中的应用方式。规则集允许你按程序集配置 Analyzer 规则的解释方式。例如，你可以将某个程序集中的 Warning 提升为 Error。有关如何创建自定义规则集的更多信息，请参阅 Microsoft Visual Studio 文档中的[创建自定义规则集](https://docs.microsoft.com/en-us/visualstudio/code-quality/how-to-create-a-custom-rule-set?view=vs-2019)。

### 默认规则集

你可以在 `Assets` 根目录中创建名为 `Default.ruleset` 的规则集文件。`Default.ruleset` 中定义的规则会应用于所有预定义程序集，以及使用 Assembly Definition 文件构建的所有程序集。

#### 覆盖默认规则集

你可以为特定程序集创建额外的规则集文件，以覆盖默认规则集。

要覆盖预定义程序集在 `Default.ruleset` 中的规则，请在 `Assets` 文件夹根目录中创建 `.ruleset` 文件，并使用 `[PredefinedAssemblyName].ruleset` 的命名格式。例如，`Assembly-CSharp.ruleset` 中的规则会应用于 `Assembly-CSharp.dll` 中的代码。

`Assets` 文件夹根目录中只允许使用以下 `.ruleset` 文件：

- `Default.ruleset`
- `Assembly-CSharp.ruleset`
- `Assembly-CSharp-firstpass.ruleset`
- `Assembly-CSharp-Editor.ruleset`
- `Assembly-CSharp-Editor-firstpass.ruleset`

要覆盖使用 `.asmdef` 文件定义的自定义程序集在 `Default.ruleset` 中的规则，请创建专用规则集文件，并将它放在 `.asmdef` 文件旁边。例如，`Assets/Scripts/Runtime/MyRuntimeAssembly.ruleset` 可以包含用于覆盖 `Assets/Scripts/Runtime/MyRuntimeAssembly.asmdef` 所代表程序集的规则集。

> [!NOTE]
> 自定义程序集的 `.ruleset` 文件名不必与程序集名称相同。

### 规则集范围和最佳实践

除非存在覆盖它的自定义程序集规则集，否则 `Default.ruleset` 会应用于项目中的所有程序集，包括预定义程序集和自定义程序集。`Default.ruleset` 是唯一一个可以应用于多个程序集的单一规则集文件。

任何其他自定义 `.ruleset` 文件都与程序集建立一对一关系。自定义 `.ruleset` 文件必须放在它所应用程序集的 Assembly Definition（`.asmdef`）文件旁边。

如果希望规则集应用于项目中的全部或大多数程序集，请将主要规则集定义在 `Default.ruleset` 中，并创建额外的 `.ruleset` 文件，将其他程序集排除在该规则集之外。

如果希望规则集只应用于少数程序集，请将规则集复制到每个目标程序集旁边。

### 工作流：在 Unity 中测试规则集文件

要在 Unity 中测试规则集文件，请执行以下步骤。

#### 步骤 1：设置规则集文件

1. 在项目的 `Assets` 文件夹中创建名为 `Subfolder` 的子文件夹。
2. 在 `Subfolder` 中：
   1. 创建一个新的 Assembly Definition（`.asmdef`）文件。
   2. 从[安装和使用现有 Analyzer 或 Source Generator](01-安装现有分析器或源生成器.md)页面复制一份 `RethrowError.cs`。
3. 在 `Assets` 中创建 `Default.ruleset` 文件，并写入以下代码：

```xml
<?xml version="1.0" encoding="utf-8"?>
<RuleSet Name="New Rule Set" Description=" " ToolsVersion="10.0">
  <Rules AnalyzerId="ErrorProne.NET.CodeAnalyzers" RuleNamespace="ErrorProne.NET.CodeAnalyzers">
    <Rule Id="ERP021" Action="Error" />
  <Rule Id="EPC12" Action="None" />
  </Rules>
</RuleSet>
```

`Default.ruleset` 文件定义了以下规则：

- 禁止 `EPC12`，即关于可疑异常处理的 Warning。
- 将 `ERP021`（关于错误异常传播的 Warning）提升为 Error。

#### 步骤 2：重新加载项目

将规则集文件添加到项目后，重新导入属于目标程序集的任意脚本。这会强制 Unity 使用新的规则集文件重新编译该程序集。重新编译后，Console 窗口中会出现两条消息：

```text
Assets\Subfolder\RethrowError.cs(15,19): error ERP021: Incorrect exception propagation. Use throw; instead.
```

```text
Assets\RethrowError.cs(15,19): error ERP021: Incorrect exception propagation. Use throw; instead.
```

注意，Unity 会将 `Default.ruleset` 中定义的规则同时应用于 `Assets/RethrowError.cs` 和 `Assets/Subfolder/RethrowError.cs`。

#### 步骤 3：添加自定义规则集

在 `Assets/Subfolder` 中创建一个 `.ruleset` 文件，并为它指定任意名称。本例使用 `Hello.ruleset`：

```xml
<?xml version="1.0" encoding="utf-8"?>
<RuleSet Name="New Rule Set" Description=" " ToolsVersion="10.0">
  <Rules AnalyzerId="ErrorProne.NET.CodeAnalyzers" RuleNamespace="ErrorProne.NET.CodeAnalyzers">
    <Rule Id="ERP021" Action="Info" />
    <Rule Id="EPC12" Action="Info" />
  </Rules>
</RuleSet>
```

新的 `Hello.ruleset` 文件会告诉 Unity 将 `EPC12` 和 `ERP021` 都以 Info 输出到 Console，而不是将它们当作 Warning 或 Error。

Unity 再次编译项目后，Console 窗口中会出现以下消息：

```text
Assets\Subfolder\RethrowError.cs(14,23): info EPC12: Suspicious exception handling: only e.Message is observed in exception block.
```

```text
Assets\Subfolder\RethrowError.cs(15,19): info ERP021: Incorrect exception propagation. Use throw; instead.
```

```text
Assets\RethrowError.cs(15,19): error ERP021: Incorrect exception propagation. Use throw; instead.
```

`Default.ruleset` 中的规则仍会应用于 `Assets/RethrowError.cs`，但不再应用于 `Assets/Subfolder/RethrowError.cs`，因为 `Hello.ruleset` 中的规则覆盖了它们。

有关所有允许的规则集 Action 文件的更多信息，请参阅 Visual Studio 文档中的[使用代码分析规则集编辑器](https://docs.microsoft.com/en-us/visualstudio/code-quality/working-in-the-code-analysis-rule-set-editor?view=vs-2019)。

### 规则集文件的替代方案

如果你控制 Analyzer 代码，可以让 Analyzer 根据特定位置或程序集采用不同的行为。例如，你可以让 Analyzer 在分析 `Assets/ThirdParty` 下的任何代码时直接返回，以防止它分析第三方代码。

例如，下面的代码片段演示了如何修改[创建和使用 Roslyn Analyzer](02-创建和使用Roslyn分析器.md)中创建的示例 Analyzer：当待分析代码位于 `Assets/ThirdParty` 或 `Assets/Legacy` 路径下时提前返回。

```csharp
private static void AnalyzeInvocation(SyntaxNodeAnalysisContext context)
{
    var invocation = (InvocationExpressionSyntax)context.Node;

    if (!(invocation.Expression is MemberAccessExpressionSyntax memberAccess))
        return;

    // Match calls where the method name is "Log"
    if (memberAccess.Name.Identifier.Text != "Log")
        return;

    // Verify the symbol belongs to UnityEngine.Debug
    var symbolInfo = context.SemanticModel.GetSymbolInfo(memberAccess);
    if (!(symbolInfo.Symbol is IMethodSymbol methodSymbol))
        return;

    var containingType = methodSymbol.ContainingType;
    if (containingType?.ToDisplayString() != "UnityEngine.Debug")
        return;

    // Early out for exempt folders
    var location = invocation.GetLocation();
    var tree = location.SourceTree;
    if (tree == null)
        return;

    var filePath = tree.FilePath ?? string.Empty;

    if (IsInExemptPath(filePath))
        return;

    var diagnostic = Diagnostic.Create(Rule, memberAccess.GetLocation());
    context.ReportDiagnostic(diagnostic);
}

private static bool IsInExemptPath(string filePath)
{
    if (string.IsNullOrEmpty(filePath))
        return false;

    var normalized = filePath.Replace('\\', '/');

    return normalized.IndexOf("/Assets/Legacy/", System.StringComparison.OrdinalIgnoreCase) >= 0
        || normalized.IndexOf("/Assets/ThirdParty/", System.StringComparison.OrdinalIgnoreCase) >= 0;
}
```

你也可以使用 `.editorconfig` 文件集中管理排除项。例如，项目根目录中的以下 `.editorconfig` 会将[创建和使用 Roslyn Analyzer](02-创建和使用Roslyn分析器.md)示例创建的 `EX0001` Warning 调整为 Error：

```editorconfig
root = true

[*.cs]
# Set EX0001 to error
dotnet_diagnostic.EX0001.severity = error
```

## 其他资源

- [特殊文件夹和脚本编译顺序](https://docs.unity3d.com/6000.7/Documentation/Manual/script-compile-order-folders.html)
- [将脚本组织到程序集](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-files.html)


---

## 文档导航

- 上一页：[[03-创建和使用Source Generator]]
- 目录：[[00-Roslyn分析器和源生成器]]
- 下一页：[[05-Roslyn Analyzer和Source Generator的Additional Files]]
