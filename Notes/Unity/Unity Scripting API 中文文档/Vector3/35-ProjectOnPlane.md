> 原文：[Vector3.ProjectOnPlane](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.ProjectOnPlane.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).ProjectOnPlane

## 声明

~~~csharp
public static Vector3 ProjectOnPlane(Vector3 vector, Vector3 planeNormal);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| vector | 要投影到平面上的向量。 |
| planeNormal | 定义投影平面的法向量。 |

## 返回

Vector3 The vector that results from projection of vector on the plane.

## 描述

将向量投影到平面上。

## 示例

~~~csharp
// This example rotates a cube above a tilted plane. As the cube rotates, the cube's position vector is projected onto the plane and rendered as a line. 

using UnityEngine;

public class ProjectOnPlaneExampleUpdate:  MonoBehaviour 
{
     GameObject  groundPlane;
     GameObject  rotObject;
     LineRenderer  line;
    

    void Start ()
    {
        // Create the plane
        groundPlane =  GameObject.CreatePrimitive ( PrimitiveType.Plane );
        groundPlane.transform.Rotate(-30, 10, 0);

        // Create the item to rotate    
        rotObject =  GameObject.CreatePrimitive ( PrimitiveType.Cube );
        rotObject.transform.position = new  Vector3 (5,5,0);
        line = rotObject.AddComponent< LineRenderer >();
    }

    void  Update ()
    {
        // Set the rotation origin
         Vector3  origin =  Vector3.zero ;

        //  Rotate  the object above the plane
        rotObject.transform.RotateAround(origin,  Vector3.up , 20 *  Time.deltaTime );

        // Project the location of the cube onto the plane
         Vector3  projected =  Vector3.ProjectOnPlane (rotObject.transform.position, groundPlane.transform.up);

        // Draw the projected vector as a line
        line.SetPosition(0, origin);
        line.SetPosition(1, projected);
        line.startWidth = 0.1f;  
    
    }
}
~~~

## 相关资源

- [Project](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Project.html)
- [Reflect](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Reflect.html)

---

## 文档导航

- 上一页：[[34-Project]]
- 目录：[[00-Vector3]]
- 下一页：[[36-Reflect]]



