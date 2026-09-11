> 原文：[Transform.TransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoints.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).TransformPoints

public void TransformPoints(Span<Vector3> positions);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| positions | 要变换的位置，每个位置都会被变换后的版本替换。 |

### 描述

将多个点从局部空间变换到世界空间，并使用变换后的版本覆盖每个原始点。

请注意，返回点的位置会受到缩放影响。如果处理的是方向向量，请使用 [Transform.TransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirections.html)。可以使用 [Transform.InverseTransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoints.html) 执行从世界空间到局部空间的逆转换。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  someObject;

    const int kNumPoints = 100;

    void Start()
    {
        // Instantiate 100 objects to the right of the current object
         Vector3 [] points = new  Vector3 [kNumPoints];
        for (int pointNum = 0; pointNum < kNumPoints; pointNum++)
        {
            points[pointNum] =  Vector3.right  * pointNum;
        }
        transform.TransformPoints(points);
        for (int pointNum = 0; pointNum < kNumPoints; pointNum++)
        {
            Instantiate(someObject, points[pointNum], someObject.transform.rotation);
        }
    }
}
~~~

相关资源：[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.InverseTransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoints.html)、[Transform.TransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirections.html)、[Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)。

---

public void TransformPoints(ReadOnlySpan<Vector3> positions, Span<Vector3> transformedPositions);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| positions | 要变换的位置，除非与 transformedPositions Span 重叠，否则函数不会修改这些位置。 |
| transformedPositions | 接收变换后位置的 Span，其长度必须与 positions 相同，否则会引发异常。如果此 Span 与 positions 重叠，但并不表示完全相同的元素，则行为未定义。 |

### 描述

将多个点从局部空间变换到世界空间，并将变换后的点写入可能不同的位置。

请注意，返回点的位置会受到缩放影响。如果处理的是方向向量，请使用 [Transform.TransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirections.html)。可以使用 [Transform.InverseTransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoints.html) 执行从世界空间到局部空间的逆转换。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  someObject;

    const int kNumPoints = 100;

    void Start()
    {
        // Instantiate 100 objects to the right of the current object
         Vector3 [] points = new  Vector3 [kNumPoints];
        for (int pointNum = 0; pointNum < kNumPoints; pointNum++)
        {
            points[pointNum] =  Vector3.right  * pointNum;
        }
         Vector3 [] transformedPoints = new  Vector3 [kNumPoints];
        transform.TransformPoints(points, transformedPoints);
        for (int pointNum = 0; pointNum < kNumPoints; pointNum++)
        {
            Instantiate(someObject, transformedPoints[pointNum], someObject.transform.rotation);
        }
    }
}
~~~

相关资源：[Transform.TransformPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformPoint.html)、[Transform.InverseTransformPoints](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.InverseTransformPoints.html)、[Transform.TransformDirections](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformDirections.html)、[Transform.TransformVectors](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.TransformVectors.html)。



