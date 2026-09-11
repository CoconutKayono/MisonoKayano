> 原文：[Vector4.operator +](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_add.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator +

## 声明

~~~csharp
public static Vector4 operator +(Vector4 a, Vector4 b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要相加的第一个向量。 |
| b | 要相加的第二个向量。 |

## 描述

将两个向量相加。将对应分量相加。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour
{
    void Start()
    {
        print(new Vector4(1, 2, 3, 4) + new Vector4(5, 6, 7, 8));
    }
}
~~~

---

## 文档导航

- 上一页：[[30-operator_divide]]
- 目录：[[00-Vector4]]
- 下一页：[[32-operator_eq]]

