> 原文：[GameObject.TryGetComponent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.TryGetComponent.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).TryGetComponent

## 声明

~~~csharp
public bool TryGetComponent<T>(out T component);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| type | 要获取的组件类型。 |
| component | 如果找到组件，则输出找到的组件。 |

## 声明

~~~csharp
public bool TryGetComponent(Type type, out Component component);
~~~

## 返回值

如果找到指定类型的组件，则返回 true；否则返回 false。

## 描述

如果指定类型的组件存在，则获取该组件。

## 示例

~~~csharp
using UnityEngine;

public class TryGetComponentExample :  MonoBehaviour 
{
 
    public  GameObject  objectToCheck;

    void Start()
    {
        if (objectToCheck.TryGetComponent< HingeJoint >(out  HingeJoint  hinge))
        {
            hinge.useSpring = false;
        }
    }
}
~~~

## 相关资源

- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponent.html)

