> 原文：[MonoBehaviour.StopAllCoroutines](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.StopAllCoroutines.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).StopAllCoroutines

## 声明

~~~csharp
public void StopAllCoroutines();
~~~

## 描述

停止此 MonoBehaviour 启动的所有协程。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

// Create two coroutines that run at different speeds.
// When the space key is pressed stop both of them.

public class ExampleClass :  MonoBehaviour 
{
    //coroutine 1
    IEnumerator DoSomething1()
    {
        while (true)
        {
            print("DoSomething1");
            yield return new  WaitForSeconds (1.0f);
        }
    }

    //coroutine 2
    IEnumerator DoSomething2()
    {
        while (true)
        {
            print("DoSomething2");
            yield return new  WaitForSeconds (1.5f);
        }
    }

    void Start()
    {
        StartCoroutine("DoSomething1");
        StartCoroutine("DoSomething2");
    }

    void  Update ()
    {
        if ( Input.GetKeyDown ("space"))
        {
            StopAllCoroutines();
            print("Stopped all Coroutines: " +  Time.time );
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[66-StartCoroutine]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[68-StopCoroutine]]



