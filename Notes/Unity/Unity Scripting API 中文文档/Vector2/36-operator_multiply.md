> 原文：[Vector2.operator *](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2-operator_multiply.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).operator *

## 声明

~~~csharp
public static Vector2 operator *(Vector2 a, float d);
~~~

## 声明

~~~csharp
public static Vector2 operator *(float d, Vector2 a);
~~~

## 声明

~~~csharp
public static Vector2 operator *(Vector2 a, Vector2 b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要相乘的向量。 |
| d | 要乘的数字。 |
| d | 要乘的数字。 |
| a | 要相乘的向量。 |
| a | 要相乘的第一个向量。 |
| b | 要相乘的第二个向量。 |

## 描述

将向量乘以数字。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // make the vector twice longer: prints (2.0,4.0)
        print(new  Vector2 (1, 2) * 2.0f);
    }
}
~~~

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // make the vector twice longer: prints (2.0,4.0)
        print(2.0f * new  Vector2 (1, 2));
    }
}
~~~

---

## 文档导航

- 上一页：[[35-operator_subtract]]
- 目录：[[00-Vector2]]
- 下一页：[[37-operator_divide]]




