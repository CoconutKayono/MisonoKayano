> 原文：[Vector2.SmoothDamp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.SmoothDamp.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).SmoothDamp

## 声明

~~~csharp
public static Vector2 SmoothDamp(Vector2 current, Vector2 target, ref Vector2 currentVelocity, float smoothTime, float maxSpeed = Mathf.Infinity, float deltaTime = Time.deltaTime);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| current | 当前位置。 |
| target | 目标位置。 |
| currentVelocity | 当前速度，函数内部修改。 |
| smoothTime | 达到目标所需的近似时间。 |
| maxSpeed | 最大速度。 |
| deltaTime | 此次调用经过的时间。 |

## 返回值

返回操作结果。

## 描述

随时间逐渐将向量改变为目标值。

## 示例

~~~csharp
// Smooth towards the target

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  Transform  target;
    public float smoothTime = 0.3F;
    private  Vector2  velocity =  Vector2.zero ;

    void  Update ()
    {
        // Define a target position above the target transform
         Vector2  targetPosition = target.TransformPoint(new  Vector2 (0, 5));

        // Smoothly move the camera towards that target position
        transform.position =  Vector2.SmoothDamp (transform.position, targetPosition, ref velocity, smoothTime);
    }
}
~~~

---

## 文档导航

- 上一页：[[32-SignedAngle]]
- 目录：[[00-Vector2]]
- 下一页：[[34-operator_Vector2]]


