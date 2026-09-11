> 原文：[Transform.LookAt](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.LookAt.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).LookAt

public void LookAt(Transform target);
public void LookAt(Transform target, Vector3 worldUp = Vector3.up);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| target | 要指向的对象。 |
| worldUp | 指定向上方向的向量。 |

### 描述

旋转 Transform，使 forward 向量指向 target 的当前位置。

随后，它会旋转 Transform，使其 up 方向向量指向由 worldUp 参数确定的方向。如果省略 worldUp 参数，函数将使用世界 Y 轴。只有当 forward 方向与 worldUp 垂直时，旋转的 up 向量才会与 worldUp 向量一致。

### 示例

~~~csharp
using UnityEngine;
// This complete script can be attached to a camera to make it
// continuously point at another object.

public class ExampleClass :  MonoBehaviour 
{
    public  Transform  target;

    void  Update ()
    {
        //  Rotate  the camera every frame so it keeps looking at the target
        transform.LookAt(target);

        // Same as above, but setting the worldUp parameter to  Vector3.left  in this example turns the camera on its side
        transform.LookAt(target,  Vector3.left );
    }
}
~~~

---

public void LookAt(Vector3 worldPosition);
public void LookAt(Vector3 worldPosition, Vector3 worldUp = Vector3.up);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| worldPosition | 要观察的点。 |
| worldUp | 指定向上方向的向量。 |

### 描述

旋转 Transform，使 forward 向量指向 worldPosition。

随后，它会旋转 Transform，使其 up 方向向量指向 worldUp 向量提示的方向。如果省略 worldUp 参数，函数将使用世界 Y 轴。只有当 forward 方向与 worldUp 垂直时，旋转的 up 向量才会与 worldUp 向量一致。

### 示例

~~~csharp
using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    void  Update ()
    {
        // Point the object at the world origin (0,0,0)
        transform.LookAt( Vector3.zero );
    }
}
~~~



