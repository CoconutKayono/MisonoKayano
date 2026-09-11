> 原文：[MonoBehaviour.StartCoroutine](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.StartCoroutine.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).StartCoroutine

## 声明

~~~csharp
public Coroutine StartCoroutine(IEnumerator routine);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| routine | 要启动的协程。 |

## 返回

Coroutine：启动的协程。

## 描述

启动协程。协程可以使用 yield 语句在任意点暂停；使用 yield 语句时，协程会暂停执行，并在下一帧自动恢复。更多信息请参阅 Manual 中的[编写和运行协程](https://docs.unity3d.com/6000.7/Documentation/Manual/Coroutines.html)。

在大多数情况下，StartCoroutine 方法会在第一次 yield return 时返回，但也可以 yield 返回其结果，以等待协程完成。协程不保证按启动顺序结束，即使它们在同一帧结束也一样。yield 任意类型（包括 null）都会使执行在稍后的帧恢复，除非协程已停止或已完成。如果协程运行至完成且没有 yield（例如 yield 语句不可达），StartCoroutine 会返回 null。

要停止协程，请使用 [MonoBehaviour.StopCoroutine](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.StopCoroutine.html) 或 [MonoBehaviour.StopAllCoroutines](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.StopAllCoroutines.html)。

## 声明

~~~csharp
public Coroutine StartCoroutine(string methodName, object value = null);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| methodName | 协程方法名称。 |
| value | 传递给协程方法的值。 |

## 返回

Coroutine：启动的协程。

## 描述

启动名为 methodName 的协程。大多数情况下，最好使用接受 IEnumerator 参数的 StartCoroutine 版本，因为它的运行时开销更低。不过，带有字符串 methodName 的 StartCoroutine 可以让你使用 MonoBehaviour.StopCoroutine 配合特定方法名停止协程。

## 示例

~~~csharp
// This example invokes a coroutine and continues executing the function in parallel.

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{

    private IEnumerator coroutine;

    void Start()
    {
        // - After 0 seconds, prints "Starting 0.0"
        // - After 0 seconds, prints "Before WaitAndPrint Finishes 0.0"
        // - After 2 seconds, prints "WaitAndPrint 2.0"
        print("Starting " +  Time.time );

        // Start function WaitAndPrint as a coroutine.

        coroutine = WaitAndPrint(2.0f);
        StartCoroutine(coroutine);

        print("Before WaitAndPrint Finishes " +  Time.time );
    }

    // every 2 seconds perform the print()
    private IEnumerator WaitAndPrint(float waitTime)
    {
        while (true)
        {
            yield return new  WaitForSeconds (waitTime);
            print("WaitAndPrint " +  Time.time );
        }
    }
}
~~~

~~~csharp
// This example invokes a coroutine and waits until it is completed.

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    IEnumerator Start()
    {
        // - After 0 seconds, prints "Starting 0.0"
        // - After 2 seconds, prints "WaitAndPrint 2.0"
        // - After 2 seconds, prints "Done 2.0"
        print("Starting " +  Time.time );

        // Start function WaitAndPrint as a coroutine. And wait until it is completed.
        // the same as yield return WaitAndPrint(2.0f);
        yield return StartCoroutine(WaitAndPrint(2.0f));
        print("Done " +  Time.time );
    }

    // suspend execution for waitTime seconds
    IEnumerator WaitAndPrint(float waitTime)
    {
        yield return new  WaitForSeconds (waitTime);
        print("WaitAndPrint " +  Time.time );
    }
}
~~~

~~~csharp
// In this example we show how to invoke a coroutine using a string name and stop it.

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    IEnumerator Start()
    {
        StartCoroutine(nameof(DoSomething), 2.0f);
        yield return new  WaitForSeconds (1);
        StopCoroutine(nameof(DoSomething));
    }

    IEnumerator DoSomething(float someParameter)
    {
        while (true)
        {
            print("DoSomething  Loop ");

            // Yield execution of this coroutine and return to the main loop until next frame
            yield return null;
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
         Debug.Log ("coroutineA created");
        yield return new  WaitForSeconds (1.0f);
        yield return StartCoroutine(coroutineB());
         Debug.Log ("coroutineA running again");
    }

    IEnumerator coroutineB()
    {
         Debug.Log ("coroutineB created");
        yield return new  WaitForSeconds (2.5f);
         Debug.Log ("coroutineB enables coroutineA to run");
    }
}
~~~

## 相关资源

- [Coroutine](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Coroutine.html)
- [YieldInstruction](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/YieldInstruction.html)

---

## 文档导航

- 上一页：[[65-Start]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[67-StopAllCoroutines]]


