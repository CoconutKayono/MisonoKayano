> 原文：[Transform.hasChanged](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-hasChanged.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).hasChanged

public bool hasChanged;

### 描述

自上次将标志设为 false 后，Transform 是否发生了变化。

任何可能导致 Transform 矩阵重新计算的变化都可能触发此标志，包括位置、旋转或缩放的任意调整，或父级发生变化。会改变 Transform 的操作不会在设置此标志前检查新值是否与之前的值不同。例如，设置 transform.position 总是会将 Transform 上的 hasChanged 设置为 true，无论实际值是否发生变化。对象实例化时会为其分配位置，这会将此标志设置为 true。Unity 不会将其设置为 false，因此如果需要，必须自行将其设置为 false。之后可以检查此标志，以确定对象的 Transform 自上次将其设置为 false 后是否发生了变化。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void  Update ()
    {
        //Checking if any change happened
        if (transform.hasChanged)
        {
            print("The transform has changed!");

            //Reset the flag to start detecting change from this moment
            transform.hasChanged = false;
        }
    }
}
~~~



