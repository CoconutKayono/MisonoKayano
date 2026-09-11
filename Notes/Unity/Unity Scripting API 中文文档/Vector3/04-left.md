> 原文：[Vector3.left](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-left.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).left

## 声明

~~~csharp
public static Vector3 left;
~~~

## 描述

Vector3(-1, 0, 0) 的简写。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        transform.position +=  Vector3.left  *  Time.deltaTime ;
    }
}
~~~

---

## 文档导航

- 上一页：[[03-forward]]
- 目录：[[00-Vector3]]
- 下一页：[[05-negativeInfinity]]


