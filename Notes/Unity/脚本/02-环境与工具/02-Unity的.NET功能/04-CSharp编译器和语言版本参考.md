# C# Compiler 和语言版本参考

> 原文：[C# compiler and language version reference](https://docs.unity3d.com/6000.7/Documentation/Manual/csharp-compiler.html)

当前版本的 Unity Editor 使用以下 C# Compiler 和语言版本：

- C# Compiler：Roslyn
- C# Language Version：C# 9.0

Editor 会向 C# Compiler 传递一组默认选项。若要在项目中传递额外选项，请参阅 [[../../10-编译和代码重载/01-脚本编译/03-条件编译/00-条件编译]]。

## Garbage Collection

默认情况下，Unity 的 Mono 和 IL2CPP Scripting Backend 都使用 Boehm-Demers-Weiser Garbage Collector，并启用 Incremental 模式。关于可用的 Garbage Collection 模式、它们的含义以及切换方式，请参阅 Unity 的 Garbage Collection 模式说明。

CoreCLR Scripting Backend 使用自己的、不同的 Garbage Collector，并且不能配置 Incremental 模式。

## 不支持的 C# 功能

Unity 使用 C# 9.0，但不支持以下功能：

- 抑制 `localsinit` 标志
- Covariant Return Types
- Module Initializers
- Unmanaged Function Pointers 的可扩展 Calling Convention
- Init-only Setters

如果在项目中使用不支持的功能，编译会生成错误。

## Record 支持

C# 9 的 `init` 和 `record` 支持存在一些限制。

完整的 Record 支持需要 `System.Runtime.CompilerServices.IsExternalInit` 类型，因为它使用 Init-only Setter；但该类型只在 .NET 5 及更高版本中提供，而 Unity 不支持这些版本。可以在自己的项目中声明 `System.Runtime.CompilerServices.IsExternalInit` 类型来绕过此问题。

不要在可序列化类型中使用 C# Record，因为 Unity 序列化系统不支持 C# Record。

## Unmanaged Function Pointer 支持

Unity 支持 C# 9 引入的 Unmanaged Function Pointer，但不支持可扩展 Calling Convention。下面的示例展示了如何正确使用 Unmanaged Function Pointer。

此示例面向 Windows 平台，并要求在 Player Settings 中启用 **Allow 'unsafe' Code**。启用路径为 **Project Settings > Player > Other Settings > Script Compilation**。关于 C# Unsafe Context，请参阅 Microsoft 的 [unsafe（C# Reference）文档](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code) 和 [Unsafe code、指针类型与 Function Pointer 文档](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code)。

```csharp
using System;
using System.Runtime.InteropServices;
using UnityEngine;

public class UnmanagedFunctionPointers : MonoBehaviour
{
    [DllImport("kernel32.dll")]
    static extern IntPtr LoadLibrary(string lpLibFileName);

    [DllImport("kernel32.dll")]
    static extern IntPtr GetProcAddress(IntPtr hModule, string lpProcName);

    // 必须在 Player Settings 中启用 Allow 'unsafe' Code。
    unsafe void Start()
    {
        #if UNITY_EDITOR_WIN || UNITY_STANDALONE_WIN
        // 此示例只适用于 Windows。
        IntPtr kernel32 = LoadLibrary("kernel32.dll");
        IntPtr getCurrentThreadId =
            GetProcAddress(kernel32, "GetCurrentThreadId");

        // 获取 Unmanaged Function Pointer。
        delegate* unmanaged[Stdcall]<UInt32> getCurrentThreadIdUnmanagedStdcall =
            (delegate* unmanaged[Stdcall]<UInt32>)getCurrentThreadId;

        Debug.Log(getCurrentThreadIdUnmanagedStdcall());
        #endif
    }
}
```

---

## 其他资源

- [[01-.NET API兼容级别]]
- [[../../10-编译和代码重载/01-脚本编译/03-条件编译/00-条件编译]]

## 文档导航

- 上一页：[[03-添加.NET Framework类库引用]]
- 目录：[[00-Unity的.NET功能]]
- 下一页：[[../../03-Unity基础类型/00-Unity基础类型]]
