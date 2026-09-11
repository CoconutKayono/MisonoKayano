> 原文：[Vector3.operator Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-operator_float3.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).operator Vector3

## 声明

~~~csharp
public static explicit operator Vector3(float3 v);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| v | 要转换为 Vector3 的 float3。 |

## 返回

Vector3 The converted Vector3 result.

## 描述

将 float3 转换为 Vector3。

## 示例

~~~csharp
// Attach this script to a  GameObject .
using UnityEngine;
using Unity.Mathematics;

public class ExampleFloat3ToVector3 :  MonoBehaviour 
{
    void Start()
    {
         float3  a = new  float3 (4f, 5f, 6f);
         Debug.Log (" Input   float3  is: " + a.ToString());

        // Implicit conversion from Unity.Mathematics.float3 to UnityEngine.Vector3
         Vector3  result = a;
         Debug.Log (" Result   Vector3  is: " + result.ToString());
    }
}
~~~

---

## 文档导航

- 上一页：[[49-operator_eq]]
- 目录：[[00-Vector3]]
- 下一页：无





