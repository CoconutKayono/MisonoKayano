> 原文：[GameObject.FindWithTag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.FindWithTag.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).FindWithTag

## 声明

~~~csharp
public static GameObject FindWithTag(string tag);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| tag | 要搜索的标签。 |

## 返回值

第一个带有指定标签的活动 GameObject；如果没有 GameObject 带有该标签，则返回 null。

## 描述

获取第一个带有指定标签的活动 GameObject。如果没有 GameObject 带有该标签，则返回 null。

使用标签前必须先在标签管理器中声明标签。如果标签不存在，或者 tag 参数为空字符串或 null，则会抛出 UnityException。

注意：如果场景中有多个活动 GameObject 带有指定标签，不能保证此方法返回特定的 GameObject。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  respawnPrefab;
    public  GameObject  respawn;
    void Start()
    {
        if (respawn == null)
            respawn =  GameObject.FindWithTag ("Respawn");

        Instantiate(respawnPrefab, respawn.transform.position, respawn.transform.rotation);
    }
}
~~~

