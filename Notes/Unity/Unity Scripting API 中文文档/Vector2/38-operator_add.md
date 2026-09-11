> 原文：[Vector2.operator +](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2-operator_add.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).operator +

## 声明

~~~csharp
public static Vector2 operator +(Vector2 a, Vector2 b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要相加的第一个向量。 |
| b | 要相加的第二个向量。 |

## 描述

将两个向量相加。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Start()
    {
        print(new  Vector2 (1, 2) + new  Vector2 (2, 3));
    }
}
~~~

---

## 文档导航

- 上一页：[[37-operator_divide]]
- 目录：[[00-Vector2]]
- 下一页：[[39-operator_eq]]



