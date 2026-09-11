> 原文：[MonoBehaviour.OnWillRenderObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnWillRenderObject.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnWillRenderObject

## 声明

~~~csharp
public void OnWillRenderObject(...);
~~~

## 描述

对象将由摄像机渲染时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleScript :  MonoBehaviour 
{
    public  Renderer  rend;

    private float timePass = 0.0f;

    void Start()
    {
        rend = GetComponent< Renderer >();
    }

    void OnWillRenderObject()
    {
        timePass +=  Time.deltaTime ;

        if (timePass > 1.0f)
        {
            timePass = 0.0f;
            print(gameObject.name + " is being rendered by " + Camera.current.name + " at " +  Time.time );
        }
    }
}
~~~

## 相关资源

- [MonoBehaviour.OnPreCull](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPreCull.html)
- [MonoBehaviour.OnPreRender](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPreRender.html)

---

## 文档导航

- 上一页：[[62-OnValidate]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[64-Reset]]






