> 原文：[Transform.SetPositionAndRotation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.SetPositionAndRotation.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).SetPositionAndRotation

public void SetPositionAndRotation(Vector3 position, Quaternion rotation);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| position | 世界空间位置。 |
| rotation | 世界空间旋转。 |

### 描述

设置 Transform 组件的世界空间位置和旋转。

同时设置 Transform 的位置和旋转时，调用此方法比单独赋值给 Transform.position 和 Transform.rotation 更高效。




