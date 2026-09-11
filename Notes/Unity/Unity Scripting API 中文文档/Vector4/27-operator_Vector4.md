> 原文：[Vector4.operator float4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_Vector4.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator float4

## 参数

| 参数 | 描述 |
| --- | --- |
| v | 要转换为 float4 的 Vector4。 |

## 返回

`float4`：转换后的 float4 结果。

## 描述

将 Vector4 转换为 float4。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // Create and display a  Vector4 .
         Vector4  vector4;

        vector4 = new  Vector4 (1.0f, 2.0f, 3.0f, 4.0f);
         Debug.Log (" Vector4 : " + vector4);

        // Convert the  Vector4  into a  Vector3 .
         Vector3  vector3;
        vector3 = vector4;

        // The 4.0f is not copied into the  Vector3 .
        // Show (1.0f, 2.0f, 3.0f).
         Debug.Log (" Vector3 : " + vector3);
    }
}
~~~

---

## 文档导航

- 上一页：[[26-Scale]]
- 目录：[[00-Vector4]]
- 下一页：[[28-operator_subtract]]


