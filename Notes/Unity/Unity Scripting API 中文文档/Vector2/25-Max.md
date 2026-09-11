> 原文：[Vector2.Max](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.Max.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).Max

## 声明

~~~csharp
public static Vector2 Max(Vector2 lhs, Vector2 rhs);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| lhs | 第一个向量。 |
| rhs | 第二个向量。 |

## 返回值

返回操作结果。

## 描述

使用两个向量的较大分量创建向量。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
         Vector2  a = new  Vector2 (1, 3);
         Vector2  b = new  Vector2 (4, 2);
        print( Vector2.Max (a, b)); // prints (4.0,3.0)
    }
}
~~~

## 相关资源

- [Min](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.Min.html)

---

## 文档导航

- 上一页：[[24-LerpUnclamped]]
- 目录：[[00-Vector2]]
- 下一页：[[26-Min]]



