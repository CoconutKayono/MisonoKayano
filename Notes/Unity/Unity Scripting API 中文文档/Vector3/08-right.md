> 原文：[Vector3.right](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-right.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).right

## 声明

~~~csharp
public static Vector3 right;
~~~

## 描述

Vector3(1, 0, 0) 的简写。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        transform.position +=  Vector3.right  *  Time.deltaTime ;
    }
}
~~~

---

## 文档导航

- 上一页：[[07-positiveInfinity]]
- 目录：[[00-Vector3]]
- 下一页：[[09-up]]


