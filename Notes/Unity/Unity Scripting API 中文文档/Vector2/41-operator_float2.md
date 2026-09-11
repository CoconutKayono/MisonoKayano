> 原文：[Vector2.operator Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2-operator_float2.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).operator Vector2

## 声明

~~~csharp
public static explicit operator Vector2(float2 v);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| v | 要转换为 Vector2 的 float2。 |

## 返回

Vector2 The converted Vector2 result.

## 描述

将 float2 转换为 Vector2。

## 示例

~~~csharp
// Attach this script to a  GameObject .
using UnityEngine;
using Unity.Mathematics; // brings in  float2 

public class Example_Vector2_FromFloat2 :  MonoBehaviour 
{
    void Start()
    {
         float2  a = new  float2 (4f, 5f);
         Debug.Log (" Input   float2  is: " + a.ToString());

        // Implicit conversion from Unity.Mathematics.float2 to UnityEngine.Vector2
         Vector2  result = a;
         Debug.Log (" Result   Vector2  is: " + result.ToString());
    }
}
~~~

---

## 文档导航

- 上一页：[[40-operator_Vector3]]
- 目录：[[00-Vector2]]
- 下一页：[[42-operator_Vector2]]





