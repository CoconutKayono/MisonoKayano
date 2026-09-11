> 原文：[Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).InverseTransformDirection

public Vector3 InverseTransformDirection(Vector3 direction);

### 描述

将方向从世界空间变换到局部空间。与 [Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html) 相反。

此操作不受 Transform 的缩放或位置影响。变换后的向量与原向量长度相同。如果需要将向量从局部空间变换到世界空间的逆操作，可以使用 [Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)。如果向量表示空间中的位置而不是方向，应使用 [Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)。如果需要一次变换多个方向，请考虑使用 [Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)，因为它比重复调用此函数快得多。

### 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // transform the world forward into local space:
         Vector3  relative;
        relative = transform.InverseTransformDirection( Vector3.forward );
         Debug.Log (relative);
    }
}
~~~

相关资源：[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)、[Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)、[Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)、[Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)。

---

public Vector3 InverseTransformDirection(float x, float y, float z);

### 描述

将方向 x、y、z 从世界空间变换到局部空间。与 [Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html) 相反。

此操作不受 Transform 的缩放或位置影响。变换后的向量与原向量长度相同。如果需要将向量从局部空间变换到世界空间的逆操作，可以使用 [Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)。如果向量表示空间中的位置而不是方向，应使用 [Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)。如果需要一次变换多个方向，请考虑使用 [Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)，因为它比重复调用此函数快得多。

### 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // transform the world forward into local space:
         Vector3  relative;
        relative = transform.InverseTransformDirection( Vector3.forward );
         Debug.Log (relative);
    }
}
~~~

相关资源：[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)、[Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)、[Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)、[Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)。


