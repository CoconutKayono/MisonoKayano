> 原文：[Vector3.operator -](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-operator_subtract.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).operator -

## 声明

~~~csharp
public static Vector3 operator -(Vector3 a, Vector3 b);
~~~

## 声明

~~~csharp
public static Vector3 operator -(Vector3 a);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要从中减去 b 的向量。 |
| b | 要从 a 中减去的向量。 |
| a | 要取反的向量。 |

## 描述

从一个向量中减去另一个向量。

## 示例

~~~csharp
// prints (-5.0,-3.0,-1.0)

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        print(new  Vector3 (1, 2, 3) - new  Vector3 (6, 5, 4));
    }
}
~~~

~~~csharp
// prints (-1.0f, -2.0f, -3.0f)

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        print(-new  Vector3 (1.0f, 2.0f, 3.0f));
    }
}
~~~

---

## 文档导航

- 上一页：[[43-operator_Vector3]]
- 目录：[[00-Vector3]]
- 下一页：[[45-operator_ne]]




