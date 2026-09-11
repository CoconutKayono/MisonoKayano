> 原文：[Vector3.SignedAngle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.SignedAngle.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).SignedAngle

## 声明

~~~csharp
public static float SignedAngle(Vector3 from, Vector3 to, Vector3 axis);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| from | 用于测量角度差的起始向量。 |
| to | 用于测量角度差的目标向量。 |
| axis | 用于计算的参考方向。 |

## 返回

float The signed angle between from and to , in degrees.

## 描述

使用第三个向量确定符号，计算两个向量之间的有符号角度。

## 示例

~~~csharp
using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    public  Transform  target;

    void  Update ()
    {
         Vector3  targetDir = target.position - transform.position;
         Vector3  forward = transform.forward;
        float angle =  Vector3.SignedAngle (targetDir, forward,  Vector3.up );
        if (angle < -5.0F)
            print("turn right");
        else if (angle > 5.0F)
            print("turn left");
        else
            print("forward");
    }
}
~~~

## 相关资源

- [Angle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Angle.html)

---

## 文档导航

- 上一页：[[38-Scale]]
- 目录：[[00-Vector3]]
- 下一页：[[40-Slerp]]



