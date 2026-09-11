> 原文：[GameObject.Find](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.Find.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).Find

## 声明

~~~csharp
public static GameObject Find(string name);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| name | 要查找的 GameObject 名称或层级路径。 |

## 返回值

找到的活动 GameObject；如果不存在名称为 name 的 GameObject，则返回 null。

## 描述

查找并返回具有指定名称或层级路径的 GameObject。

此方法只返回活动 GameObject。如果 name 包含 / 字符，则会将其视为 Hierarchy 窗口中 GameObject 的路径。GameObject.Find 会搜索整个场景，且不会自动缓存结果；每次调用都会重新执行搜索，因此不建议在性能关键代码或 MonoBehaviour.Update 中频繁调用。

如果要查找子 GameObject，通常更适合使用 Transform.Find，因为它只搜索指定 Transform 的子对象。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

// This returns the  GameObject  named  Hand  in one of the Scenes.

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  hand;

    void Example()
    {
        // This returns the  GameObject  named  Hand .
        hand =  GameObject.Find (" Hand ");

        // This returns the  GameObject  named  Hand .
        //  Hand  must not have a parent in the  Hierarchy  view.
        hand =  GameObject.Find ("/ Hand ");

        // This returns the  GameObject  named  Hand ,
        // which is a child of  Arm  > Monster.
        // Monster must not have a parent in the  Hierarchy  view.
        hand =  GameObject.Find ("/Monster/ Arm / Hand ");

        // This returns the  GameObject  named  Hand ,
        // which is a child of  Arm  > Monster.
        // Monster can have a parent in the  Hierarchy  view.
        hand =  GameObject.Find ("Monster/ Arm / Hand ");
    }
}
~~~

~~~csharp
using UnityEngine;
using System.Collections;

// Find the  GameObject  named  Hand  and rotate it every frame

public class ExampleClass :  MonoBehaviour 
{
    private  GameObject  hand;

    void Start()
    {
        hand =  GameObject.Find ("/Monster/ Arm / Hand ");
    }

    void  Update ()
    {
        hand.transform.Rotate(0, 100 *  Time.deltaTime , 0);
    }
}
~~~

## 相关资源

- [GameObject.FindGameObjectsWithTag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.FindGameObjectsWithTag.html)


