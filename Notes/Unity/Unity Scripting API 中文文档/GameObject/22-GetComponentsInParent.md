> 原文：[GameObject.GetComponentsInParent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentsInParent.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).GetComponentsInParent

## 声明

~~~csharp
public T[] GetComponentsInParent<T>();
~~~

## 声明

~~~csharp
public T[] GetComponentsInParent<T>(bool includeInactive);
~~~

## 声明

~~~csharp
public void GetComponentsInParent<T>(bool includeInactive, List<T> results);
~~~

## 声明

~~~csharp
public Component[] GetComponentsInParent(Type type, bool includeInactive = false);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| includeInactive | 是否在搜索中包含未激活的 GameObject。 |
| results | 用于接收结果的列表。 |
| type | 要获取的组件类型。 |

## 返回值

GameObject 及其父对象上指定类型组件的引用集合。

## 描述

获取指定 GameObject 及其任意父对象上所有 T 类型组件的引用。

## 示例

~~~csharp
using UnityEngine;

public class GetComponentsInParentExample :  MonoBehaviour 
{
     // Disable the spring on all HingeJoints in the referenced  GameObject  and its parents

    public  GameObject  objectToCheck;

    void Start()
    {
         HingeJoint [] hingeJoints;

        hingeJoints = objectToCheck.GetComponentsInParent< HingeJoint >();

        if (hingeJoints != null)
        {
            foreach ( HingeJoint  joint in hingeJoints)
            {
                joint.useSpring = false;
            }
        }
        else
        {
            // Try again, looking for inactive GameObjects
             HingeJoint [] hingesInactive = objectToCheck.GetComponentsInParent< HingeJoint >(true);

            foreach ( HingeJoint  joint in hingesInactive)
            {
                joint.useSpring = false;
            }
        }
    }
}
~~~

~~~csharp
using UnityEngine;
using System.Collections.Generic;

public class GetComponentsInParentExample :  MonoBehaviour 
{
     // Disable the spring on all HingeJoints in the referenced  GameObject  and its parents

    public  GameObject  objectToCheck;

    void Start()
    {
        List< HingeJoint > hingeJoints = new List< HingeJoint >();

        objectToCheck.GetComponentsInParent< HingeJoint >(false, hingeJoints);

        if (hingeJoints != null)
        {
            foreach ( HingeJoint  joint in hingeJoints)
            {
                joint.useSpring = false;
            }
        }
        else
        {
            // Try again, looking for inactive GameObjects
            List< HingeJoint > hingesInactive = new List< HingeJoint >();

            objectToCheck.GetComponentsInParent< HingeJoint >(true, hingesInactive);

            foreach ( HingeJoint  joint in hingesInactive)
            {
                joint.useSpring = false;
            }
        }
    }
}
~~~

## 相关资源

- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponentsInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentsInChildren.html)
- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponentsInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentsInChildren.html)

