# DllImport Attribute

> 原文：[DllImport attribute](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-dllimport.html)

使用 `DllImportAttribute` 标识 Scripting Runtime 可以从哪里找到 Unmanaged Function。对于运行时加载的 Dynamic Library，在 Attribute 中使用 Library File Name。如果省略 File Extension 以及 POSIX Platform 使用的 `lib` Prefix，Library 会按照 Platform Convention 加载：

- **Windows**：添加 `.dll` File Extension。例如，将 “MyLibraryName” 作为 “MyLibraryName.dll” 加载。
- **POSIX**（macOS、iOS、Android 等）：添加常见 File Extension（`.so`、`.dll`、`.dylib`、`.bundle`），并尝试带 `lib` Prefix 和不带 Prefix 的名称。例如，将 “MyLibraryName” 作为以下名称加载：

  - MyLibraryName.bundle、libMyLibraryName.bundle
  - MyLibraryName.dll、libMyLibraryName.dll
  - MyLibraryName.dylib、libMyLibraryName.dylib
  - MyLibraryName.so、libMyLibraryName.so

此机制允许你在 `DllImportAttribute` 中指定基础 Library Name，并让 Library 在多个 Platform 上成功加载。也可以指定带 Extension 的精确 File Name。

以下示例可跨 Platform 工作（假设已经将每个 Platform 所需的 Library File 添加到 Unity Project）：

```csharp
[DllImport("SimpleMath")]
static extern float AddTwoFloats(float f1, float f2);
```

以下示例只在 macOS 和 Apple Mobile Platform 上工作，因为它显式指定了 `.bundle` File：

```csharp
[DllImport("libStringUtilities.bundle")]
static extern void SendStringArray([In] string[] strings, int length);
```

对于静态链接 Library 和 Source Code Plug-in，将字符串 `__Internal`（两个前导下划线字符）用作 `DllImportAttribute` Value：

```csharp
[DllImport("__Internal")]
static extern int AddTwoIntegers(int i1, int i2);
```

**Notes**：

- Unity 只支持在 Android 和 Apple Mobile Platform 上对预编译 Library 进行静态链接。
- Unity 只在使用 IL2CPP Scripting Backend 时支持 Source Code Plug-in。

---

## 文档导航

- 上一页：[[04-NativeArrays]]
- 目录：[[00-Native Plug-in]]
- 下一页：[[00-脚本序列化]]
