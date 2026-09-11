> 原文：[Transform.GetPositionAndRotation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.GetPositionAndRotation.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).GetPositionAndRotation

public void GetPositionAndRotation(out Vector3 position, out Quaternion rotation);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| position | 世界空间位置输出值。 |
| rotation | 世界空间旋转输出值。 |

### 描述

使用 Transform 当前的世界空间位置和旋转更新 out 参数 position 和 rotation。

注意：同时获取 Transform 的 position 和 rotation 时，调用此方法比单独查询 Transform.position 和 Transform.rotation 更高效。此方法通常用于获取 Transform 在世界空间中的位置和旋转，以便显示或评估。例如：transform.GetPositionAndRotation(out Vector3 position, out Quaternion rotation)。下面的示例记录 GameObject 的 Transform 在世界空间中的位置和旋转。

### 示例

~~~csharp
using UnityEngine;

// Attach this script to a  GameObject  as a component.
public class GetPositionAndRotationExample :  MonoBehaviour 
{
    void Start()
    {
        // transform refers to the  Transform  of the  GameObject  this script is attached to.
        transform.GetPositionAndRotation(out  Vector3  position, out  Quaternion  rotation);

        // We will convert the rotation  Quaternion  to Euler angles for readability.
         Debug.Log ($"{name} is located at {position}, and has the rotation {rotation.eulerAngles}");
    }
}
~~~

相关资源：[Quaternion](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.html)、[Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html)。
