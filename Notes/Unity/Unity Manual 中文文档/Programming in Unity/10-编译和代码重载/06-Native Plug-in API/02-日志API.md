# Native Plug-in Logging API

> 原文：[Native plug-in API for logging](https://docs.unity3d.com/6000.7/Documentation/Manual/low-level-native-plugin-logging.html)

使用 `IUnityLog` Interface 从 Native Plug-in Code 写入 Unity Log。Logging 的 Low-level Native API 位于 `IUnityLog.h` Header File 中，该文件位于 [[01-Native Plug-in API简介#Plugin API 文件夹|PluginAPI 文件夹]]。

该文件包含一个 `Log` 函数，其声明如下：

```cpp
void(UNITY_INTERFACE_API * Log)(UnityLogType type, const char* message, const char *fileName, const int fileLine);
```

可以直接调用该函数：

```cpp
s_UnityLog->Log(kUnityLogTypeLog, "Here is a regular log", __FILE__, __LINE__);
```

不过，为了方便，Native Logging API 定义了以下宏，将不同 Log Level 的调用封装到 `Log` 函数中：

| 宏 | 说明 |
| --- | --- |
| `UNITY_LOG(PTR_, MSG_)` | 使用以 Pointer 传入的 Log Interface（`PTR_`），将给定的 `char*`（`MSG_`）写入普通 Log 消息。等价于 Managed API 的 [`Debug.Log`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Debug.Log.html)。 |
| `UNITY_LOG_WARNING(PTR_, MSG_)` | 使用以 Pointer 传入的 Log Interface（`PTR_`），将给定的 `char*`（`MSG_`）写入 Warning-Level Log 消息。等价于 Managed API 的 [`Debug.LogWarning`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Debug.LogWarning.html)。 |
| `UNITY_LOG_ERROR(PTR_, MSG_)` | 使用以 Pointer 传入的 Log Interface（`PTR_`），将给定的 `char*`（`MSG_`）写入 Error-Level Log 消息。等价于 Managed API 的 [`Debug.LogError`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Debug.LogError.html)。 |

以下 Code Example 在 C++ 中实现 `IUnityLog` Interface，并使用这些预定义宏写入不同 Level 的 Log 输出：

```cpp
#include "IUnityLog.h"

static IUnityLog* s_UnityLog = NULL;

// Additional macros to include file and line number from the native code
#define UNITY_LOG_STRINGIZE_DETAIL(x) #x
#define UNITY_LOG_STRINGIZE(x) UNITY_LOG_STRINGIZE_DETAIL(x)
#define COMPOSE(MESSAGE) "[" __FILE__ ":" UNITY_LOG_STRINGIZE(__LINE__) "] " MESSAGE
#define NATIVE_LOG(PTR, MESSAGE) UNITY_LOG(PTR, COMPOSE(MESSAGE))
#define NATIVE_WARNING(PTR, MESSAGE) UNITY_LOG_WARNING(PTR, COMPOSE(MESSAGE))
#define NATIVE_ERROR(PTR, MESSAGE) UNITY_LOG_ERROR(PTR, COMPOSE(MESSAGE))

// Unity plugin load event
extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API UnityPluginLoad(IUnityInterfaces * unityInterfacesPtr)
{
    s_UnityLog = unityInterfacesPtr->Get<IUnityLog>();
}

// Unity plugin unload event
extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API UnityPluginUnload()
{
    s_UnityLog = nullptr;
}

extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API GenerateLog()
{
    // Output different log level messages to the Unity console
    UNITY_LOG(s_UnityLog, "Regular log message");
    UNITY_LOG_WARNING(s_UnityLog, "Warning log message");
    UNITY_LOG_ERROR(s_UnityLog, "Error log message");

    // Wrap log functions to provide native file and line number in output
    NATIVE_LOG(s_UnityLog, "Regular log with native file name and line number");
    NATIVE_WARNING(s_UnityLog, "Warning log with native file name and line number");
    NATIVE_ERROR(s_UnityLog, "Error log with native file name and line number");
}
```

> **Note**：将 Native File 和 Line Number 嵌入消息的附加宏，是针对一个已知问题的 Workaround：通过 `UNITY_LOG` 及其等价宏调用 `Log` 函数时，Unity 未能包含这些信息。

## 其他资源

- [The Debug class](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Debug.html)
- [Log files reference](https://docs.unity3d.com/6000.7/Documentation/Manual/log-files.html)

---

## 文档导航

- 上一页：[[07-性能分析API]]
- 目录：[[00-Native Plug-in API]]
- 下一页：[[00-代码优化]]
