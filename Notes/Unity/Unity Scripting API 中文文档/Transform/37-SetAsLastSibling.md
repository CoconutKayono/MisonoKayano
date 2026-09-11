> 原文：[Transform.SetAsLastSibling](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.SetAsLastSibling.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).SetAsLastSibling

public void SetAsLastSibling();

### 描述

将 Transform 移到局部 Transform 列表的末尾。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI; //Required when using UI Elements.
using UnityEngine.EventSystems; // Required when using event data.

public class ExampleClass :  MonoBehaviour , IPointerDownHandler
{
    public  RectTransform  panelRectTransform;

    //Invoked when the mouse pointer goes down on a UI element.
    public void OnPointerDown(PointerEventData data)
    {
        // Puts the panel to the front as it is now the last UI element to be drawn.
        panelRectTransform.SetAsLastSibling();
    }
}
~~~




