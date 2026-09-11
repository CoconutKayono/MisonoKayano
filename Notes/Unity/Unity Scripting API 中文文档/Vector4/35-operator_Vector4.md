> 原文：[Vector4.operator Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_Vector4.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator Vector3

## 参数

| 参数 | 描述 |
| --- | --- |
| v | 要转换的 Vector4。 |

## 描述

将 Vector4 转换为 Vector3。Vector4.w 会被丢弃。

同一页面还提供将 Vector4 转换为 Vector2 的隐式转换：Vector4 的 z 和 w 分量会被丢弃。

## 示例

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        Vector4 vector4 = new Vector4(1.0f, 2.0f, 3.0f, 4.0f);
        Vector3 vector3 = vector4;
        Debug.Log("Vector3: " + vector3);
    }
}
~~~

---

## 文档导航

- 上一页：[[34-operator_Vector3]]
- 目录：[[00-Vector4]]
- 下一页：[[34-operator_Vector3]]

