> 原文：[Vector2Int](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2Int.html)

# Vector2Int

## 描述

使用整数表示二维向量和点。

此结构用于某些不需要浮点精度的二维位置和向量表示场合。

## 静态属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-down]] | down | Vector2Int(0, -1) 的简写。 |
| [[02-left]] | left | Vector2Int(-1, 0) 的简写。 |
| [[04-one]] | one | Vector2Int(1, 1) 的简写。 |
| [[14-right]] | right | Vector2Int(1, 0) 的简写。 |
| [[16-up]] | up | Vector2Int(0, 1) 的简写。 |
| [[19-zero]] | zero | Vector2Int(0, 0) 的简写。 |

## 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[03-magnitude]] | magnitude | 返回此向量的长度（只读）。 |
| [[15-sqrMagnitude]] | sqrMagnitude | 返回此向量长度的平方（只读）。 |
| [[26-Index_operator]] | this[int] | 分别使用 [0] 或 [1] 访问 x 或 y 分量。 |
| [[17-x]] | x | 向量的 X 分量。 |
| [[18-y]] | y | 向量的 Y 分量。 |

## 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[21-Clamp]] | Clamp | 将 Vector2Int 限制在 min 和 max 给定的边界内。 |
| [[23-Equals]] | Equals | 判断向量与对象是否相等。 |
| [[25-GetHashCode]] | GetHashCode | 获取 Vector2Int 的哈希代码。 |
| [[31-Set]] | Set | 设置现有 Vector2Int 的 x 和 y 分量。 |
| [[32-ToString]] | ToString | 将此向量格式化为字符串。 |

## 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[20-CeilToInt]] | CeilToInt | 对每个值向上取整，将 Vector2 转换为 Vector2Int。 |
| [[22-Distance]] | Distance | 计算两个向量之间的距离。 |
| [[24-FloorToInt]] | FloorToInt | 对每个值向下取整，将 Vector2 转换为 Vector2Int。 |
| [[27-Max]] | Max | 使用两个向量的最大分量创建向量。 |
| [[28-Min]] | Min | 使用两个向量的最小分量创建向量。 |
| [[29-RoundToInt]] | RoundToInt | 对每个值进行舍入，将 Vector2 转换为 Vector2Int。 |
| [[30-Scale]] | Scale | 按分量相乘两个向量。 |

## 运算符

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[08-operator_int2]] | int2 | 将 Vector2Int 转换为 int2。 |
| [[11-operator_subtract]] | operator - | 从一个向量中减去另一个向量。 |
| [[10-operator_ne]] | operator != | 如果向量不同，则返回 true。 |
| [[09-operator_multiply]] | operator * | 将一个向量乘以另一个向量。 |
| [[06-operator_divide]] | operator / | 将向量除以一个数字。 |
| [[05-operator_add]] | operator + | 将两个向量相加。 |
| [[07-operator_eq]] | operator == | 如果两个向量相等，则返回 true。 |
| [[12-operator_Vector2Int]] | Vector2 | 将 Vector2Int 转换为 Vector2。 |
| [[12-operator_Vector2Int]] | Vector2Int | 将 int2 转换为 Vector2Int。 |
| [[13-operator_Vector3Int]] | Vector3Int | 将 Vector2Int 转换为 Vector3Int。 |

---

## 文档导航

- 上一页：无
- 目录：[[00-Vector2Int]]
- 下一页：[[01-down]]
