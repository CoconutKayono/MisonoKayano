> 原文：[MonoBehaviour.Start](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.Start.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).Start

## 声明

~~~csharp
public void Start(...);
~~~

## 描述

在首次帧更新之前调用。

## 示例

~~~csharp
// Initializes the target variable.
// target is private and thus not editable in the Inspector

// The ExampleClass starts with Awake.  The  GameObject  class has activeSelf
// set to false.  When activeSelf is set to true the Start() and  Update ()
// functions will be called causing the ExampleClass to run.
// Note that ExampleClass (Script) in the Inspector is turned off.  It
// needs to be ticked to make script call Start.

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    private float update;

    void Awake()
    {
         Debug.Log ("Awake");
        update = 0.0f;
    }

    IEnumerator Start()
    {
         Debug.Log ("Start1");
        yield return new  WaitForSeconds (2.5f);
         Debug.Log ("Start2");
    }

    void  Update ()
    {
        update +=  Time.deltaTime ;
        if (update > 1.0f)
        {
            update = 0.0f;
             Debug.Log (" Update ");
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[64-Reset]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[66-StartCoroutine]]



