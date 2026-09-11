> 原文：[Vector3.Index_operator](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Index_operator.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).this[int]

## 声明

~~~csharp
public float this[int];
~~~

## 描述

使用 [0]、[1]、[2] 分别访问 x、y、z 分量。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  Vector3  p;

    void Example()
    {
        // set p.y as 5.0f
        p[1] = 5.0f;
    }
}
~~~

---

## 文档导航

- 上一页：[[13-sqrMagnitude]]
- 目录：[[00-Vector3]]
- 下一页：[[15-x]]


