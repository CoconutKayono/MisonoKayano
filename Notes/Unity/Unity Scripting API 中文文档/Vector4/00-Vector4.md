> 原文：[Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html)

# Vector4

- 命名空间：UnityEngine
- 实现接口：IEquatable<Vector4>、IFormattable

## 描述

四维向量的表示。

此结构用于某些场合表示四分量向量，例如 Mesh 切线和着色器参数。在大多数其他情况下使用 Vector3。

## 静态属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-negativeInfinity]] | negativeInfinity | Vector4 四个分量均为 float.NegativeInfinity 的简写。 |
| [[02-one]] | one | Vector4(1,1,1,1) 的简写。 |
| [[03-positiveInfinity]] | positiveInfinity | Vector4 四个分量均为 float.PositiveInfinity 的简写。 |
| [[04-zero]] | zero | Vector4(0,0,0,0) 的简写。 |

## 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[05-magnitude]] | magnitude | 返回此向量的长度。（只读） |
| [[06-normalized]] | normalized | 创建基于当前向量的归一化副本。 |
| [[07-sqrMagnitude]] | sqrMagnitude | 返回此向量长度的平方。（只读） |
| [[08-Index_operator]] | this[int] | 使用 [0]、[1]、[2]、[3] 访问 x、y、z、w 分量。 |
| [[09-w]] | w | 向量的 W 分量。 |
| [[10-x]] | x | 向量的 X 分量。 |
| [[11-y]] | y | 向量的 Y 分量。 |
| [[12-z]] | z | 向量的 Z 分量。 |

## 构造函数

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[13-ctor]] | Vector4 | 使用给定的 x、y、z、w 分量创建新向量。 |

## 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[14-Equals]] | Equals | 比较两个向量并判断它们是否相等。 |
| [[15-Set]] | Set | 设置现有 Vector4 的 x、y、z、w 分量。 |
| [[16-ToString]] | ToString | 将此向量格式化为字符串。 |

## 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[17-Distance]] | Distance | 返回 a 与 b 之间的距离。 |
| [[18-Dot]] | Dot | 计算两个向量的点积。 |
| [[19-Lerp]] | Lerp | 在两个向量之间线性插值。 |
| [[20-LerpUnclamped]] | LerpUnclamped | 在两个向量之间线性插值。 |
| [[21-Max]] | Max | 使用两个向量的较大分量创建向量。 |
| [[22-Min]] | Min | 使用两个向量的较小分量创建向量。 |
| [[23-MoveTowards]] | MoveTowards | 将点 current 移向 target。 |
| [[24-Normalize]] | Normalize | 使此向量的长度为 1。 |
| [[25-Project]] | Project | 将向量投影到另一个向量上。 |
| [[26-Scale]] | Scale | 按分量相乘两个向量。 |

## 运算符

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[27-operator_Vector4]] | float4 | 将 Vector4 转换为 float4。 |
| [[28-operator_subtract]] | operator - | 从一个向量中减去另一个向量。 |
| [[29-operator_multiply]] | operator * | 将向量乘以数字。 |
| [[30-operator_divide]] | operator / | 将向量除以数字。 |
| [[31-operator_add]] | operator + | 将两个向量相加。 |
| [[32-operator_eq]] | operator == | 如果两个向量近似相等，则返回 true。 |
| [[35-operator_Vector4]] | Vector2 | 将 Vector4 转换为 Vector2。 |
| [[35-operator_Vector4]] | Vector3 | 将 Vector4 转换为 Vector3。 |
| [[34-operator_Vector3]] | Vector4 | 将 Vector3 转换为 Vector4。 |
| [[33-operator_Vector2]] | Vector4 | 将 Vector2 转换为 Vector4。 |
| [[37-operator_float4]] | Vector4 | 将 float4 转换为 Vector4。 |

---

## 文档导航

- 上一页：无
- 目录：[[00-Vector4]]
- 下一页：[[01-negativeInfinity]]
