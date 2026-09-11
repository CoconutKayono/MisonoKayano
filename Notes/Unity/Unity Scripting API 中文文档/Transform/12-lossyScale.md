> 原文：[Transform.lossyScale](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-lossyScale.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).lossyScale

public Vector3 lossyScale;

### 描述

对象的全局缩放。（只读）

请注意，如果父 Transform 具有缩放，并且子对象发生了任意旋转，则缩放会发生倾斜。因此，缩放无法准确地用三分量向量表示，只能用 3x3 矩阵表示。不过，这种表示方式使用起来非常不方便。lossyScale 是一个便利属性，会尽可能匹配实际的世界缩放。如果对象没有倾斜，则该值完全正确；如果存在倾斜，该值通常也不会有太大差异。

### 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        print(transform.lossyScale);
    }
}
~~~



