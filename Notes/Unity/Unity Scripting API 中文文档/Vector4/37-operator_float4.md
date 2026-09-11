> 原文：[Vector4.operator Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_float4.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator Vector4

## 参数

| 参数 | 描述 |
| --- | --- |
| v | 要转换的 float4。 |

## 返回

`Vector4`：转换后的 Vector4 结果。

## 描述

将 float4 转换为 Vector4。这是将输入 float4 值转换为 Vector4 的隐式转换运算符。

## 示例

~~~csharp
// Attach this script to a  GameObject .
using UnityEngine;
using Unity.Mathematics;

public class ExampleFloat4Conversion :  MonoBehaviour 
{
    void Start()
    {
         float4  a = new  float4 (1f, 2f, 3f, 4f);
         Debug.Log (" Input   float4  is: " + a.ToString());

        // Implicitly convert Unity.Mathematics.float4 to UnityEngine.Vector4
         Vector4  result = a;
         Debug.Log (" Result   Vector4  is: " + result.ToString());
    }
}
~~~

---

## 文档导航

- 上一页：[[33-operator_Vector2]]
- 目录：[[00-Vector4]]
- 下一页：无


