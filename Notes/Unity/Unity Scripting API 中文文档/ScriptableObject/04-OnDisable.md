> 原文：[ScriptableObject.OnDisable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.OnDisable.html)

# [ScriptableObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html).OnDisable

## 描述

当脚本化对象离开作用域时调用。

在以下情况下会调用 `OnDisable`：

- 在 Hierarchy 窗口中加载场景时，针对当前已加载到内存但未被该场景引用的 `ScriptableObject`。
- 对之前在 Project 窗口中取消选中的 `ScriptableObject` 调用 `Resources.UnloadUnusedAssets` 时。
- 发生域重载时，对所有已加载到内存的 `ScriptableObject` 调用。对象重新创建后会调用 `OnEnable`。

```csharp
using UnityEngine;
using System;

public class EventManager
{
    public static event Action OnEvent;

    public static void TriggerEvent()
    {
        OnEvent?.Invoke();
    }
}

public class EventListenerSO : ScriptableObject
{
    void OnEnable()
    {
        Debug.Log("ScriptableObject enabled. Subscribing to event.");
        EventManager.OnEvent += OnEventReceived;
    }

    void OnDisable()
    {
        Debug.Log("ScriptableObject disabled. Unsubscribing from event.");
        EventManager.OnEvent -= OnEventReceived;
    }

    void OnEventReceived()
    {
        Debug.Log("Event received by ScriptableObject!");
    }
}
```

---

## 文档导航

- 上一页：[[03-OnDestroy]]
- 目录：[[00-ScriptableObject]]
- 下一页：[[05-OnEnable]]
