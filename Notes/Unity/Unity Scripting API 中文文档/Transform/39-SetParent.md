> 原文：[Transform.SetParent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.SetParent.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).SetParent

public void SetParent(Transform p);
public void SetParent(Transform parent, bool worldPositionStays);

### 参数

| 参数 | 中文说明 |
| --- | --- |
| parent | 要设置的父 Transform。 |
| worldPositionStays | 是否保留世界位置、旋转和缩放。 |

### 描述

设置 Transform 的父级。

此方法与 parent 属性相同，但还允许 Transform 保留其局部方向，而不是其全局方向。例如，如果 GameObject 之前位于其父对象旁边，将 worldPositionStays 设置为 false 会使 GameObject 相对于新父对象保持相同的相邻方式。worldPositionStays 参数的默认值为 true。下面的图像展示了包含三个 GameObject 的场景：新的父立方体、父球体和子球体。新的父立方体位于屏幕左侧，子球体位于其原始位置，即屏幕右侧父球体旁边。调用 SetParent 并将 worldPositionStays 设置为 true 后，所有对象都保持在其原始位置。调用 SetParent 并将 worldPositionStays 设置为 false 后，子球体位置保持不变，但现在相对于新的父立方体。

### 示例

~~~csharp
using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  child;

    public  Transform  parent;

    //Invoked when a button is clicked.
    public void Example( Transform  newParent)
    {
        // Sets "newParent" as the new parent of the child  GameObject .
        child.transform.SetParent(newParent);

        // Same as above, except worldPositionStays set to false
        // makes the child keep its local orientation rather than
        // its global orientation.
        child.transform.SetParent(newParent, false);

        // Setting the parent to ‘null’ unparents the  GameObject 
        // and turns child into a top-level object in the hierarchy
        child.transform.SetParent(null);
    }
}
~~~


