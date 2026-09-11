> 原文：[Transform.localRotation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-localRotation.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).localRotation

public Quaternion localRotation;

### 描述

相对于父 Transform 旋转的 Transform 旋转。

Unity 在内部使用 Quaternion 存储旋转。要旋转对象，请使用 Transform.Rotate。要以 Euler 角修改旋转，请使用 Transform.localEulerAngles。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        transform.localRotation =  Quaternion.identity ;
    }
}
~~~

另一个示例：

~~~csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//  Rotate  a cylinder around the x and z axes. Switch from one to the other
// when the rotation in the current axis reaches 360 degrees.

public class ExampleScript :  MonoBehaviour 
{
    private float x;
    private float z;
    private bool rotateX;
    private float rotationSpeed;

    void Start()
    {
        x = 0.0f;
        z = 0.0f;
        rotateX = true;
        rotationSpeed = 75.0f;
    }

    void  FixedUpdate ()
    {
        if (rotateX == true)
        {
            x +=  Time.deltaTime  * rotationSpeed;

            if (x > 360.0f)
            {
                x = 0.0f;
                rotateX = false;
            }
        }
        else
        {
            z +=  Time.deltaTime  * rotationSpeed;

            if (z > 360.0f)
            {
                z = 0.0f;
                rotateX = true;
            }
        }

        transform.localRotation =  Quaternion.Euler (x, 0, z);
    }
}
~~~


