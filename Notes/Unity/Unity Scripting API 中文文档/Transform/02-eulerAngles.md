> 原文：[Transform.eulerAngles](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-eulerAngles.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).eulerAngles

public Vector3 eulerAngles;

#### 描述

以度数表示的旋转 Euler 角。

Transform.eulerAngles 表示世界空间中的旋转。在 Inspector 中查看 GameObject 的旋转时，可能会看到与此属性中存储的角度值不同的值。这是因为 Inspector 显示的是局部旋转，详情请参阅 [Transform.localEulerAngles](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-localEulerAngles.html)。

Euler 角可以通过围绕各个轴执行三次独立旋转来表示三维旋转。在 Unity 中，这些旋转依次围绕 Z 轴、X 轴和 Y 轴执行。

可以通过设置此属性来设置 Quaternion 的旋转，也可以通过读取此属性来读取 Euler 角值。

使用 .eulerAngles 属性设置旋转时，需要理解：虽然你提供了 X、Y 和 Z 旋转值来描述旋转，但这些值不会存储在旋转中。相反，X、Y 和 Z 值会被转换为 Quaternion 的内部格式。

读取 .eulerAngles 属性时，Unity 会将 Quaternion 的内部旋转表示转换为 Euler 角。由于任意给定旋转都可以用多种 Euler 角表示，因此读回的值可能与赋值时的值大不相同。如果你尝试逐步递增这些值来生成动画，这可能会造成困惑。

为了避免这类问题，建议在处理旋转时不要依赖读取 .eulerAngles 得到一致的结果，尤其是在尝试逐步递增旋转来生成动画时。有关更好的实现方式，请参阅 [Quaternion * 运算符](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion-operator_multiply.html)。

下面的示例演示如何根据用户输入，使用 eulerAngles 旋转 GameObject。示例表明，我们不会依赖读取 Quaternion.eulerAngles 来递增旋转，而是使用 Vector3 currentEulerAngles 设置旋转。所有旋转变化都发生在 currentEulerAngles 变量中，然后将其应用于 Quaternion，从而避免上述问题。

```csharp
using UnityEngine;
public class ExampleScript : MonoBehaviour
{
    float rotationSpeed = 45;
    Vector3 currentEulerAngles;
    float x;
    float y;
    float z;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.X)) x = 1 - x;
        if (Input.GetKeyDown(KeyCode.Y)) y = 1 - y;
        if (Input.GetKeyDown(KeyCode.Z)) z = 1 - z;

        //modifying the Vector3, based on input multiplied by speed and time
        currentEulerAngles += new Vector3(x, y, z) * Time.deltaTime * rotationSpeed;

        //apply the change to the gameObject
        transform.eulerAngles = currentEulerAngles;
    }

    void OnGUI()
    {
        GUIStyle style = new GUIStyle();
        style.fontSize = 24;
        GUI.Label(new Rect(10, 0, 0, 0), "Rotating on X:" + x + " Y:" + y + " Z:" + z, style);

        GUI.Label(new Rect(10, 25, 0, 0), "Transform.eulerAngle: " + transform.eulerAngles, style);
    }
}
```

不要单独设置 eulerAngles 的某一个轴（例如 eulerAngles.x = 10;），因为这会导致漂移和不期望的旋转。设置新值时，应像上面的示例一样一次性设置全部轴。Unity 会将角度转换为 [Transform.rotation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-rotation.html) 中存储的旋转，并从该旋转转换回来。

角度以 360 度为模。例如，指定 1、361 或 -17999 会得到相同的角度，正如上一个示例所示，其中 currentEulerAngles 的 x、y 和 z 会随时间递增并超过 360。


