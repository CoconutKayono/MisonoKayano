> 原文：[Transform.RotateAround](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.RotateAround.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).RotateAround

public void RotateAround(Vector3 point, Vector3 axis, float angle);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| point | 轴经过的世界空间点。 |
| axis | 旋转轴。 |
| angle | 旋转角度。 |

### 描述

围绕穿过世界坐标 point 的轴旋转 Transform，旋转角度为 angle。

这会同时修改 Transform 的位置和旋转，但不会影响其缩放。如果提供的轴的长度过于接近零，则函数会直接返回而不执行任何旋转。有关 Unity 中旋转的更多信息，请参阅《使用 Quaternion 类控制旋转》。相关资源：Transform.Rotate。

### 示例

~~~csharp
using UnityEngine;

//Attach this script to a  GameObject  to rotate around the target position.
public class Example :  MonoBehaviour 
{
    //Assign a  GameObject  in the Inspector to rotate around
    public  GameObject  target;

    void  Update ()
    {
        // Spin the object around the target at 20 degrees/second.
        transform.RotateAround(target.transform.position,  Vector3.up , 20 *  Time.deltaTime );
    }
}
~~~


