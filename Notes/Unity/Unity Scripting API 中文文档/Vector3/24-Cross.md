> 原文：[Vector3.Cross](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Cross.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Cross

## 声明

~~~csharp
public static Vector3 Cross(Vector3 lhs, Vector3 rhs);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| lhs | 第一个输入向量。 |
| rhs | 第二个输入向量。 |

## 返回

Vector3 The cross product of the lhs and rhs vectors. This vector is usually not normalized.

## 描述

计算两个三维向量的叉积。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    // Get the normal to a triangle from the three corner points a, b, and o, where o is the common origin point used to calculate two side vectors of the triangle.
     Vector3  GetNormal( Vector3  a,  Vector3  b,  Vector3  o)
    {
        // Calculate vectors corresponding to two of the sides of the triangle.
         Vector3  side1 = a - o;
         Vector3  side2 = b - o;

        // Cross the vectors to get a perpendicular vector, then normalize it. This is the  Result  vector in the drawing above.
        return  Vector3.Cross (side1, side2).normalized;
    }
}
~~~

---

## 文档导航

- 上一页：[[23-ClampMagnitude]]
- 目录：[[00-Vector3]]
- 下一页：[[25-Distance]]





