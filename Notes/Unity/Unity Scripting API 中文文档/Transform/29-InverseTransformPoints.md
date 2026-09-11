> 原文：[Transform.InverseTransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoints.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).InverseTransformPoints

public void InverseTransformPoints(Span<Vector3> positions);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| positions | 要变换的位置，每个位置都会被变换后的版本替换。 |

### 描述

将多个位置从世界空间变换到局部空间，并使用变换后的版本覆盖每个原始位置。

此函数本质上是 [Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html) 的逆操作，Transform.TransformPoints 用于将位置从局部空间转换到世界空间。请注意，返回的位置会受到缩放影响。如果处理的是方向向量而不是位置，请使用 [Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)。

相关资源：[Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)、[Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)、[Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)、[Transform.InverseTransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVectors.html)。

---

public void InverseTransformPoints(ReadOnlySpan<Vector3> positions, Span<Vector3> transformedPositions);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| positions | 要变换的位置，除非与 transformedPositions Span 重叠，否则函数不会修改这些位置。 |
| transformedPositions | 接收变换后位置的 Span，其长度必须与 positions 相同，否则会引发异常。如果此 Span 与 positions 重叠，但并不表示完全相同的元素，则行为未定义。 |

### 描述

将多个位置从世界空间变换到局部空间，并将变换后的位置写入可能不同的位置。

此函数本质上是 [Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html) 的逆操作，Transform.TransformPoints 用于将位置从局部空间转换到世界空间。请注意，返回的位置会受到缩放影响。如果处理的是方向向量而不是位置，请使用 [Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)。

相关资源：[Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)、[Transform.InverseTransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoint.html)、[Transform.InverseTransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformDirections.html)、[Transform.InverseTransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformVectors.html)。



