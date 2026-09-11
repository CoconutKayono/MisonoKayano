> 原文：[MonoBehaviour.didStart](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour-didStart.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).didStart

## 声明

~~~csharp
public bool didStart;
~~~

## 描述

指示 Start 是否已在此 MonoBehaviour 上调用。

## 示例

~~~csharp
using UnityEngine;

public class NewBehaviourScript :  MonoBehaviour 
{
    void Awake()
    {
        // Awake gets called before Start, therefore will print 'false'.
         Debug.Log (this.didStart);
    }

    void Start()
    {
        // Code is within Start, therefore will print 'true', as Start was called.
         Debug.Log (this.didStart);
    }
}
~~~

---

## 文档导航

- 上一页：[[02-didAwake]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[04-print]]



