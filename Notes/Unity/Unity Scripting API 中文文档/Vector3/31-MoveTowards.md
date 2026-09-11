> 原文：[Vector3.MoveTowards](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.MoveTowards.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).MoveTowards

## 声明

~~~csharp
public static Vector3 MoveTowards(Vector3 current, Vector3 target, float maxDistanceDelta);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| current | 要从其开始移动的位置。 |
| target | 要移动到的位置。 |
| maxDistanceDelta | Distance to move current per call. |

## 返回

Vector3 The new position.

## 描述

将向量逐步移向目标点。

## 示例

~~~csharp
// To run this example, create a cube  GameObject  positioned at the origin of the scene. 
// Attach this script to the cube. 
//
// This example creates a cylinder  GameObject  that becomes the target position for the 
// cube. When the cube reaches the cylinder, the cylinder is re-positioned to the 
// initial location of the cube. The cube then changes direction and moves towards the 
// cylinder again.

using UnityEngine;

public class MoveTowardsExample :  MonoBehaviour 
{
    // Adjust the speed for the application.
    public float speed = 1.0f;

    // The target (cylinder) position.
    private  Transform  target;

    void Awake()
    {
        //  Position  the cube at the origin.
        transform.position = new  Vector3 (0.0f, 0.0f, 0.0f);

        // Create and position the cylinder. Reduce the diameter.
         GameObject  cylinder =  GameObject.CreatePrimitive ( PrimitiveType.Cylinder );
        cylinder.transform.localScale = new  Vector3 (0.15f, 1.0f, 0.15f);

        // Set target value to cylinder position.
        target = cylinder.transform;
        target.transform.position = new  Vector3 (0.8f, 0.0f, 0.8f);

        //  Position  the camera.
        Camera.main.transform.position = new  Vector3 (0.85f, 1.0f, -3.0f);
        Camera.main.transform.localEulerAngles = new  Vector3 (15.0f, -20.0f, -0.5f);

        // Create and position the floor.
         GameObject  floor =  GameObject.CreatePrimitive ( PrimitiveType.Plane );
        floor.transform.position = new  Vector3 (0.0f, -1.0f, 0.0f);
    }

    void  Update ()
    {
        // Move our position a step closer to the target.
        float step =  speed *  Time.deltaTime ; // calculate distance to move
        transform.position =  Vector3.MoveTowards (transform.position, target.position, step);

        // Check if the position of the cube and sphere are approximately equal.
        if ( Vector3.Distance (transform.position, target.position) < 0.001f)
        {
            // Reset the target position to the original object position.
            target.position *= -1.0f;
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[30-Min]]
- 目录：[[00-Vector3]]
- 下一页：[[32-Normalize]]




