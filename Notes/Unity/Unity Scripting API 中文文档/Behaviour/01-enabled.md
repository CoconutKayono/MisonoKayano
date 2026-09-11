> 原文：[Behaviour.enabled](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Behaviour-enabled.html)

# [Behaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Behaviour.html).enabled

## 声明

~~~csharp
public bool enabled;
~~~

## 描述

启用 Behaviour 时，对应 GameObject、脚本和其他脚本回调会处于启用状态。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI; // Required when Using UI elements.

public class Example :  MonoBehaviour 
{
    public  Image  pauseMenu;

    public void Start()
    {
        //Enables the pause menu UI.
        pauseMenu.enabled = true;
    }
}
~~~
