# 托管代码剥离和 Unity Linker

> 原文：[Managed code stripping and the Unity linker](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-linker.html)

Unity 的构建过程使用名为 Unity Linker 的工具来剥离托管代码。Unity Linker 是经过定制、用于 Unity 的 [IL Linker](https://github.com/mono/linker) 版本。Unity Linker 中专用于 Unity Engine 的自定义部分并未公开。

Unity Linker 同时负责 Managed Code Stripping，以及 Engine Code Stripping 过程的一部分。后者是通过 IL2CPP scripting backend 提供的独立过程，用于移除未使用的 Engine Code。更多信息请参阅 [`PlayerSettings.StripEngineCode`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/PlayerSettings-stripEngineCode.html)。

## Unity Linker 如何剥离程序集

构建 Unity 项目时，构建过程会先将 C# 代码编译为一种名为 Common Intermediate Language（CIL）的 .NET 字节码格式。Unity 会将这些 CIL 字节码打包到称为程序集（assemblies）的文件中。你在项目中使用的 .NET Framework 库和任何 C# libraries plug-ins 也会预先打包为 CIL 字节码程序集。

出于 Managed Code Stripping 的目的，程序集分为以下类别：

- **.NET Class Library assemblies**：包括 Mono class libraries，例如 `mscorlib.dll` 和 `System.dll`，以及 `netstandard.dll` 等 .NET class library facade assemblies。
- **Platform SDK assemblies**：包括特定于某个平台 SDK 的托管程序集。例如，Universal Windows Platform SDK 中的 `windows.winmd` 程序集。
- **Unity Engine Module assemblies**：包括构成 Unity Engine 的托管程序集，例如 `UnityEngine.Core.dll`。
- **Project assemblies**：包括项目专用的程序集，例如：
  - Script assemblies，例如 `Assembly-CSharp.dll`。
  - Precompiled assemblies。
  - [Assembly Definition Assemblies](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-files.html)。
  - Package assemblies。

通常，项目中不属于上述任一类别的程序集不会由 Unity Linker 处理，并会从 Player 构建中排除。

在构建期间，Unity Linker 会处理所有适用类型的程序集，并执行以下操作：

1. 根据适用于程序集类型和已配置代码剥离级别的[[06-Unity Linker标记规则参考#root-marking-rules|根标记规则]]，标记根类型、方法、属性和字段。
2. 分析已标记的根，根据适用的[[06-Unity Linker标记规则参考#dependency-marking-rules|依赖标记规则]]识别并标记这些根所依赖的托管代码。
3. 删除程序集内剩余的未标记代码，因为这些代码无法通过应用程序代码中的任何执行路径到达。

## 方法体编辑

在 **High** [[02-配置托管代码剥离|剥离级别]] 下，Unity Linker 会编辑方法体，以进一步减小代码体积。Unity Linker 只会编辑 .NET Class Library assemblies 中的方法体。

Unity Linker 可以通过以下方式编辑方法体：

- 移除不可达分支：移除检查 `System.Environment.OSVersion.Platform`、且对于当前目标平台不可达的 `if` 语句块。
- Inline 只访问字段的方法：将获取或设置字段的方法调用替换为对字段的直接访问。这通常可以让 Unity 完全移除该方法。使用 Mono scripting backend 时，Unity Linker 只有在方法调用方根据字段可见性可以直接访问该字段时才会执行此更改。对于 IL2CPP，visibility 规则不适用，因此 Unity Linker 会在适当的地方执行此更改。
- Inline 只返回 `const` 值的方法。
- 移除返回类型为 `void` 且为空的方法调用。
- 当 `finally` 块为空时，移除 `try-finally` 块。移除空调用可能会创建空的 `finally` 块；发生这种情况时，Unity Linker 会在编辑方法期间移除整个 `try-finally` 块。例如，编译器可能会在 `foreach` 循环中生成 `try-finally` 块，用于调用 `Dispose`。

> **注意**：编辑方法体后，程序集的源代码将不再与程序集中的编译代码匹配，这可能使调试更加困难。

## 其他资源

- [[04-使用注释保留代码]]
- [[06-Unity Linker标记规则参考]]

---

## 文档导航

- 上一页：[[00-托管代码剥离]]
- 目录：[[00-托管代码剥离]]
- 下一页：[[02-配置托管代码剥离]]
