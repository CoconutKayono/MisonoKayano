> 原文：[MonoBehaviour.OnApplicationFocus](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnApplicationFocus.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnApplicationFocus

## 声明

~~~csharp
public void OnApplicationFocus(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| hasFocus | True if the GameObjects have focus, else False. |

## 描述

当应用获得或失去焦点时发送给所有 GameObject。

## 示例

~~~csharp
using UnityEngine;

public class AppPaused :  MonoBehaviour 
{
    bool isPaused = false;

    void OnGUI()
    {
        if (isPaused)
             GUI.Label (new  Rect (100, 100, 50, 30), "Game paused");
    }

    void OnApplicationFocus(bool hasFocus)
    {
        isPaused = !hasFocus;
    }

    void OnApplicationPause(bool pauseStatus)
    {
        isPaused = pauseStatus;
    }
}
~~~

---

## 文档导航

- 上一页：[[15-OnAnimatorMove]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[17-OnApplicationPause]]






