> 原文：[GameObject.GetComponent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponent.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).GetComponent

## 声明

~~~csharp
public T GetComponent();
~~~

## 返回值

GameObject 上指定类型的组件；如果没有找到，则返回 null。

## 描述

通过向泛型方法提供组件类型参数，获取指定类型组件的引用。

## 示例

~~~csharp
using UnityEngine;

public class GetComponentExample :  MonoBehaviour 
// Attach this script to a  GameObject  as a component.
{
// Create a reference to another  GameObject  in the scene. Set a value for this in the Other Game Object field
// in the Inspector window before entering Play mode. The referenced  GameObject  must contain a
//  HingeJoint  component.
    public  GameObject  otherGameObject;

    void Start()
    {
         HingeJoint  hinge = otherGameObject.GetComponent< HingeJoint >();
        // Perform null check to confirm a valid  HingeJoint  component was successfully returned.
        if (hinge != null)
        {
            hinge.useSpring = false;
        }
    }
}
~~~

~~~csharp
using UnityEngine;

public class GetComponentExample :  MonoBehaviour 
// Attach this script to a  GameObject  as a component.
{
// Create a reference to another  GameObject  in the scene. Set a value for this in the Other Game Object field
// in the Inspector window before entering Play mode. The referenced  GameObject  must contain a
//  HingeJoint  component.
    public  GameObject  otherGameObject;

    void Start()
    {
    // This version of this method returns a  Component , so use the as operator to safely
    // convert it to the derived  HingeJoint  type
         HingeJoint  hinge = otherGameObject.GetComponent(typeof( HingeJoint )) as  HingeJoint ;
    // Perform null check to confirm that the returned type was successfully converted to  HingeJoint .
        if (hinge != null)
        {
            hinge.useSpring = false;
        }
    }
}
~~~

~~~csharp
using UnityEngine;

public class GetComponentNonPerformantExample :  MonoBehaviour 
// Attach this script to a  GameObject  as a component.
{
// Create a reference to another  GameObject  in the scene. Set a value for this in the Other Game Object field
// in the Inspector window before entering Play mode. The referenced  GameObject  must contain a
//  HingeJoint  component.
    public  GameObject  otherGameObject;

    void Start()
    {
        // This version of this method returns a  Component , so use the as operator to safely
        // convert it to the derived  HingeJoint  type
         HingeJoint  hinge = otherGameObject.GetComponent(" HingeJoint ") as  HingeJoint ;
        // Perform null check to confirm a valid  HingeJoint  component was successfully returned.
        if (hinge != null)
        {
            hinge.useSpring = false;
        }
    }
}
~~~

## 相关资源

- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponents](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponents.html)
- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponents](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponents.html)
- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponents](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponents.html)

---

## 声明

~~~csharp
public Component GetComponent(Type type);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| type | 要搜索的组件类型，以 Type 对象指定。 |

## 返回值

GameObject 上指定类型的组件；如果没有找到，则返回 null。

## 描述

获取指定类型组件的引用。

---

## 声明

~~~csharp
public Component GetComponent(string type);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| type | 要搜索的组件类型名称，以字符串指定。 |

## 返回值

GameObject 上指定类型的组件；如果没有找到，则返回 null。

## 描述

获取指定类型组件的引用。


