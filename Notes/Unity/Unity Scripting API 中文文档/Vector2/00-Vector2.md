> 原文：[Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html)

# Vector2

- 命名空间：UnityEngine
- 实现接口：IEquatable<Vector2>、IFormattable

## 描述

2D 向量和点的表示。

此结构用于某些场合表示 2D 位置和向量，例如 Mesh 中的纹理坐标或 Material 中的纹理偏移。在大多数其他情况下使用 Vector3。

## 静态属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-down]] | down | Vector2(0, -1) 的简写。 |
| [[02-left]] | left | Vector2(-1, 0) 的简写。 |
| [[03-negativeInfinity]] | negativeInfinity | Vector2(float.NegativeInfinity, float.NegativeInfinity) 的简写。 |
| [[04-one]] | one | Vector2(1, 1) 的简写。 |
| [[05-positiveInfinity]] | positiveInfinity | Vector2(float.PositiveInfinity, float.PositiveInfinity) 的简写。 |
| [[06-right]] | right | Vector2(1, 0) 的简写。 |
| [[07-up]] | up | Vector2(0, 1) 的简写。 |
| [[08-zero]] | zero | Vector2(0, 0) 的简写。 |

## 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[09-magnitude]] | magnitude | 返回此向量的长度。（只读） |
| [[10-normalized]] | normalized | 返回基于当前向量的归一化向量。 |
| [[11-sqrMagnitude]] | sqrMagnitude | 返回此向量长度的平方。（只读） |
| [[12-Index_operator]] | this[int] | 使用 [0] 或 [1] 分别访问 x 或 y 分量。 |
| [[13-x]] | x | 向量的 X 分量。 |
| [[14-y]] | y | 向量的 Y 分量。 |

## 构造函数

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[15-ctor]] | Vector2 | 使用给定的 x、y 分量构造新向量。 |

## 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[16-Equals]] | Equals | 判断给定向量是否与此向量完全相等。 |
| [[17-Set]] | Set | 设置现有 Vector2 的 x、y 分量。 |
| [[18-ToString]] | ToString | 将此向量格式化为字符串。 |

## 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[19-Angle]] | Angle | 获取 from 与 to 之间的无符号角度。 |
| [[20-ClampMagnitude]] | ClampMagnitude | 创建给定向量的副本，并将其长度限制为最大长度。 |
| [[21-Distance]] | Distance | 返回 a 与 b 之间的距离。 |
| [[22-Dot]] | Dot | 计算两个向量的点积。 |
| [[23-Lerp]] | Lerp | 按 t 在线性插值 a 与 b。 |
| [[24-LerpUnclamped]] | LerpUnclamped | 按 t 在线性插值 a 与 b。 |
| [[25-Max]] | Max | 使用两个向量的较大分量创建向量。 |
| [[26-Min]] | Min | 使用两个向量的较小分量创建向量。 |
| [[27-MoveTowards]] | MoveTowards | 将点 current 移向 target。 |
| [[28-Normalize]] | Normalize | 使此向量的长度为 1。 |
| [[29-Perpendicular]] | Perpendicular | 返回垂直于此 2D 向量的 2D 向量。 |
| [[30-Reflect]] | Reflect | 使向量从由法线定义的表面反射。 |
| [[31-Scale]] | Scale | 按分量相乘两个向量。 |
| [[32-SignedAngle]] | SignedAngle | 获取 from 与 to 之间的有符号角度。 |
| [[33-SmoothDamp]] | SmoothDamp | 随时间逐渐将向量改变为目标值。 |

## 运算符

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[34-operator_Vector2]] | float2 | 将 Vector2 转换为 float2。 |
| [[35-operator_subtract]] | operator - | 从一个向量中减去另一个向量。 |
| [[36-operator_multiply]] | operator * | 将向量乘以数字。 |
| [[37-operator_divide]] | operator / | 将向量除以数字。 |
| [[38-operator_add]] | operator + | 将两个向量相加。 |
| [[39-operator_eq]] | operator == | 如果两个向量近似相等，则返回 true。 |
| [[40-operator_Vector3]] | Vector2 | 将 Vector3 转换为 Vector2。 |
| [[41-operator_float2]] | Vector2 | 将 float2 转换为 Vector2。 |
| [[42-operator_Vector2]] | Vector3 | 将 Vector2 转换为 Vector3。 |

---

## 文档导航

- 上一页：无
- 目录：[[00-Vector2]]
- 下一页：[[01-down]]
