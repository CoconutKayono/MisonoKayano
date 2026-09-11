> 原文：[Vector4.operator Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_Vector3.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator Vector4

## 参数

| 参数 | 描述 |
| --- | --- |
| v | 要转换的 Vector3。 |

## 描述

将 Vector3 转换为 Vector4。Vector3 可以隐式转换为 Vector4，结果中的 w 设置为零。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour
{
    void Start()
    {
        Vector3 color = new Vector3(1.0f, 0.25f, 0f);
        Vector4 colorWithOpacity = color;
        colorWithOpacity.w = 0.75f;
    }
}
~~~

---

## 文档导航

- 上一页：[[33-operator_Vector2]]
- 目录：[[00-Vector4]]
- 下一页：[[35-operator_Vector4]]

