> 原文：[Transform.Translate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.Translate.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).Translate

public void Translate(Vector3 translation);
public void Translate(Vector3 translation, Space relativeTo = Space.Self);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| translation | 要应用的平移量。 |
| relativeTo | 确定是相对于 Transform 的局部空间移动，还是相对于 Scene 世界空间移动。 |

### 描述

沿 Transform 的 x、y 和 z 轴，分别按照 translation 参数的 x、y 和 z 分量移动。

如果省略 relativeTo 或将其设置为 Space.Self，则相对于 Transform 的局部轴移动（即在 Scene 视图中选择对象时显示的 x、y 和 z 轴）。如果 relativeTo 为 Space.World，则相对于世界坐标系移动。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void  Update ()
    {
        // Move the object forward along its z axis 1 unit/second.
        transform.Translate( Vector3.forward  *  Time.deltaTime );

        // Move the object upward in world space 1 unit/second.
        transform.Translate( Vector3.up  *  Time.deltaTime ,  Space.World );
    }
}
~~~

---

public void Translate(float x, float y, float z);
public void Translate(float x, float y, float z, Space relativeTo = Space.Self);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| x | 沿 x 轴移动的距离。 |
| y | 沿 y 轴移动的距离。 |
| z | 沿 z 轴移动的距离。 |
| relativeTo | 确定是相对于 Transform 的局部空间移动，还是相对于 Scene 世界空间移动。 |

### 描述

沿 x 轴移动 x，沿 y 轴移动 y，沿 z 轴移动 z。

如果省略 relativeTo 或将其设置为 Space.Self，则相对于 Transform 的局部轴移动（即在 Scene 视图中选择对象时显示的 x、y 和 z 轴）。如果 relativeTo 为 Space.World，则相对于世界坐标系移动。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void  Update ()
    {
        // Move the object forward along its z axis 1 unit/second.
        transform.Translate(0, 0,  Time.deltaTime );

        // Move the object upward in world space 1 unit/second.
        transform.Translate(0,  Time.deltaTime , 0,  Space.World );
    }
}
~~~

---

public void Translate(Vector3 translation, Transform relativeTo);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| translation | 要应用的平移量。 |
| relativeTo | 要使用其局部坐标系的 Transform。 |

### 描述

沿 Transform 的 x、y 和 z 轴，分别按照 translation 参数的 x、y 和 z 分量移动。

移动相对于 relativeTo 的局部坐标系进行。如果 relativeTo 为 null，则相对于世界坐标系移动。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void  Update ()
    {
        // Move the object to the right relative to the camera 1 unit/second.
        transform.Translate( Vector3.right  *  Time.deltaTime , Camera.main.transform);
    }
}
~~~

---

public void Translate(float x, float y, float z, Transform relativeTo);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| x | 沿 x 轴移动的距离。 |
| y | 沿 y 轴移动的距离。 |
| z | 沿 z 轴移动的距离。 |
| relativeTo | 要使用其局部坐标系的 Transform。 |

### 描述

沿 x 轴移动 x，沿 y 轴移动 y，沿 z 轴移动 z。

移动相对于 relativeTo 的局部坐标系进行。如果 relativeTo 为 null，则相对于世界坐标系移动。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void  Update ()
    {
        // Move the object to the right relative to the camera 1 unit/second.
        transform.Translate( Time.deltaTime , 0, 0, Camera.main.transform);
    }
}
~~~



