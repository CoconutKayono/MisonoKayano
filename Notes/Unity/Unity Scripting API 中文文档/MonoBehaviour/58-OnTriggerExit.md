> 原文：[MonoBehaviour.OnTriggerExit](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerExit.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnTriggerExit

## 声明

~~~csharp
public void OnTriggerExit(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 参与此次碰撞的另一个 Collider。 |

## 描述

另一个 Collider 离开此 Collider 的触发器时调用。

## 示例

~~~csharp
// Destroy everything that leaves the trigger

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnTriggerExit( Collider  other)
    {
        Destroy(other.gameObject);
    }
}
~~~

---

## 文档导航

- 上一页：[[57-OnTriggerEnter2D]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[59-OnTriggerExit2D]]








