> 原文：[Vector4.operator Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4-operator_Vector2.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).operator Vector4

## 参数

| 参数 | 描述 |
| --- | --- |
| v | 要转换的 Vector2。 |

## 描述

将 Vector2 转换为 Vector4。Vector2 可以隐式转换为 Vector4，结果中的 z 和 w 设置为零。

## 示例

~~~csharp
using UnityEngine;
using System.Collections.Generic;

public class ExampleScript : MonoBehaviour
{
    void Start()
    {
        Renderer renderer = GetComponent<Renderer>();
        renderer.material.SetVector("_SomeVariable", Vector2.one);
    }
}
~~~

---

## 文档导航

- 上一页：[[32-operator_eq]]
- 目录：[[00-Vector4]]
- 下一页：[[34-operator_Vector3]]

