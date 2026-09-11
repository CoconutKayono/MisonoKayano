# IUnityMemoryManager API 参考

> 原文：[IUnityMemoryManager API reference](https://docs.unity3d.com/6000.7/Documentation/Manual/low-level-native-plugin-memory-manager-api-reference.html)

本页提供 `IUnityMemoryManager` Interface 的 API Reference。

## CreateAllocator

### Declaration

`UnityAllocator* (UNITY_INTERFACE_API * CreateAllocator)(const char* areaName, const char* objectName);`

### Parameters

| Parameter | Description |
| --- | --- |
| **`const char* areaName`** | 此 Allocator 所属宽泛类别的名称。 |
| **`const char* objectName`** | 此特定 Allocator 的名称。 |

### Description

创建一个可以分配 Memory Block 的新 Allocator 对象。

## DestroyAllocator

### Declaration

`void(UNITY_INTERFACE_API * DestroyAllocator)(UnityAllocator * allocator);`

### Parameters

| Parameter | Description |
| --- | --- |
| **`UnityAllocator * allocator`** | 要删除的 Allocator。 |

### Description

删除现有的 Allocator 对象。

## Allocate

### Declaration

`void* (UNITY_INTERFACE_API * Allocate)(UnityAllocator * allocator, size_t size, size_t align, const char* file, int32_t line);`

### Parameters

| Parameter | Description |
| --- | --- |
| **`UnityAllocator * allocator`** | 用于 Allocation 的 Allocator。 |
| **`size_t size`** | 要分配的 Memory 大小，单位为 Byte。 |
| **`size_t align`** | 结果 Pointer 的 Memory Address Alignment。 |
| **`const char* file`** | 发起此 Allocation 调用的 Source File 路径。此处使用预定义宏 `__FILE__`。 |
| **`int32_t line`** | 发起此 Allocation 调用的 Source File 行号。此处使用预定义宏 `__LINE__`。 |

### Description

使用现有 Allocator 分配一个 Memory Block。此方法返回新分配 Memory 的 Pointer。

## Deallocate

### Declaration

`void(UNITY_INTERFACE_API * Deallocate)(UnityAllocator * allocator, void* ptr, const char* file, int32_t line);`

### Parameters

| Parameter | Description |
| --- | --- |
| **`UnityAllocator * allocator`** | 用于 Deallocation 的 Allocator。 |
| **`void* ptr`** | 指向要释放 Memory 的 Pointer。 |
| **`const char* file`** | 发起此 Deallocation 调用的 Source File 路径。此处使用预定义宏 `__FILE__`。 |
| **`int32_t line`** | 发起此 Deallocation 调用的 Source File 行号。此处使用预定义宏 `__LINE__`。 |

### Description

释放指定 Pointer 指向的 Memory。此操作不会将 Pointer 设置为 `NULL`。

## Reallocate

### Declaration

`void* (UNITY_INTERFACE_API * Reallocate)(UnityAllocator * allocator, void* ptr, size_t size, size_t align, const char* file, int32_t line);`

### Parameters

| Parameter | Description |
| --- | --- |
| **`UnityAllocator * allocator`** | 用于 Reallocation 操作的 Allocator。 |
| **`void* ptr`** | 指向要释放 Memory 的 Pointer。 |
| **`size_t size`** | 要分配的 Memory 大小，单位为 Byte。 |
| **`size_t align`** | 结果 Pointer 的 Memory Address Alignment。 |
| **`const char* file`** | 发起此 Reallocation 调用的 Source File 路径。此处使用预定义宏 `__FILE__`。 |
| **`int32_t line`** | 发起此 Reallocation 调用的 Source File 行号。此处使用预定义宏 `__LINE__`。 |

### Description

重新分配现有 Pointer，使其指向另一个 Memory Block。

## Implementation example

下面是 `IUnityMemoryManager` Interface 的一个实现示例。

```cpp
#include "IUnityInterface.h"
#include "IUnityMemoryManager.h"
#include <cstdint>

static IUnityMemoryManager* s_MemoryManager = NULL;
static UnityAllocator* s_Alloc = NULL;
extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API UnityPluginLoad(IUnityInterfaces * unityInterfaces)
{
    s_MemoryManager = unityInterfaces->Get<IUnityMemoryManager>();
    if (s_MemoryManager  == NULL)
    return;

    // Create an allocator. This allows you to see the allocation root in the profiler when taking snapshots. Under plug-ins-native - Plugin Backend Allocator
   // All memory allocated here also goes under kMemNativePlugin
    s_Alloc = s_MemoryManager->CreateAllocator("plug-ins-native", "Plugin Backend Allocator");
}

extern "C" void UNITY_INTERFACE_EXPORT UNITY_INTERFACE_API UnityPluginUnload()
{
    //Free allocator
    s_MemoryManager->DestroyAllocator(s_Alloc);
    s_Alloc = NULL;
    s_MemoryManager = NULL;
}

void DoMemoryOperations()
{
    // Allocate 1KB memory
    void* mem = s_MemoryManager->Allocate(s_Alloc, 1 * 1024, 16, __FILE__, __LINE__);
     // Reallocate the same pointer with 2KB
    mem = s_MemManager->Reallocate(s_Alloc, mem, 2 * 1024, 16, __FILE__, __LINE__);
    // Delete allocated memory
    s_MemoryManager->Deallocate(s_Alloc, mem, __FILE__, __LINE__);
}
```

## 其他资源

- [[06-Shader Compiler API]]
- [[07-性能分析API]]
- [[02-日志API]]

---

## 文档导航

- 上一页：[[03-内存管理API]]
- 目录：[[00-Native Plug-in API]]
- 下一页：[[07-性能分析API]]
