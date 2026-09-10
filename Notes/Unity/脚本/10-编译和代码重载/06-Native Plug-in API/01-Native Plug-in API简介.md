# Native Plug-in API 简介

> 原文：[Introduction to native plug-in API](https://docs.unity3d.com/6000.7/Documentation/Manual/native-plugin-interface-introduction.html)

除用于编写 Managed Code 的公开 C# API 外，Unity 还提供一个较小的 Native Interface，可以让 Native Plug-in 访问 Unity Editor 和 Engine 的功能。

<a id="plugin-api-folder"></a>

## Plugin API 文件夹

Native Interface 是一组与 C 或 C++ 兼容的 Header（`.h`）文件，随 Unity Editor 一起安装。这些文件位于 `PluginAPI` 文件夹中，具体位置取决于所使用的 Operating System：

- **Windows**：`<UnityInstallPath>\Editor\Data\PluginAPI`。
- **macOS**：右键点击 Unity Application，选择 **Show Package Contents**。Header 位于 `Contents/Resources/PluginAPI` 文件夹中。
- **Linux**：`<UnityInstallPath>/Editor/Data/PluginAPI`。

每个 Header 文件都在其中以 Code Comment 的形式包含额外文档。关于如何开始实现 Native Interface，请参阅主 Header 文件 `IUnityInterface.h` 中的 Code Comment。

<a id="compatibility"></a>

## 接口兼容性

所有 Unity Native Plug-in API Header File 都兼容使用 C++ 编写的 Plug-in，但只有部分 Header File 兼容使用 C 编写的 Plug-in。

如果尝试将不兼容 C 的文件作为 C 编译，文件会报告错误：`"This file cannot be compiled in a C environment"`。Header File 源码中也包含对应的检查：

```cpp
#ifndef __cplusplus
#error "This file cannot be compiled in a C environment"
#endif
```

## 接口注册表

为了处理 Unity 的主要事件，Plug-in 必须导出 `UnityPluginLoad` 和 `UnityPluginUnload` 函数。`IUnityInterfaces` 使 Plug-in 能够访问这些函数；它们位于 Plug-in API 的 `IUnityInterface.h` 中。

下面的示例使用 `IUnityInterfaces` 将 `IUnityGraphics` Interface 加载到一个 Pointer 中。这是一个标准方法，可以重复使用它从 Native Plug-in API 加载其他 Interface：

```cpp
#include "IUnityInterface.h"
#include "IUnityGraphics.h"
// Unity plugin load event
extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API
    UnityPluginLoad(IUnityInterfaces* unityInterfaces)
{
    IUnityGraphics* graphics = unityInterfaces->Get<IUnityGraphics>();
}
```

## 其他资源

- [[05-图形和渲染API]]
- [[06-Shader Compiler API]]
- [[03-内存管理API]]
- [[07-性能分析API]]
- [[02-日志API]]

---

## 文档导航

- 上一页：[[00-Native Plug-in API]]
- 目录：[[00-Native Plug-in API]]
- 下一页：[[05-图形和渲染API]]
