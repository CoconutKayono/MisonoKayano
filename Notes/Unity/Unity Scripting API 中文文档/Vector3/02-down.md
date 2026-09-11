> 原文：[Vector3.down](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-down.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).down

## 声明

~~~csharp
public static Vector3 down;
~~~

## 描述

Vector3(0, -1, 0) 的简写。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        transform.position +=  Vector3.down  *  Time.deltaTime ;
    }
}
~~~

---

## 文档导航

- 上一页：[[01-back]]
- 目录：[[00-Vector3]]
- 下一页：[[03-forward]]


