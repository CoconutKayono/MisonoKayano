> 原文：[MonoBehaviour.OnTriggerEnter](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerEnter.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnTriggerEnter

## 声明

~~~csharp
public void OnTriggerEnter(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 参与此次碰撞的另一个 Collider。 |

## 描述

另一个 Collider 进入此 Collider 的触发器时调用。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    private float speed = 2f;

    //Moves this  GameObject  2 units a second in the forward direction
    void  Update ()
    {
        transform.Translate( Vector3.forward  *  Time.deltaTime  * speed);
    }

    //Upon collision with another  GameObject , this  GameObject  will reverse direction
    private void OnTriggerEnter( Collider  other)
    {
        speed = speed * -1;
    }
}
~~~

---

## 文档导航

- 上一页：[[55-OnTransformParentChanged]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[57-OnTriggerEnter2D]]








