> 原文：[Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).TransformVector

public Vector3 TransformVector(Vector3 vector);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| vector | 要变换的局部空间向量。 |

#### 返回值

Vector3 变换后的向量（位于世界空间中）。

### 描述

将向量从局部空间变换到世界空间。

此操作不受 Transform 位置影响，但会受到缩放影响。返回向量的长度可能与 vector 不同。如果需要将向量从世界空间变换到局部空间的逆操作，可以使用 [Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)。如果需要一次变换多个向量，请考虑使用 [Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)，因为它比重复调用此函数快得多。

相关资源：[Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)、[Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)、[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)。

---

public Vector3 TransformVector(float x, float y, float z);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| x | 局部空间向量的 x 分量。 |
| y | 局部空间向量的 y 分量。 |
| z | 局部空间向量的 z 分量。 |

#### 返回值

Vector3 变换后的向量（位于世界空间中）。

### 描述

将向量 x、y、z 从局部空间变换到世界空间。

此操作不受 Transform 位置影响，但会受到缩放影响。返回向量的长度可能与向量不同。如果需要将向量从世界空间变换到局部空间的逆操作，可以使用 [Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)。如果需要一次变换多个向量，请考虑使用 [Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)，因为它比重复调用此函数快得多。

相关资源：[Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)、[Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)、[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)。


