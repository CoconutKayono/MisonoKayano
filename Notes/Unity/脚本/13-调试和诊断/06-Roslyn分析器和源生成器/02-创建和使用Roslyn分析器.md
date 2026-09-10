# 创建和使用 Roslyn Analyzer

> 原文：[Create and use a Roslyn analyzer](https://docs.unity3d.com/6000.7/Documentation/Manual/create-roslyn-analyzer.html)

你可以使用代码分析器检查代码中的错误、规则违规和代码风格问题。与源代码生成器一样，你可以使用现有的分析器，也可以创建自己的分析器。

要在 IDE 中创建 Roslyn Analyzer，然后将它应用于 Unity 项目，请执行以下操作：

1. 在 IDE 中创建一个面向 `.NET Standard 2.0` 的 C# 类库项目，并将项目命名为 `ExampleAnalyzer`。

2. 为项目安装 `Microsoft.CodeAnalysis.Csharp` NuGet Package。要与 Unity 配合使用，你的分析器必须使用 [Microsoft.CodeAnalysis.Csharp 4.3](https://www.nuget.org/packages/Microsoft.CodeAnalysis.CSharp/4.3.0)。

3. 在 IDE 项目中创建一个新的 C# 文件，并添加以下代码：

```csharp
using System.Collections.Immutable;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Diagnostics;

namespace ExampleAnalyzer
{
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public class DebugLogAnalyzer : DiagnosticAnalyzer
{
    public const string DiagnosticId = "EX0001";

    private static readonly LocalizableString Title =
        "Avoid using Debug.Log";

    private static readonly LocalizableString MessageFormat =
        "Debug.Log call detected - consider removing it before shipping";

    private static readonly LocalizableString Description =
        "Debug.Log calls can impact performance and clutter the console in production builds.";

    private const string Category = "Usage";

    private static readonly DiagnosticDescriptor Rule = new DiagnosticDescriptor(
        DiagnosticId,
        Title,
        MessageFormat,
        Category,
        DiagnosticSeverity.Warning,
        isEnabledByDefault: true,
        description: Description);

    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics =>
        ImmutableArray.Create(Rule);

    public override void Initialize(AnalysisContext context)
    {
        context.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);
        context.EnableConcurrentExecution();
        context.RegisterSyntaxNodeAction(AnalyzeInvocation, SyntaxKind.InvocationExpression);
    }

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

        var diagnostic = Diagnostic.Create(Rule, memberAccess.GetLocation());
        context.ReportDiagnostic(diagnostic);
    }
}
   }
```

4. 使用 **release** 构建配置构建分析器。

5. 在分析器的项目文件夹中，找到 `bin/Release/netstandard2.0/ExampleAnalyzer.dll` 文件。

6. 将此文件复制到 Unity 项目的 `Assets` 文件夹中。

7. 在 **Asset Browser** 中单击 `.dll` 文件，打开 [Plugin Inspector](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-in-inspector.html) 窗口。

8. 在 **Select platforms for plugin** 下，取消选中 **Any Platform**。

9. 在 **Include Platforms** 下，取消选中 **Editor**、**Standalone** 以及其他任何已选中的平台。

10. 在 **Asset Labels** 下，单击标签图标，打开 **Asset Labels** 子菜单。

11. 创建并分配一个名为 **RoslynAnalyzer** 的新标签。具体来说，在 **Asset Labels** 子菜单的文本输入框中输入 `RoslynAnalyzer`，然后按 Enter。该标签必须完全匹配，并且区分大小写。创建后，该标签会一直显示在 **Asset Labels** 子菜单中。你可以单击菜单中的标签名称，将它分配给其他分析器。

要测试分析器是否正常工作，请在 Editor 中[创建一个新的 MonoBehaviour 脚本](https://docs.unity3d.com/6000.7/Documentation/Manual/creating-scripts.html)，并使用以下代码：

```csharp
using UnityEngine;

public class TestScript : MonoBehaviour
{
    void Start()
    {
        Debug.Log("Hello world"); // Should trigger EX0001 warning
    }
}
```

Unity 重新编译脚本后，Console 中会出现以下警告：

```text
TestScript.cs(8,9): warning EX0001: Debug.Log call detected - consider removing it before shipping
```

有关创建 Roslyn Analyzer 的更多信息，请参阅 Microsoft 文档中的 [Tutorial: Write your first analyzer and code fix](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/tutorials/how-to-write-csharp-analyzer-code-fix)。

## 报告分析器诊断信息

要查看分析器和源代码生成器的总执行时间，或查看每个分析器、源代码生成器的相对执行时间，请转到 **Edit > Preferences**（macOS：**Unity > Settings**）> **Editor Diagnostics > Core**，并启用 `EnableDomainReloadTimings`。启用后，相关信息会显示在 Console 窗口中。

## 其他资源

- [安装和使用现有分析器或源代码生成器](https://docs.unity3d.com/6000.7/Documentation/Manual/install-existing-analyzer.html)
- [创建和使用 Source Generator](https://docs.unity3d.com/6000.7/Documentation/Manual/create-source-generator.html)

---

## 文档导航

- 上一页：[[01-安装现有分析器或源生成器]]
- 目录：[[00-Roslyn分析器和源生成器]]
- 下一页：[[03-创建和使用Source Generator]]
