> 原文：[GameObject.SendMessage](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SendMessage.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).SendMessage

## 声明

~~~csharp
public void SendMessage(string methodName, Object value = null, SendMessageOptions options = SendMessageOptions.RequireReceiver);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| methodName | 要调用的方法名称。 |
| value | 要传递给方法的可选参数值。 |
| options | 如果目标对象不存在该方法，是否引发错误。 |

## 描述

在附加到 GameObject 的每个 MonoBehaviour 上调用指定方法。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // Calls the function ApplyDamage with a value of 5
        // Every script attached to the  GameObject 
        // that has an ApplyDamage function will be called.
        gameObject.SendMessage("ApplyDamage", 5.0);
    }
}

public class Example2 :  MonoBehaviour 
{
    public void ApplyDamage(float damage)
    {
        print(damage);
    }
}
~~~

## 相关资源

- [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html)
- [GameObject.SendMessageUpwards](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SendMessageUpwards.html)


