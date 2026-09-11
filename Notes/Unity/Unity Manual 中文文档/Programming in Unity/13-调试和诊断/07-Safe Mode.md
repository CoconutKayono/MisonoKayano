# Safe Mode

> 原文：[Safe Mode](https://docs.unity3d.com/6000.7/Documentation/Manual/SafeMode.html)

## 概览

当你打开存在脚本编译错误的项目时，Unity Editor 可能会进入 Safe Mode。Safe Mode 旨在提供最适合解决编译错误的环境，让你能够快速将项目恢复到可用状态。

在 Safe Mode 中，Unity 提供功能受限的最小化 Editor 用户界面。它只导入与脚本相关的 Asset，并阻止导入非脚本 Asset，例如模型、材质、纹理和 Prefab。这是因为 Safe Mode 不是用于制作内容的模式，而是专门用于解决编译错误。

Safe Mode 永远不会运行项目或其 Package 中的 managed code。这意味着你自己的脚本，例如 [Editor 脚本](https://docs.unity3d.com/6000.7/Documentation/Manual/ExtendingTheEditor.html)、Asset post-processor 和 Scripted Importer，都不会运行。

Safe Mode 还会禁用 [Burst](https://docs.unity3d.com/6000.7/Documentation/Manual/com.unity.burst.html) 和 [Roslyn Analyzer](https://docs.unity3d.com/6000.7/Documentation/Manual/roslyn-analyzers.html)。这样可以确保即使项目处于严重损坏的状态，Safe Mode 中的 Editor 仍然完全可用且可靠。

当 Unity 检测到所有编译错误都已消失时，会自动退出 Safe Mode。退出后，Unity 会完整导入项目，Editor 也会恢复正常的全部功能。

## 编译错误的常见原因

以下是一些可能导致编译错误的常见场景：

- 将项目从较旧版本的 Unity 升级到较新版本。
- 使用不同于项目创建版本的 Unity 打开项目。
- 打开缺少 Package 或 Package 版本不正确的项目。
- 打开自己的脚本中存在错误的项目。
- 在版本控制下打开项目，而最近拉取的更改包含编译错误。

如果不使用 Safe Mode 打开存在编译错误的项目，可能会导致多种问题。例如，项目中的 Package 可能无法加载或无法正常工作，Asset 可能被错误导入，进而在 [Library](https://docs.unity3d.com/6000.7/Documentation/Manual/ImportingAssets.html#asset-processing) 或 [Cache Server](https://docs.unity3d.com/6000.7/Documentation/Manual/UnityAccelerator.html) 中产生不正确的缓存 Artifact。

在这些情况下，你通常不希望等待项目其余部分导入完成后才能解决错误。Safe Mode 为你提供了解决这些脚本相关问题的工具；如果你使用版本控制，也可以先更新到包含修复内容的项目版本，而不必等待项目完整导入。

## 进入 Safe Mode

当你打开存在编译错误的项目时，Editor 会显示一个对话框，询问你是否要进入 Safe Mode：

![打开存在编译错误的项目时，Enter Safe Mode? 对话框会询问是否进入 Safe Mode](SafeModeDialog.png)

此时有三个选择：

- **Enter Safe Mode**
- **Ignore** 错误并打开项目
- **Quit** Unity

大多数情况下，你应该选择 **Enter Safe Mode** 来解决项目中的错误。如果你使用版本控制，也可以借此拉取包含错误修复的更改。Safe Mode 能为解决编译错误提供最佳环境，让你在 Unity 导入项目其余内容之前，快速将项目恢复到可用状态。

不过，在某些情况下你可能不想进入 Safe Mode。这时可以 **Quit** Unity，或者 **Ignore** 错误。

> [!NOTE]
> 你可以在 **Edit > Preferences > Asset Pipeline > Show Enter Safe Mode Dialog** 中禁用此对话框。禁用后，Unity 在打开存在编译错误的项目时会自动进入 Safe Mode。

### 不进入 Safe Mode 直接退出

Safe Mode 专门用于修复编译错误。如果你在团队项目中工作，但并不负责导致错误的脚本，也不知道如何处理，那么应该在对话框中选择 **Quit**，并向团队中的程序员寻求建议。

### 忽略错误并继续导入

在某些情况下，你并不需要项目处于可用状态。例如，你可能只是打开旧项目以复制其中的部分内容，或检查项目的配置方式。此时可以忽略错误，直接以损坏状态打开项目。

如果选择 **Ignore**，之后又想在 Safe Mode 中打开项目，可以关闭并重新打开 Unity，再次访问 **Enter Safe Mode** 对话框。

### 忽略编译错误的影响

如果选择忽略错误，Unity 会继续导入其余 Asset，并完整打开项目。可能产生的影响包括：

- 项目可能无法使用。在错误解决之前，你可能无法进入 Play Mode 或创建项目 Build；此外，项目中的 Package 可能无法正确加载，甚至完全无法加载。
- Unity 可能需要导入两次 Asset：第一次是在启动时，第二次是在你解决项目编译错误之后。这会增加项目恢复到可用状态所需的加载时间。
- 如果项目使用 [Scriptable Render Pipeline](https://docs.unity3d.com/6000.7/Documentation/Manual/scriptable-render-pipeline-introduction.html)，渲染管线可能无法加载，从而导致诸如 [Error Shader](https://docs.unity3d.com/6000.7/Documentation/Manual/shader-error.html) 之类的视觉问题。
- 脚本编译错误可能在项目中造成次生错误。例如，如果项目中的 Scripted Importer 因编译错误无法加载，Asset 可能会以错误状态导入。

Safe Mode 的设计目的就是帮助你避免这些问题。

## Safe Mode 中的 Editor

在 Safe Mode 中，Unity 提供功能受限的最小化 Editor 界面。

![Safe Mode 中的 Unity Editor](SafeModeEditor.png)

Editor 顶部工具栏区域会显示 Safe Mode 横幅，该横幅取代标准的 Editor 工具栏。横幅会指示当前处于 Safe Mode，并提供 **Exit Safe Mode** 按钮，让你可以忽略剩余错误并退出 Safe Mode。

横幅还会指示项目是否使用 [preview Package](https://docs.unity3d.com/6000.7/Documentation/Manual/pack-preview.html)。

Unity Editor 在 Safe Mode 中仍保留与[代码编辑器的集成](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-ide-support.html)。因此，你可以双击脚本 Asset 或 [Console error](https://docs.unity3d.com/6000.7/Documentation/Manual/Console.html) 打开关联脚本，也可以通过 **Assets** 菜单打开 C# 项目。它还保留与[版本控制系统](https://docs.unity3d.com/6000.7/Documentation/Manual/VersionControl.html)的集成。

### Safe Mode 中受限的窗口集合

Safe Mode 中的 Editor 只显示有限的窗口，包括：

- Console 窗口
- Project 窗口
- Inspector 窗口
- Package Manager 窗口

这些是 Safe Mode 中唯一可用的窗口，因为它们与修复编译错误有关。Safe Mode 中无法使用其他窗口。

### Safe Mode 中的 Editor 菜单

在 Safe Mode 中，Editor 主菜单中的可用选项会被限制为一组有限的功能。你只能看到和选择与脚本工作有关的菜单选项；用于创建和处理其他内容的常规选项不可用。例如，你不能创建或打开 Scene，也不能创建 Primitive Shape、Light 或 Camera 等非脚本 Asset。

**GameObject** 和 **Component** 菜单不会出现，**Window** 菜单也只提供受限的窗口集合。

![Safe Mode 中显示可用 Asset 创建选项的受限 Editor 菜单](SafeModeLimitedMenu.png)

### Safe Mode 中的 Project 窗口

Safe Mode 中的 Project 窗口与正常模式相比有一些功能差异。

主要区别是你只能选择与编译相关的 Asset，不能选择其他类型的 Asset。其他 Asset 仍会以灰色条目显示在 Project 窗口中，但你不能选择或编辑它们。

具体来说，你可以在 Safe Mode 中交互的编译相关 Asset 类型包括：

- C# 文件（`.cs`）
- DLL 文件（`.dll`）
- Assembly Definition（`.asmdef`）文件
- Response 文件（`.rsp`）
- RuleSet 文件（`.ruleset`）

此外，不可选择 Asset 的图标不会显示 Asset 内容的预览，而是显示代表该 Asset 类型的通用图标。

![Project 窗口为不可选择的 Asset 显示通用图标](SafeModeProjectWindow.png)

**Create (+)** 菜单按钮处于禁用状态，Project 窗口的上下文菜单也只提供一组精简选项。

![Safe Mode 中 Project 窗口内已禁用的 Create (+) 菜单按钮](SafeModeCreateButton.png)

## 退出 Safe Mode

当你解决所有编译错误后，Unity 会自动退出 Safe Mode。随后 Unity 会继续打开项目并导入 Asset。

如果仍有编译错误，但你想退出 Safe Mode，请在 Safe Mode 工具栏中选择 **Exit Safe Mode** 按钮。不建议这样做（请参阅[忽略编译错误的影响](#忽略编译错误的影响)），Unity 会显示对话框要求你确认决定。

![Safe Mode 工具栏中的 Exit Safe Mode 按钮](SafeModeExitButton.png)

如果在项目仍有错误时退出 Safe Mode，之后又想返回 Safe Mode，可以关闭并重新打开 Unity，再次访问 **Enter Safe Mode** 对话框。

## Batch Mode 中的 Safe Mode

在 Batch Mode 中，如果项目存在编译错误，Unity 会自动退出，除非你使用 `-ignoreCompilerErrors` [命令行参数](https://docs.unity3d.com/6000.7/Documentation/Manual/CommandLineArguments.html)。


---

## 文档导航

- 上一页：[[05-Roslyn Analyzer和Source Generator的Additional Files]]
- 目录：[[00-调试和诊断]]
- 下一页：[[00-脚本]]
