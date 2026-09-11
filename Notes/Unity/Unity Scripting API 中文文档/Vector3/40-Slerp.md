> 原文：[Vector3.Slerp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Slerp.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Slerp

## 声明

~~~csharp
public static Vector3 Slerp(Vector3 a, Vector3 b, float t);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | 要在其间进行插值的第一个 Vector3 方向。 |
| b | 要在其间进行插值的第二个 Vector3 方向。 |
| t | 插值参数，预期范围为 [0,1]。 |

## 返回

Vector3 The resulting spherically interpolated Vector3 direction.

## 描述

在两个三维向量之间进行球面插值。

## 示例

~~~csharp
// Animates the position in an arc between sunrise and sunset.

using UnityEngine;
using System.Collections;

public class Vector3SlerpExample :  MonoBehaviour 
{
    public  Transform  sunrise;
    public  Transform  sunset;

    //  Time  to move from sunrise to sunset position, in seconds.
    public float journeyTime = 1.0f;

    // The time at which the animation started.
    private float startTime;

    void Start()
    {
        // Note the time at the start of the animation.
        startTime =  Time.time ;
    }

    void  Update ()
    {
        // The center of the arc
         Vector3  center = (sunrise.position + sunset.position) * 0.5F;

        // move the center a bit downwards to make the arc vertical
        center -= new  Vector3 (0, 1, 0);

        // Interpolate over the arc relative to center
         Vector3  riseRelCenter = sunrise.position - center;
         Vector3  setRelCenter = sunset.position - center;

        // The fraction of the animation that has happened so far is
        // equal to the elapsed time divided by the desired time for
        // the total journey.
        float fracComplete = ( Time.time  - startTime) / journeyTime;

        transform.position =  Vector3.Slerp (riseRelCenter, setRelCenter, fracComplete);
        transform.position += center;
    }
}
~~~

## 相关资源

- [Lerp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Lerp.html)
- [SlerpUnclamped](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.SlerpUnclamped.html)

---

## 文档导航

- 上一页：[[39-SignedAngle]]
- 目录：[[00-Vector3]]
- 下一页：[[41-SlerpUnclamped]]



