# Unity 中的 Native Plug-in 简介

> 原文：[Introduction to native plug-ins in Unity](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-overview.html)

Native Plug-in 提供一个可以从 Managed（C#）Script 访问的 C Interface。

Unity Native Plug-in 支持使用标准 .NET [Platform invoke](https://learn.microsoft.com/en-us/dotnet/framework/interop/consuming-unmanaged-dll-functions) 功能。该功能允许 C# Code 调用由 Native Code Library 导出的 Unmanaged Function。它使用称为 [Marshalling](https://learn.microsoft.com/en-us/dotnet/framework/interop/marshalling-data-with-platform-invoke) 的过程在 Managed Code 和 Unmanaged Code 之间传输数据。

Native Plug-in 示例请参阅 Github 上的 [Simplest Plug-in example](https://github.com/Unity-Technologies/DesktopSamples/tree/master/SimplestPluginExample)。

## 导入 Native Plug-in

可以用两种基本形式将 Native Plug-in 导入 Unity Project：

- 针对特定 Platform 和 CPU Architecture 预编译的 Binary File。
- 作为 Unity Project Build Process 一部分进行编译的 Source Code File。
  （要将 Source Code File 作为 Native Plug-in 使用，Project 必须使用 IL2CPP Scripting Backend。）

要在 Unity 中工作，Native Plug-in 必须使用 C Linkage 导出其 External Function。这种 Linkage 可以避免 C++ Name Mangling 及其他 Application Binary Interface（ABI）问题。

要从 Managed C# Code 访问 Unmanaged Function，需要声明一个名称相同、返回类型和参数类型兼容的 C# `static extern` Function，然后像调用其他 Method 一样调用它。完整的声明规则和示例请参阅 [[00-调用函数]]。

Unity 在 Apple Mobile Platform（iOS、tvOS 和 visionOS）以及 Android 上支持预编译 Static Library。作为 Source Code File 导入 Unity Project 的 Plug-in 也会被静态链接。Unity 在使用 IL2CPP Scripting Backend 的 Project 中支持 Source Code Plug-in。Editor Script 或 Play Mode 中运行的 Code 不支持 Source Code Plug-in。

将 Plug-in File 导入 Unity Project 后，必须设置决定何时加载 Library 的属性。为此，请在 Unity Project Panel 中选中导入的 File，并在 Inspector 中设置相关属性。更多信息请参阅 [Change plug-in settings](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-in-inspector.html#change-plug-in-settings)。

**Note**：在 Unity Editor Session 中加载 Native Plug-in 后——无论是通过 Editor Script 加载，还是在 Play Mode 中加载——Editor 都无法卸载它。要在 Editor Process 加载 Native Plug-in 后更新它（无论是预编译 Binary 还是 Source Code File），必须重启 Editor Application。否则，Editor 会继续使用已加载的 Plug-in 版本，而不是更新后的版本。

## 与 Native Plug-in 互操作

你在 Unity 中编写的 C# Code 由 Scripting Runtime 管理。Scripting Runtime 管理数据在内存中的存储位置，并会定期移动数据以避免内存碎片。另一方面，Native Plug-in 中的 Unmanaged Code 直接处理自己的内存，并可以使用 Pointer 指向特定的内存位置。编写与 Unmanaged Code 互操作的 Managed Code 时，必须注意数据存储的位置、访问数据的时间，以及哪一侧负责释放不再需要的内存。

某些 Data Type 在 Managed Code 和 Native Code 中的表示方式不同。.NET 提供 Interop Marshaller，为大多数 Type 提供默认表示和转换。在默认行为不正确或不是最优选择的情况下，.NET Interop Services API 提供以下 Attribute，让你可以为特定 Data Type 明确定义所需的表示和转换：

- [StructLayoutAttribute](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.structlayoutattribute)
- [MarshallAsAttribute](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.marshalasattribute)
- [FieldOffsetAttribute](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.fieldoffsetattribute)

更多信息请参阅 [[00-传递数据]]。

## Native Plug-in 基本示例

一个带有单个 Function 的简单 C-language Native Library 可能如下：

```c
float ExamplePluginFunction ()
{
    return 5.0F;
}
```

**Note**：为简洁起见，此最小示例省略了 Export Annotation。预编译 Dynamic Library（例如下面使用 `[DllImport("PluginName")]` 导入的 Library）必须导出其 Function。各 Platform 导出 Function 所需的 `EXPORT_API` Annotation，请参阅 [Call unmanaged functions from managed code](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-invoke-unmanaged.html)。

如果单独编译了此 Code 并将编译好的 Library 导入 Unity Project，可以使用以下 C# Script 调用 `ExamplePluginFunction()`：

```csharp
using UnityEngine;
using System.Runtime.InteropServices;

class ExampleScript : MonoBehaviour
{
    // Use the library file name for dynamically linked libraries.
    [DllImport ("PluginName")]
    private static extern float ExamplePluginFunction ();

    void Awake ()
    {
        // Calls the ExamplePluginFunction inside the plugin
        // And prints 5 to the console
        Debug.Log (ExamplePluginFunction ());
    }
}
```

如果以 Source Code 形式导入 Native Code，则必须在 DllImport Attribute 中使用 `__Internal`，而不是 Library Name：

```csharp
using UnityEngine;
using System.Runtime.InteropServices;

class ExampleScript : MonoBehaviour
{
    // Use __Internal instead of the library name for source-code plug-ins.
    [DllImport ("__Internal")]
    private static extern float ExamplePluginFunction ();

    void Awake ()
    {
        // Calls the ExamplePluginFunction inside the plugin
        // And prints 5 to the console
        Debug.Log (ExamplePluginFunction ());
    }
}
```

关于如何确定要加载的 Native Plug-in Library，详见 [[04-DllImport属性]]。

## 其他资源

Managed Code 与 Unmanaged Code 之间的互操作是一个复杂主题。本 Documentation 仅用于简要介绍。要更深入地理解该主题，请参阅以下 .NET Documentation：

- [Interop Marshalling](https://learn.microsoft.com/en-us/dotnet/framework/interop/interop-marshalling)
- [Default Marshalling Behavior](https://learn.microsoft.com/en-us/dotnet/framework/interop/default-marshalling-behavior)
- [Marshalling Data with Platform Invoke](https://learn.microsoft.com/en-us/dotnet/framework/interop/marshalling-data-with-platform-invoke)

**Note**：本文讨论的是 **Platform Invoke** Interop Model。不过，你也可以使用 Microsoft .NET Documentation 中讨论的 COM Interop Model。

---

## 文档导航

- 上一页：[[04-为桌面平台构建Plug-in]]
- 目录：[[00-Native Plug-in]]
- 下一页：[[00-调用函数]]
