> 原文：[Transform.InverseTransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVectors.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).InverseTransformVectors

### 参数

| 参数 | 中文说明 |
| --- | --- |
| vectors | 要变换的向量，每个向量都会被变换后的版本替换。 |

### 描述

将多个向量从世界空间变换到局部空间，并使用变换后的版本覆盖每个原始位置。与 [Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html) 相反。

此操作不受 Transform 的位置影响，但会受到缩放影响。变换后的向量长度可能与原向量不同。相关资源：[Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)、[Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)、[Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)、[Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)。

---

public void InverseTransformVectors(ReadOnlySpan<Vector3> vectors, Span<Vector3> transformedVectors);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| vectors | 要变换的向量，除非与 transformedVectors Span 重叠，否则函数不会修改这些向量。 |
| transformedVectors | 接收变换后向量的 Span，其长度必须与 vectors 相同，否则会引发异常。如果此 Span 与 vectors 重叠，但并不表示完全相同的元素，则行为未定义。 |

### 描述

将向量 x、y、z 从世界空间变换到局部空间，并将变换后的位置写入可能不同的位置。与 [Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html) 相反。

此操作不受 Transform 的位置影响，但会受到缩放影响。变换后的向量长度可能与原向量不同。相关资源：[Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)、[Transform.InverseTransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVector.html)、[Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)、[Transform.InverseTransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirection.html)。



