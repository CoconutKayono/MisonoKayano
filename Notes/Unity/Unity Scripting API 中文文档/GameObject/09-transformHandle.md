> 原文：[GameObject.transformHandle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-transformHandle.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).transformHandle

## 声明

~~~csharp
public TransformHandle transformHandle;
~~~

## 描述

GameObject 的 TransformHandle。（只读）

每个 GameObject 都有一个 TransformHandle，该对象无法移除。

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        gameObject.transformHandle.Translate(1, 1, 1);
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
        gameObject.transformHandle.Translate(1, 1, 1);
    }
}
~~~

