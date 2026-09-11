> 原文：[ScriptableObject.OnDestroy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.OnDestroy.html)

# [ScriptableObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html).OnDestroy

## 描述

当脚本化对象即将销毁时调用。

下面的示例包含一个 `ScriptableObject` 脚本和一个访问它的 `MonoBehaviour` 脚本。示例同时展示了 `Awake`、`OnEnable`、`OnDisable` 和 `OnDestroy` 的调用。

```csharp
using UnityEngine;

public class ScriptObj : ScriptableObject
{
    public int A;

    public void Awake() { A = 1; Debug.Log("Awake: " + A); }
    public void OnEnable() { Debug.Log("OnEnable"); }
    public void OnDisable() { Debug.Log("OnDisable"); }
    public void OnDestroy() { Debug.Log("OnDestroy"); }
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

- 上一页：[[02-Awake]]
- 目录：[[00-ScriptableObject]]
- 下一页：[[04-OnDisable]]
