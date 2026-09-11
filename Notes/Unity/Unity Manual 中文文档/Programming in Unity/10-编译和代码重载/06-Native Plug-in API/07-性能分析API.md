# Native Plug-in Profiling API

> 原文：[Native plug-in API for profiling](https://docs.unity3d.com/6000.7/Documentation/Manual/LowLevelNativePluginProfiler.html)

可以使用 Low-level Native Plug-in Profiler API 扩展 [Profiler](https://docs.unity3d.com/6000.7/Documentation/Manual/profiler-introduction.html)，收集 Native Plug-in Code 的性能数据，或准备将 Profiling Data 发送到第三方 Profiling Tool，例如 Razor（PS4）、PIX（Xbox、Windows）、Chrome Tracing、ETW、ITT、Vtune 或 Telemetry。

Low-level Native Plug-in Profiler API 提供以下 Interface，用于 Unity Profiler 与外部工具之间的通信：

- **IUnityProfiler**：使用此 Interface 从 Native Plug-in Code 向 Unity Profiler 添加 Instrumentation Event。
- **IUnityProfilerCallbacks**：使用此 Interface 拦截 Unity Profiler Event，并将其存储或重定向到其他 Tool。

## IUnityProfiler API 参考

使用 `IUnityProfiler` Plug-in API 向 Native Plug-in 添加 Instrumentation。Plug-in API 由 `IUnityProfiler` Interface 表示，该 Interface 声明在 `IUnityProfiler.h` Header 中，位于 [[01-Native Plug-in API简介#Plugin API 文件夹|PluginAPI 文件夹]]。

| Method | Description |
| --- | --- |
| `CreateMarker` | 创建一个表示具名 Instrumentation Scope 的 Profiler Marker，随后可以用它生成 Instrumentation Sample。 |
| `SetMarkerMetadataName` | 指定可随 Instrumentation Sample 传递的 Profiler Marker 自定义参数名称。 |
| `BeginSample` | 开始一个以 Profiler Marker 命名的 Code Instrumentation Section。 |
| `EndSample` | 结束一个 Instrumentation Section。 |
| `EmitEvent` | 发出带 Metadata 的 Generic Event。 |
| `IsEnabled` | 如果 Profiler 正在捕获 Data，则返回 1。 |
| `IsAvailable` | Profiler 可用的 Editor 或 Development Player 返回 1，Release Player 返回 0。 |
| `RegisterThread` | 以指定名称注册当前 Thread。 |
| `UnregisterThread` | 从 Profiler 注销当前 Thread。 |

### IUnityProfiler 示例

以下示例生成可由 Profiler Window 显示的 Profiler Event：

```cpp
#include <IUnityInterface.h>
#include <IUnityProfiler.h>

static IUnityProfiler* s_UnityProfiler = NULL;
static const UnityProfilerMarkerDesc* s_MyPluginMarker = NULL;
static bool s_IsDevelopmentBuild = false;

static void MyPluginWorkMethod()
{
    if (s_IsDevelopmentBuild)
        s_UnityProfiler->BeginSample(s_MyPluginMarker);

    // Code I want to see in Unity Profiler as "MyPluginMethod".
    // ...

    if (s_IsDevelopmentBuild)
        s_UnityProfiler->EndSample(s_MyPluginMarker);
}

extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API UnityPluginLoad(IUnityInterfaces* unityInterfaces)
{
    s_UnityProfiler = unityInterfaces->Get<IUnityProfiler>();
    if (s_UnityProfiler == NULL)
        return;
    s_IsDevelopmentBuild = s_UnityProfiler->IsAvailable() != 0;
    s_UnityProfiler->CreateMarker(&s_MyPluginMarker, "MyPluginMethod", kUnityProfilerCategoryOther, kUnityProfilerMarkerFlagDefault, 0);
}

extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API UnityPluginUnload()
{
    s_UnityProfiler  = NULL;
}
```

## IUnityProfilerCallbacks API Callback

Native Profiler Plug-in API 在 Unity Subsystem 与第三方 Profiling API 之间提供一个 Interface，因此可以使用外部 Profiling Tool 分析 Unity Application。`IUnityProfilerCallbacks` Header 暴露此 API，该 Header 位于 Unity Installation 的 `<UnityInstallPath>\Editor\Data\PluginAPI` 文件夹中。例如，在 macOS 上右键点击 Unity Application 并选择 **Show Package Contents**，Header 位于 `Contents/Resources/PluginAPI` 文件夹中。

以下 Unity Profiler Feature 有助于捕获 Instrumentation Data，以便分析 Application 的性能：

| Profiler Feature | Description |
| --- | --- |
| **Categories** | Unity 将 Profile Data 分组到 Category（例如 Rendering、Scripting 和 Animation），并为每个 Category 分配一种颜色。带颜色的 Category 有助于在 Profiler Window 中直观区分 Data 类型。Profiler Native Plug-in API 会检索这些颜色，因此可以在外部 Profiling Tool 中使用它们。 |
| **Usage flags** | Usage Flag 充当 Filter，减少 Unity 发送给外部 Profiling Tool 的 Data 量。可以使用 Usage Flag 在 Unity 将 Profiling Data 发送到外部 Tool 前移除不必要的信息。Profiler 对 Event Marker 应用以下 Usage Flag，以便 Filter Data：<br><br>**Availability flags**：标记 Marker 在 Unity Editor、Development Player 还是 Release Player 中是否可用。<br><br>**Verbosity levels**：与 Editor 中正在执行的任务类型及其所需的信息级别有关（例如 Internal、Debug 或 User Level）。 |
| **Frame events** | 可以使用 Profiler Native Plug-in API 在外部 Profiling Tool 中执行 Frame-Time Analysis。 |
| **Thread profiling** | Unity 会在线程上执行大量工作（例如 Main Thread、Render Thread 和 Job System Worker Thread）。可以使用 Profiler Native Plug-in API 在任意 Thread 上启用 Profiling。 |

要在集成第三方 Profiler 的 C/C++ Plug-in Code 中使用 Unity Profiler 生成的 Instrumentation Data，可以使用以下最小 Callback 集合：

| Callback | Function |
| --- | --- |
| `RegisterCreateCategoryCallback` | 注册一个 `IUnityProfilerCreateCategoryCallback` Callback，每当 Unity 创建 Category 时获取 Profiler Category Name 和 Color。 |
| `RegisterCreateMarkerCallback` | 注册一个 `IUnityProfilerCreateMarkerCallback` Callback，每当 Unity 创建 Marker 时调用。使用它获取 Marker 的 Name、Profiler Category 和 Usage Flag。Callback Function 的 `const UnityProfilerMarkerDesc* markerDesc` 参数表示一个持久 Pointer，指向 Marker Description；可以在 `RegisterMarkerEventCallback` 中使用它 Filter Marker。 |
| `RegisterMarkerEventCallback` | 注册一个 `IUnityProfilerMarkerEventCallback` Callback，Unity 在 Single-Shot、Scoped、Memory Allocation 或 Garbage Collection Event 发生时调用它。随后可以使用此 Callback 调用外部 Profiling Tool 中的相关 Function。**Note**：Unity 使用 `GC.Alloc` Marker 表示 Memory Allocation Event，使用 `GC.Collect` Marker 表示 Garbage Collection Event。 |
| `RegisterFrameCallback` | 将 Sample 封装到 Logical Frame 中，使不使用 Frame 的外部 Profiling Tool 能够使用这些 Sample。同时注册一个 Callback，在 Unity 开始下一个 Logical CPU Frame 时运行。 |
| `RegisterCreateThreadCallback` | 注册一个 Callback，在 Unity 为 Profiling 注册 Thread 时获取其 Internal Thread Name。 |

### IUnityProfilerCallbacks 示例

此示例展示如何将 Unity Profiler Event 传递给使用 Push/Pop Semantics 的另一个 Profiler。它提供两个函数：

- `void MyProfilerPushMarker(const char* name)`：Push 一个具名 Marker。
- `void MyProfilerPopMarker()`：Pop Instrumentation Marker。

下面的示例提供将 Begin 和 End Instrumentation Event 从 Unity Profiler 传递给外部 Profiler 所需的最小实现：

```cpp
#include <IUnityInterface.h>
#include <IUnityProfilerCallbacks.h>

static IUnityProfilerCallbacks* s_UnityProfilerCallbacks = NULL;

static void UNITY_INTERFACE_API MyProfilerEventCallback(const UnityProfilerMarkerDesc* markerDesc, UnityProfilerMarkerEventType eventType, unsigned short eventDataCount, const UnityProfilerMarkerData* eventData, void* userData)
{
    switch (eventType)
    {
        case kUnityProfilerMarkerEventTypeBegin:
        {
            MyProfilerPushMarker(markerDesc->name);
            break;
        }
        case kUnityProfilerMarkerEventTypeEnd:
        {
            MyProfilerPopMarker();
            break;
        }
    }
}

static void UNITY_INTERFACE_API MyProfilerCreateMarkerCallback(const UnityProfilerMarkerDesc* markerDesc, void* userData)
{
    s_UnityProfilerCallbacks->RegisterMarkerEventCallback(markerDesc, MyProfilerEventCallback, NULL);
}

extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API UnityPluginLoad(IUnityInterfaces* unityInterfaces)
{
    s_UnityProfilerCallbacks = unityInterfaces->Get<IUnityProfilerCallbacks>();
    s_UnityProfilerCallbacks->RegisterCreateMarkerCallback(&MyProfilerCreateMarkerCallback, NULL);
}

extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API UnityPluginUnload()
{
    s_UnityProfilerCallbacks->UnregisterCreateMarkerCallback(&MyProfilerCreateMarkerCallback, NULL);
    s_UnityProfilerCallbacks->UnregisterMarkerEventCallback(NULL, &MyProfilerEventCallback, NULL);
}
```

> **Note**：要从所有 Marker 注销给定 Callback，请将第一个参数设置为 `null`，运行 `UnregisterEventCallback`。

### UnitySystracePlugin 示例

可以每帧动态注册和注销 Marker Callback。以下示例根据第三方 Profiler 的状态启用和禁用 Callback，以减少 Profiling Overhead。

```cpp
| static void UNITY_INTERFACE_API SystraceFrameCallback(void* userData)
{
    bool isCapturing = ATrace_isEnabled();
    if (isCapturing != s_isCapturing)
    {
        s_isCapturing = isCapturing;
        if (isCapturing)
        {
            s_UnityProfilerCallbacks->
              RegisterCreateMarkerCallback(SystraceCreateEventCallback, NULL);
        }
        else
        {
            s_UnityProfilerCallbacks->
              UnregisterCreateMarkerCallback(SystraceCreateEventCallback, NULL);
            s_UnityProfilerCallbacks->
              UnregisterMarkerEventCallback(NULL, SystraceEventCallback, NULL);
        }
    }
}
```

> **Note**：要从所有 Marker 注销给定 Callback，请将第一个参数设置为 `null`，运行 `UnregisterEventCallback`。

## Special Marker

Unity 有以下包含有用 Metadata 的 Special Marker：

- `Profiler.DefaultMarker`
- `GC.Alloc`

### Profiler.DefaultMarker

`Profiler.DefaultMarker` 是 Unity 为 [`Profiler.BeginSample`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Profiling.Profiler.BeginSample.html) 和 [`Profiler.EndSample`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Profiling.Profiler.EndSample.html) Event 保留的 Marker。

在上一个示例中，`kUnityProfilerMarkerEventTypeBegin eventType` 对应 `Profiler.BeginSample` Event，并包含以下 Data：

- **Int32**：`UnityEngine.Object` Instance ID。如果未指定 Object，则为 0。
- **UInt16 array**：传递给 `Profiler.BeginSample` 的 UTF16 String。大小单位为 Byte。
- **UInt32**：Category Index。

### GC.Alloc

`GC.Alloc` 是对应 Garbage Collection Allocation 的 Marker，包含以下 Data：

- **Int64**：Allocation 大小。

## 其他资源

- [Native plug-ins](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native.html)
- [Profiler introduction](https://docs.unity3d.com/6000.7/Documentation/Manual/profiler-introduction.html)
- [Adding profiling information to your code](https://docs.unity3d.com/6000.7/Documentation/Manual/profiler-adding-information-code.html)

---

## 文档导航

- 上一页：[[04-IUnityMemoryManager API参考]]
- 目录：[[00-Native Plug-in API]]
- 下一页：[[02-日志API]]
