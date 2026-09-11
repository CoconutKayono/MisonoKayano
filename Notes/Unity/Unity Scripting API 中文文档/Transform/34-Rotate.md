> 原文：[Transform.Rotate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.Rotate.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).Rotate

### 描述

使用 Transform.Rotate 以多种方式旋转 GameObject。旋转通常使用 Euler 角而不是 Quaternion 提供。

可以指定使用世界轴或局部轴进行旋转。世界轴旋转使用 Scene 的坐标系，因此开始旋转 GameObject 时，其 x、y 和 z 轴与世界 x、y 和 z 轴对齐。因此，如果在世界空间中旋转立方体，其轴会与世界对齐。在 Unity Editor 的 Scene 视图中选择立方体时，旋转 Gizmos 会显示左右、上下和前后旋转轴。移动这些 Gizmos 会使立方体绕这些轴旋转。如果取消选择后重新选择立方体，轴会重新回到世界对齐状态。局部旋转使用 GameObject 自身的坐标系。因此，新创建的立方体的 x、y 和 z 轴使用零旋转。旋转立方体会更新旋转轴。如果取消选择后重新选择立方体，轴会保持之前的方向。未使用 Local Gizmo Toggle 旋转的立方体、使用 Local Gizmo Toggle 旋转的立方体、未使用 Global Gizmo Toggle 旋转的立方体、使用 Global Gizmo Toggle 旋转的立方体。有关 Unity 中旋转的更多信息，请参阅《使用 Quaternion 类控制旋转》。

public void Rotate(Vector3 eulers, Space relativeTo = Space.Self);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| eulers | 要应用的 Euler 角旋转。 |
| relativeTo | 确定是相对于 GameObject 的局部空间旋转，还是相对于 Scene 世界空间旋转。 |

### 描述

按以下顺序分别绕 z 轴旋转 eulerAngles.z 度、绕 x 轴旋转 eulerAngles.x 度、绕 y 轴旋转 eulerAngles.y 度。

Rotate 接受一个作为 Euler 角的 Vector3 参数。第二个参数是旋转轴，可以设置为局部轴（Space.Self）或全局轴（Space.World）。旋转量由 Euler 角决定。

---

public void Rotate(float xAngle, float yAngle, float zAngle, Space relativeTo = Space.Self);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| xAngle | 绕 X 轴旋转 GameObject 的角度。 |
| yAngle | 绕 Y 轴旋转 GameObject 的角度。 |
| zAngle | 绕 Z 轴旋转 GameObject 的角度。 |
| relativeTo | 确定是相对于 GameObject 的局部空间旋转，还是相对于 Scene 世界空间旋转。 |

### 描述

此方法的实现按以下顺序分别绕 z 轴旋转 zAngle 度、绕 x 轴旋转 xAngle 度、绕 y 轴旋转 yAngle 度。

Rotate 可以使用三个 float 指定 x、y 和 z 的 Euler 角。示例展示了两个立方体：一个使用 Space.Self（GameObject 的局部空间和轴），另一个使用 Space.World（相对于 Scene 的空间和轴）。它们都会先绕 X 轴旋转 90 度，因此默认不会与世界轴对齐。可以使用 Inspector 中公开的 xAngle、yAngle 和 zAngle 值，观察不同旋转值如何应用于两个立方体。你可能会注意到，立方体的当前方向和 Space 选项会影响其视觉旋转方式。尝试在 Scene 视图中选择立方体并调整值，以理解这些值之间的相互作用。

### 示例

~~~csharp
using UnityEngine;

//  Transform.Rotate  example
//
// This script creates two different cubes: one red which is rotated using  Space.Self ; one green which is rotated using  Space.World .
// Add it onto any  GameObject  in a scene and hit play to see it run. The rotation is controlled using xAngle, yAngle and zAngle, modifiable on the inspector.

public class ExampleScript :  MonoBehaviour 
{
    public float xAngle, yAngle, zAngle;

    private  GameObject  cube1, cube2;

    void Awake()
    {
        cube1 =  GameObject.CreatePrimitive ( PrimitiveType.Cube );
        cube1.transform.position = new  Vector3 (0.75f, 0.0f, 0.0f);
        cube1.transform.Rotate(90.0f, 0.0f, 0.0f,  Space.Self );
        cube1.GetComponent< Renderer >().material.color =  Color.red ;
        cube1.name = "Self";

        cube2 =  GameObject.CreatePrimitive ( PrimitiveType.Cube );
        cube2.transform.position = new  Vector3 (-0.75f, 0.0f, 0.0f);
        cube2.transform.Rotate(90.0f, 0.0f, 0.0f,  Space.World );
        cube2.GetComponent< Renderer >().material.color =  Color.green ;
        cube2.name = "World";
    }

    void  Update ()
    {
        cube1.transform.Rotate(xAngle, yAngle, zAngle,  Space.Self );
        cube2.transform.Rotate(xAngle, yAngle, zAngle,  Space.World );
    }
}
~~~

---

public void Rotate(Vector3 axis, float angle, Space relativeTo = Space.Self);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| axis | 要应用旋转的轴。 |
| angle | 要应用的旋转角度。 |
| relativeTo | 确定是相对于 GameObject 的局部空间旋转，还是相对于 Scene 世界空间旋转。 |

### 描述

围绕给定轴旋转对象，旋转角度由给定 angle 定义。Rotate 接受轴、角度以及局部或全局参数。旋转轴可以指向任意方向。

---

public void Rotate(Vector3 eulers);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| eulers | 要应用的 Euler 角旋转。 |

### 描述

按以下顺序分别绕 z 轴旋转 eulerAngles.z 度、绕 x 轴旋转 eulerAngles.x 度、绕 y 轴旋转 eulerAngles.y 度。旋转相对于 GameObject 的局部空间（Space.Self）。

---

public void Rotate(float xAngle, float yAngle, float zAngle);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| xAngle | 绕 X 轴旋转 GameObject 的角度。 |
| yAngle | 绕 Y 轴旋转 GameObject 的角度。 |
| zAngle | 绕 Z 轴旋转 GameObject 的角度。 |

### 描述

此方法的实现按以下顺序分别绕 z 轴旋转 zAngle 度、绕 x 轴旋转 xAngle 度、绕 y 轴旋转 yAngle 度。旋转相对于 GameObject 的局部空间（Space.Self）。

---

public void Rotate(Vector3 axis, float angle);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| axis | 要应用旋转的轴。 |
| angle | 要应用的旋转角度。 |

### 描述

围绕给定轴旋转对象，旋转角度由给定 angle 定义。Rotate 接受轴、角度以及局部或全局参数。旋转轴可以指向任意方向。旋转相对于 GameObject 的局部空间（Space.Self）。



