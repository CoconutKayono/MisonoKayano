> 原文：[Vector3.operator /](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-operator_divide.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).operator /

## 声明

~~~csharp
public static Vector3 operator /(Vector3 a, float d);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要除以 d 的向量。 |
| d | 除数。 |

## 描述

将向量除以数字。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        // make the vector twice shorter: prints (0.5,1.0,1.5)
        print(new  Vector3 (1, 2, 3) / 2.0F);
    }
}
~~~

---

## 文档导航

- 上一页：[[46-operator_multiply]]
- 目录：[[00-Vector3]]
- 下一页：[[48-operator_add]]


