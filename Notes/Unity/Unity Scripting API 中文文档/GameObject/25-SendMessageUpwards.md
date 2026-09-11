> 原文：[GameObject.SendMessageUpwards](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SendMessageUpwards.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).SendMessageUpwards

## 声明

~~~csharp
public void SendMessageUpwards(string methodName, Object value = null, SendMessageOptions options = SendMessageOptions.RequireReceiver);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| methodName | 要调用的方法名称。 |
| value | 要传递给方法的可选参数值。 |
| options | 如果目标对象不存在该方法，是否引发错误。 |

## 描述

在附加到 GameObject 的每个 MonoBehaviour 以及该行为的每个祖先对象上调用指定方法。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        // Calls the function ApplyDamage with a value of 5
        gameObject.SendMessageUpwards("ApplyDamage", 5.0);
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
- [GameObject.SendMessage](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SendMessage.html)


