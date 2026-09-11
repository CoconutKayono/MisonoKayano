> 原文：[ScriptableObject.Awake](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.Awake.html)

# [ScriptableObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html).Awake

## 描述

创建 `ScriptableObject` 实例时调用。

当创建新的 `ScriptableObject` 实例时会调用 `Awake`，包括：编辑器启动时处理已打开场景引用的对象；在编辑器中通过 Create Asset 菜单创建资源时；运行时通过 `ScriptableObject.CreateInstance` 实例化或运行时加载资源时；首次加载场景中引用该对象的对象时；首次在 Project 窗口中选中该对象时。如果原实例已经被垃圾回收，后续加载或选中也会再次调用。

注意：编辑模式下作为资源创建的 `ScriptableObject`，进入播放模式时不会重新创建。若要在进入播放模式时初始化 `ScriptableObject`，请使用 [`ScriptableObject.OnEnable`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.OnEnable.html)。

下面的示例包含一个 `ScriptableObject` 脚本和一个访问它的 `MonoBehaviour` 脚本。

```csharp
using UnityEngine;

public class ScriptObj : ScriptableObject
{
    public int A;

    public void Awake()
    {
        A = 1;
        Debug.Log("Awake: " + A);
    }

    public void OnDestroy()
    {
        Debug.Log("OnDestroy");
    }
}

public class ScriptObjExample : MonoBehaviour
{
    ScriptObj test;

    void Start()
    {
        test = (ScriptObj)ScriptableObject.CreateInstance(typeof(ScriptObj));
        Debug.Log(test.A);
    }
}
```

---

## 文档导航

- 上一页：[[01-CreateInstance]]
- 目录：[[00-ScriptableObject]]
- 下一页：[[03-OnDestroy]]
