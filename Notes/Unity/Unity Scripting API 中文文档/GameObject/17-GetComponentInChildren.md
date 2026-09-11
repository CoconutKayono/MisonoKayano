> 原文：[GameObject.GetComponentInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentInChildren.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).GetComponentInChildren

## 声明

~~~csharp
public T GetComponentInChildren<T>(bool includeInactive = false);
~~~

## 声明

~~~csharp
public Component GetComponentInChildren(Type type);
~~~

## 声明

~~~csharp
public Component GetComponentInChildren(Type type, bool includeInactive);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| includeInactive | 是否在搜索中包含未激活的 GameObject。 |

## 返回值

GameObject 或其子对象上指定类型的组件引用；如果没有找到，则返回 null。

## 描述

获取指定 GameObject 或其任意子对象上 T 类型组件的引用。

## 示例

~~~csharp
using UnityEngine;

public class GetComponentInChildrenExample :  MonoBehaviour 
{
    // Disable the spring on the first  HingeJoint  component found on the referenced  GameObject  or any of its children

    public  GameObject  objectToCheck;

    void Start()
    {
         HingeJoint  hinge = objectToCheck.GetComponentInChildren< HingeJoint >();

        if (hinge != null)
        {
            hinge.useSpring = false;
        }
        else
        {
            // Try again, looking for inactive GameObjects
             HingeJoint  hingeInactive = objectToCheck.GetComponentInChildren< HingeJoint >(true);

            if (hingeInactive != null)
            {
                hingeInactive.useSpring = false;
            }
        }
    }
}
~~~

~~~csharp
using UnityEngine;

public class GetComponentInChildrenExample :  MonoBehaviour 
{
     // Disable the spring on the first  HingeJoint  component found on the referenced  GameObject  or any of its children

    public  GameObject  objectToCheck;

    void Start()
    {
         HingeJoint  hinge = gameObject.GetComponentInChildren(typeof( HingeJoint )) as  HingeJoint ;

        if (hinge != null)
        {
            hinge.useSpring = false;
        }
        else
        {
            // Try again, looking for inactive GameObjects
             HingeJoint  hingeInactive = gameObject.GetComponentInChildren(typeof( HingeJoint ), true) as  HingeJoint ;

            if (hingeInactive != null)
            {
                hingeInactive.useSpring = false;
            }
        }
    }
}
~~~

## 相关资源

- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponents](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponents.html)
- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponents](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponents.html)
