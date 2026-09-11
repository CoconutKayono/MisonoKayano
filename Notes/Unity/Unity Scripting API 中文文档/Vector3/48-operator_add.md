> 原文：[Vector3.operator +](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-operator_add.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).operator +

## 声明

~~~csharp
public static Vector3 operator +(Vector3 a, Vector3 b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 加法的左操作数。 |
| b | 加法的右操作数。 |

## 返回

Vector3 A Vector3 initialized with the component-wise sum of the left and right operands.

## 描述

按分量相加两个三维向量。

## 示例

~~~csharp
// prints (5.0,7.0,9.0)

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Start()
    {
        print(new  Vector3 (1, 2, 3) + new  Vector3 (4, 5, 6));
    }
}
~~~

---

## 文档导航

- 上一页：[[47-operator_divide]]
- 目录：[[00-Vector3]]
- 下一页：[[49-operator_eq]]


