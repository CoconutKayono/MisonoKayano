> 原文：[MonoBehaviour.StopCoroutine](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.StopCoroutine.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).StopCoroutine

## 声明

~~~csharp
public void StopCoroutine(string methodName);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| methodName | 要停止的协程方法名称。 |

## 描述

停止第一个名为 methodName 的协程，或停止当前行为上运行的、存储在 routine 中的协程。

## 声明

~~~csharp
public void StopCoroutine(IEnumerator routine);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| routine | 要停止的协程。 |

## 描述

停止指定的协程。

## 声明

~~~csharp
public void StopCoroutine(Coroutine routine);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| routine | 要停止的协程。 |

## 描述

停止指定的协程。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class Example :  MonoBehaviour 
{
    // keep a copy of the executing script
    private IEnumerator coroutine;

    // Use this for initialization
    void Start()
    {
        print("Starting " +  Time.time );
        coroutine = WaitAndPrint(3.0f);
        StartCoroutine(coroutine);
        print("Done " +  Time.time );
    }

    // print to the console every 3 seconds.
    // yield is causing WaitAndPrint to pause every 3 seconds
    public IEnumerator WaitAndPrint(float waitTime)
    {
        while (true)
        {
            yield return new  WaitForSeconds (waitTime);
            print("WaitAndPrint " +  Time.time );
        }
    }

    void  Update ()
    {
        if ( Input.GetKeyDown ("space"))
        {
            StopCoroutine(coroutine);
            print("Stopped " +  Time.time );
        }
    }
}
~~~

~~~csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    void Start()
    {
        StartCoroutine(coroutineA());
    }

    IEnumerator coroutineA()
    {
        // wait for 1 second
        yield return new  WaitForSeconds (1.0f);
         Debug.Log ("coroutineA() started: " +  Time.time );

        // wait for another 1 second and then create b
        yield return new  WaitForSeconds (1.0f);
         Coroutine  b = StartCoroutine(coroutineB());

        yield return new  WaitForSeconds (2.0f);
         Debug.Log ("coroutineA() finished " +  Time.time );

        // B() was expected to run for 10 seconds
        // but was shut down here after 3.0f
        StopCoroutine(b);
        yield return null;
    }

    IEnumerator coroutineB()
    {
        float f = 0.0f;
        float start =  Time.time ;

         Debug.Log ("coroutineB() started " + start);

        while (f < 10.0f)
        {
             Debug.Log ("coroutineB(): " + f);
            yield return new  WaitForSeconds (1.0f);
            f = f + 1.0f;
        }

        // Intended to handling exit of the this coroutine.
        // However coroutineA() shuts coroutineB() down. This
        // means the following lines are not called.
        float t =  Time.time  - start;
         Debug.Log ("coroutineB() finished " + t);
        yield return null;
    }
}
~~~

---

## 文档导航

- 上一页：[[67-StopAllCoroutines]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[69-Update]]

