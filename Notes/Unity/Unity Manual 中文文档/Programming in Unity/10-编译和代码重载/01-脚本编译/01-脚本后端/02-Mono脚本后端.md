# Mono 脚本后端

> 原文：[Mono scripting back end](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-mono.html)

Mono 脚本后端是 Unity 对开源 Mono 项目的分支。Mono 是成熟的跨平台 .NET Runtime，为兼容的平台提供 Unity Editor 和 Player 的运行环境。它迭代速度快、工具支持良好，但 Runtime 性能低于 IL2CPP，并且与最新 .NET 功能并不完全一致。

Mono 使用 JIT 编译在 Runtime 将 C# 代码转换为机器码。Mono 管理托管对象的生命周期，处理代码重载，并使用 Boehm-Demers-Weiser 垃圾回收器自动回收超出作用域的对象。垃圾回收器的行为可以进行一定程度的配置。

Mono 支持托管代码调试。

## 使用 Mono 构建项目

打开 **File > Build Profiles**，然后选择 **Build** 开始构建。

可以通过以下两种方式更改 Unity 构建应用时使用的脚本后端：

1. 在 Editor 中打开 **Edit > Project Settings**，点击 **Player Settings**，在当前平台的 **Player** 设置中进入 **Other Settings > Configuration**，从 **Scripting Backend** 下拉菜单选择 **Mono**。也可以在 **File > Build Profiles** 中打开 **Player Settings** 标签。
2. 通过 Editor scripting API 使用 `PlayerSettings.SetScriptingBackend` 更改脚本后端。

Mono 和 IL2CPP 都要求针对每个目标平台分别进行一次新构建。例如，同时支持 Android 和 iOS 时，需要构建两次并生成一个 Android 二进制文件和一个 iOS 二进制文件。

## Domain Reload

Unity Editor 内嵌 Mono，因此在 Editor 的 Play mode 中运行时，C# 代码由 Mono 管理并受 Mono 限制。修改脚本会触发 AppDomain reload。还可以配置 Unity 进入 Play mode 的方式，使 Editor 在进入 Play mode 时执行 domain reload，从而重置静态状态。

如果保持默认的关闭 domain reload 设置，代码必须通过其他方式处理静态状态的重置。有关配置方式，请参阅“不进行 domain reload 进入 Play mode”。

## 优化 Mono 构建

Mono 和 IL2CPP 使用相同的基础 .NET 类库，因此许多性能问题和最佳实践适用于两者。但在 Mono 上下文中，还应注意以下事项：

- Mono 使用 JIT，在大型代码库中可能比 IL2CPP 的 AOT 编译具有更低的 Runtime 性能和更长的启动时间。始终使用 Unity Profiler 查找 GC 和 JIT 热点；Project Auditor 也可以帮助识别和修复常见性能问题。
- 会在 Runtime 产生大量分配的编码方式会增加垃圾回收器开销并降低性能。应遵循 Unity 托管内存代码优化指南。
- Unity API 通常不是线程安全的，必须从 Unity 主线程调用。避免将 .NET `Task` 用于 Unity API；对于本身是异步且运行时间较长的操作，可以使用 `Awaitable` 类作为更高效的替代方案。
- 对于生命周期较短但计算密集的并行工作，可以使用 Job System，并通过 Burst 编译。
- Mono 对 `DateTime`、`TimeZoneInfo` 和 `CultureInfo` 的实现可能与 Windows .NET 行为不同。务必在目标平台上测试全球化和 Culture 相关代码。

## 使用 Burst 优化 Runtime 性能

在适合的项目中，可以将 Burst compiler 与 Mono 一起使用，把兼容代码部分编译为高度优化的机器码，从而提高项目的 Runtime 性能。

---

## 文档导航

- 上一页：[[01-脚本后端简介]]
- 目录：[[00-脚本后端]]
- 下一页：[[00-IL2CPP脚本后端]]
