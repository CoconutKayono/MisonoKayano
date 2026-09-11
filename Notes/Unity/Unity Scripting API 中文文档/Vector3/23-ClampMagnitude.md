> 原文：[Vector3.ClampMagnitude](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.ClampMagnitude.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).ClampMagnitude

## 声明

~~~csharp
public static Vector3 ClampMagnitude(Vector3 vector, float maxLength);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| vector | 要复制的向量。 |
| maxLength | 返回向量的最大长度。 |

## 返回

Vector3 A copy of vector with its magnitude clamped to maxLength .

## 描述

创建给定 Vector3 的副本，并将其长度限制为最大长度。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    // Move the object around with the arrow keys but confine it
    // to a given radius around a center point.

    public  Vector3  centerPt;
    public float radius;

    void  Update ()
    {
        // Get the new position for the object.
         Vector3  movement = new  Vector3 ( Input.GetAxis ("Horizontal"), 0,  Input.GetAxis ("Vertical"));
         Vector3  newPos = transform.position + movement;

        // Calculate the distance of the new position from the center point. Keep the direction
        // the same but clamp the length to the specified radius.
         Vector3  offset = newPos - centerPt;
        transform.position = centerPt +  Vector3.ClampMagnitude (offset, radius);
    }
}
~~~

---

## 文档导航

- 上一页：[[22-Angle]]
- 目录：[[00-Vector3]]
- 下一页：[[24-Cross]]


