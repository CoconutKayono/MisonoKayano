> 原文：[Vector3.Scale](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Scale.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Scale

## 声明

~~~csharp
public static Vector3 Scale(Vector3 a, Vector3 b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要相乘的第一个向量。 |
| b | 要相乘的第二个向量。 |
| scale | 要相乘的向量。 |

## 返回

Vector3 A component of a multiplied by the same component of b .

## 描述

按分量相乘两个向量。

## 示例

~~~csharp
// Calculate the two vectors generating a result.
// This will compute  Vector3 (2, 6, 12)

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        print( Vector3.Scale (new  Vector3 (1, 2, 3), new  Vector3 (2, 3, 4)));
    }
}
~~~

---

## 声明

~~~csharp
public void Scale(Vector3 scale);
~~~

## 描述

按分量相乘两个向量。

---

## 文档导航

- 上一页：[[37-RotateTowards]]
- 目录：[[00-Vector3]]
- 下一页：[[39-SignedAngle]]





