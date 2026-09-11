> 原文：[Transform.SetAsFirstSibling](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.SetAsFirstSibling.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).SetAsFirstSibling

public void SetAsFirstSibling();

### 描述

将 Transform 移到局部 Transform 列表的开头。

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
        // Puts the panel to the back as it is now the first UI element to be drawn.
        panelRectTransform.SetAsFirstSibling();
    }
}
~~~




