> 原文：[Vector2.operator -](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2-operator_subtract.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).operator -

## 声明

~~~csharp
public static Vector2 operator -(Vector2 a, Vector2 b);
~~~

## 声明

~~~csharp
public static Vector2 operator -(Vector2 a);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要从中减去 b 的向量。 |
| b | 要从 a 中减去的向量。 |
| a | 要取反的向量。 |

## 返回

Vector2 The difference between the two vectors, returned as a Vector2 struct.

## 描述

从一个向量中减去另一个向量。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // Create two vectors.
         Vector2  A = new  Vector2 (1, 2);
         Vector2  B = new  Vector2 (3, 2);
        
        // Subtract vector B from vector A.
         Vector2  C = A - B;
        
        // Print the result.
        print(C);
    }
}
~~~

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
       // Create a vector.
        Vector2  A = new  Vector2 (1, 2);
       
       // Find the negative value.
        Vector2  B = - A;
  
       // Print the result.
        print(B + " is the negative of " + A);
    }
}
~~~

---

## 文档导航

- 上一页：[[34-operator_Vector2]]
- 目录：[[00-Vector2]]
- 下一页：[[36-operator_multiply]]




