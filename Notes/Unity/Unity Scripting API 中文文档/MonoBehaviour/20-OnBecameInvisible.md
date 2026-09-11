> 原文：[MonoBehaviour.OnBecameInvisible](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnBecameInvisible.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnBecameInvisible

## 声明

~~~csharp
public void OnBecameInvisible(...);
~~~

## 描述

当 Renderer 不再被任何摄像机看到时调用。

## 示例

~~~csharp
// Disables the behaviour when it is invisible

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnBecameInvisible()
    {
        enabled = false;
    }
}
~~~

---

## 文档导航

- 上一页：[[19-OnAudioFilterRead]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[21-OnBecameVisible]]





