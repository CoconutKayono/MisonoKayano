# Native Plug-in 和内部调用支持

> 原文：[Native plug-in and internal call support](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics-dllimport.html)

要调用 Native 函数，请使用 [`[DllImport]`](https://docs.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.dllimportattribute?view=net-6.0)：

```csharp
[DllImport("MyNativeLibrary")]
public static extern int Foo(int arg);
```

Burst 还支持 Unity 内部实现的内部调用：

```csharp
// UnityEngine.Mathf 中
[MethodImpl(MethodImplOptions.InternalCall)]
public static extern int ClosestPowerOfTwo(int value);
```

`DllImport` 只支持 [Native Plug-in](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native.html)，不支持 `kernel32.dll` 这类依赖平台的库。

对于所有 `DllImport` 和内部调用，参数或返回值只能使用以下类型：

| 类型 | 支持的类型 |
| --- | --- |
| 内置类型和 intrinsic 类型 | `byte` / `sbyte`、`short` / `ushort`、`int` / `uint`、`long` / `ulong`、`float`、`double`、`System.IntPtr` / `System.UIntPtr`、`Unity.Burst.Intrinsics.v64` / `Unity.Burst.Intrinsics.v128` / `Unity.Burst.Intrinsics.v256` |
| 指针和引用 | `sometype*`：指向本表中其他类型的指针；`ref sometype`：对本表中其他类型的引用。 |
| 句柄结构体 | `unsafe struct MyStruct { void* Ptr; }`：包含单个指针字段的结构体；`unsafe struct MyStruct { int Value; }`：包含单个整数字段的结构体。 |

**注意**：不支持按值传递结构体；必须通过指针或引用传递。唯一的例外是句柄结构体。句柄结构体是只包含一个指针类型或整数类型字段的结构体。

## 相关资源

- [HPC# 概览](01-高性能CSharp简介.md)
- [Burst intrinsics 概览](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics.html)

---

## 文档导航

- 上一页：[[08-CSharp和.NET类型支持]]
- 目录：[[00-CSharp语言支持]]
- 下一页：[[../07-Burst Intrinsics/00-Burst Intrinsics]]
