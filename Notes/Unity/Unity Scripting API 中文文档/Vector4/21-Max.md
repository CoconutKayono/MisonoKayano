> 原文：[Vector4.Max](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Max.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).Max

## 声明

~~~csharp
public static Vector4 Max(Vector4 lhs, Vector4 rhs);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| lhs | 要比较的第一个向量。 |
| rhs | 要比较的第二个向量。 |

## 返回

`Vector4`：由给定向量的最大分量组成的向量。

## 描述

使用两个向量的较大分量创建向量。

其他资源：[Min 函数](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Min.html)。

## 示例

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        Vector4 a = new Vector4(1, 2, 3, 5);
        Vector4 b = new Vector4(4, 3, 2, 0);
        print(Vector4.Max(a, b)); // prints (4.0,3.0,3.0,5.0)
    }
}
~~~

## 相关资源

- [Min](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Min.html)

---

## 文档导航

- 上一页：[[20-LerpUnclamped]]
- 目录：[[00-Vector4]]
- 下一页：[[22-Min]]


