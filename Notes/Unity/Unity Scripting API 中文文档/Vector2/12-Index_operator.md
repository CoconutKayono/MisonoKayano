> 原文：[Vector2.Index_operator](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.Index_operator.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).this[int]

## 声明

~~~csharp
public float this[int];
~~~

## 描述

使用 [0] 或 [1] 分别访问 x 或 y 分量。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
         Vector2  p = new  Vector2 ();
        p[1] = 5; // the same as p.y = 5
    }
}
~~~

---

## 文档导航

- 上一页：[[11-sqrMagnitude]]
- 目录：[[00-Vector2]]
- 下一页：[[13-x]]


