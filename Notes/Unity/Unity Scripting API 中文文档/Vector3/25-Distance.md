> 原文：[Vector3.Distance](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Distance.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Distance

## 声明

~~~csharp
public static float Distance(Vector3 a, Vector3 b);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 作为 Vector3 的第一个三维点。 |
| b | 作为 Vector3 的第二个三维点。 |

## 返回

float The scalar distance between points a and b .

## 描述

计算两个三维点之间的距离。

## 示例

~~~csharp
using UnityEngine;

public class Vector3DistanceExample :  MonoBehaviour 
{
    // the first point is this transform's position
    public  Transform  other;

    void Start()
    {
        if (other)
        {
            // the second point is the position of the  MonoBehaviour 's transform
            float dist =  Vector3.Distance (other.position, transform.position);
            print("Distance to other: " + dist);
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[24-Cross]]
- 目录：[[00-Vector3]]
- 下一页：[[26-Dot]]


