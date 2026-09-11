> 原文：[Transform.rotation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-rotation.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).rotation

public Quaternion rotation;

### 描述

在世界空间中存储 Transform 旋转的 Quaternion。

Transform.rotation 存储一个 Quaternion。可以使用 rotation 旋转 GameObject 或提供当前旋转。不要尝试编辑或修改 rotation。Transform.rotation 小于 180 度。Transform.rotation 不会发生万向节锁。要旋转 Transform，请使用使用 Euler 角的 Transform.Rotate。如果要匹配 Inspector 中看到的值，请对返回的 Quaternion 使用 Quaternion.eulerAngles 属性。

### 示例

~~~csharp
using UnityEngine;

//  Transform.rotation  example.

//  Rotate  a  GameObject  using a  Quaternion .
// Tilt the cube using the arrow keys. When the arrow keys are released
// the cube will be rotated back to the center using Slerp.

public class ExampleScript :  MonoBehaviour 
{
    float smooth = 5.0f;
    float tiltAngle = 60.0f;

    void  Update ()
    {
        // Smoothly tilts a transform towards a target rotation.
        float tiltAroundZ =  Input.GetAxis ("Horizontal") * tiltAngle;
        float tiltAroundX =  Input.GetAxis ("Vertical") * tiltAngle;

        //  Rotate  the cube by converting the angles into a  quaternion .
         Quaternion  target =  Quaternion.Euler (tiltAroundX, 0, tiltAroundZ);

        // Dampen towards the target rotation
        transform.rotation =  Quaternion.Slerp (transform.rotation, target,   Time.deltaTime  * smooth);
    }
}
~~~

在上面的示例中，旋转由四元数描述。有关更多信息，请参阅《使用 Quaternion 类控制旋转》。


