> 原文：[MonoBehaviour.Reset](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.Reset.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).Reset

## 声明

~~~csharp
public void Reset(...);
~~~

## 描述

在脚本首次附加到 GameObject 或重置时调用。

## 示例

~~~csharp
// Sets target to a default value.
// This could be used in a follow camera.

using UnityEngine;

public class Example :  MonoBehaviour 
{
    public  GameObject  target;

    void Reset()
    {
        //Output the message to the Console
         Debug.Log ("Reset");
        if (!target)
            target =  GameObject.FindWithTag ("Player");
    }
}
~~~

---

## 文档导航

- 上一页：[[63-OnWillRenderObject]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[65-Start]]



