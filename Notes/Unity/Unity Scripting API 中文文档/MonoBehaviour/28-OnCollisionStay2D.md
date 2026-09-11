> 原文：[MonoBehaviour.OnCollisionStay2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionStay2D.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnCollisionStay2D

## 声明

~~~csharp
public void OnCollisionStay2D(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 与此碰撞关联的 Collision2D 数据。 |

## 描述

另一个对象上的 Collider 接触此对象的 Collider 的每一帧发送（仅限 2D 物理）。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    float rechargeRate = 10.0f;
    float batteryLevel;

    void OnCollisionStay2D( Collision2D  collision)
    {
        if (collision.gameObject.tag == "RechargePoint")
        {
            batteryLevel =  Mathf.Min (batteryLevel + rechargeRate *  Time.deltaTime , 100.0f);
        }
    }
}
~~~

## 相关资源

- [Collision2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collision2D.html)
- [OnCollisionEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionEnter2D.html)
- [OnCollisionExit2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionExit2D.html)

---

## 文档导航

- 上一页：[[27-OnCollisionStay]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[29-OnControllerColliderHit]]






