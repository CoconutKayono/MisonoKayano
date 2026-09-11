> 原文：[Vector3.Min](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Min.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Min

## 声明

~~~csharp
public static Vector3 Min(Vector3 lhs, Vector3 rhs);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| lhs | 要检查的第一个向量。 |
| rhs | 要检查的第二个向量。 |

## 返回

Vector3 A vector that is made from the smallest components of two vectors.

## 描述

使用两个向量的较小分量创建向量。

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
        print( Vector3.Min (a, b));     // prints (1.0f, 2.0f, 2.0f)
    }
}
~~~

## 相关资源

- [Max](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Max.html)

---

## 文档导航

- 上一页：[[29-Max]]
- 目录：[[00-Vector3]]
- 下一页：[[31-MoveTowards]]






