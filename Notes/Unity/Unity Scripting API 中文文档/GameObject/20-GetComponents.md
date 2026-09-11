> 原文：[GameObject.GetComponents](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponents.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).GetComponents

## 声明

~~~csharp
public T[] GetComponents<T>();
~~~

## 声明

~~~csharp
public void GetComponents<T>(List<T> results);
~~~

## 声明

~~~csharp
public Component[] GetComponents(Type type);
~~~

## 声明

~~~csharp
public void GetComponents(Type type, List<Component> results);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| type | 要获取的组件类型。 |
| results | 用于接收结果的列表。 |

## 返回值

GameObject 上指定类型组件的引用集合；使用 List 重载时将结果写入 results。

## 描述

获取指定 GameObject 上所有 T 类型组件的引用。

## 示例

~~~csharp
using UnityEngine;

public class GetComponentsExample :  MonoBehaviour 
{
    // Disable the spring on all HingeJoints in the referenced  GameObject 

    public  GameObject  objectToCheck;

    void Start()
    {
         HingeJoint [] hingeJoints;

        hingeJoints = objectToCheck.GetComponents< HingeJoint >();

        foreach ( HingeJoint  joint in hingeJoints)
        {
            joint.useSpring = false;
        }
    }
}
~~~

~~~csharp
using UnityEngine;
using System.Collections.Generic;

public class GetComponentsExample :  MonoBehaviour 
{
    // Disable the spring on all HingeJoints in the referenced  GameObject 

    public  GameObject  objectToCheck;

    void Start()
    {
        List< HingeJoint > hingeJoints = new List< HingeJoint >();

        objectToCheck.GetComponents(hingeJoints);

        foreach ( HingeJoint  joint in hingeJoints)
        {
            joint.useSpring = false;
        }
    }
}
~~~

~~~csharp
using UnityEngine;

public class GetComponentsExample :  MonoBehaviour 
{
    // Disable the spring on all HingeJoints in the referenced  GameObject 

    public  GameObject  objectToCheck;

    void Start()
    {
         Component [] hingeJoints;

        hingeJoints = objectToCheck.GetComponents(typeof( HingeJoint ));

        foreach ( HingeJoint  joint in hingeJoints)
        {
            joint.useSpring = false;
        }
    }
}
~~~

~~~csharp
using UnityEngine;
using System.Collections.Generic;

public class GetComponentsExample :  MonoBehaviour 
{
   // Disable the spring on all HingeJoints in the referenced  GameObject 

    public  GameObject  objectToCheck;


    void Start()
    {
        List< Component > hingeJoints = new List< Component >();

        objectToCheck.GetComponents(typeof( HingeJoint ), hingeJoints);

        foreach ( HingeJoint  joint in hingeJoints)
        {
            joint.useSpring = false;
        }
    }
}
~~~

## 相关资源

- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponentsInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentsInChildren.html)
- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponentsInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentsInChildren.html)
- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponentsInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentsInChildren.html)
- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponentsInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentsInChildren.html)

