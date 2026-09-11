> 原文：[Vector4.operator *](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_multiply.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator *

## 声明

~~~csharp
public static Vector4 operator *(Vector4 a, float d);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要相乘的向量。 |
| d | 要乘的数字。 |

## 描述

将向量乘以一个数字。将 a 的每个分量乘以数字 d。

## 声明

~~~csharp
public static Vector4 operator *(float d, Vector4 a);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| d | 要相乘的数字。 |
| a | 要相乘的向量。 |

## 描述

将数字乘以向量。将数字 d 乘以 a 的每个分量。

## 示例

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        print(new Vector4(1, 2, 3, 4) * 2.0f);
        print(2.0f * new Vector4(1, 2, 3, 4));
    }
}
~~~

---

## 文档导航

- 上一页：[[28-operator_subtract]]
- 目录：[[00-Vector4]]
- 下一页：[[30-operator_divide]]

