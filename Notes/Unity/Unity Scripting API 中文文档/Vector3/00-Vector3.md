> 原文：[Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html)

# Vector3

- 命名空间：UnityEngine
- 实现接口：IEquatable<Vector3>、IFormattable

## 描述

3D 向量和点的表示。

此结构在 Unity 中用于传递 3D 位置和方向，也包含执行常用向量运算的函数。还可以使用 Quaternion 和 Matrix4x4 等类操作向量和点，例如旋转或变换向量和点。

## 静态属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-back]] | back | Vector3(0, 0, -1) 的简写。 |
| [[02-down]] | down | Vector3(0, -1, 0) 的简写。 |
| [[03-forward]] | forward | Vector3(0, 0, 1) 的简写。 |
| [[04-left]] | left | Vector3(-1, 0, 0) 的简写。 |
| [[05-negativeInfinity]] | negativeInfinity | Vector3(float.NegativeInfinity, float.NegativeInfinity, float.NegativeInfinity) 的简写。 |
| [[06-one]] | one | Vector3(1, 1, 1) 的简写。 |
| [[07-positiveInfinity]] | positiveInfinity | Vector3(float.PositiveInfinity, float.PositiveInfinity, float.PositiveInfinity) 的简写。 |
| [[08-right]] | right | Vector3(1, 0, 0) 的简写。 |
| [[09-up]] | up | Vector3(0, 1, 0) 的简写。 |
| [[10-zero]] | zero | Vector3(0, 0, 0) 的简写。 |

## 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[11-magnitude]] | magnitude | 返回此向量的长度。（只读） |
| [[12-normalized]] | normalized | 返回当前向量方向上的单位向量。 |
| [[13-sqrMagnitude]] | sqrMagnitude | 返回此向量长度的平方。（只读） |
| [[14-Index_operator]] | this[int] | 使用 [0]、[1]、[2] 分别访问 x、y、z 分量。 |
| [[15-x]] | x | 向量的 X 分量。 |
| [[16-y]] | y | 向量的 Y 分量。 |
| [[17-z]] | z | 向量的 Z 分量。 |

## 构造函数

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[18-ctor]] | Vector3 | 创建新的三维向量或点。 |

## 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[19-Equals]] | Equals | 检查给定对象是否与此向量完全相等。 |
| [[20-Set]] | Set | 设置现有 Vector3 的 x、y、z 分量。 |
| [[21-ToString]] | ToString | 将此向量格式化为字符串。 |

## 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[22-Angle]] | Angle | 计算两个向量之间的角度。 |
| [[23-ClampMagnitude]] | ClampMagnitude | 创建长度限制为最大值的 Vector3 副本。 |
| [[24-Cross]] | Cross | 计算两个三维向量的叉积。 |
| [[25-Distance]] | Distance | 计算两个三维点之间的距离。 |
| [[26-Dot]] | Dot | 计算同一坐标空间中两个三维向量的点积。 |
| [[27-Lerp]] | Lerp | 在两个点之间线性插值。 |
| [[28-LerpUnclamped]] | LerpUnclamped | 在两个向量之间线性插值，允许超出端点。 |
| [[29-Max]] | Max | 使用两个向量的较大分量创建向量。 |
| [[30-Min]] | Min | 使用两个向量的较小分量创建向量。 |
| [[31-MoveTowards]] | MoveTowards | 将向量逐步移向目标点。 |
| [[32-Normalize]] | Normalize | 在保持方向的同时将当前向量长度归一化为 1。 |
| [[33-OrthoNormalize]] | OrthoNormalize | 使向量归一化并彼此正交。 |
| [[34-Project]] | Project | 将向量投影到另一个向量上。 |
| [[35-ProjectOnPlane]] | ProjectOnPlane | 将向量投影到平面上。 |
| [[36-Reflect]] | Reflect | 使向量从由法向量定义的平面反射。 |
| [[37-RotateTowards]] | RotateTowards | 将向量 current 旋转到 target。 |
| [[38-Scale]] | Scale | 按分量相乘两个向量。 |
| [[39-SignedAngle]] | SignedAngle | 使用第三个向量确定符号，计算两个向量之间的有符号角度。 |
| [[40-Slerp]] | Slerp | 在两个三维向量之间进行球面插值。 |
| [[41-SlerpUnclamped]] | SlerpUnclamped | 在两个向量之间进行球面插值。 |
| [[42-SmoothDamp]] | SmoothDamp | 随时间逐渐将向量改变为目标值。 |

## 运算符

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[43-operator_Vector3]] | float3 | 将 Vector3 转换为 float3。 |
| [[44-operator_subtract]] | operator - | 从一个向量中减去另一个向量。 |
| [[45-operator_ne]] | operator != | 如果向量不同，则返回 true。 |
| [[46-operator_multiply]] | operator * | 将向量乘以数字。 |
| [[47-operator_divide]] | operator / | 将向量除以数字。 |
| [[48-operator_add]] | operator + | 按分量相加两个三维向量。 |
| [[49-operator_eq]] | operator == | 如果两个向量近似相等，则返回 true。 |
| [[50-operator_float3]] | Vector3 | 将 float3 转换为 Vector3。 |

---

## 文档导航

- 上一页：无
- 目录：[[00-Vector3]]
- 下一页：[[01-back]]
