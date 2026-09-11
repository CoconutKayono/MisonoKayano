> 原文：[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).TransformPoint

public Vector3 TransformPoint(Vector3 position);

### 描述

将位置从局部空间变换到世界空间。

请注意，返回的位置会受到缩放影响。如果处理的是方向向量，请使用 [Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)。可以使用 [Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html) 执行从世界空间到局部空间的逆转换。如果需要一次变换多个点，请考虑使用 [Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)，因为它比重复调用此函数快得多。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  someObject;
    public  Vector3  thePosition;

    void Start()
    {
        // Instantiate an object to the right of the current object
        thePosition = transform.TransformPoint( Vector3.right  * 2);
        Instantiate(someObject, thePosition, someObject.transform.rotation);
    }
}
~~~

相关资源：[Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)、[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)、[Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html)。

---

public Vector3 TransformPoint(float x, float y, float z);

### 描述

将位置 x、y、z 从局部空间变换到世界空间。

请注意，返回的位置会受到缩放影响。如果处理的是方向向量，请使用 [Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)。可以使用 [Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html) 执行从世界空间到局部空间的逆转换。如果需要一次变换多个点，请考虑使用 [Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)，因为它比重复调用此函数快得多。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  someObject;

    void Start()
    {
        // Instantiate an object to the right of the current object
         Vector3  thePosition = transform.TransformPoint(2, 0, 0);
        Instantiate(someObject, thePosition, someObject.transform.rotation);
    }
}
~~~

相关资源：[Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)、[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)、[Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html)。



