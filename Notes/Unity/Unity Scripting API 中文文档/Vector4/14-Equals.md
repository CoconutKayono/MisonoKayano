> 原文：[Vector4.Equals](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.Equals.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).Equals

## 声明

~~~csharp
public bool Equals(Object other);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 要与此向量进行比较的对象。 |

## 返回

`bool`：如果 `other` 是与此向量完全相等的 `Vector4`，则为 `true`，否则为 `false`。

## 描述

比较两个向量并判断它们是否相等。

由于浮点数精度问题，对于本质上相等但并非完全相等的向量，此方法可能返回 `false`。使用 [== 运算符](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_eq.html) 测试近似相等。

## 声明

~~~csharp
public bool Equals(Vector4 other);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 要与此向量进行比较的向量。 |

## 返回

`bool`：如果给定向量与此向量完全相等，则为 `true`，否则为 `false`。

## 描述

比较两个向量并判断它们是否相等。

由于浮点数精度问题，对于本质上相等但并非完全相等的向量，此方法可能返回 `false`。使用 [== 运算符](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_eq.html) 测试近似相等。

---

## 文档导航

- 上一页：[[13-ctor]]
- 目录：[[00-Vector4]]
- 下一页：[[15-Set]]

