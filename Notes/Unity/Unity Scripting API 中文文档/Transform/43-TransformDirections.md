> 原文：[Transform.TransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirections.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).TransformDirections

public void TransformDirections(Span<Vector3> directions);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| directions | 要变换的方向，每个方向都会被变换后的版本替换。 |

### 描述

将多个方向从局部空间变换到世界空间，并使用变换后的版本覆盖每个原始方向。

此操作不受 Transform 的缩放或位置影响。变换后的向量与原向量长度相同。如果需要将向量从世界空间变换到局部空间的逆操作，可以使用 [Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)。如果这些向量表示位置而不是方向，应使用 [Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)。

相关资源：[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)、[Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)、[Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)、[Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)。

---

public void TransformDirections(ReadOnlySpan<Vector3> directions, Span<Vector3> transformedDirections);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| directions | 要变换的方向，除非与 transformedDirections Span 重叠，否则函数不会修改这些方向。 |
| transformedDirections | 接收变换后方向的 Span，其长度必须与 directions 相同，否则会引发异常。如果此 Span 与 directions 重叠，但并不表示完全相同的元素，则行为未定义。 |

### 描述

将多个方向从局部空间变换到世界空间，并将变换后的方向写入可能不同的位置。

此操作不受 Transform 的缩放或位置影响。变换后的向量与原向量长度相同。如果需要将向量从世界空间变换到局部空间的逆操作，可以使用 [Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)。如果这些向量表示位置而不是方向，应使用 [Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)。

相关资源：[Transform.TransformDirection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirection.html)、[Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)、[Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)、[Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)。


