> 原文：[GameObject.transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-transform.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).transform

## 声明

~~~csharp
public Transform transform;
~~~

## 描述

附加到 GameObject 的 Transform。（只读）

每个 GameObject 创建时都会附加一个 Transform 组件，并且该组件无法移除。

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        gameObject.transform.Translate(1, 1, 1);
    }
}
~~~

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        gameObject.transform.Translate(1, 1, 1);
    }
}
~~~

