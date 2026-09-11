> 原文：[MonoBehaviour.OnCollisionExit](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionExit.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnCollisionExit

## 声明

~~~csharp
public void OnCollisionExit(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| collision | 与此次碰撞相关的 Collision 数据。 |

## 描述

此 Collider/Rigidbody 停止接触另一个 Rigidbody/Collider 时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class Example :  MonoBehaviour 
{
    void OnCollisionExit( Collision  other)
    {
        print("No longer in contact with " + other.transform.name);
    }
}
~~~

---

## 文档导航

- 上一页：[[24-OnCollisionEnter2D]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[26-OnCollisionExit2D]]








