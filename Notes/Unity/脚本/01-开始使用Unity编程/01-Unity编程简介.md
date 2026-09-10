# Unity 编程简介

> 原文：[Introduction to programming in Unity](https://docs.unity3d.com/6000.7/Documentation/Manual/intro-to-scripting.html)

Unity 的设计具有可定制和可扩展性，几乎所有功能在一定程度上都可以通过脚本控制。你可以在各种 Editor 窗口中配置许多项目内容，而这些内容通常都有对应的公共 C# 类表示，可以在代码中访问。

你可以使用 Editor API 定制和扩展 Editor 创作工具，改善开发工作流；也可以使用 Engine API 定义应用程序的运行时功能，包括图形、物理、角色行为和对用户输入的响应。

Scripting API 参考提供了所有公共 Unity API 的完整、权威说明。Unity Manual 则提供额外的背景知识和使用指导。

## Unity 的脚本环境

Unity 支持使用 C# 编程语言编写脚本。C#（读作 C-sharp）是一种托管的面向对象语言，属于 .NET 平台，并运行在跨平台的 .NET Runtime 上。如果其他 .NET 语言能够编译为兼容的 DLL，也可以与 Unity 一起使用；相关信息请参阅 [[../10-编译和代码重载/05-集成第三方代码库/02-Managed Plug-in]]。

“脚本环境”包含两部分：

- 你自己的本地编程环境，包括代码编辑器（IDE）、集成的源代码管理方案和操作系统。
- Unity 提供的 C# 脚本环境。Unity 的特定版本支持特定版本的 .NET 平台，这决定了代码可以使用哪些 .NET 类库。

关于脚本环境和相关工具的更多信息，请参阅 [[../02-环境与工具/00-环境与工具]]。

## Unity 中的脚本工作方式

C# 脚本是扩展名为 `.cs` 的文件，也是项目中的 Asset。它们存储在 `Assets` 文件夹中，并作为 Asset Database 的一部分保存。你可以通过 **Assets > Create > Scripting** 子菜单创建继承常用 Unity 内置类型的模板脚本。

Unity 会配置一个默认的 External Script Editor，用于打开脚本 Asset 进行编辑。通常应选择 Unity 支持的 IDE 之一。

只要代码兼容当前启用的 .NET 配置文件，你就可以创建普通的 C# 类型和逻辑，用于游戏中的各种功能。但如果自定义类型继承 Unity 内置类型，它们会在 Unity 中获得额外功能：

- 继承 `UnityEngine.Object` 的类型可以赋值给 Inspector 窗口中的字段。
- 继承 `MonoBehaviour` 后，脚本可以作为 Component 附加到 `GameObject`，控制 Scene 中 `GameObject` 的行为。

关于可以继承的 Unity 基础类型，请参阅 [[../03-Unity基础类型/00-Unity基础类型]]。关于在 Inspector 中查看和编辑脚本 Component，请参阅 [[04-检查脚本]]。

## Editor 脚本与 Runtime 脚本

代码可能运行在两种不同的环境中：

- 在创作阶段的 Unity Editor 中，通常用于支持开发流程的自定义编辑工具和窗口。
- 在应用程序 Runtime 中，作为用户体验的一部分运行。

只包含 Editor 专用代码的源文件通常称为 Editor 脚本。可以将它们放入名为 `Editor` 的文件夹，或使用程序集定义文件创建仅限 Editor 的程序集，从而将其排除在 Player 构建之外。关于 `Editor` 文件夹，请参阅 [[../10-编译和代码重载/01-脚本编译/03-条件编译/01-Unity中的条件编译]]。

也可以使用 `#if UNITY_EDITOR` 预处理器指令，将部分代码设置为仅在 Editor 中进行条件编译。关于此功能，请参阅 [[../10-编译和代码重载/01-脚本编译/03-条件编译/00-条件编译]]。

Unity 的大多数核心公共 API 位于 `UnityEditor` 或 `UnityEngine` Namespace 中。`UnityEditor` Namespace 中的 API 只能在 Editor 中使用；在 Runtime 代码中尝试使用它们会导致编译错误。

在 Editor 中工作时，有些代码可能需要同时在 Edit Mode 和 Play Mode 中运行。例如，你可以在 Play Mode 中调用部分 `UnityEditor` API，用于测试、可视化或触发 Asset 操作；也可以通过在代码中使用 `[ExecuteInEditMode]` 或 `[ExecuteAlways]` Attribute，让部分 `UnityEngine` API 在 Edit Mode 中运行。

无论如何，都必须确保将 Editor 脚本以及使用 `UnityEditor` API 的代码排除在 Runtime Player 构建之外。

## 编译与代码重载

编译会把你编写的 C# 代码转换为能在指定目标平台上运行的代码。编译的某些方面由你控制，另一些则不由你控制。将脚本组织到不同程序集可以减少不必要的重新编译，并帮助管理依赖关系。使用条件编译则可以选择性地将代码片段包含在编译结果中，或将其排除。

根据设置不同，Unity 会在多种情况下重新编译和重载代码。代码重载对于让更改生效，以及在 Edit Mode 和 Play Mode 之间切换时保存状态都很重要；但它也会影响性能和迭代时间。因此，需要理解这些成本，并配置 Unity 的代码重载行为来减轻影响。相关内容请参阅 [[../10-编译和代码重载/00-编译和代码重载]]。

## 其他资源

- [[02-创建脚本]]
- [[03-命名脚本]]
- [[04-检查脚本]]
- [[../03-Unity基础类型/00-Unity基础类型]]

---

## 文档导航

- 上一页：[[00-开始使用Unity编程]]
- 目录：[[00-开始使用Unity编程]]
- 下一页：[[02-创建脚本]]
