# Unity 的 .NET 功能

> 原文：[Unity .NET features](https://docs.unity3d.com/6000.7/Documentation/Manual/overview-of-dot-net-in-unity.html)

Unity 集成 .NET 平台，使项目可以编写运行在多种硬件和平台上的高性能 C# 代码。具体 API 范围取决于 API Compatibility Level、目标平台和硬件配置。

Unity 对 .NET 的集成包含多个方面：代码可使用的 API 范围、C# Compiler 版本、语言特性，以及不同目标平台和硬件配置下的支持差异。选择的 API Compatibility Level 会影响 Unity 能够针对项目代码进行编译的 .NET API 集合。

使用 .NET API 时，应同时检查 API Compatibility Level、目标平台和构建硬件，而不能只根据 Editor 中能够编译通过来判断 Player 一定支持该 API。

| 页面 | 说明 |
| --- | --- |
| [[01-.NET API兼容级别]] | 选择 Unity 编译项目代码时使用的 .NET API Compatibility Level。 |
| [[02-不兼容的.NET API]] | 了解与 Unity 程序集加载和管理系统不兼容的 .NET API。 |
| [[03-添加.NET Framework类库引用]] | 引用 Unity 默认不会编译的 .NET 类库 API。 |
| [[04-CSharp编译器和语言版本参考]] | 了解 Unity 使用的 C# Compiler 和 Language Version。 |

---

## 其他资源

- [Unity Learn：Scripting](https://unity3d.com/learn/tutorials/topics/scripting)

## 文档导航

- 上一页：[[00-Unity的.NET功能]]
- 目录：[[00-Unity的.NET功能]]
- 下一页：[[01-.NET API兼容级别]]
