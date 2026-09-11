> 原文：[MonoBehaviour.OnMouseOver](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseOver.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnMouseOver

## 声明

~~~csharp
public void OnMouseOver(...);
~~~

## 描述

鼠标停留在 Collider 上时调用。

## 示例

~~~csharp
//Attach this script to a  GameObject  to have it output messages when your mouse hovers over it.
using UnityEngine;

public class OnMouseOverExample :  MonoBehaviour 
{
    void OnMouseOver()
    {
        //If your mouse hovers over the  GameObject  with the script attached, output this message
         Debug.Log ("Mouse is over  GameObject .");
    }

    void OnMouseExit()
    {
        //The mouse is no longer hovering over the  GameObject  so output this message each frame
         Debug.Log ("Mouse is no longer on  GameObject .");
    }
}
~~~

~~~csharp
// This second example changes the  GameObject 's color to red when the mouse hovers over it
// Ensure the  GameObject  has a  MeshRenderer 

using UnityEngine;

public class OnMouseOverColor :  MonoBehaviour 
{
    //When the mouse hovers over the  GameObject , it turns to this color (red)
     Color  m_MouseOverColor =  Color.red ;

    //This stores the  GameObject ’s original color
     Color  m_OriginalColor;

    //Get the  GameObject ’s mesh renderer to access the  GameObject ’s material and color
     MeshRenderer  m_Renderer;

    void Start()
    {
        //Fetch the mesh renderer component from the  GameObject 
        m_Renderer = GetComponent< MeshRenderer >();
        //Fetch the original color of the  GameObject 
        m_OriginalColor = m_Renderer.material.color;
    }

    void OnMouseOver()
    {
        // Change the color of the  GameObject  to red when the mouse is over  GameObject 
        m_Renderer.material.color = m_MouseOverColor;
    }

    void OnMouseExit()
    {
        // Reset the color of the  GameObject  back to normal
        m_Renderer.material.color = m_OriginalColor;
    }
}
~~~

---

## 文档导航

- 上一页：[[41-OnMouseExit]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[43-OnMouseUp]]





