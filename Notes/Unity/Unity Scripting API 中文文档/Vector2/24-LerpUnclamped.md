> 原文：[Vector2.LerpUnclamped](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.LerpUnclamped.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).LerpUnclamped

## 声明

~~~csharp
public static Vector2 LerpUnclamped(Vector2 a, Vector2 b, float t);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| a | 起始向量。 |
| b | 结束向量。 |
| t | 插值系数。 |

## 返回值

返回操作结果。

## 描述

按 t 在线性插值 a 与 b，t 不会限制在 [0, 1] 范围内。

## 相关资源

- [Lerp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.Lerp.html)

---

## 文档导航

- 上一页：[[23-Lerp]]
- 目录：[[00-Vector2]]
- 下一页：[[25-Max]]


