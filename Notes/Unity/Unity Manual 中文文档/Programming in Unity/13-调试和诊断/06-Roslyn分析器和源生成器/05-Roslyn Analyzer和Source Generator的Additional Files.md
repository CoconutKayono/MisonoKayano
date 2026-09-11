# Roslyn Analyzer 和 Source Generator 的 Additional Files

> 原文：[Additional files for Roslyn analyzers and source generators](https://docs.unity3d.com/6000.7/Documentation/Manual/roslyn-analyzers-additional-files.html)

你可以将 [Additional Files](https://github.com/dotnet/roslyn/blob/main/docs/analyzers/Using%20Additional%20Files.md) 添加到项目中，供 Roslyn Analyzer 或 Source Generator 使用。只要文件扩展名为 `.additionalfile`，并且位于 `Assets` 文件夹或其子文件夹中，Unity Editor 就会将它识别为 Roslyn Analyzer 的 Additional File。

## 命名 Additional Files

要让文件传递给编译流程，文件名必须遵循 `Filename.[Analyzer Name].additionalfile` 格式。不包含 `[Analyzer Name]` 部分的文件会被导入，但不会传递给编译流程。

`[Analyzer Name]` 部分区分大小写，并且必须与 Additional File 目标 Analyzer 的名称匹配。`Filename` 部分不能包含句点（`.`）。

<a id="filtering"></a>

## Additional File 过滤

每个已编译程序集都会根据该[程序集定义](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-files.html)正在运行的 Analyzer，接收经过 `[Analyzer Name]` 过滤的 Additional File 列表。例如，假设项目中有以下程序集和 Analyzer：

- Assembly1 使用名为 `Analyzer1` 的 Analyzer。
- Assembly2 使用名为 `Analyzer2` 的 Analyzer。
- Assembly3 同时使用 `Analyzer1` 和 `Analyzer2`。

如果项目包含以下四个 Additional File：`FileA.Analyzer1.additionalfile`、`FileB.Analyzer2.additionalfile`、`FileC.additionalfile` 和 `FileD.Analyzer3.additionalfile`，Unity 会将以下 Additional File 列表传递给相应程序集：

- Assembly1：`FileA.Analyzer1.additionalfile`
- Assembly2：`FileB.Analyzer2.additionalfile`
- Assembly3：`FileA.Analyzer1.additionalfile`、`FileB.Analyzer2.additionalfile`

`FileC` 没有 `[Analyzer Name]` 部分，`FileD` 引用了项目中不存在的 Analyzer，因此 Unity 不会将这两个文件传递给编译流程。

## 从代码中获取可用的 Additional Files

Analyzer 可以从 Analyzer Context 中获取已编译程序集包含的完整 Additional File 列表。该列表包含程序集中的所有 Additional File，而不仅仅是名称与当前 Analyzer 匹配的文件。下面的示例演示了这一点：

```csharp
using System.IO;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace SourceGeneratorTest1;


[Generator]
public class SG2 : ISourceGenerator
{
    public void Execute(GeneratorExecutionContext context)
    {
        var pathOfFileWithTypeName = context.AdditionalFiles.FirstOrDefault(file => file.Path.Contains("GenerateType.SourceGenerator.Test.2.additionalfile"));
        if (pathOfFileWithTypeName == null)
        {
            // no additional file found, do not generate a type.
            return;
        }

        var @namespace = context.Compilation.SyntaxTrees.First().GetRoot().DescendantNodes().OfType<NamespaceDeclarationSyntax>().FirstOrDefault()?.Name?.ToString() ?? "NoNamespace";

        // an additional file has been passed; read the type name from the file.
        string generatedTypeName = File.ReadAllText(pathOfFileWithTypeName.Path);

        context.AddSource(
            "SG2.generated.cs", 
            $$"""
            namespace {{@namespace}}
            {
                public partial class {{generatedTypeName}}
                {
                }
            }
            """);
    }

    public void Initialize(GeneratorInitializationContext context)
    {
    }
}
```

> [!NOTE]
> 本示例只用于演示如何使用 Analyzer Context 检查 Additional Files。可用于生产环境的 Source Generator 需要更全面的代码，以处理错误并确保正确的功能和性能。

在前面的[过滤示例](#filtering)中，`Analyzer1` 和 `Analyzer2` 都可以获取 Assembly3 中名称以它们任意一个名称命名的 Additional File。每个 Analyzer 都负责检查 Additional Files 中是否存在自己可以使用的数据。

你还可以在 Editor 代码中使用 [`ScriptCompilerOptions.RoslynAdditionalFilePaths`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Compilation.ScriptCompilerOptions.RoslynAdditionalFilePaths.html) 属性，获取指定程序集包含的 Additional File 列表。

## 其他资源

- [`ScriptCompilerOptions.RoslynAdditionalFilePaths`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Compilation.ScriptCompilerOptions.RoslynAdditionalFilePaths.html)
- [创建和使用 Source Generator](https://docs.unity3d.com/6000.7/Documentation/Manual/create-source-generator.html)
- [安装和使用现有 Analyzer 或 Source Generator](https://docs.unity3d.com/6000.7/Documentation/Manual/install-existing-analyzer.html)


---

## 文档导航

- 上一页：[[04-Analyzer范围和规则集文件]]
- 目录：[[00-Roslyn分析器和源生成器]]
- 下一页：[[07-Safe Mode]]
