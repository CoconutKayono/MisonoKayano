> 原文：[MonoBehaviour.OnGUI](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnGUI.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnGUI

## 声明

~~~csharp
public void OnGUI(...);
~~~

## 描述

处理 GUI 事件。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnGUI()
    {
        if ( GUI.Button (new  Rect (10, 10, 150, 100), "I am a button"))
        {
            print("You clicked the button!");
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[34-OnEnable]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[36-OnJointBreak]]



