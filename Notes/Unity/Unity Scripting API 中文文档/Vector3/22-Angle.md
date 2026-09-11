> 原文：[Vector3.Angle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Angle.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Angle

## 声明

~~~csharp
public static float Angle(Vector3 from, Vector3 to);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| from | 用于测量角度差的起始向量。 |
| to | 用于测量角度差的目标向量。 |

## 返回

float The angle in degrees between the two vectors.

## 描述

计算两个向量之间的角度。

## 示例

~~~csharp
using UnityEngine;

public class AngleExample :  MonoBehaviour 
{
    public  Transform  target;

    // prints "close" if the z-axis of this transform looks
    // almost towards the target

    void  Update ()
    {
         Vector3  targetDir = target.position - transform.position;
        float angle =  Vector3.Angle (targetDir, transform.forward);

        if (angle < 5.0f)
            print("Close");
    }
}
~~~

## 相关资源

- [SignedAngle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.SignedAngle.html)

---

## 文档导航

- 上一页：[[21-ToString]]
- 目录：[[00-Vector3]]
- 下一页：[[23-ClampMagnitude]]



