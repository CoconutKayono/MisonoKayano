> 原文：[Vector4.MoveTowards](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.MoveTowards.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).MoveTowards

## 声明

~~~csharp
public static Vector4 MoveTowards(Vector4 current, Vector4 target, float maxDistanceDelta);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| current | 当前点。 |
| target | 目标点。 |
| maxDistanceDelta | 允许的最大距离。使用负值会将向量推离目标。 |

## 返回

`Vector4`：从 current 向 target 移动、最多移动 maxDistanceDelta 的新位置。

## 描述

将点 current 向 target 移动。这基本上与 [Vector4.Lerp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Lerp.html) 相同，但此方法确保移动距离不会超过 maxDistanceDelta。maxDistanceDelta 为负值时，会将向量推离 target。

---

## 文档导航

- 上一页：[[22-Min]]
- 目录：[[00-Vector4]]
- 下一页：[[24-Normalize]]

