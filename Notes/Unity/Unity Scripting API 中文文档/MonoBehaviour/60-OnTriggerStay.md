> 原文：[MonoBehaviour.OnTriggerStay](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerStay.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnTriggerStay

## 声明

~~~csharp
public void OnTriggerStay(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 参与此次碰撞的另一个 Collider。 |

## 描述

另一个 Collider 持续停留在此 Collider 的触发器中时调用。

## 示例

~~~csharp
// Applies an upwards force to all rigidbodies that enter the trigger.

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnTriggerStay( Collider  other)
    {
        if (other.attachedRigidbody)
        {
            other.attachedRigidbody.AddForce( Vector3.up  * 10);
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[59-OnTriggerExit2D]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[61-OnTriggerStay2D]]








