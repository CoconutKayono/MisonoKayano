> 原文：[Vector2.Distance](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.Distance.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).Distance

## 声明

~~~csharp
public static float Distance(Vector2 a, Vector2 b);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| a | 第一个点。 |
| b | 第二个点。 |

## 返回值

返回操作结果。

## 描述

返回 a 与 b 之间的距离。

## 示例

~~~csharp
using UnityEngine;

public class DistanceExample_enemy :  MonoBehaviour 
{
    // Add a reference to the player, which is set in the Inspector window
    public  GameObject  player;

    // Set the distance at which the enemy attacks
    public float attackDistanceThreshold = 2f;

    void  Update ()
    {
        // Take the position of the player, and the position of this  GameObject 
         Vector2  playerPosition = player.transform.position;
         Vector2  myPosition = transform.position;

        // Use  Vector2.Distance  to obtain the distance between the player position and this  GameObject 's position
        float distance =  Vector2.Distance (myPosition, playerPosition);

        // Check if the player is close enough
        if(distance < attackDistanceThreshold)
        {
            Attack(player);
        }
    }

    void Attack( GameObject  target)
    {
        // Insert the attack logic here
         Debug.Log ($"{name} attacks {target.name}");
    }
}
~~~

---

## 文档导航

- 上一页：[[20-ClampMagnitude]]
- 目录：[[00-Vector2]]
- 下一页：[[22-Dot]]


