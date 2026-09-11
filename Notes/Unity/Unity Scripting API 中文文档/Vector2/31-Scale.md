> 原文：[Vector2.Scale](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.Scale.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).Scale

## 声明

~~~csharp
public static Vector2 Scale(Vector2 a, Vector2 b);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| a | 第一个向量。 |
| b | 第二个向量。 |
| scale | 用于缩放的向量。 |

## 返回值

返回操作结果。

## 描述

按分量相乘两个向量。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // prints (2.0,6.0)
        print( Vector2.Scale (new  Vector2 (1, 2), new  Vector2 (2, 3)));
    }
}
~~~

---

## 声明

~~~csharp
public void Scale(Vector2 scale);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| a | 第一个向量。 |
| b | 第二个向量。 |
| scale | 用于缩放的向量。 |

## 返回值

无返回值。

## 描述

按分量相乘两个向量。

---

## 文档导航

- 上一页：[[30-Reflect]]
- 目录：[[00-Vector2]]
- 下一页：[[32-SignedAngle]]


