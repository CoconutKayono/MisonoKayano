> 原文：[Vector4.Normalize](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Normalize.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).Normalize

## 声明

~~~csharp
public void Normalize();
~~~

## 描述

使此向量的长度为 1。归一化后，向量保持相同方向，但其长度为 1.0。请注意，此函数会改变当前向量。如果希望保持当前向量不变，请使用 [normalized 属性](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-normalized.html)。如果此向量太小而无法归一化，则会将其设置为零。

其他资源：[normalized 属性](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-normalized.html)。

## 声明

~~~csharp
public static Vector4 Normalize(Vector4 a);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要归一化的向量。 |

## 返回

`Vector4`：与原向量方向相同、长度为 1.0 的新向量。

## 描述

根据给定向量返回归一化向量。归一化向量的长度为 1，方向与给定向量相同。如果给定向量太小而无法归一化，则返回零向量。请注意，此方法不会修改给定向量。若要修改并归一化当前向量，请使用不带参数的 Normalize 函数。

其他资源：[normalized 函数](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-normalized.html)。

## 相关资源

- [normalized](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-normalized.html)
- [normalized](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-normalized.html)

---

## 文档导航

- 上一页：[[23-MoveTowards]]
- 目录：[[00-Vector4]]
- 下一页：[[25-Project]]


