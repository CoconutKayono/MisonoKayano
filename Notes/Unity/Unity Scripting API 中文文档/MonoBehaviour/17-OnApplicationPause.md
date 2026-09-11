> 原文：[MonoBehaviour.OnApplicationPause](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnApplicationPause.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnApplicationPause

## 声明

~~~csharp
public void OnApplicationPause(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| pauseStatus | True if the application is paused, False if playing. |

## 描述

播放中的应用因失去或重新获得焦点而暂停或恢复时发送给所有 GameObject。

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

- 上一页：[[16-OnApplicationFocus]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[18-OnApplicationQuit]]






