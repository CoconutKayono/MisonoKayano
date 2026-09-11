> 原文：[GameObject.CompareTag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.CompareTag.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).CompareTag

## 声明

~~~csharp
public bool CompareTag(string tag);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| tag | 要检查的 GameObject 标签。 |

## 返回值

如果 GameObject 附加了指定标签，则返回 true，否则返回 false。

## 描述

检查 GameObject 是否附加了指定标签。

## 示例

~~~csharp
// Immediate death trigger.
// Destroys any colliders that enter the trigger, if they are tagged "Player".
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnTriggerEnter( Collider  other)
    {
        if (other.gameObject.CompareTag("Player"))
        {
            Destroy(other.gameObject);
        }
    }
}
~~~

~~~csharp
// Immediate death trigger.
// Destroys any colliders that enter the trigger, if they are tagged "Player".
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    private  TagHandle  _playerTag;
    public void OnEnable()
    {
        _playerTag =  TagHandle.GetExistingTag ("Player");
    }

    void OnTriggerEnter( Collider  other)
    {
        if (other.gameObject.CompareTag(_playerTag))
        {
            Destroy(other.gameObject);
        }
    }
}
~~~

## 相关资源

- [GameObject.FindWithTag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.FindWithTag.html)
- [TagHandle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/TagHandle.html)

---

## 声明

~~~csharp
public bool CompareTag(TagHandle tag);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| tag | 表示要检查的 GameObject 标签的 TagHandle。 |

## 返回值

如果 GameObject 附加了指定标签，则返回 true，否则返回 false。

## 描述

此重载接受 TagHandle；如果同一个 TagHandle 可用于多次调用，它可能比接受 string 的重载更快。


