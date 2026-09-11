> 原文：[Transform.localScale](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-localScale.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).localScale

public Vector3 localScale;

### 描述

相对于 GameObject 父级的 Transform 缩放。

下面的示例创建一个缩放为 (1,1,1) 的球体 GameObject。随后，应用程序会反复将 Transform.localScale 从 1.0 缩小到 0.25，再恢复到 1.0。

### 示例

~~~csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Example :  MonoBehaviour 
{
    private  GameObject  sphere;
    private  Vector3  scaleChange, positionChange;

    void Awake()
    {
        Camera.main.clearFlags =  CameraClearFlags.SolidColor ;

        // Create a sphere at the origin.
        sphere =  GameObject.CreatePrimitive ( PrimitiveType.Sphere );
        sphere.transform.position = new  Vector3 (0, 0, 0);

        // Create a plane and move down by 0.5.
         GameObject  plane =  GameObject.CreatePrimitive ( PrimitiveType.Plane );
        plane.transform.position = new  Vector3 (0, -0.5f, 0);

        // Change the floor color to blue.
        // The blue material is present in  Resources  and not created in this script.
         Renderer  rend = plane.GetComponent< Renderer >();
        rend.material =  Resources.Load < Material >("blue");

        scaleChange = new  Vector3 (-0.01f, -0.01f, -0.01f);
        positionChange = new  Vector3 (0.0f, -0.005f, 0.0f);
    }

    void  Update ()
    {
        sphere.transform.localScale += scaleChange;
        sphere.transform.position += positionChange;

        // Move upwards when the sphere hits the floor or downwards
        // when the sphere scale extends 1.0f.
        if (sphere.transform.localScale.y < 0.1f || sphere.transform.localScale.y > 1.0f)
        {
            scaleChange = -scaleChange;
            positionChange = -positionChange;
        }
    }
}
~~~



