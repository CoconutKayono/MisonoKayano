> 原文：[Vector4.operator ==](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_eq.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator ==

## 声明

~~~csharp
public static bool operator ==(Vector4 lhs, Vector4 rhs);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| lhs | 要比较的第一个向量。 |
| rhs | 要比较的第二个向量。 |

## 描述

如果两个向量近似相等，则返回 `true`。为了允许浮点数精度误差，当两个向量之差的长度小于 1e-5 时，会认为它们相等。

其他资源：[Equals](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Equals.html)。

## 相关资源

- [Equals](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Equals.html)

---

## 文档导航

- 上一页：[[31-operator_add]]
- 目录：[[00-Vector4]]
- 下一页：[[33-operator_Vector2]]


