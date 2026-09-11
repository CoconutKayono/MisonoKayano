> 原文：[Vector3.SmoothDamp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.SmoothDamp.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).SmoothDamp

## 声明

~~~csharp
public static Vector3 SmoothDamp(Vector3 current, Vector3 target, ref Vector3 currentVelocity, float smoothTime, float maxSpeed = Mathf.Infinity, float deltaTime = Time.deltaTime);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| current | 初始位置。 |
| target | 要移动到的位置。 |
| currentVelocity | 初始速度。函数每次在 Update 函数中运行时都会修改此值。请将此参数作为引用值传入。 |
| smoothTime | Approximately the time it will take to reach the target. A smaller value will reach the target faster. |
| maxSpeed | 移动时可达到的最大速度。默认没有最大速度。 |
| deltaTime | 调用此函数之间的时间。默认值为 Time.deltaTime，因此 SmoothDamp 每帧调用一次。 |

## 返回

Vector3 The new position, moved part of the way from current towards target .

## 描述

随时间逐渐将向量改变为目标值。

## 示例

~~~csharp
// This example creates a sphere and moves the attached  GameObject  to  
// just in front of the sphere. 
// Attach this example to a camera object to view the movement.
using UnityEngine;

public class SmoothDampExample :  MonoBehaviour 

{
    public float smoothTime = 15;
    public   Vector3  velocity = new  Vector3 (0,0,2);
     Vector3  targetPos;

    void Start()
    {
        //  Position  the camera
        transform.position = new  Vector3 (0,3,-10);
        
        // Create a sphere in front and below the camera.
         Vector3  spherePos = this.transform.position + new  Vector3 (0,-3,20);
         GameObject  sphere =  GameObject.CreatePrimitive ( PrimitiveType.Sphere );
        sphere.transform.position = spherePos;

        // Set final camera target position to just in front of the sphere
        targetPos = spherePos - new  Vector3 (0,0,2);
    }

    void  Update ()
    {
        // Smoothly move the camera towards that target position. The velocity 
        // decreases as the camera moves closer to the target position
        transform.position =  Vector3.SmoothDamp (transform.position, targetPos, ref velocity, smoothTime);
    }
}
~~~

---

## 文档导航

- 上一页：[[41-SlerpUnclamped]]
- 目录：[[00-Vector3]]
- 下一页：[[43-operator_Vector3]]




