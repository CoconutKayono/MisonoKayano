> 原文：[Transform.localPosition](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-localPosition.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).localPosition

public Vector3 localPosition;

### 描述

相对于父 Transform 的位置。

如果 Transform 没有父级，则它与 Transform.position 相同。与大多数 Transform 操作一样，localPosition 可能并不总是可访问，尤其是在某些操作期间（例如执行撤销操作时），或在 Transform 层级完全初始化之前。例如，OnValidate() 可能会在层级完全设置之前调用，从而可能记录错误。如果尝试在不兼容的时间访问 localPosition，它将返回 Vector3.zero，而不是实际值。

请注意，在计算世界位置时，会将父 Transform 的世界旋转和缩放应用到局部位置。这意味着 Transform.position 中的 1 个单位始终是 1 个单位，而 Transform.localPosition 中的 1 个单位会受到所有祖先对象缩放的影响。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void Example()
    {
        // Move the object to the same position as the parent:
        transform.localPosition = new  Vector3 (0, 0, 0);

        // Get the y component of the position relative to the parent
        // and print it to the Console
        print(transform.localPosition.y);
    }
}
~~~



