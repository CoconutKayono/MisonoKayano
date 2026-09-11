> 原文：[Vector2.Angle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.Angle.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).Angle

## 声明

~~~csharp
public static float Angle(Vector2 from, Vector2 to);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| from | 第一个向量。 |
| to | 第二个向量。 |

## 返回值

返回操作结果。

## 描述

获取 from 与 to 之间的无符号角度（度）。

## 示例

~~~csharp
using UnityEngine;

public class Vector :  MonoBehaviour 
{
    //Use these to get the  GameObject 's positions
     Vector2  m_MyFirstVector;
     Vector2  m_MySecondVector;

    float m_Angle;

    //You must assign to these two GameObjects in the Inspector
    public  GameObject  m_MyObject;
    public  GameObject  m_MyOtherObject;

    void Start()
    {
        //Initialise the Vector
        m_MyFirstVector =  Vector2.zero ;
        m_MySecondVector =  Vector2.zero ;
        m_Angle = 0.0f;
    }

    void  Update ()
    {
        //Fetch the first  GameObject 's position
        m_MyFirstVector = new  Vector2 (m_MyObject.transform.position.x, m_MyObject.transform.position.y);
        //Fetch the second  GameObject 's position
        m_MySecondVector = new  Vector2 (m_MyOtherObject.transform.position.x, m_MyOtherObject.transform.position.y);
        //Find the angle for the two Vectors
        m_Angle =  Vector2.Angle (m_MyFirstVector, m_MySecondVector);

        //Draw lines from origin point to Vectors
         Debug.DrawLine ( Vector2.zero , m_MyFirstVector,  Color.magenta );
         Debug.DrawLine ( Vector2.zero , m_MySecondVector,  Color.blue );

        //Log values of Vectors and angle in Console
         Debug.Log ("MyFirstVector: " + m_MyFirstVector);
         Debug.Log ("MySecondVector: "  + m_MySecondVector);
         Debug.Log (" Angle  Between Objects: " + m_Angle);
    }

    void OnGUI()
    {
        //Output the angle found above
         GUI.Label (new  Rect (25, 25, 200, 40), " Angle  Between Objects" + m_Angle);
    }
}
~~~

## 相关资源

- [SignedAngle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.SignedAngle.html)

---

## 文档导航

- 上一页：[[18-ToString]]
- 目录：[[00-Vector2]]
- 下一页：[[20-ClampMagnitude]]



