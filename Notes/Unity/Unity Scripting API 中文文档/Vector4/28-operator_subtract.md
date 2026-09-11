> 原文：[Vector4.operator -](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_subtract.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator -

## 声明

~~~csharp
public static Vector4 operator -(Vector4 a, Vector4 b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要从中减去 b 的向量。 |
| b | 要从 a 中减去的向量。 |

## 描述

从一个向量中减去另一个向量。将 b 的每个分量从 a 中减去。

## 声明

~~~csharp
public static Vector4 operator -(Vector4 a);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要取反的向量。 |

## 描述

对向量取反。结果中的每个分量都会取反。

## 示例

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        print(new Vector4(1, 2, 3, 4) - new Vector4(6, 5, 4, 3));
        print(-new Vector4(1, 2, 3, 4));
    }
}
~~~

---

## 文档导航

- 上一页：[[27-operator_Vector4]]
- 目录：[[00-Vector4]]
- 下一页：[[29-operator_multiply]]

