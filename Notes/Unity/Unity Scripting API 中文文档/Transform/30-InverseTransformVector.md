> 原文：[Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).InverseTransformVector

public Vector3 InverseTransformVector(Vector3 vector);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| vector | 要变换的世界空间向量。 |

#### 返回值

Vector3 变换后的向量（位于局部空间中）。

### 描述

将向量从世界空间变换到局部空间。与 [Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html) 相反。

此操作不受 Transform 位置影响，但会受到缩放影响。返回向量的长度可能与 vector 不同。如果需要一次变换多个向量，请考虑使用 [Transform.InverseTransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVectors.html)，因为它比重复调用此函数快得多。

相关资源：[Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html)、[Transform.InverseTransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVectors.html)、[Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)、[Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)。

---

public Vector3 InverseTransformVector(float x, float y, float z);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| x | 世界空间向量的 x 分量。 |
| y | 世界空间向量的 y 分量。 |
| z | 世界空间向量的 z 分量。 |

#### 返回值

Vector3 变换后的向量（位于局部空间中）。

### 描述

将向量 x、y、z 从世界空间变换到局部空间。与 [Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html) 相反。

此操作不受 Transform 位置影响，但会受到缩放影响。返回向量的长度可能与向量不同。如果需要一次变换多个向量，请考虑使用 [Transform.InverseTransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVectors.html)，因为它比重复调用此函数快得多。

相关资源：[Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html)、[Transform.InverseTransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVectors.html)、[Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)、[Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)。



