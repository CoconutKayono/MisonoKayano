> 原文：[Vector3.forward](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-forward.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).forward

## 声明

~~~csharp
public static Vector3 forward;
~~~

## 描述

Vector3(0, 0, 1) 的简写。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        transform.position +=  Vector3.forward  *  Time.deltaTime ;
    }
}
~~~

---

## 文档导航

- 上一页：[[02-down]]
- 目录：[[00-Vector3]]
- 下一页：[[04-left]]


