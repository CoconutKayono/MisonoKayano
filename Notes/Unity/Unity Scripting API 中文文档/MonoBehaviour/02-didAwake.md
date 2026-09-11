> 原文：[MonoBehaviour.didAwake](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour-didAwake.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).didAwake

## 声明

~~~csharp
public bool didAwake;
~~~

## 描述

指示 Awake 是否已在此 MonoBehaviour 上调用。

## 示例

~~~csharp
using UnityEngine;

public class NewBehaviourScript :  MonoBehaviour 
{
    void Awake()
    {
        // Code is within Awake, therefore will print 'true', as Awake was called.
         Debug.Log (this.didAwake);
    }

    void Start()
    {
        // Will print 'true', as Start is called after Awake.
         Debug.Log (this.didAwake);
    }
}
~~~

---

## 文档导航

- 上一页：[[01-destroyCancellationToken]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[03-didStart]]



