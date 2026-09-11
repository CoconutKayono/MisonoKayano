> 原文：[Object.Destroy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Destroy.html)

# Object.Destroy

```csharp
public static void Destroy(Object obj, float t = 0.0F);
```

## 参数

| 参数 | 说明 |
| --- | --- |
| `obj` | 要销毁的对象。 |
| `t` | 销毁前可选的延迟时间（秒）。 |

## 描述

移除 `GameObject`、组件或资源。如果指定 `t`，会在经过 `t` 秒后销毁；计时从调用 `Destroy` 的时刻开始。实际销毁总是延迟到当前 `Update` 循环之后，但一定发生在渲染之前。

如果对象是组件，只会移除并销毁该组件；如果对象是 `GameObject`，则会同时销毁该对象、所有组件以及所有 Transform 子对象。

调用 `Destroy(obj, t)` 后，即使调用它的脚本后来被禁用或销毁，对象仍会在 `t` 秒后被安排销毁。对可能已经被销毁或为 `null` 的对象调用此方法是安全的。延迟销毁受 `Time.timeScale` 影响；当时间缩放为 0（例如游戏暂停）时，销毁会延迟到时间恢复。

另请参阅：[[07-DestroyImmediate]]。

```csharp
using UnityEngine;

public class ScriptExample : MonoBehaviour
{
    void DestroyGameObject() => Destroy(gameObject);

    void DestroyScriptInstance() => Destroy(this);

    void DestroyComponent() => Destroy(GetComponent<Rigidbody>());

    void DestroyObjectDelayed() => Destroy(gameObject, 5);

    void Update()
    {
        if (Input.GetButton("Fire1") && GetComponent<BoxCollider>())
            Destroy(GetComponent<BoxCollider>());
    }
}
```

---

## 文档导航

- 上一页：[[05-ToString]]
- 目录：[[00-Object]]
- 下一页：[[07-DestroyImmediate]]
