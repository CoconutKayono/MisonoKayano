> 原文：[Vector2.operator Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2-operator_Vector2.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).operator Vector3

## 声明

~~~csharp
public static implicit operator Vector3(Vector2 v);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| v | 要转换的 Vector2。 |

## 描述

将 Vector2 转换为 Vector3。

## 示例

~~~csharp
using UnityEngine;

public class ExampleScript :  MonoBehaviour 
{
    void Start()
    {
         Vector2  v2 = new  Vector2 (1, 2);
         Debug.Log (" Vector2  is: " + v2);

        // convert v2 to v3
         Vector3  v3 = v2;
         Debug.Log (" Vector3  is: " + v3);

        // convert v3 to new  Vector3 
         Debug.Log ("Set v3 to (3, 4, 5)");
        v3 = new  Vector3 (3, 4, 5);

        // convert v3 to v2
        v2 = v3;
         Debug.Log (" Vector2  is: " + v2);
    }
}
~~~

---

## 文档导航

- 上一页：[[41-operator_float2]]
- 目录：[[00-Vector2]]
- 下一页：无





