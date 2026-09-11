> 原文：[Transform.GetLocalPositionAndRotation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.GetLocalPositionAndRotation.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).GetLocalPositionAndRotation

public void GetLocalPositionAndRotation(out Vector3 localPosition, out Quaternion localRotation);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| localPosition | 局部位置输出值。 |
| localRotation | 局部旋转输出值。 |

### 描述

使用 Transform 当前的局部空间位置和旋转更新 out 参数 localPosition 和 localRotation。

注意：同时获取 Transform 的 localPosition 和 localRotation 时，调用此方法比单独查询 Transform.localPosition 和 Transform.localRotation 稍高效。如果 Transform 没有父级，调用此方法等价于调用 Transform.GetPositionAndRotation。此方法通常用于获取 Transform 在局部空间中的位置和旋转，以便显示或评估。例如：transform.GetLocalPositionAndRotation(out Vector3 localPosition, out Quaternion localRotation)。下面的示例记录 GameObject 的 Transform 在局部空间中的位置和旋转。

### 示例

~~~csharp
using UnityEngine;

// Attach this script to a  GameObject  as a component.
public class GetLocalPositionAndRotationExample :  MonoBehaviour 
{
    void Start()
    {
        // transform refers to the  Transform  of the  GameObject  this script is attached to.
        transform.GetLocalPositionAndRotation(out  Vector3  localPosition, out  Quaternion  localRotation);

        // We will convert the rotation  Quaternion  to Euler angles for readability.
         Debug.Log ($"{name} is located at {localPosition}, and has the rotation {localRotation.eulerAngles} relative to its parent.");
    }
}
~~~

相关资源：[Quaternion](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.html)、[Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html)。
