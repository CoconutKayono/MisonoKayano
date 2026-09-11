> 原文：[ScriptableObject.OnEnable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.OnEnable.html)

# [ScriptableObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html).OnEnable

## 描述

对象加载时调用。

每当 `ScriptableObject` 实例加载到内存时都会调用 `OnEnable`，包括编辑器启动、在编辑器中创建资源、运行时实例化或加载资源、域重载、首次加载引用该对象的场景以及首次在 Project 窗口中选中该对象等情况。

通常，对于内存中的某个 `ScriptableObject` 资源实例，`OnEnable` 只调用一次，适合用于初始化。如果被多次调用，通常表示该对象被重新实例化，例如取消在 Project 窗口中的选择、打开不引用它的新场景、脚本重新编译或资源重新导入。编辑器有时也会为属性检查或编辑创建临时实例；每个临时实例都会收到自己的 `OnEnable` 调用，但对象被垃圾回收或未经过正常清理而销毁时，`OnDisable` 可能不会调用。 `OnEnable` 不能是协程。

```csharp
using UnityEngine;

[CreateAssetMenu(menuName = "Example/CounterData")]
public class CounterData : ScriptableObject
{
    public int counter;

    void OnEnable()
    {
        counter = 0;
        Debug.Log("Counter reset on enable.");
    }
}
```

---

## 文档导航

- 上一页：[[04-OnDisable]]
- 目录：[[00-ScriptableObject]]
- 下一页：[[06-OnValidate]]
