> 原文：[Vector3.Dot](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Dot.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Dot

## 声明

~~~csharp
public static float Dot(Vector3 lhs, Vector3 rhs);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| lhs | 点积的左操作数。 |
| rhs | 点积的右操作数。 |

## 返回

float The dot product of the lhs and rhs vectors.

## 描述

计算同一坐标空间中两个三维向量的点积。

## 示例

~~~csharp
// detects if other transform is behind this object

using UnityEngine;
using System.Collections;

public class Vector3DotProductExample :  MonoBehaviour 
{
    public  Transform  other;

    void  Update ()
    {
        if (other)
        {
            // transform the forward vector from local to world space
             Vector3  forward = transform.TransformDirection( Vector3.forward );
            // calculate a unit vector from the other object to this object
             Vector3  toOther =  Vector3.Normalize (other.position - transform.position);
            // use the dot product sign to determine whether other is in front or behind
            if ( Vector3.Dot (forward, toOther) < 0)
            {
                print("The other transform is behind me!");
            }
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[25-Distance]]
- 目录：[[00-Vector3]]
- 下一页：[[27-Lerp]]


