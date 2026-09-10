# IL2CPP 简介

> 原文：[Introduction to IL2CPP](https://docs.unity3d.com/6000.7/Documentation/Manual/il2cpp-introduction.html)

IL2CPP（Intermediate Language To C++）是 Unity 自研的 **AOT（ahead-of-time）Scripting Backend**。它会把 C# 编译生成的 IL（Intermediate Language）转换为 C++，再使用目标平台的 C++ Compiler 生成 Native Code，并按平台格式打包到应用中，例如 APK/AAB、iOS App Bundle 或 Windows 可执行文件与 DLL。

IL2CPP 支持所有 Unity 平台。与 Mono Scripting Backend 相比，它可能带来更好的运行时性能和更短的启动时间，但因为构建产物包含机器码，通常会增加构建时间和最终包体大小。IL2CPP 也支持与 Mono 类似的 Managed Code 调试。

## 使用 IL2CPP 构建项目

安装 Unity 时需要安装 IL2CPP Module。可以在 Unity Hub 中将它作为模块添加到现有 Editor。然后在 **Edit > Project Settings > Player > Other Settings > Configuration > Scripting Backend** 中选择 **IL2CPP**，也可以通过 `PlayerSettings.SetScriptingBackend` 设置。

IL2CPP 生成 C++ 时需要目标平台的原生工具链，因此通常不支持任意跨平台编译。Linux 是例外，Unity 提供 Linux IL2CPP Cross-Compiler，允许在其他桌面平台上构建 Linux Player。

## IL2CPP 的构建流程

构建时 Unity 会依次执行：

1. Roslyn C# Compiler 将项目代码和所需 Package 代码编译为 .NET DLL（Managed Assembly）。
2. Unity 执行 Managed Code Stripping，减少最终应用中不需要的代码。
3. IL2CPP 将 Managed Assembly 转换为标准 C++。
4. C++ Compiler 使用平台原生工具链编译生成的 C++ 与 IL2CPP Runtime。
5. Unity 按目标平台生成可执行文件或 DLL。

## 优化构建时间

- 将 Unity 项目目录和目标构建目录排除在 Anti-malware 扫描之外。
- 把项目和构建目录放在速度较快的磁盘上，因为 IL 转换和 C++ 编译会产生大量读写。
- 将 **IL2CPP Code Generation** 从 **Optimize for runtime speed** 改为 **Optimize for code size and build time**，以减少构建时间和二进制大小；代价是可能降低运行时性能。
- 在 Linux 和 QNX 上可将 **IL2CPP LTO Mode** 设置为 **Thin**，以减少相较 Full 模式的构建时间。

在适合的项目中，还可以让 Burst 与 IL2CPP 配合，为兼容的代码生成高度优化的机器码。

## 其他资源

- [IL2CPP 编译器选项参考](https://docs.unity3d.com/6000.7/Documentation/Manual/il2cpp-compiler-options.html)
- [[05-Linux IL2CPP交叉编译器]]
- [[02-IL2CPP托管Stack Trace]]
- [减小构建文件大小](https://docs.unity3d.com/6000.7/Documentation/Manual/reducing-build-size.html)


---

## 文档导航

- 上一页：[[00-IL2CPP脚本后端]]
- 目录：[[00-IL2CPP脚本后端]]
- 下一页：[[02-IL2CPP托管Stack Trace]]
