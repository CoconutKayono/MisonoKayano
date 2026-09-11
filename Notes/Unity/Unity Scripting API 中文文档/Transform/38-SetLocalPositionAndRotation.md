> 原文：[Transform.SetLocalPositionAndRotation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.SetLocalPositionAndRotation.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).SetLocalPositionAndRotation

public void SetLocalPositionAndRotation(Vector3 localPosition, Quaternion localRotation);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| localPosition | 局部位置。 |
| localRotation | 局部旋转。 |

### 描述

在局部空间中设置 Transform 组件的位置和旋转，即相对于其父 Transform。

同时设置 Transform 的位置和旋转时，调用此方法比单独赋值给 Transform.localPosition 和 Transform.localRotation 稍高效。如果 Transform 没有父级，调用此方法等价于调用 Transform.SetPositionAndRotation。




