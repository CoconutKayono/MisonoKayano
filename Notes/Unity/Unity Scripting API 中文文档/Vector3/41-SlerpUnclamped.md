> 原文：[Vector3.SlerpUnclamped](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.SlerpUnclamped.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).SlerpUnclamped

## 声明

~~~csharp
public static Vector3 SlerpUnclamped(Vector3 a, Vector3 b, float t);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要在其间插值的第一个向量。 |
| b | 要在其间插值的第二个向量。 |
| t | 插值量。 |

## 返回

Vector3 The spherically interpolated vector between a and b . Values of t outside the range [0, 1] extrapolate beyond a or b .

## 描述

在两个向量之间进行球面插值。

## 相关资源

- [Slerp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Slerp.html)

---

## 文档导航

- 上一页：[[40-Slerp]]
- 目录：[[00-Vector3]]
- 下一页：[[42-SmoothDamp]]





