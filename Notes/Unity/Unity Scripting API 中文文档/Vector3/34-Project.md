> 原文：[Vector3.Project](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Project.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Project

## 声明

~~~csharp
public static Vector3 Project(Vector3 vector, Vector3 onNormal);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| vector | 要投影的向量。 |
| onNormal | 要投影到的向量。此向量不需要进行归一化。 |

## 返回

Vector3 The vector that results from the projection of vector . This vector points in the same direction as onNormal .

## 描述

将向量投影到另一个向量上。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Slide( Transform  target,  Vector3  railDirection)
    {
         Vector3  heading = target.position - transform.position;
         Vector3  force =  Vector3.Project (heading, railDirection);

        GetComponent< Rigidbody >().AddForce(force);
    }
}
~~~

---

## 文档导航

- 上一页：[[33-OrthoNormalize]]
- 目录：[[00-Vector3]]
- 下一页：[[35-ProjectOnPlane]]


