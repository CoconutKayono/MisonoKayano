# Native Plug-in 图形和 Rendering API

> 原文：[Native plug-in API for graphics and rendering](https://docs.unity3d.com/6000.7/Documentation/Manual/low-level-native-plugin-rendering-extensions.html)

使用 `IUnityGraphics` Interface 让 Plug-in 访问通用 Graphics Device 功能。该 Interface 定义在 `IUnityGraphics.h` Header File 中，位于 [[01-Native Plug-in API简介#Plugin API 文件夹|PluginAPI 文件夹]]。

以下 Script 使用 `IUnityGraphics` Interface 注册 Callback：

```cpp
#include "IUnityInterface.h"
#include "IUnityGraphics.h"
    
static IUnityInterfaces* s_UnityInterfaces = NULL;
static IUnityGraphics* s_Graphics = NULL;
static UnityGfxRenderer s_RendererType = kUnityGfxRendererNull;
    
// Unity plugin load event
extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API
    UnityPluginLoad(IUnityInterfaces* unityInterfaces)
{
    s_UnityInterfaces = unityInterfaces;
    s_Graphics = unityInterfaces->Get<IUnityGraphics>();
        
    s_Graphics->RegisterDeviceEventCallback(OnGraphicsDeviceEvent);
        
    // Run OnGraphicsDeviceEvent(initialize) manually on plugin load
    // to not miss the event in case the graphics device is already initialized
    OnGraphicsDeviceEvent(kUnityGfxDeviceEventInitialize);
}
    
// Unity plugin unload event
extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API
    UnityPluginUnload()
{
    s_Graphics->UnregisterDeviceEventCallback(OnGraphicsDeviceEvent);
}
    
static void UNITY_INTERFACE_API
    OnGraphicsDeviceEvent(UnityGfxDeviceEventType eventType)
{
    switch (eventType)
    {
        case kUnityGfxDeviceEventInitialize:
        {
            s_RendererType = s_Graphics->GetRenderer();
            //TODO: user initialization code on graphics device initialization. 
            For example, D3D11 resource creation.
            break;
        }
        case kUnityGfxDeviceEventShutdown:
        {
            s_RendererType = kUnityGfxRendererNull;
            //TODO: user graphics API code to call on graphics device shutdown.
            break;
        }
        case kUnityGfxDeviceEventBeforeReset:
        {
            //TODO: user graphics API code to call before graphics device reset.
            break;
        }
        case kUnityGfxDeviceEventAfterReset:
        {
            //TODO: user graphics API code to call after graphics device reset.
            break;
        }
    };
}
```

## Rendering Thread 上的 Plug-in Callback

如果 Platform 和可用 CPU 数量允许，可以使用 Multithreading 在 Unity 中进行 Rendering。

> **Note**：使用 Multithreaded Rendering 时，Rendering API Command 会在与 MonoBehaviour Script 不同的 Thread 上运行。Main Thread 与 Render Thread 之间的通信意味着，Plug-in 可能不会立即开始 Rendering，具体取决于 Main Thread 已推送到 Render Thread 的工作量。

要从 Plug-in 进行 Rendering，请在 Managed Plug-in Script 中调用 [`GL.IssuePluginEvent`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GL.IssuePluginEvent.html)。这会使 Unity 的 Rendering Pipeline 在 Render Thread 中调用 Native Function。例如，如果从 Camera 的 `OnPostRender` 函数调用 `GL.IssuePluginEvent`，该函数会在 Camera 完成 Rendering 后立即调用 Plug-in Callback。

下面是 Native Plug-in Code：

```cpp
// Plugin function to handle a specific rendering event
static void UNITY_INTERFACE_API OnRenderEvent(int eventID)
{
    // User rendering code
}
    
// Freely defined function to pass a callback to plugin-specific scripts
extern "C" UnityRenderingEvent UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API
    GetRenderEventFunc()
{
    return OnRenderEvent;
}
```

下面是对应的 Managed Code：

```csharp
#if UNITY_IPHONE && !UNITY_EDITOR
[DllImport ("__Internal")]
#else
[DllImport("RenderingPlugin")]
#endif
private static extern IntPtr GetRenderEventFunc();
    
// Queue a specific callback to be called on the render thread
GL.IssuePluginEvent(GetRenderEventFunc(), 1);
```

`UnityRenderingEvent` Callback 的 Signature 位于 [Native Rendering Plugin sample](https://github.com/Unity-Technologies/NativeRenderingPlugin/tree/master/PluginSource/source/Unity) 的 `IUnityGraphics.h` 中。

## 使用 OpenGL Graphics API 的 Plug-in

OpenGL Object 有两类：

- **Across OpenGL Context 共享的 Object**，例如 Texture、Buffer、Renderbuffer、Sampler、Query、Shader 和 Program Object。
- **每个 OpenGL Context 独有的 Object**，例如 Vertex Array、Framebuffer、Program Pipeline、Transform Feedback 和 Sync Object。

Unity 使用多个 OpenGL Context。初始化和关闭 Editor 与 Player 时，Unity 依赖一个 Master Context；但在 Rendering 时使用专用 Context。因此，不能在 `kUnityGfxDeviceEventInitialize` 和 `kUnityGfxDeviceEventShutdown` Event 期间创建 Per-Context Object。

<a name="vulkan-plugin"></a>

## 使用 Vulkan Graphics API 的 Plug-in

开发使用 Vulkan Graphics API 的 Native Graphics Plug-in 时，可以通过 [Validation Layer](https://docs.unity3d.com/6000.7/Documentation/Manual/EditorCommandLineArguments.html#debugging) 启用 Debugging。要启用 Validation Layer，请确保以下设置，以避免 Plug-in 执行期间发生 Crash：

- 在 Native Graphics Plug-in 所在的同一目录中添加 Validation Layer Plug-in。
- 在 [Plug-in Inspector window](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-in-inspector.html) 中，为 Native Plug-in 和 Vulkan Validation Layer Plug-in 配置相同的 **Load on Startup** 设置。

## Rendering Extensions API

Unity 还支持能够在特定 Event 发生时接收 Callback 的 Low-level Rendering Extension。这主要用于在 Plug-in 中实现和控制 Low-level Rendering，并让 Plug-in 支持 Unity 的 Multithreaded Rendering。

由于此 Extension 的 Low-level 特性，可能需要在 Device 创建前预加载 Plug-in。目前的约定基于名称：Plug-in Name 必须以 `GfxPlugin` 开头，例如 `GfxPluginMyNativePlugin`。

Unity 暴露的 Rendering Extension 定义位于 `IUnityRenderingExtensions.h` 文件中，该文件位于 [[01-Native Plug-in API简介#Plugin API 文件夹|PluginAPI 文件夹]]。

所有支持 Native Plug-in 的 Platform 都支持这些 Extension。

要使用 Rendering Extension，Plug-in 应导出 `UnityRenderingExtEvent`，并可选择导出 `UnityRenderingExtQuery`。更多信息请参阅 Header File 中的文档。

## Rendering Thread 上的 Plug-in Callback

每当 Unity 触发内置 Event 之一时，Plug-in 都会通过 `UnityRenderingExtEvent` 被调用。也可以在 Script 中通过 [`CommandBuffer.IssuePluginEventAndData`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CommandBuffer.IssuePluginEventAndData.html) 或 [`CommandBuffer.IssuePluginCustomBlit`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CommandBuffer.IssuePluginCustomBlit.html) 将 Callback 添加到 CommandBuffer。

## 其他资源

- [[06-Shader Compiler API]]
- [[03-内存管理API]]
- [[07-性能分析API]]
- [[02-日志API]]
- [Android 上的 Vulkan validation layers](https://developer.android.com/ndk/guides/graphics/validation-layer)

---

## 文档导航

- 上一页：[[01-Native Plug-in API简介]]
- 目录：[[00-Native Plug-in API]]
- 下一页：[[06-Shader Compiler API]]
