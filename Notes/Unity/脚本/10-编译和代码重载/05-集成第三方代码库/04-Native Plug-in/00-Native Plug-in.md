# Native Plug-in

> 原文：[Native plug-ins](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native.html)

Unity 支持 Native **Plug-in**。Native Plug-in 是使用 C、C++ 和 Objective-C 等 Language 编写的 Unmanaged Code Library。Plug-in 让你编写的 Managed Code 可以调用这些 Library 中的 Function。借助此功能，你可以集成 Middleware Library，并复用现有的 C/C++ Code。既可以使用预编译 Library，也可以将 Source Code File 作为 Plug-in 使用。使用 Source Code 时，Unity 会静态编译并链接 Plug-in Code。

| Topic | Description |
| --- | --- |
| [[01-Unity中的Native Plug-in简介]] | 如何导入和使用 Native Plug-in。 |
| [[02-调用函数/00-调用函数]] | 如何从 Managed C# Code 调用 Native Plug-in 中的 Unmanaged Function，以及如何从 Unmanaged Code 回调 Managed Code。 |
| [[03-在托管和非托管代码间传递数据/00-传递数据]] | 如何在 Managed Code 与 Unmanaged Code 之间交换数据。 |

**Note**：Unity 还提供了一组 Native API，让你可以创建并使用直接与 Rendering、Profiling 和 Logging 等 Unity Engine System 交互的 Plug-in。使用这些 API 时，Native Plug-in 可以直接与 Unity Runtime 互操作，而无需经过 Managed Application Code。Unity 会自动发现并加载使用这些 API 的 Plug-in。更多信息请参阅 [Native plug-in APIs](https://docs.unity3d.com/6000.7/Documentation/Manual/native-plugin-interface.html)。使用这些 API 的 Native Plug-in 示例请参阅 [Native Rendering Plugin](https://github.com/Unity-Technologies/NativeRenderingPlugin)。

关于 Native Plug-in 的 Platform-specific Information，请参阅 [Platform development](https://docs.unity3d.com/6000.7/Documentation/Manual/PlatformSpecific.html) 下的相关部分。

## 其他资源

- [Low-level native plug-in interface](https://docs.unity3d.com/6000.7/Documentation/Manual/native-plugin-interface.html)
- [Platform development](https://docs.unity3d.com/6000.7/Documentation/Manual/PlatformSpecific.html)
- [DllImportAttribute](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.dllimportattribute?view=net-7.0)
- [Mono Interop with native libraries](https://www.mono-project.com/docs/advanced/pinvoke/)
- [Consuming Unmanaged DLL Functions](https://learn.microsoft.com/en-us/dotnet/framework/interop/consuming-unmanaged-dll-functions)
- [Marshalling Data with Platform Invoke](https://learn.microsoft.com/en-us/dotnet/framework/interop/marshalling-data-with-platform-invoke)

---

## 文档导航

- 上一页：[[../04-为桌面平台构建Plug-in]]
- 目录：[[../00-集成第三方代码库]]
- 下一页：[[01-Unity中的Native Plug-in简介]]
