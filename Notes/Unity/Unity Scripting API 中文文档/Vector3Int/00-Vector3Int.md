> 原文：[Vector3Int](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3Int.html)

# Vector3Int

## 描述

使用整数表示三维向量和点。

此结构用于某些不需要浮点精度的三维位置和向量表示场合。

## 静态属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-back]] | back | 负 z 方向的单位向量。 |
| [[03-down]] | down | Vector3Int(0, -1, 0) 的简写。 |
| [[04-forward]] | forward | Vector3Int(0, 0, 1) 的简写。 |
| [[05-left]] | left | Vector3Int(-1, 0, 0) 的简写。 |
| [[07-one]] | one | Vector3Int(1, 1, 1) 的简写。 |
| [[17-right]] | right | Vector3Int(1, 0, 0) 的简写。 |
| [[19-up]] | up | Vector3Int(0, 1, 0) 的简写。 |
| [[23-zero]] | zero | Vector3Int(0, 0, 0) 的简写。 |

## 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[06-magnitude]] | magnitude | 返回此向量的长度（只读）。 |
| [[18-sqrMagnitude]] | sqrMagnitude | 返回此向量长度的平方（只读）。 |
| [[30-Index_operator]] | this[int] | 分别使用 [0]、[1] 或 [2] 访问 x、y 或 z 分量。 |
| [[20-x]] | x | 向量的 X 分量。 |
| [[21-y]] | y | 向量的 Y 分量。 |
| [[22-z]] | z | 向量的 Z 分量。 |

## 构造函数

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[02-ctor]] | Vector3Int | 使用 x、y、z 分量初始化并返回新的 Vector3Int 实例。 |

## 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[25-Clamp]] | Clamp | 将 Vector3Int 限制在 min 和 max 给定的边界内。 |
| [[27-Equals]] | Equals | 判断对象是否与此向量相等。 |
| [[29-GetHashCode]] | GetHashCode | 获取 Vector3Int 的哈希代码。 |
| [[35-Set]] | Set | 设置现有 Vector3Int 的 x、y 和 z 分量。 |
| [[36-ToString]] | ToString | 将此向量格式化为字符串。 |

## 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[24-CeilToInt]] | CeilToInt | 对每个值向上取整，将 Vector3 转换为 Vector3Int。 |
| [[26-Distance]] | Distance | 计算两个给定向量之间的距离。 |
| [[28-FloorToInt]] | FloorToInt | 对给定 Vector3 的每个值向下取整并转换为 Vector3Int。 |
| [[31-Max]] | Max | 使用两个向量的最大分量创建向量。 |
| [[32-Min]] | Min | 使用两个向量的最小分量创建向量。 |
| [[33-RoundToInt]] | RoundToInt | 对 Vector3 的每个值进行舍入并转换为 Vector3Int。 |
| [[34-Scale]] | Scale | 按分量相乘两个向量。 |

## 运算符

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[11-operator_int3]] | int3 | 将 Vector3Int 转换为 int3。 |
| [[14-operator_subtract]] | operator - | 从一个向量中减去另一个向量。 |
| [[13-operator_ne]] | operator != | 如果向量不同，则返回 true。 |
| [[12-operator_multiply]] | operator * | 将一个向量乘以另一个向量。 |
| [[09-operator_divide]] | operator / | 将向量除以一个数字。 |
| [[08-operator_add]] | operator + | 将两个向量相加。 |
| [[10-operator_eq]] | operator == | 如果两个向量相等，则返回 true。 |
| [[15-operator_Vector2Int]] | Vector2Int | 将 Vector3Int 转换为 Vector2Int。 |
| [[16-operator_Vector3Int]] | Vector3 | 将 Vector3Int 转换为 Vector3。 |
| [[16-operator_Vector3Int]] | Vector3Int | 将 int3 转换为 Vector3Int。 |

---

## 文档导航

- 上一页：无
- 目录：[[00-Vector3Int]]
- 下一页：[[01-back]]
