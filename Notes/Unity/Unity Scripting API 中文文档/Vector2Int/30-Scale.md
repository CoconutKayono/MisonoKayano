> 原文：[Vector2Int.Scale](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2Int.Scale.html)

# [Vector2Int](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2Int.html).Scale

## 声明

~~~csharp
public static Vector2Int Scale(Vector2Int a, Vector2Int b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要与 b 相乘的向量。 |
| b | 要与 a 相乘的向量。 |

## 返回

Vector2Int：a 的每个分量与 b 的相应分量相乘的结果。

## 描述

按分量相乘两个向量。结果中的每个分量都是 a 的分量与 b 中相同分量的乘积。

## 声明

~~~csharp
public void Scale(Vector2Int scale);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| scale | 要与此向量相乘的向量。 |

## 描述

将此向量的每个分量与 scale 的相应分量相乘。

---

## 文档导航

- 上一页：[[29-RoundToInt]]
- 目录：[[00-Vector2Int]]
- 下一页：[[31-Set]]

