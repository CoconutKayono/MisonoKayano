> 原文：[Transform.root](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-root.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).root

public Transform root;

### 描述

返回层级中最顶层的 Transform。

（此属性永远不会返回 null；如果此 Transform 没有父级，则返回其自身。）

### 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    // Is a collision between two objects with different roots?
    void OnCollisionEnter( Collision  collision)
    {
        if (collision.transform.root != transform.root)
        {
            print("The colliding objects are not in the same hierarchy");
        }
    }
}
~~~



