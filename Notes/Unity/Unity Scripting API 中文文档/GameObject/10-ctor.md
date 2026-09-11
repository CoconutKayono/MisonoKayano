> 原文：[GameObject.GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-ctor.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-ctor.html).GameObject

## 声明

~~~csharp
public GameObject();
~~~

## 声明

~~~csharp
public GameObject(string name);
~~~

## 声明

~~~csharp
public GameObject(string name, params Type[] components);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| name | 新 GameObject 的名称。 |
| components | 要附加到新 GameObject 的组件类型。 |

## 描述

创建新的 GameObject；可以选择指定名称以及要附加的组件集合。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    private void Start()
    {
         GameObject  exampleOne = new  GameObject ();
        exampleOne.name = "GameObject1";
        exampleOne.AddComponent< Rigidbody >();

         GameObject  exampleTwo = new  GameObject ("GameObject2");
        exampleTwo.AddComponent< Rigidbody >();

         GameObject  exampleThree = new  GameObject ("GameObject3", typeof( Rigidbody ), typeof( BoxCollider ));
    }
}
~~~
