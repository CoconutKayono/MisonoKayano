# Linux IL2CPP 交叉编译器

> 原文：[Linux IL2CPP cross-compiler](https://docs.unity3d.com/6000.7/Documentation/Manual/linux-il2cpp-crosscompiler.html)

Linux IL2CPP 交叉编译器是一组 sysroot 和 toolchain Package，允许你在任意 Standalone 平台上构建 Linux IL2CPP Player，而不需要使用 Linux Unity Editor 或依赖 Mono。

如果满足前置条件，选择 Linux 构建目标时 Unity 会自动安装这些 Package。如果要退出自动安装并使用自己的 sysroot 和 toolchain Package，请转到 **Edit > Project Settings > Toolchain Management**，禁用 **Install Toolchain package automatically** 复选框。如果这些 Package 已经安装，还需要从 Package Manager 中移除它们。

## 前置条件

Unity 需要满足以下条件才能安装 IL2CPP 交叉编译器 Package：

- 为选定的 Linux toolchain Package 预留足够的可用磁盘空间。详细信息请参阅[Linux toolchain Package 所需磁盘空间](#linux-toolchain-package-所需磁盘空间)。
- 将脚本后端设置为 IL2CPP。设置方法：转到 **Edit > Project Setting > Player Settings for Linux > Other Settings > Configuration**，将 **Scripting Backend** 设置为 **IL2CPP**。
- IL2CPP 模块。有关如何安装 IL2CPP 模块的信息，请按照[添加模块](https://docs.unity.com/hub/add-modules)中的步骤操作。

## Linux sysroot Package

Linux sysroot Package 是一个包含构建 Linux 所需全部 Header 和 Library 的目录。

每个操作系统（OS）的构建系统都各不相同。如果使用某个特定 OS 的 Header 和 Library 构建，构建出的 Player 可能无法在其他操作系统上运行。为了解决此问题，Unity 提供了一个 sysroot，用它构建出的 Player 可以在所有受支持的 Linux 平台上运行。

## Linux toolchain Package

Unity 为 macOS、Windows 和 Linux 提供 toolchain Package。这些平台以各自独特的方式构建 Linux。

Linux toolchain Package 是 Unity 从各个操作系统构建 Linux 时所需的一组工具，包括 Compiler 和 Linker。

## Linux toolchain Package 所需磁盘空间

确保有足够的磁盘空间来完成 Package 的下载、解压和使用。

如果少数情况下无法确定磁盘空间是否足够，可以定义 `UNITY_SYSROOT_CACHE` 环境变量，并使用它存储解压后的 sysroot 和 toolchain Package。环境变量是在 Unity 外部设置、供 Unity 使用的变量。在此情况下，可以设置一个缓存目录，让 Unity 在解压 sysroot 和 toolchain Package 时使用。环境变量因操作系统而异，因此需要遵循操作系统的相关指南进行设置。

下表显示了各个 toolchain Package 所需的总磁盘空间：

| Toolchain Package | 所需磁盘空间 |
| --- | ---: |
| `com.unity.toolchain.linux-x86_64` | 462 MB |
| `com.unity.toolchain.macos-x86_64-linux-x86_64` | 2 GB |
| `com.unity.toolchain.win-x86_64-linux-x86_64` | 2 GB |

## 使用 Linux IL2CPP 交叉编译器

如果满足本页列出的所有前置条件，就可以将项目构建为 Linux Player。Unity 会在构建时自动使用 Linux IL2CPP 交叉编译器。

要构建 Linux Player，请执行以下步骤：

1. 打开 **Build Profiles** 窗口（菜单：**File > Build Profiles**）。
2. 在 **Platforms** 面板的平台列表中选择 **Linux**，或为 **Linux** 平台[创建构建配置](https://docs.unity3d.com/6000.7/Documentation/Manual/create-build-profile.html)。
3. 选择 **Switch Platform**。
4. 选择 **Build** 或 **Build And Run**。

## 其他资源

- [如何在 Unity Editor 中添加模块](https://docs.unity.com/hub/add-modules)
- [Linux Build Settings 平台文档](https://docs.unity3d.com/6000.7/Documentation/Manual/Buildsettings-linux.html)
- [Linux Player 设置](https://docs.unity3d.com/6000.7/Documentation/Manual/PlayerSettings-linux.html)
- [[04-额外IL2CPP编译器参数]]


---

## 文档导航

- 上一页：[[04-额外IL2CPP编译器参数]]
- 目录：[[00-IL2CPP脚本后端]]
- 下一页：[[06-IL2CPP限制]]
