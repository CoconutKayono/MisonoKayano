# 代码分析和源代码生成

> 原文：[Code analysis and source generation](https://docs.unity3d.com/6000.7/Documentation/Manual/roslyn-analyzers.html)

代码分析器会检查源代码，并报告诊断信息，以帮助查找错误或强制执行规则。源代码生成器会在编译期间运行，并创建会成为程序一部分的额外源代码。

在 C#/.NET 生态中，源代码生成器和分析器都建立在同一个 Roslyn 编译器平台上，因此分析器通常称为 Roslyn analyzer。

分析器和源代码生成器都会作为 managed plugin 导入 Unity 项目。你可以编写自己的分析器或源代码生成器，也可以导入现有的第三方库。

## 本目录页面

| 页面 | 说明 |
| --- | --- |
| [[01-安装现有分析器或源生成器]] | 从 NuGet 安装并使用现有的代码分析器或源代码生成器。 |
| [[02-创建和使用Roslyn分析器]] | 创建一个 Roslyn Analyzer，并将其用于 Unity 项目。 |
| [[03-创建和使用Source Generator]] | 创建一个 Source Generator，并将其用于 Unity 项目。 |
| [[04-Analyzer范围和规则集文件]] | 了解 Analyzer 的作用范围以及规则集文件。 |
| [[05-Roslyn Analyzer和Source Generator的Additional Files]] | 为 Roslyn Analyzer 或 Source Generator 提供额外文件。 |

## 其他资源

- [C# 编译器](https://docs.unity3d.com/6000.7/Documentation/Manual/csharp-compiler.html)
- [使用 Roslyn Analyzer 进行调试](https://unity.com/how-to/debugging-with-rosyln-analyzers)

---

## 文档导航

- 上一页：[[05-Stack Trace日志]]
- 目录：[[00-Roslyn分析器和源生成器]]
- 下一页：[[01-安装现有分析器或源生成器]]
