> 原文：[Vector4.Lerp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Lerp.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).Lerp

## 声明

~~~csharp
public static Vector4 Lerp(Vector4 a, Vector4 b, float t);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要在其间插值的第一个点。 |
| b | 要在其间插值的第二个点。 |
| t | 插值量。 |

## 返回

`Vector4`：当 t 为 0 时返回 a；当 t 为 1 时返回 b；当 t 为 0.5 时返回 a 和 b 的中点。

## 描述

在两个向量之间进行线性插值。

按 t 的量在 a 和 b 之间插值。参数 t 会限制在 `[0...1]` 范围内。当 t = 0 时返回 a；当 t = 1 时返回 b；当 t = 0.5 时返回 a 和 b 的中点。

其他资源：[LerpUnclamped](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.LerpUnclamped.html)。

## 相关资源

- [LerpUnclamped](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.LerpUnclamped.html)

---

## 文档导航

- 上一页：[[18-Dot]]
- 目录：[[00-Vector4]]
- 下一页：[[20-LerpUnclamped]]


