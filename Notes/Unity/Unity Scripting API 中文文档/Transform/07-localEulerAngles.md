> 原文：[Transform.localEulerAngles](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-localEulerAngles.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).localEulerAngles

public Vector3 localEulerAngles;

### 描述

相对于父 Transform 旋转、以度数表示的 Euler 角旋转。

Euler 角可以通过围绕各个轴执行三次独立旋转来表示三维旋转。在 Unity 中，这些旋转依次围绕 Z 轴、X 轴和 Y 轴执行。

可以通过设置此属性来设置 Quaternion 的旋转，也可以通过读取此属性来读取 Euler 角值。使用 eulerAngles 属性设置旋转时，需要理解：虽然你提供了 X、Y 和 Z 旋转值来描述旋转，但这些值不会存储在旋转中。相反，X、Y 和 Z 值会被转换为 Quaternion 的内部格式。

读取 eulerAngles 属性时，Unity 会将 Quaternion 的内部旋转表示转换为 Euler 角。由于任意给定旋转都可以用多种 Euler 角表示，因此读回的值可能与赋值时的值大不相同。如果你尝试逐步递增这些值来生成动画，这可能会造成困惑。

为了避免这类问题，建议在处理旋转时不要依赖读取 eulerAngles 得到一致的结果，尤其是在尝试逐步递增旋转来生成动画时。有关更好的实现方式，请参阅 Quaternion * 运算符。

下面的示例演示如何根据用户输入，使用 eulerAngles 旋转 GameObject。示例表明，我们不会依赖读取 Quaternion.eulerAngles 来递增旋转，而是使用 Vector3 currentEulerAngles 设置旋转。所有旋转变化都发生在 currentEulerAngles 变量中，然后将其应用于 Quaternion，从而避免上述问题。

### 示例

~~~csharp
using UnityEngine;
public class ExampleScript :  MonoBehaviour 
{
    float rotationSpeed = 45;
     Vector3  currentEulerAngles;
    float x;
    float y;
    float z;

    void  Update ()
    {
        if ( Input.GetKeyDown ( KeyCode.X )) x = 1 - x;
        if ( Input.GetKeyDown ( KeyCode.Y )) y = 1 - y;
        if ( Input.GetKeyDown ( KeyCode.Z )) z = 1 - z;
    
        //modifying the  Vector3 , based on input multiplied by speed and time
        currentEulerAngles += new  Vector3 (x, y, z) *  Time.deltaTime  * rotationSpeed;
    
        //apply the change to the gameObject
        transform.localEulerAngles = currentEulerAngles;
    }

    void OnGUI()
    {
         GUIStyle  style = new  GUIStyle ();
        style.fontSize = 24;
         GUI.Label (new  Rect (10, 0, 0, 0), "Rotating on X:" + x + " Y:" + y + " Z:" + z, style);

         GUI.Label (new  Rect (10, 50, 0, 0), "Transform.localEulerAngle: " + transform.localEulerAngles, style);
    }
}
~~~

Unity 会自动将角度转换为 Transform.localRotation 中存储的旋转，并从该旋转转换回来。


