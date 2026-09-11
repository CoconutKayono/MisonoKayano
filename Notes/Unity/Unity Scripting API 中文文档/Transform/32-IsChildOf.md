> 原文：[Transform.IsChildOf](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.IsChildOf.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).IsChildOf

public bool IsChildOf(Transform parent);

### 描述

判断此 Transform 是否是 parent 的子对象。

返回一个布尔值，用于指示此 Transform 是否是给定 Transform 的子对象。如果此 Transform 是子对象、深层子对象（子对象的子对象）或与给定 Transform 相同，则返回 true；否则返回 false。

### 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void OnTriggerEnter( Collider  col)
    {
        // Ignore trigger events if between this collider and colliders in children
        // Eg. when you have a complex character with multiple triggers colliders.
        if (col.transform.IsChildOf(transform))
        {
            return;
        }

        print("Do something here");
    }
}
~~~






