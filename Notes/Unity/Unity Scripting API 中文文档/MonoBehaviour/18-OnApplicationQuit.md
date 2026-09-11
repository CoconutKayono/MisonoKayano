> 原文：[MonoBehaviour.OnApplicationQuit](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnApplicationQuit.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnApplicationQuit

## 声明

~~~csharp
public void OnApplicationQuit(...);
~~~

## 描述

应用退出前发送给所有活动的 GameObject。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnApplicationQuit()
    {
         Debug.Log (" Application  ending after " +  Time.time  + " seconds");
    }
}
~~~

---

## 文档导航

- 上一页：[[17-OnApplicationPause]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[19-OnAudioFilterRead]]





