> 原文：[Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).InverseTransformPoint

public Vector3 InverseTransformPoint(Vector3 position);

### 描述

将位置从世界空间变换到局部空间。

此函数本质上是 [Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html) 的逆操作，Transform.TransformPoint 用于将位置从局部空间转换到世界空间。请注意，返回的位置会受到缩放影响。如果处理的是方向向量而不是位置，请使用 [Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)。如果需要一次变换多个点，请考虑使用 [Transform.InverseTransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoints.html)，因为它比重复调用此函数快得多。

### 示例

~~~csharp
// Calculate the transform's position relative to the camera.
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  Transform  cam;
    public  Vector3  cameraRelative;

    void Start()
    {
        cam = Camera.main.transform;
         Vector3  cameraRelative = cam.InverseTransformPoint(transform.position);

        if (cameraRelative.z > 0)
            print("The object is in front of the camera");
        else
            print("The object is behind the camera");
    }
}
~~~

相关资源：[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.InverseTransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoints.html)、[Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)、[Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)。

---

public Vector3 InverseTransformPoint(float x, float y, float z);

### 描述

将位置 x、y、z 从世界空间变换到局部空间。

此函数本质上是 [Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html) 的逆操作，Transform.TransformPoint 用于将位置从局部空间转换到世界空间。请注意，返回的位置会受到缩放影响。如果处理的是方向向量而不是位置，请使用 [Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)。如果需要一次变换多个点，请考虑使用 [Transform.InverseTransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoints.html)，因为它比重复调用此函数快得多。

### 示例

~~~csharp
// Calculate the world origin relative to this transform.
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Start()
    {
         Vector3  relativePoint = transform.InverseTransformPoint(0, 0, 0);

        if (relativePoint.z > 0)
            print("The world origin is in front of this object");
        else
            print("The world origin is behind this object");
    }
}
~~~

相关资源：[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.InverseTransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoints.html)、[Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)、[Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)。



