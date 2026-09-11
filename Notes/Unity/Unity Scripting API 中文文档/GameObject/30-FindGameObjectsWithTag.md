> 原文：[GameObject.FindGameObjectsWithTag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.FindGameObjectsWithTag.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).FindGameObjectsWithTag

## 声明

~~~csharp
public static GameObject[] FindGameObjectsWithTag(string tag);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| tag | 要用来搜索 GameObject 的标签名称。 |

## 返回值

所有带有指定标签的活动 GameObject 数组。如果没有 GameObject 带有该标签，则返回空数组。

## 描述

获取所有带有指定标签的活动 GameObject 数组。如果没有 GameObject 带有该标签，则返回空数组。

## 示例

~~~csharp
// Instantiates respawnPrefab at the location
// of all GameObjects tagged "Respawn".

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  respawnPrefab;
    public  GameObject [] respawns;
    void Start()
    {
        if (respawns == null)
            respawns =  GameObject.FindGameObjectsWithTag ("Respawn");

        foreach ( GameObject  respawn in respawns)
        {
            Instantiate(respawnPrefab, respawn.transform.position, respawn.transform.rotation);
        }
    }
}
~~~

~~~csharp
// Find the name of the closest enemy

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  FindClosestEnemy()
    {
         GameObject [] gos;
        gos =  GameObject.FindGameObjectsWithTag ("Enemy");
         GameObject  closest = null;
        float distance =  Mathf.Infinity ;
         Vector3  position = transform.position;
        foreach ( GameObject  go in gos)
        {
             Vector3  diff = go.transform.position - position;
            float curDistance = diff.sqrMagnitude;
            if (curDistance < distance)
            {
                closest = go;
                distance = curDistance;
            }
        }
        return closest;
    }
}
~~~

~~~csharp
using UnityEngine;

// Search for GameObjects with a tag that is not used

public class Example :  MonoBehaviour 
{
    void Start()
    {
         GameObject [] gameObjects;
        gameObjects =  GameObject.FindGameObjectsWithTag ("Enemy");

        if (gameObjects.Length == 0)
        {
             Debug.Log ("No GameObjects are tagged with 'Enemy'");
        }
    }
}
~~~

