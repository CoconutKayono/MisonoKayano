# Unity 脚本符号参考

> 原文：[Unity scripting symbol reference](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-symbol-reference.html)

<a name="Platform"></a>

## 平台符号

Unity 会根据创作平台和构建目标平台自动定义某些符号，具体如下：

| 定义 | 功能 |
| --- | --- |
| `UNITY_EDITOR` | 用于从游戏代码调用 Unity Editor 脚本的脚本符号。 |
| `UNITY_EDITOR_WIN` | Windows 上 Editor 代码的脚本符号。 |
| `UNITY_EDITOR_OSX` | macOS 上 Editor 代码的脚本符号。 |
| `UNITY_EDITOR_LINUX` | Linux 上 Editor 代码的脚本符号。 |
| `UNITY_EMBEDDED_LINUX` | 嵌入式 Linux 的脚本符号。 |
| `UNITY_QNX` | QNX 的脚本符号。 |
| `UNITY_STANDALONE_OSX` | 专门用于 macOS（包括 Universal、PPC 和 Intel 架构）编译或执行代码的脚本符号。 |
| `UNITY_STANDALONE_WIN` | 专门用于 Windows 独立应用程序编译或执行代码的脚本符号。 |
| `UNITY_STANDALONE_LINUX` | 专门用于 Linux 独立应用程序编译或执行代码的脚本符号。 |
| `UNITY_STANDALONE` | 用于为任何独立平台（Mac OS X、Windows 或 Linux）编译或执行代码的脚本符号。 |
| `UNITY_SERVER` | 用于为[专用服务器](https://docs.unity3d.com/6000.7/Documentation/Manual/dedicated-server.html)（macOS、Windows 或 Linux）编译或执行代码的脚本符号。 |
| `UNITY_IOS` | 用于为 iOS 平台编译或执行代码的脚本符号。 |
| `UNITY_ANDROID` | Android 平台的脚本符号。 |
| `UNITY_TVOS` | Apple TV 平台的脚本符号。 |
| `UNITY_VISIONOS` | VisionOS 平台的脚本符号。 |
| `UNITY_WSA` | 通用 Windows 平台的脚本符号。 |
| `UNITY_WSA_10_0` | 通用 Windows 平台的脚本符号。 |
| `UNITY_WEBGL` | Web 的脚本符号。 |
| `UNITY_ANALYTICS` | 用于从游戏代码调用 Unity Analytics 方法的脚本符号。 |
| `UNITY_ASSERTIONS` | 断言控制过程的脚本符号。对于 Editor 代码，`UNITY_ASSERTIONS` 始终有定义；对于启用了 Debug 和 Checked 托管代码变体的开发构建和构建，它也有定义。 |
| `UNITY_ENABLE_CHECKS` | 启用安全检查的脚本符号。对于 Editor 代码，`UNITY_ENABLE_CHECKS` 始终有定义；对于使用 Debug 和 Checked 托管代码变体的构建，它也有定义。 |
| `UNITY_INCLUDE_INSTRUMENTATION` | 启用检测代码路径（例如性能分析器）的脚本符号。对于 Editor 代码，`UNITY_INCLUDE_INSTRUMENTATION` 始终有定义；对于使用 Debug、Checked 和 Instrumented 托管代码变体的构建，它也有定义。 |
| `UNITY_64` | 64 位平台的脚本符号。实际上**不应使用**此符号，因为它无法在所有 64 位架构上工作，并且同一平台上的不同 CPU 架构可能共享相同的已编译程序集。若要根据架构有条件地执行代码，请使用标准 `if` 语句检查 [`IntPtr.Size`](https://learn.microsoft.com/en-us/dotnet/api/system.intptr.size?view=net-8.0)：32 位进程中其值为 `4`，64 位进程中其值为 `8`。示例请参阅 [[01-Unity中的条件编译#条件执行]]。 |

<a name="Editor"></a>

## Unity Editor 版本符号

Unity 会根据当前使用的 Unity Editor 版本自动定义某些脚本符号。

给定版本号 `X.Y.Z`（例如 6000.0.33），Unity 会以以下格式公开三个全局脚本符号：`UNITY_X`、`UNITY_X_Y` 和 `UNITY_X_Y_Z`。

以下是 Unity 6000.0.33 中公开的脚本符号示例：

| 定义 | 功能 |
| --- | --- |
| `UNITY_6000` | Unity 6 发布版本的脚本符号，在每个 6000.Y.Z 版本中公开。 |
| `UNITY_6000_0` | Unity 6.0 主版本的脚本符号，在每个 6000.0.Z 版本中公开。 |
| `UNITY_6000_0_33` | Unity 6000.0.33 次版本的脚本符号。 |

还可以根据编译或执行某段代码所需的最低 Unity 版本选择性地编译代码。按照前面所述的版本格式（`X.Y`），Unity 会公开一个格式为 `UNITY_X_Y_OR_NEWER` 的全局 `#define`（例如 `UNITY_6000_0_OR_NEWER`），可用于此目的。

<a name="Other"></a>

## 其他符号

Unity 定义的其他符号如下：

| 定义 | 功能 |
| --- | --- |
| `CSHARP_7_3_OR_NEWER` | 使用 C# 7.3 或更高版本支持编译脚本时定义。 |
| `ENABLE_MONO` | Mono 的脚本后端 `#define`。 |
| `ENABLE_IL2CPP` | IL2CPP 的脚本后端 `#define`。 |
| `ENABLE_VR` | 目标构建平台支持 VR 时定义。这不表示当前已启用 VR，也不表示已安装支持 VR 所需的插件和包。 |
| `NET_2_0` | 在 Mono 和 IL2CPP 上使用 .NET 2.0 API 兼容性级别构建脚本时定义。 |
| `NET_2_0_SUBSET` | 在 Mono 和 IL2CPP 上使用 .NET 2.0 Subset API 兼容性级别构建脚本时定义。 |
| `NET_LEGACY` | 在 Mono 和 IL2CPP 上使用 .NET 2.0 或 .NET 2.0 Subset API 兼容性级别构建脚本时定义。 |
| `NET_4_6` | 在 Mono 和 IL2CPP 上使用 .NET 4.x API 兼容性级别构建脚本时定义。 |
| `NET_STANDARD_2_0` | 在 Mono 和 IL2CPP 上使用 .NET Standard 2.0 API 兼容性级别构建脚本时定义。 |
| `NET_STANDARD_2_1` | 在 Mono 和 IL2CPP 上使用 .NET Standard 2.1 API 兼容性级别构建脚本时定义。 |
| `NET_STANDARD` | 在 Mono 和 IL2CPP 上使用 .NET Standard 2.1 API 兼容性级别构建脚本时定义。 |
| `NETSTANDARD2_1` | 在 Mono 和 IL2CPP 上使用 .NET Standard 2.1 API 兼容性级别构建脚本时定义。 |
| `NETSTANDARD` | 在 Mono 和 IL2CPP 上使用 .NET Standard 2.1 API 兼容性级别构建脚本时定义。 |
| `ENABLE_WINMD_SUPPORT` | 在 IL2CPP 上启用 Windows Runtime 支持时定义。更多信息请参阅 [WinRT API in C# scripts for UWP](https://docs.unity3d.com/6000.7/Documentation/Manual/windowsstore-scripts.html)。 |
| `ENABLE_INPUT_SYSTEM` | 在 Player Settings 中启用 Input System 包时定义。 |
| `ENABLE_LEGACY_INPUT_MANAGER` | 在 Player Settings 中启用旧版 Input Manager 时定义。 |
| `DEVELOPMENT_BUILD` | 脚本运行在启用了 **Development Build** 选项构建的 Player 中时定义。此定义只反映构建时是否启用了开发构建选项。若要了解脚本是否正在开发构建模式下运行，请使用 [`Debug.isDebugBuild`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Debug-isDebugBuild.html)。仅凭 `DEVELOPMENT_BUILD` 不足以判断当前是否正在运行开发构建，因为大多数平台允许在不重新构建项目的情况下，在开发构建和非开发构建之间切换。不过，某些平台不支持在 Editor 中切换开发构建和非开发构建，而是要求在构建完成后切换。例如，在 Windows 上，可以在 Visual Studio 中选择 **Create Visual Studio solution** 选项，以决定使用开发构建还是非开发构建。Visual Studio 中的切换不会重新编译脚本，因此不会重新评估脚本定义。还可以通过在游戏构建中将 `UnityPlayer.dll` 替换为开发构建中的同一文件，从最终游戏构建切换到开发构建，以调试正在运行的游戏构建。 |
| `UNITY_CLOUD_BUILD` | 使用 [Unity Build Automation](https://docs.unity.com/ugs/en-us/manual/devops/manual/unity-build-automation) 构建项目时定义。 |

> **注意：** `DEBUG` 符号由 C# 预定义。在 Unity 中，使用 `#if DEBUG` 指令等价于使用 `#if UNITY_EDITOR || DEVELOPMENT_BUILD`。

## 其他资源

- [[04-测试条件编译]]
- [[02-自定义脚本符号]]


---

## 文档导航

- 上一页：[[01-Unity中的条件编译]]
- 目录：[[00-条件编译]]
- 下一页：[[02-自定义脚本符号]]
