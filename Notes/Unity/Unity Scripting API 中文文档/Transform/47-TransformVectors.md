> 原文：[Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).TransformVectors

public void TransformVectors(Span<Vector3> vectors);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| vectors | 要变换的向量，每个向量都会被变换后的版本替换。 |

### 描述

将多个向量从局部空间变换到世界空间，并使用变换后的版本覆盖每个原始向量。

此操作不受 Transform 位置影响，但会受到缩放影响。变换后的向量长度可能与原向量不同。

相关资源：[Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html)、[Transform.InverseTransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVectors.html)、[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)。

---

public void TransformVectors(ReadOnlySpan<Vector3> vectors, Span<Vector3> transformedVectors);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| vectors | 要变换的向量，除非与 transformedVectors Span 重叠，否则函数不会修改这些向量。 |
| transformedVectors | 接收变换后向量的 Span，其长度必须与 vectors 相同，否则会引发异常。如果此 Span 与 vectors 重叠，但并不表示完全相同的元素，则行为未定义。 |

### 描述

将多个向量从局部空间变换到世界空间，并将变换后的版本写入可能不同的位置。

此操作不受 Transform 位置影响，但会受到缩放影响。变换后的向量长度可能与原向量不同。

相关资源：[Transform.TransformVector](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVector.html)、[Transform.InverseTransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVectors.html)、[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)。



