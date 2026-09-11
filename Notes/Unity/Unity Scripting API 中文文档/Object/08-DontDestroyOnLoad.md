> 原文：[Object.DontDestroyOnLoad](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-DontDestroyOnLoad.html)

# Object.DontDestroyOnLoad

```csharp
public static void DontDestroyOnLoad(Object target);
```

## 参数

| 参数 | 说明 |
| --- | --- |
| `target` | 场景切换时不销毁的对象。 |

## 描述

加载新场景时不要销毁目标对象。加载新场景会销毁当前场景中的所有对象；调用 `Object.DontDestroyOnLoad` 可以在场景加载期间保留对象。如果目标是组件或 `GameObject`，Unity 也会保留其 Transform 子对象。此方法只对根 `GameObject` 或根 `GameObject` 上的组件有效，且不返回值。

```csharp
using UnityEngine;

public class DontDestroy : MonoBehaviour
{
    void Awake()
    {
        GameObject[] objs = GameObject.FindGameObjectsWithTag("music");
        if (objs.Length > 1)
            Destroy(gameObject);

        DontDestroyOnLoad(gameObject);
    }
}
```

上例用于保留跨场景播放的背景音乐：给背景音乐对象添加 `music` 标签和 `AudioSource`，并将此脚本附加到该对象。实际页面还提供了使用 `SceneManager.LoadScene` 在两个场景间切换的 `SceneSwap` 完整示例。

---

## 文档导航

- 上一页：[[07-DestroyImmediate]]
- 目录：[[00-Object]]
- 下一页：[[09-FindAnyObjectByType]]
