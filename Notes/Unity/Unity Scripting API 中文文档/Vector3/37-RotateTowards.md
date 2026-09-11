> 原文：[Vector3.RotateTowards](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.RotateTowards.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).RotateTowards

## 声明

~~~csharp
public static Vector3 RotateTowards(Vector3 current, Vector3 target, float maxRadiansDelta, float maxMagnitudeDelta);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| current | 要处理的向量。 |
| target | 目标向量。 |
| maxRadiansDelta | 此旋转允许的最大弧度角。 |
| maxMagnitudeDelta | 此旋转允许的向量长度最大变化量。 |

## 返回

Vector3 The location that RotateTowards generates.

## 描述

将向量 current 旋转到 target。

## 示例

~~~csharp
using UnityEngine;

// To use this script, attach it to the  GameObject  that you would like to rotate towards another game object.
// After attaching it, go to the inspector and drag the  GameObject  you would like to rotate towards into the target field.
// Move the target around in the scene view to see the  GameObject  continuously rotate towards it.
public class Example :  MonoBehaviour 
{
    // The target marker.
    public  Transform  target;

    // Angular speed in radians per sec.
    public float speed = 1.0f;

    void  Update ()
    {
        // Determine which direction to rotate towards
         Vector3  targetDirection = target.position - transform.position;

        // The step size is equal to speed times frame time.
        float singleStep = speed *  Time.deltaTime ;

        //  Rotate  the forward vector towards the target direction by one step
         Vector3  newDirection =  Vector3.RotateTowards (transform.forward, targetDirection, singleStep, 0.0f);

        // Draw a ray pointing at our target in
         Debug.DrawRay (transform.position, newDirection,  Color.red );

        // Calculate a rotation a step closer to the target and applies rotation to this object
        transform.rotation =  Quaternion.LookRotation (newDirection);
    }
}
~~~

## 相关资源

- [Quaternion.RotateTowards](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.RotateTowards.html)

---

## 文档导航

- 上一页：[[36-Reflect]]
- 目录：[[00-Vector3]]
- 下一页：[[38-Scale]]



