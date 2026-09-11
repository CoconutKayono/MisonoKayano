> 原文：[Vector2.operator /](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2-operator_divide.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).operator /

## 声明

~~~csharp
public static Vector2 operator /(Vector2 a, float d);
~~~

## 声明

~~~csharp
public static Vector2 operator /(Vector2 a, Vector2 b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要除的向量。 |
| d | 除数。 |
| a | 要除的向量。 |
| b | 要相除的向量。 |

## 描述

将向量除以数字。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // make the vector twice shorter: prints (0.5,1.0)
        print(new  Vector2 (1, 2) / 2.0f);
    }
}
~~~

---

## 文档导航

- 上一页：[[36-operator_multiply]]
- 目录：[[00-Vector2]]
- 下一页：[[38-operator_add]]




