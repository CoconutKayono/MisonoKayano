> 原文：[Vector3.ctor](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-ctor.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).ctor

## 声明

~~~csharp
public Vector3(float x, float y, float z);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| x | 向量的 x 分量。 |
| y | 向量的 y 分量。 |
| z | 向量的 z 分量。 |
| x | 向量的 x 分量。 |
| y | 向量的 y 分量。 |

## 描述

创建新的三维向量或点。

## 示例

~~~csharp
// Attach this script to a  GameObject .
// Attach a  Rigidbody  component to the  GameObject  (Click  Add Component  button in the Inspector window and go to  Physics < Rigidbody )
// This script moves a  GameObject  upwards using a  Vector3 
using UnityEngine;

public class Vector3CtorExample :  MonoBehaviour 
{
     Vector3  m_YDirectionVector;
     Rigidbody  m_Rigidbody;
    float m_Speed = 2.0f;

    void Start()
    {
        // Initialize the Y direction vector
        m_YDirectionVector = new  Vector3 (0.0f, 1.0f, 0.0f);
        // Fetch the RigidBody you attach to the  GameObject 
        m_Rigidbody = GetComponent< Rigidbody >();
    }

    void  Update ()
    {
        // Move the RigidBody m_Speed units per second  in the Y direction
        m_Rigidbody.linearVelocity = m_YDirectionVector * m_Speed;
    }
}
~~~

---

## 声明

~~~csharp
public Vector3(float x, float y);
~~~

## 描述

创建新的三维向量或点。

---

## 文档导航

- 上一页：[[17-z]]
- 目录：[[00-Vector3]]
- 下一页：[[19-Equals]]

