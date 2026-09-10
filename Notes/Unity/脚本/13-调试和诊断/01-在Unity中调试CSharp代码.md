# 在 Unity 中调试 C# 代码

> 原文：[Debug C# code in Unity](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-debugging.html)

你可以在应用程序运行时使用 Debugger 检查源代码。每个受支持的 IDE 都有必须安装的依赖项，只有完成安装后，IDE 才能正确地与 Unity 集成。有关在 Unity 中配置受支持 IDE 进行调试所需内容的详细信息，请参阅 [[../02-环境与工具/01-集成开发环境支持]]。

尽管这些 IDE 支持的调试功能略有不同，但它们都提供断点、单步执行和变量检查等基本功能。你可以将 IDE 连接到 Unity Editor 或 Unity Player 来调试代码。

Unity 的 Managed Code 调试支持除 Web 之外的所有平台，并同时适用于 `Mono` 和 `IL2CPP` Scripting Backend。

## 在 Unity Editor 中调试

要在代码于 Editor 中运行时调试 Edit Mode 或 Play Mode 代码，请执行以下操作：

1. [[../02-环境与工具/01-集成开发环境支持|配置 IDE]]，用于 Unity 开发和调试。
2. 将 [Editor 的代码优化模式](#设置-unity-editor-的代码优化模式) 设置为 **Debug**。
3. 将 IDE [连接到 Unity Editor](#将-ide-连接到-unity-editor-或-player-进程)。

> **提示**：在 Batch Mode 下运行 Editor 时，可以使用命令行参数 [`-wait-for-managed-debugger`](EditorCommandLineArguments.html#debugging-arguments)，让 Editor 在启动前等待 Managed Debugger 连接。

## 在 Unity Player 中调试

要在代码于 Unity Player 中运行时调试 Play Mode 代码，请执行以下操作：

1. [[../02-环境与工具/01-集成开发环境支持|配置 IDE]]，用于 Unity 开发和调试。
2. 构建项目时启用 **Development Build** 和 **Script Debugging** 选项。也可以启用 **Wait For Managed Debugger** 选项，让 Player 在启动并运行任何脚本代码前等待 Debugger 连接。
3. 将 IDE [连接到 Unity Player](#将-ide-连接到-unity-editor-或-player-进程)。

> **注意**：在 Batch Mode 下运行 Player 时，可以使用命令行参数 [`-wait-for-managed-debugger`](PlayerCommandLineArguments.html)，让 Player 在启动前等待 Managed Debugger 连接。

## 设置 Unity Editor 的代码优化模式

Editor 的代码优化设置有两种模式：

- **Debug**：允许连接外部 Debugger，但 Play Mode 中的代码运行速度较慢。
- **Release**：Play Mode 中的代码运行速度更快，但无法连接外部 Debugger。

要[将 Debugger 连接到 Editor](#将-ide-连接到-unity-editor-或-player-进程)，必须先将 Editor 的代码优化模式设置为 Debug。可以通过以下方式更改代码优化设置：

- **从 Editor 状态栏设置**：点击 [状态栏](StatusBar.html) 右下角的代码优化模式按钮（Bug 图标）。此时会打开一个小弹出窗口，点击其中的按钮即可切换模式。
- **从 Preferences 窗口设置**：要更改 Unity Editor 启动时使用的模式，请选择 **Edit > Preferences**（macOS：**Unity > Settings**）> **General**，然后更改 **Code Optimization On Startup** 设置。
- **从代码设置**：可以使用 `ManagedDebugger`、`Compilation.CompilationPipeline-codeOptimization` 和 `Compilation.CodeOptimization` API 更改代码优化模式。
- **从命令行设置**：使用 `-releaseCodeOptimization` 命令行参数以 Release 模式启动 Editor，或使用 `-debugCodeOptimization` 参数以 Debug 模式启动 Editor。更多信息请参阅 [Debugging arguments](EditorCommandLineArguments.html#debugging)。

## 设置断点

断点用于指定代码执行时暂停的位置。在 IDE 中，可以在希望 Debugger 停止的代码行上设置断点。当 IDE 停在断点处时，可以逐步查看变量的内容。

如果你[将 IDE 连接到 Unity Editor](#将-ide-连接到-unity-editor-或-player-进程)，Editor 会在断点处变得无响应，直到你在 IDE 中选择继续执行，或停止调试。

有关如何设置断点的更多信息，请参阅所用 IDE 的相关文档：

- [Visual Studio](https://learn.microsoft.com/en-us/visualstudio/debugger/get-started-with-breakpoints)
- [Visual Studio Code](https://code.visualstudio.com/docs/editor/debugging#_breakpoints)
- [Rider](https://www.jetbrains.com/help/rider/Using_Breakpoints.html)

## 将 IDE 连接到 Unity Editor 或 Player 进程

将 IDE 连接到 Unity Editor 或 Unity Player 进程的方式取决于所使用的 IDE。某些 IDE 提供专用于 Unity 的连接选项，其操作方式可能不同于连接其他应用程序的标准流程。

有关如何连接 Unity 进行调试的信息，请参阅所用 IDE 的相关文档：

- Visual Studio：[Using Visual Studio Tools for Unity（Windows）](https://docs.microsoft.com/en-us/visualstudio/gamedev/unity/get-started/using-visual-studio-tools-for-unity?pivots=windows#unity-debugging)
- Visual Studio Code：[Unity Development with VS Code](https://code.visualstudio.com/docs/other/unity)
- JetBrains Rider：[Debug Unity Applications](https://www.jetbrains.com/help/rider/Debugging_Unity_Applications.html)

连接到 Unity Editor 后，返回 Unity Editor 并进入 Play Mode，即可开始调试。

要连接到构建后的 Player，请在 IDE 中选择 Player 的 IP 地址（或计算机名称）和端口。连接 Debugger 后，即可正常开始调试。

> **注意**：IDE 会显示所有可供调试的 Unity 实例。如果 Editor 和 Player 同时运行，请确认区分 Editor 进程和 Player 进程。

### Android

要调试运行在 Android 设备上的 Unity Player，请通过 USB 或 TCP 连接设备。例如，在 Visual Studio 中连接 Android 设备时，选择 **Debug > Attach Unity Debugger**。随后会显示正在运行 Player 实例的设备列表。

更多信息请参阅 [在 Android 设备上调试](android-debugging-on-an-android-device.html)。

### iOS

要调试运行在 iOS 设备上的 Unity Player，请通过 TCP 连接设备。

确保设备只有一个活动的网络接口（推荐使用 Wi-Fi，并关闭蜂窝数据），并确保 IDE 与设备之间没有阻止 TCP 端口的防火墙（上方截图中的端口号为 `56000`）。

> **重要**：iOS 不支持通过 USB 进行调试。

更多信息请参阅 [测试和调试 iOS 应用程序](ios-testing-and-debugging.html)。

## 其他资源

- [[02-调试故障排查]]
- [[../02-环境与工具/01-集成开发环境支持]]


---

## 文档导航

- 上一页：[[00-调试和诊断]]
- 目录：[[00-调试和诊断]]
- 下一页：[[02-调试故障排查]]
