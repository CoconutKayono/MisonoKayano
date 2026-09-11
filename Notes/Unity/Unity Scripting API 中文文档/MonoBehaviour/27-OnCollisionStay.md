> 原文：[MonoBehaviour.OnCollisionStay](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionStay.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnCollisionStay

## 声明

~~~csharp
public void OnCollisionStay(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 与此次碰撞相关的 Collision 数据。 |

## 描述

每帧为接触另一个 Collider 或 Rigidbody 的每个 Collider 或 Rigidbody 调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnCollisionStay( Collision  collisionInfo)
    {
        //  Debug -draw all contact points and normals
        foreach ( ContactPoint  contact in collisionInfo.contacts)
        {
             Debug.DrawRay (contact.point, contact.normal,  Color.white );
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[26-OnCollisionExit2D]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[28-OnCollisionStay2D]]








