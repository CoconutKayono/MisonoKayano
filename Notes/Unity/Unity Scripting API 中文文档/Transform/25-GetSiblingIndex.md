> 原文：[Transform.GetSiblingIndex](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.GetSiblingIndex.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).GetSiblingIndex

public int GetSiblingIndex();

### 返回

int 此 Transform 相对于其同级对象的索引。

### 描述

获取此 Transform 相对于其同级对象的索引。

当 GameObject 有多个直接子对象时，这些子对象会被视为彼此的“同级对象”。同级索引描述子对象在同级组中的顺序。父 GameObject 的第一个子对象索引为 0，第二个子对象索引为 1，以此类推。非活动 GameObject 仍会计入同级组。同级索引会影响 Hierarchy 窗口中子对象的显示顺序，也会被 Layout Group 等组件用于控制对象的视觉顺序。有关 Layout Group 的更多信息，请参阅 AutoLayout。调用 Transform.GetChild 时，传递给该方法的参数就是同级索引。要设置 GameObject 的同级索引，请参阅 Transform.SetSiblingIndex。

### 示例

~~~csharp
//This script demonstrates how to return (GetSiblingIndex) and change (SetSiblingIndex) the sibling index of a  GameObject .
//Attach this script to the  GameObject  you would like to change the sibling index of.
//To see this in action, make this  GameObject  the child of another  GameObject , and create siblings for it.


using UnityEngine;

public class TransformGetSiblingIndex :  MonoBehaviour 
{
    //Use this to change the hierarchy of the  GameObject  siblings
    int m_IndexNumber;

    void Start()
    {
        //Initialise the Sibling Index to 0
        m_IndexNumber = 0;
        //Set the Sibling Index
        transform.SetSiblingIndex(m_IndexNumber);
        //Output the Sibling Index to the console
         Debug.Log ("Sibling Index : " + transform.GetSiblingIndex());
    }

    void OnGUI()
    {
        //Press this  Button  to increase the sibling index number of the  GameObject 
        if ( GUI.Button (new  Rect (0, 0, 200, 40), "Add Index Number"))
        {
            //Make sure the index number doesn't exceed the Sibling Index by more than 1
            if (m_IndexNumber <= transform.GetSiblingIndex())
            {
                //Increase the Index Number
                m_IndexNumber++;
            }
        }

        //Press this  Button  to decrease the sibling index number of the  GameObject 
        if ( GUI.Button (new  Rect (0, 40, 200, 40), "Minus Index Number"))
        {
            //Make sure the index number doesn't go below 0
            if (m_IndexNumber >= 1)
            {
                //Decrease the index number
                m_IndexNumber--;
            }
        }
        //Detect if any of the Buttons are being pressed
        if ( GUI.changed )
        {
            // Update  the Sibling Index of the  GameObject 
            transform.SetSiblingIndex(m_IndexNumber);
             Debug.Log ("Sibling Index : " + transform.GetSiblingIndex());
        }
    }
}
~~~






