# Native Plug-in Shader Compiler API

> 原文：[Native plug-in API for shader compiler](https://docs.unity3d.com/6000.7/Documentation/Manual/low-level-native-plugin-shader-compiler-access.html)

使用 Unity Low-level Shader Compiler API 将不同 Variant 注入 Shader。这是一种 Event-Driven 方法：当特定内置 Event 发生时，Plug-in 会接收 Callback。

Unity 暴露的 Shader Compiler Access Extension 定义位于 `IUnityShaderCompilerAccess.h` Header File 中，该文件位于 [[01-Native Plug-in API简介#Plugin API 文件夹|PluginAPI 文件夹]]。

> **Note**：这些 Extension 当前只支持 D3D11。`IUnityShaderCompilerAccess.h` 只能作为 C++ 编译。尝试将其作为 C 编译会产生 [[01-Native Plug-in API简介#接口兼容性|兼容性错误]]。

## Shader Compiler Access Extension API

要使用该 Rendering Extension，Plug-in 必须导出 `UnityShaderCompilerExtEvent`。关于如何实现此 API，请参阅 `IUnityShaderCompilerAccess.h` Header File 中的 Code Comment。

每当 Unity 触发内置 Event 之一时，Plug-in 都会通过 `UnityShaderCompilerExtEvent` 接收 Callback。也可以在 Script 中通过 `CommandBuffer.IssuePluginEventAndData` 或 `CommandBuffer.IssuePluginCustomBlit` Command 将 Callback 添加到 CommandBuffer。

除了基本的 Script Interface 外，Unity 中的 Native Plug-in 还可以在特定 Event 发生时接收 Callback。这主要用于在 Plug-in 中实现 Low-level Rendering，并使其支持 Unity 的 Multithreaded Rendering。

## Shader Compiler Access Configuration Interface

Unity 提供 `IUnityShaderCompilerExtPluginConfigure` Interface，用于配置 Shader Compiler Access。Plug-in 可以使用此 Interface 保留自己的 Keyword，并配置 Shader Program 和 GPU Program Compiler Mask。这决定了要为哪些 Shader Type 或 GPU Program 调用 Plug-in。

## 其他资源

- [[03-内存管理API]]
- [[07-性能分析API]]
- [[02-日志API]]

---

## 文档导航

- 上一页：[[05-图形和渲染API]]
- 目录：[[00-Native Plug-in API]]
- 下一页：[[03-内存管理API]]
