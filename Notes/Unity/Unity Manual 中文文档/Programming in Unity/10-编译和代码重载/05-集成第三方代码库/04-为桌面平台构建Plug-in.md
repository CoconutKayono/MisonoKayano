# 为桌面平台构建 Plug-in

> 原文：[Building plug-ins for desktop platforms](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-for-desktop.html)

桌面平台 Plug-in 是使用 C、C++ 和 Objective-C 编写的 Native Code Library。本页介绍 macOS、Windows 和 Linux 的 Plug-in。更多信息请参阅 [[00-Native Plug-in]]。

## macOS Plug-in

你可以将 macOS Plug-in 部署为 Bundle；如果使用 **IL2CPP** Scripting Backend，也可以部署为 Loose C++ File，并使用 `[DllImport("__Internal")]` 语法调用它。关于 Loose C++ Plug-in 的更多信息，请参阅 [C++ source code plugins for IL2CPP](https://docs.unity3d.com/6000.7/Documentation/Manual/macOSIL2CPPScriptingBackend.html)。

要使用 Xcode 创建 Bundle Project：

1. 打开 Xcode。
2. 选择 **File** > **New** > **Project** > **macOS** > **Framework & Library** > **Bundle**。

关于使用 Xcode 的更多信息，请参阅 [Apple 的 Xcode 文档](https://developer.apple.com/documentation/xcode)。

### Requirements

- 可以将 Plug-in 构建为兼容 64-bit Architecture 的 Universal Binary。或者，也可以提供单独的 dylib File。
- 如果使用 C++（`.cpp`）或 Objective-C（`.mm`）实现 Plug-in，必须使用 C Linkage 声明 Function：

```cpp
extern "C"
{
  float ExamplePluginFunction ();
}
```

## Windows Plug-in

Windows 上的 Plug-in 可以是带有 Exported Function 的 `.dll` 文件，也可以是在使用 IL2CPP 时采用的 Loose C++ File。可以使用大多数能够创建 `.dll` 文件的 Language 和 Development Environment 来创建 Plug-in。必须对所有 C++ Function 使用 C Linkage，以避免 Name Mangling 问题。

## Linux Plug-in

Linux 上的 Plug-in 是带有 Exported Function 的 `.so` 文件。虽然这些 Library 通常使用 C 或 C++，但也可以使用任何 Language。必须对所有 C++ Function 使用 C Linkage，以避免 Name Mangling 问题。

在构建 Linux Native Plug-in 时，如果构建出的 Library 依赖另一个 Native Plug-in，必须在编译它时为该 Library 指定 `rpath`。

添加 Linker Flag `-Wl, -rpath=$ORIGIN` 来指定 Runtime Search Path。该 Linker Flag 会指示 Loader：除了搜索 System Search Path 外，还要在当前 Library 所在目录中查找其依赖项。可以与 `-Wl, -rpath=$ORIGIN` 一起添加其他 Linker Flag，但 Unity 不会控制这些 Flag。例如：`/usr/bin/g++ -o binary.c.o -Wl,-rpath=$ORIGIN`。

或者，可以在 Environment 中设置 `LD_LIBRARY_PATH=dependency path`，指示 Loader 在该路径中查找依赖项。Linux 不会自动在当前目录中查找依赖项。请确保设置正确的 Dependency Search Path，因为路径错误会在 Unity Editor 中造成 Missing Library Error。

## 在 Unity 中管理 Plug-in

在 Unity 中，**Plugin Inspector** 负责管理 Plug-in。要访问 **Plugin Inspector**，请在 **Project window** 中选中 Plug-in File。对于 Standalone Platform，可以选择 Library 兼容的 CPU Architecture。对于 Cross-platform Plug-in，必须包含 `.bundle` 文件（macOS）、`.dll` 文件（Windows）和 `.so` 文件（Linux）。Unity 会自动为目标 Platform 选择正确的 Plug-in，并将其包含在 Player 中。更多信息请参阅 [Import and configure plug-ins](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-in-inspector.html)。

![Plugin Inspector](plugin-inspector.png)

## 从 C# Script 调用 Plug-in

将构建好的 Plug-in 放在 **Assets** 文件夹或适当的 Architecture-specific Sub-directory 中。之后，当你从 C# Script 调用它时，Unity 会按名称找到它。例如：`[DllImport ("PluginName")] private static extern float ExamplePluginFunction ();`

**Note**：不要在 `PluginName` Value 中包含 Library Prefix 或 File Extension。例如，如果 Windows 上 Plug-in File 的实际名称是 `PluginName.dll`，或者 Linux 上是 `libPluginName`，那么两种情况下 Value 都应为 `PluginName`。

## 卸载 Plug-in

Native Plug-in 一旦加载到 Editor Session 中，就无法卸载。要更改已经加载的 Plug-in，必须重启 Unity Editor。

当你从 Editor Script 调用 Plug-in Function，或者进入 Play Mode 且 Plug-in 的 **Load on startup** 选项已启用时，Editor 会加载 Native Plug-in。使用 Script 手动加载 Plug-in 时，它也会被加载到 Editor Session 中。

## Plug-in 示例

可以下载并使用以下 Project，学习如何在 Unity 中实现 Plug-in。

- [Simplest Plugin Example](https://github.com/Unity-Technologies/DesktopSamples/tree/master/SimplestPluginExample)：该 Project 实现基本操作（例如打印数字、打印字符串、将两个 Float 相加以及将两个 Integer 相加）。该 Project 包含 Windows、macOS 和 Linux Project File。
- [Native Renderer Plugin](https://github.com/Unity-Technologies/NativeRenderingPlugin)：这是一个 Low-level Rendering Plug-in。它在所有常规 Rendering 完成后从 C++ Code 渲染一个旋转三角形，并使用 `Texture.GetNativeTexturePtr` 访问 Procedural Texture，从 C++ Code 填充该 Texture。该 Project 包含 Windows、UWP、macOS、Web 和 Android File。

## 其他资源

- [[02-Managed Plug-in]]
- [[00-Native Plug-in]]
- [Native plug-in interface](https://docs.unity3d.com/6000.7/Documentation/Manual/native-plugin-interface.html)

---

## 文档导航

- 上一页：[[02-Managed Plug-in]]
- 目录：[[00-集成第三方代码库]]
- 下一页：[[00-Native Plug-in]]
