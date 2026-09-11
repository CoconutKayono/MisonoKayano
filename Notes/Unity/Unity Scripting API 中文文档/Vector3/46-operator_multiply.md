> 原文：[Vector3.operator *](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-operator_multiply.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).operator *

## 声明

~~~csharp
public static Vector3 operator *(Vector3 a, float d);
~~~

## 声明

~~~csharp
public static Vector3 operator *(float d, Vector3 a);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要乘以 d 的向量。 |
| d | 要与 a 相乘的数字。 |
| d | 要与 a 相乘的数字。 |
| a | 要与 d 相乘的向量。 |

## 描述

将向量乘以数字。

## 示例

~~~csharp
// make the vector twice longer: prints (2.0,4.0,6.0)
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        print(new  Vector3 (1.0f, 2.0f, 3.0f) * 2.0f);
    }
}
~~~

~~~csharp
// make the vector twice longer: prints (2.0f, 4.0f, 6.0f)

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        print(2.0f * new  Vector3 (1.0f, 2.0f, 3.0f));
    }
}
~~~

---

## 文档导航

- 上一页：[[45-operator_ne]]
- 目录：[[00-Vector3]]
- 下一页：[[47-operator_divide]]




