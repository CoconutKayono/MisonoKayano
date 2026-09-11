> 原文：[GameObject.GetComponentInParent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentInParent.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).GetComponentInParent

## 声明

~~~csharp
public T GetComponentInParent<T>(bool includeInactive = false);
~~~

## 声明

~~~csharp
public Component GetComponentInParent(Type type);
~~~

## 声明

~~~csharp
public Component GetComponentInParent(Type type, bool includeInactive);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| includeInactive | 是否在搜索中包含未激活的 GameObject。 |
| type | 要获取的组件类型。 |

## 返回值

GameObject 或其任意父对象上指定类型的组件引用；如果没有找到，则返回 null。

## 描述

获取指定 GameObject 或其任意父对象上 T 类型组件的引用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class GetComponentInParentExample :  MonoBehaviour 
{
    // Disable the spring on the first  HingeJoint  component found on the referenced  GameObject  or any of its parents

    public  GameObject  objectToCheck;

    void Start()
    {
         HingeJoint  hinge = objectToCheck.GetComponentInParent< HingeJoint >();

        if (hinge != null)
        {
            hinge.useSpring = false;
        }
    }
}
~~~

~~~csharp
using UnityEngine;
using System.Collections;

public class GetComponentInParentExample :  MonoBehaviour 
{
    // Disable the spring on the first  HingeJoint  component found on the referenced  GameObject  or any of its parents

    public  GameObject  objectToCheck;

    void Start()
    {
         HingeJoint  hinge = objectToCheck.GetComponentInParent(typeof( HingeJoint )) as  HingeJoint ;

        if (hinge != null)
        {
            hinge.useSpring = false;
        }
    }
}
~~~

## 相关资源

- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponentsInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentsInChildren.html)

