> 原文：[MonoBehaviour.OnParticleCollision](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnParticleCollision.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnParticleCollision

## 声明

~~~csharp
public void OnParticleCollision(...);
~~~

## 描述

粒子系统中的粒子碰撞 Collider 时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class ExampleClass :  MonoBehaviour 
{
    public  ParticleSystem  part;
    public List< ParticleCollisionEvent > collisionEvents;

    void Start()
    {
        part = GetComponent< ParticleSystem >();
        collisionEvents = new List< ParticleCollisionEvent >();
    }

    void OnParticleCollision( GameObject  other)
    {
        int numCollisionEvents = part.GetCollisionEvents(other, collisionEvents);

         Rigidbody  rb = other.GetComponent< Rigidbody >();
        int i = 0;

        while (i < numCollisionEvents)
        {
            if (rb)
            {
                 Vector3  pos = collisionEvents[i].intersection;
                 Vector3  force = collisionEvents[i].velocity * 10;
                rb.AddForce(force);
            }
            i++;
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[44-OnMouseUpAsButton]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[46-OnParticleSystemStopped]]





