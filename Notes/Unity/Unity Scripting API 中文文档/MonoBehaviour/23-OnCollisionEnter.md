> 原文：[MonoBehaviour.OnCollisionEnter](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionEnter.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnCollisionEnter

## 声明

~~~csharp
public void OnCollisionEnter(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| collision | 与此次碰撞相关的 Collision 数据。 |

## 描述

此 Collider/Rigidbody 开始接触另一个 Rigidbody/Collider 时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
     AudioSource  audioSource;

    void Start()
    {
        audioSource = GetComponent< AudioSource >();
    }

    void OnCollisionEnter( Collision  collision)
    {
        foreach ( ContactPoint  contact in collision.contacts)
        {
             Debug.DrawRay (contact.point, contact.normal,  Color.white );
        }

        if (collision.relativeVelocity.magnitude > 2)
            audioSource.Play();
    }
}
~~~

---

## 文档导航

- 上一页：[[22-OnChildRectTransformDimensionsChange]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[24-OnCollisionEnter2D]]








