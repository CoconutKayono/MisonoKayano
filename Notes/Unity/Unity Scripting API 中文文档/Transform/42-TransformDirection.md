> 原文：[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).TransformDirection

public Vector3 TransformDirection(Vector3 direction);

### 描述

将方向从局部空间变换到世界空间。

此操作不受 Transform 的缩放或位置影响。返回向量与 direction 长度相同。如果需要将向量从世界空间变换到局部空间的逆操作，可以使用 [Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)。如果向量表示位置而不是方向，应使用 [Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html) 进行转换。如果需要一次变换多个方向，请考虑使用 [Transform.TransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirections.html)，因为它比重复调用此函数快得多。

相关资源：[Transform.TransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirections.html)、[Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)、[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html)。

---

public Vector3 TransformDirection(float x, float y, float z);

### 描述

将方向 x、y、z 从局部空间变换到世界空间。

此操作不受 Transform 的缩放或位置影响。返回向量与 direction 长度相同。如果需要将向量从世界空间变换到局部空间的逆操作，可以使用 [Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)。如果向量表示位置而不是方向，应使用 [Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html) 进行转换。如果需要一次变换多个方向，请考虑使用 [Transform.TransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirections.html)，因为它比重复调用此函数快得多。

相关资源：[Transform.TransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirections.html)、[Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)、[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html)。


