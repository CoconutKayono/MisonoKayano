> 原文：[Behaviour.isActiveAndEnabled](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Behaviour-isActiveAndEnabled.html)

# [Behaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Behaviour.html).isActiveAndEnabled

## 声明

~~~csharp
public bool isActiveAndEnabled;
~~~

## 描述

如果 Behaviour 当前处于活动状态并已启用，则返回 true。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class Example :  MonoBehaviour 
{
    public  Image  pauseMenu;

    public void  Update ()
    {
        //Checks if the  GameObject  and  Image  are active and enabled.
        if (pauseMenu.isActiveAndEnabled)
        {
            //If the  Image  is enabled, print "Enabled" in the console. Stops when the image or  GameObject  is disabled.
             Debug.Log ("Enabled");
        }
    }
}
~~~


