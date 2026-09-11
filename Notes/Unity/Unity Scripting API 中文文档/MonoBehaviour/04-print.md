> 原文：[MonoBehaviour.print](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour-print.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).print

## 声明

~~~csharp
public static void print(Object message);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| message | 要在控制台中显示的消息。 |

## 描述

将消息输出到 Unity 控制台。

## 示例

~~~csharp
using UnityEngine;

public class PrintExample :  MonoBehaviour 
{
    public int playerHealth = 85;
    public int maxHealth = 100;

    void Start()
    {
        // Simply print a message in the console
        print("The Start method has been called.");

        // Log variables using string interpolation
        print($"Initial player health: {playerHealth}");

        // Log a variable using formatting
        float healthPercentage = playerHealth / (float)maxHealth;
        print($"The player's total score is: {healthPercentage:F2}");
    }
}
~~~

## 相关资源

- [Debug.Log](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Debug.Log.html)
- [Debug.LogWarning](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Debug.LogWarning.html)
- [Debug.LogError](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Debug.LogError.html)

---

## 文档导航

- 上一页：[[03-didStart]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[05-runInEditMode]]







