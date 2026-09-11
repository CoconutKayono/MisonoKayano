> 原文：[GameObject.AddComponent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.AddComponent.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).AddComponent

## 声明

~~~csharp
public Component AddComponent(Type componentType);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| componentType | 要添加到 GameObject 的组件类型。 |

## 返回值

新添加的组件。

## 描述

向 GameObject 添加指定类型的组件。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class AddComponentExample :  MonoBehaviour 
{
    void Start()
    {
         SphereCollider  sc = gameObject.AddComponent(typeof( SphereCollider )) as  SphereCollider ;
    }
}
~~~

~~~csharp
using UnityEngine;
using System.Collections;

public class AddComponentExample :  MonoBehaviour 
{
    void Start()
    {
         SphereCollider  sc = gameObject.AddComponent< SphereCollider >();
    }
}
~~~

## 相关资源

- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [Object.Destroy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Destroy.html)
- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)
- [Object.Destroy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Destroy.html)

---

## 声明

~~~csharp
public T AddComponent();
~~~

## 返回值

新添加的 T 类型组件。

## 描述

向 GameObject 添加指定类型的组件。泛型重载可以直接指定组件类型，而不需要传入 Type 对象。


