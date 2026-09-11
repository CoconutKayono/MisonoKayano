> 原文：[GameObject.GetComponentAtIndex](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentAtIndex.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).GetComponentAtIndex

## 声明

~~~csharp
public Component GetComponentAtIndex(int index);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| index | GameObject 组件数组中的索引。 |

## 返回值

指定索引处的组件引用。

## 描述

获取 GameObject 组件数组中指定索引处的组件引用。

## 示例

~~~csharp
using UnityEngine;

public class GetComponentAtIndexExample :  MonoBehaviour 
{
    public  GameObject  otherGameObject;

    void Start()
    {
         HingeJoint  hinge = otherGameObject.GetComponentAtIndex(5) as  HingeJoint ;

        if (hinge != null)
        {
            hinge.useSpring = false;
        }
    }
}
~~~

~~~csharp
using UnityEngine;

public class GetTComponentAtIndexExample :  MonoBehaviour 
{
    public  GameObject  otherGameObject;

    void Start()
    {
         HingeJoint  hinge = otherGameObject.GetComponentAtIndex< HingeJoint >(5);

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
- [GameObject.GetComponentCount](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentCount.html)
- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [GameObject.GetComponents](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponents.html)

---

## 声明

~~~csharp
public T GetComponentAtIndex(int index);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| index | GameObject 组件数组中的索引。 |

## 返回值

指定索引处的 T 类型组件引用。

## 描述

获取 GameObject 组件数组中指定索引处的组件引用。


