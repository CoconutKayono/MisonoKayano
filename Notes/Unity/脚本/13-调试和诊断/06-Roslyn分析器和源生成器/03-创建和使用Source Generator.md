# 创建和使用 Source Generator

> 原文：[Create and use a source generator](https://docs.unity3d.com/6000.7/Documentation/Manual/create-source-generator.html)

你可以将 Source Generator 作为脚本编译过程中的附加步骤，在编译现有代码时添加新代码。与代码分析器一样，你可以使用现有的 Source Generator，也可以创建自己的 Source Generator。

> [!NOTE]
> Unity 仅支持 `System.Text.Json` Namespace 的 `6.0.0-preview` 版本。如果希望在应用程序中使用此 Namespace，请确保使用 `6.0.0-preview` 版本。有关 `System.Text.Json` 的更多信息，请参阅 Microsoft 的 [System.Text.Json Namespace documentation](https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-6)。

要在 IDE 中创建 Source Generator，然后将它应用于 Unity 项目，请执行以下操作：

1. 在 IDE 中创建一个面向 `.NET Standard 2.0` 的 C# 类库项目，并将项目命名为 `ExampleSourceGenerator`。

2. 为项目安装 `Microsoft.CodeAnalysis.Csharp` NuGet Package。要与 Unity 配合使用，你的 Source Generator 必须使用 [Microsoft.CodeAnalysis.Csharp 4.3](https://www.nuget.org/packages/Microsoft.CodeAnalysis.CSharp/4.3.0)。

3. 在 IDE 项目中创建一个新的 C# 文件，并添加以下代码：

```csharp
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.Text;
using System.Text;

namespace ExampleSourceGenerator
{
    [Generator]
    public class ExampleSourceGenerator : ISourceGenerator
    {
        public void Execute(GeneratorExecutionContext context)
        {
            System.Console.WriteLine(System.DateTime.Now.ToString());

            var sourceBuilder = new StringBuilder(
            @"
            using System;
            namespace ExampleSourceGenerated
            {
                public static class ExampleSourceGenerated
                {
                    public static string GetTestText()
                    {
                        return ""This is from source generator ");

            sourceBuilder.Append(System.DateTime.Now.ToString());

            sourceBuilder.Append(
                @""";
                    }
    }
}
");

            context.AddSource("exampleSourceGenerator", SourceText.From(sourceBuilder.ToString(), Encoding.UTF8));
        }

        public void Initialize(GeneratorInitializationContext context) { }
    }
}
```

4. 使用 **release** 构建配置构建 Source Generator。

5. 在 Source Generator 的项目文件夹中，找到 `bin/Release/netstandard2.0/ExampleSourceGenerator.dll` 文件。

6. 将此文件复制到 Unity 项目的 `Assets` 文件夹中。

7. 在 **Asset Browser** 中单击 `.dll` 文件，打开 [Plugin Inspector](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-in-inspector.html) 窗口。

8. 在 **Select platforms for plugin** 下，取消选中 **Any Platform**。

9. 在 **Include Platforms** 下，取消选中 **Editor**、**Standalone** 以及其他任何已选中的平台。

10. 在 **Asset Labels** 下，单击标签图标，打开 **Asset Labels** 子菜单。

11. 创建并分配一个名为 **RoslynAnalyzer** 的新标签。具体来说，在 **Asset Labels** 子菜单的文本输入框中输入 `RoslynAnalyzer`，然后按 Enter。该标签必须完全匹配，并且区分大小写。创建后，该标签会一直显示在 **Asset Labels** 子菜单中。你可以单击菜单中的标签名称，将它分配给其他分析器。

要测试 Source Generator 是否正常工作，请在 Editor 中[创建一个新的 MonoBehaviour 脚本](https://docs.unity3d.com/6000.7/Documentation/Manual/creating-scripts.html)，并使用以下代码：

```csharp
using UnityEngine;

public class HelloFromSourceGenerator : MonoBehaviour
{
    static string GetStringFromSourceGenerator()
    {
        return ExampleSourceGenerated.ExampleSourceGenerated.GetTestText();
    }

    // Start is called before the first frame update
    void Start()
    {
        var output = "Test";
        output = GetStringFromSourceGenerator();
        Debug.Log(output);
    }
}
```

如果 Source Generator 被注入到多个程序集，IDE 会显示关于冲突（CS0436）的编译器警告。要移除该警告，可以采取以下任一措施：

- 将 `ExampleSourceGenerator` 示例中的 `ExampleSourceGenerated` 类设为 `internal`。**重要**：在这种情况下，只能从同一个程序集中访问生成的类。
- 修改 `ExampleSourceGenerated` 类的名称，使其对于给定程序集是唯一的，例如 `ExampleSourceGenerated_MyAssembly`。

12. 将此脚本添加到场景中的 GameObject，然后进入 Play mode。Source Generator 会在 Console 窗口中输出一条消息，其中包括时间戳。

有关 Source Generator 的更多信息，请参阅 Microsoft 的 [Source Generators documentation](https://docs.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/source-generators-overview)。

## 其他资源

- [安装和使用现有分析器或源代码生成器](https://docs.unity3d.com/6000.7/Documentation/Manual/install-existing-analyzer.html)

---

## 文档导航

- 上一页：[[02-创建和使用Roslyn分析器]]
- 目录：[[00-Roslyn分析器和源生成器]]
- 下一页：[[04-Analyzer范围和规则集文件]]
