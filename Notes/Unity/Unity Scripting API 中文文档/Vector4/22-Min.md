> 原文：[Vector4.Min](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Min.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).Min

## 声明

~~~csharp
public static Vector4 Min(Vector4 lhs, Vector4 rhs);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| lhs | 要比较的第一个向量。 |
| rhs | 要比较的第二个向量。 |

## 返回

`Vector4`：由给定向量的最小分量组成的向量。

## 描述

使用两个向量的较小分量创建向量。

其他资源：[Max 函数](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Max.html)。

## 示例

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        Vector4 a = new Vector4(1, 2, 3, 5);
        Vector4 b = new Vector4(4, 3, 2, 0);
        print(Vector4.Min(a, b)); // prints (1.0,2.0,2.0,0.0)
    }
}
~~~

## 相关资源

- [Max](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Max.html)

---

## 文档导航

- 上一页：[[21-Max]]
- 目录：[[00-Vector4]]
- 下一页：[[23-MoveTowards]]


