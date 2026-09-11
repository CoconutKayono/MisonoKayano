> 原文：[MonoBehaviour.OnMouseExit](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseExit.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnMouseExit

## 声明

~~~csharp
public void OnMouseExit(...);
~~~

## 描述

鼠标离开 Collider 时调用。

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

---

## 文档导航

- 上一页：[[40-OnMouseEnter]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[42-OnMouseOver]]





