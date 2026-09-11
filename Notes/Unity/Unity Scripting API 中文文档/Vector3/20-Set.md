> 原文：[Vector3.Set](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Set.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Set

## 声明

~~~csharp
public void Set(float newX, float newY, float newZ);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| newX | X component value. |
| newY | Y component value. |
| newZ | Z component value. |

## 描述

设置现有 Vector3 的 x、y、z 分量。

## 示例

~~~csharp
// Attach this script to a  GameObject . Create an empty  GameObject  that will act as your "New  Transform ". Assign this in the Inspector.
// Press the "Set" button in the game to set the  GameObject 's position to the "New  Transform " position.

using UnityEngine;
using UnityEngine.EventSystems;

public class Example :  MonoBehaviour 
{
    // Use this to set the new position of the  GameObject 
     Vector3  m_MyPosition;

    // Set an external  Transform  in the Inspector which is the  GameObject ’s starting point
    public  Transform  m_NewTransform;

    void Start()
    {
        // Set the new Vector to be that of the  Transform  you attach in the Inspector
        m_MyPosition.Set(m_NewTransform.position.x, m_NewTransform.position.y, 0);
    }

    void OnGUI()
    {
        // Press the  Button  to set the  GameObject  to this new position
        if ( GUI.Button (new  Rect (0, 0, 100, 40), "Set"))
        {
            transform.position = m_MyPosition;
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[19-Equals]]
- 目录：[[00-Vector3]]
- 下一页：[[21-ToString]]



