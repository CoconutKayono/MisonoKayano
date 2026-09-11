> 原文：[Vector3Int.operator Vector3Int](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3Int-operator_Vector3Int.html)

# [Vector3Int](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3Int.html).operator Vector3Int

## 声明

~~~csharp
public Vector3Int operator Vector3Int(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| v | 要转换为 Vector3 的 Vector3Int。 |

## 返回

Vector3 The converted Vector3 result.

## 描述

执行与 Vector3Int 相关的隐式转换。

## 示例

~~~csharp
// Attach this script to a  GameObject .
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
         Vector3Int  a = new  Vector3Int (4,5,6);
         Debug.Log (" Input   Vector3Int  is: " + a.ToString());

        
         Vector3  result = a;
         Debug.Log (" Result   Vector3  is: " + result.ToString());
    }
}
~~~

---

## 文档导航

- 上一页：[[15-operator_Vector2Int]]
- 目录：[[00-Vector3Int]]
- 下一页：[[17-right]]



