> 原文：[MonoBehaviour.OnTriggerStay2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerStay2D.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnTriggerStay2D

## 声明

~~~csharp
public void OnTriggerStay2D(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 参与此次碰撞的另一个 Collider2D。 |

## 描述

另一个 Collider2D 持续停留在此 Collider2D 的触发器中时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnTriggerStay2D( Collider2D  other)
    {
        other.attachedRigidbody.AddForce(-0.1F * other.attachedRigidbody.linearVelocity);
    }
}
~~~

## 相关资源

- [Collider2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider2D.html)
- [OnTriggerEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerEnter2D.html)
- [OnTriggerExit2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerExit2D.html)

---

## 文档导航

- 上一页：[[60-OnTriggerStay]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[62-OnValidate]]









