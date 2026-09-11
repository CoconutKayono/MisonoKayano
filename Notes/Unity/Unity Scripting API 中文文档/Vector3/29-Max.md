> 原文：[Vector3.Max](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Max.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Max

## 声明

~~~csharp
public static Vector3 Max(Vector3 lhs, Vector3 rhs);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| lhs | 要检查的第一个向量。 |
| rhs | 要检查的第二个向量。 |

## 返回

Vector3 A vector that is made from the largest components of two vectors.

## 描述

使用两个向量的较大分量创建向量。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  Vector3  a = new  Vector3 (1, 2, 3);
    public  Vector3  b = new  Vector3 (4, 3, 2);

    void Example()
    {
        print( Vector3.Max (a, b)); // prints (4.0f, 3.0f, 3.0f)
    }
}
~~~

## 相关资源

- [Min](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Min.html)

---

## 文档导航

- 上一页：[[28-LerpUnclamped]]
- 目录：[[00-Vector3]]
- 下一页：[[30-Min]]






