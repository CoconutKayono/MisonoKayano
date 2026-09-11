> 原文：[Transform.GetChild](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.GetChild.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).GetChild

public Transform GetChild(int index);

### 参数

| 参数 | 描述 |
| --- | --- |
| index | 要返回的子 Transform 的索引。必须小于 Transform.childCount。 |

### 返回

Transform 按索引返回的子 Transform。

### 描述

按索引返回 Transform 子对象。

如果 Transform 没有子对象，或者 index 参数的值大于子对象数量，则会生成错误。此时会出现“Transform child out of bounds”错误。可以通过 childCount 获取子对象数量。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  Transform  meeple;
    public  GameObject  grandChild;

    public void Example()
    {
        //Assigns the transform of the first child of the Game Object this script is attached to.
        meeple = this.gameObject.transform.GetChild(0);

        //Assigns the first child of the first child of the Game Object this script is attached to.
        grandChild = this.gameObject.transform.GetChild(0).GetChild(0).gameObject;
    }
}
~~~





