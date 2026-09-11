> 原文：[Vector2.ctor](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2-ctor.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).ctor

## 声明

~~~csharp
public Vector2(float x, float y);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| x | X 分量。 |
| y | Y 分量。 |

## 返回值

返回操作结果。

## 描述

使用给定的 x、y 分量构造新向量。

## 示例

~~~csharp
//This script moves a  GameObject  to a new x position using a  Vector2 .
//Attach this script to a  GameObject 
//Set your x position in the Inspector

using UnityEngine;

public class Examples :  MonoBehaviour 
{
     Vector2  m_NewPosition;
    //This is the new X position. Set it in the Inspector.
    public float m_XPosition;

    // Use this for initialization
    void Start()
    {
        //Initialise the vector
        m_NewPosition = new  Vector2 (0.0f, 0.0f);
    }

    void  Update ()
    {
        //Press the space key to change the x component of the vector
        if ( Input.GetKeyDown ( KeyCode.Space ))
        {
            m_NewPosition.x = m_XPosition;
        }
        //Change the position depending on the vector
        transform.position = m_NewPosition;
    }
}
~~~

~~~csharp
//This script shows how a  GameObject  can be moved to new positions using vectors.

//Attach this script to a  GameObject . Click on the  GameObject  and the Inspector window appears. Change the “Second Vector” in the Inspector
//Attach a  GameObject  in the MyTransform field
//Also create 3 UI Buttons ( Create > UI > Button ) and go to each of their Inspectors to change their OnClick method (click the  +  button)
//Put your  GameObject  in each field. Use the  No function  dropdown to assign one  Button  with the  ZeroButton method, one with PositiveButton method and the other with the GameObjectButton method.


using UnityEngine;

public class Example :  MonoBehaviour 
{
    //Use these to set the  GameObject 's position
     Vector2  m_MyFirstVector;
    //Set this Vector in the Inspector (the position you would like the  GameObject  to move to)
    public  Vector2  m_MySecondVector;
     Vector2  m_MyThirdVector;

    //You must assign to this  Transform  in the Inspector (could be another  GameObject )
    public  Transform  m_MyTransform;

    void Start()
    {
        //Set the first vector to be at (0, 0, 0)
        m_MyFirstVector =  Vector2.zero ;
        //Set the third vector to the  GameObject  you set in the Inspector's position
        m_MyThirdVector = m_MyTransform.position;
    }

    public void ZeroButton()
    {
        //Press this  Button  to move your  GameObject  to the first vector position (0, 0)
        //Use this to move your  GameObject  to the origin (be wary of parent GameObjects)
        transform.position = m_MyFirstVector;
    }

    //Press this  Button  to move your  GameObject  to the second vector position (100, 200)
    public void PositionButton()
    {
        //Use this to move your  GameObject  to a specified position
        transform.position = m_MySecondVector;
    }

    //Press this  Button  to move your  GameObject  to the third vector position (The m_MyTransform's position)
    public void GameObjectButton()
    {
        //Use this to move your  GameObject  to another  GameObject 's position
        transform.position = m_MyThirdVector;
    }
}
~~~

~~~csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ExampleScene :  MonoBehaviour 
{
    void Start()
    {
        float degrees = 45.0f;
        float radians = degrees *  Mathf.Deg2Rad ;

         Vector2  vec2 = new  Vector2 ( Mathf.Cos (radians),  Mathf.Sin (radians));
         Debug.Log (vec2);
    }
}
~~~

---

## 文档导航

- 上一页：[[14-y]]
- 目录：[[00-Vector2]]
- 下一页：[[16-Equals]]


