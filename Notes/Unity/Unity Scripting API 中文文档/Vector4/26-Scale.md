> 原文：[Vector4.Scale](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Scale.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).Scale

## 声明

~~~csharp
public static Vector4 Scale(Vector4 a, Vector4 b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要相乘的第一个向量。 |
| b | 要相乘的第二个向量。 |

## 返回

`Vector4`：每个分量都是 a 与 b 对应分量乘积的向量。

## 描述

按分量相乘两个向量。结果中的每个分量都是 a 的分量与 b 中相同分量的乘积。

## 示例

~~~csharp
public void Scale(Vector4 scale);
~~~

## 声明

~~~csharp
public void Scale(Vector4 scale);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| scale | 按分量与此向量相乘的向量。 |

## 描述

将此向量的每个分量与 scale 的相应分量相乘。

---

## 文档导航

- 上一页：[[25-Project]]
- 目录：[[00-Vector4]]
- 下一页：[[27-operator_Vector4]]

