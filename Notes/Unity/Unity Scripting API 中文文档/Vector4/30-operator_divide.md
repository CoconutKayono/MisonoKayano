> 原文：[Vector4.operator /](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_divide.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator /

## 声明

~~~csharp
public static Vector4 operator /(Vector4 a, float d);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要除的向量。 |
| d | 除数。 |

## 描述

将向量除以一个数字。将 a 的每个分量除以数字 d。

## 示例

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        // Prints (0.5, 1.0, 1.5, 2.5)
        print(new Vector4(1, 2, 3, 5) / 2);
    }
}
~~~

---

## 文档导航

- 上一页：[[29-operator_multiply]]
- 目录：[[00-Vector4]]
- 下一页：[[31-operator_add]]

