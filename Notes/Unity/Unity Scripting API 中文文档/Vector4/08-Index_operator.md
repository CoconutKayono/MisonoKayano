> 原文：[Vector4.Index_operator](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Index_operator.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).this[int]

## 声明

~~~csharp
public float this[int];
~~~

## 描述

使用 [0]、[1]、[2]、[3] 访问 x、y、z、w 分量。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
         Vector4   p = new  Vector4 ();
        p[3] = 5; // the same as p.w = 5
    }
}
~~~

---

## 文档导航

- 上一页：[[07-sqrMagnitude]]
- 目录：[[00-Vector4]]
- 下一页：[[09-w]]


