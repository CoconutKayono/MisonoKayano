# 额外 IL2CPP 编译器参数

> 原文：[Additional IL2CPP compiler arguments](https://docs.unity3d.com/6000.7/Documentation/Manual/handling-IL2CPP-additional-args.html)

你可以使用 [`PlayerSettings.SetAdditionalIl2CppArgs`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/PlayerSettings.SetAdditionalIl2CppArgs.html) API，或设置 `IL2CPP_ADDITIONAL_ARGS` 环境变量，为 IL2CPP Compiler 提供额外参数。

> **警告**：向 IL2CPP Compiler 传递额外参数是一项实验性功能，用于在复杂项目中调试和优化 IL2CPP 代码生成。与[诊断开关](https://docs.unity3d.com/6000.7/Documentation/Manual/preferences-editor-diagnostics.html)一样，该功能面向高级开发者，并应与 Unity 支持团队协作使用。参数会直接传给 C++ Compiler，不经过解释，因此极有可能破坏构建。Unity 保留在不另行通知的情况下更改或移除此功能的权利。

下表列出了可以用来向 IL2CPP Compiler 提供额外标志的参数：

| 参数 | 描述 |
| --- | --- |
| `--compiler-flags="<flags>"` | 向 C++ Compiler 传递额外标志。将 `<flags>` 替换为所需标志。例如，`--compiler-flags=\"COMPILER_FLAG_1 COMPILER_FLAG_2\"` 会将 `COMPILER_FLAG_1` 和 `COMPILER_FLAG_2` 编译器标志传递给 C++ Compiler。 |
| `--linker-flags="<flags>"` | 向 Linker 传递额外标志。将 `<flags>` 替换为所需标志。例如，`--linker-flags="\LINKER_FLAG_1 LINKER_FLAG_2\"` 会将 Linker 标志传递给 Linker。 |

多个参数之间必须使用空格分隔，如下所示：

```csharp
PlayerSettings.SetAdditionalIl2CppArgs("--compiler-flags=\"COMPILER_FLAG_1 COMPILER_FLAG_2\" --linker-flags="\LINKER_FLAG_1 LINKER_FLAG_2\"");
```

> **注意**：多次调用 `SetAdditionalIl2CppArgs` 会覆盖之前提供的所有标志。向此方法传入空字符串，可以移除之前提供的所有额外参数。

有效的 Compiler 和 Linker 标志因平台而异，具体取决于 IL2CPP 在该平台上使用的底层 C++ Compiler（`msvc` 或 `clang`）。如需有效的编译器和链接器选项列表，请参阅相关第三方文档中的 [msvc 编译器选项](https://learn.microsoft.com/en-us/cpp/build/reference/compiler-options?view=msvc-170)、[msvc 链接器选项](https://learn.microsoft.com/en-us/cpp/build/reference/linker-options?view=msvc-170)，或 [clang 编译器和链接器选项](https://clang.llvm.org/docs/ClangCommandLineReference.html)。

## 检查是否设置了参数

如果项目设置了额外的 IL2CPP 参数，那么为多个平台进行编译可能不会按预期工作，尤其是在[为 Linux 交叉编译](https://docs.unity3d.com/6000.7/Documentation/Manual/linux-il2cpp-crosscompiler.html)时。

要检查是否已经设置了额外的 IL2CPP 参数，请执行以下任一操作：

- 检查是否设置了 `IL2CPP_ADDITIONAL_ARGS` 环境变量。
- 在 `ProjectSettings/ProjectSettings.asset` 中，检查 Editor 脚本是否包含名为 `additionalIl2CppArgs` 的值。

> **重要**：额外的 IL2CPP 参数会全局应用于所有平台。如果为非目标平台设置参数，可能导致编译问题。使用 `IPreprocessBuildWithContext` Hook，确保只为需要这些参数的平台设置 IL2CPP 参数。

### IPreprocessBuildWithContext Hook

你可以使用 [`IPreprocessBuildWithContext`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Build.IPreprocessBuildWithContext.html) 回调，在构建脚本或 Build 对话框中设置额外参数：

```csharp
class MyCustomPreprocessBuild: IPreprocessBuildWithContext
{
    public int callbackOrder { get { return 0; } }
    public void OnPreprocessBuild(BuildCallbackContext ctx)
    {
        string addlArgs = "";
        if (ctx.Report.summary.platform == BuildTarget.StandaloneWindows || ctx.Report.summary.platform == BuildTarget.StandaloneWindows64)
            addlArgs = "--compiler-flags=\"d2ssa-cfg-jt\"";
        UnityEngine.Debug.Log($"Setting Additional IL2CPP Args = \"{addlArgs}\" for platform {report.summary.platform}");
        PlayerSettings.SetAdditionalIl2CppArgs(addlArgs);
    }
}
```

## 其他资源

- [[05-Linux IL2CPP交叉编译器]]
- [[02-IL2CPP托管Stack Trace]]
- [讨论：如何为 IL2CPP 调用添加编译器或链接器标志](https://discussions.unity.com/t/how-to-add-compiler-or-linker-flags-for-il2cpp-invocation/221183)


---

## 文档导航

- 上一页：[[03-IL2CPP运行时代码检查]]
- 目录：[[00-IL2CPP脚本后端]]
- 下一页：[[05-Linux IL2CPP交叉编译器]]
