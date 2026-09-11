> 原文：[Transform.SetSiblingIndex](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.SetSiblingIndex.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).SetSiblingIndex

public void SetSiblingIndex(int index);

### 参数

| 参数 | 描述 |
| --- | --- |
| index | Index to set. |

### 描述

设置同级索引。

使用此方法更改 GameObject 的同级索引。如果一个 GameObject 与其他 GameObject 共享父对象并处于同一层级（即它们共享同一个直接父对象），这些 GameObject 就称为同级对象。同级索引表示每个 GameObject 在此同级层级中的位置。设置 Transform 的同级索引时，其他同级对象可能会更改其同级索引，以便腾出空间或填补空缺。例如，对于同级对象 a、b 和 c，其索引分别为 0、1 和 2；对 Transform c 调用 SetSiblingIndex(0) 还会使 Transform a 的同级索引变为 1，Transform b 的同级索引变为 2。使用 SetSiblingIndex 可以更改 GameObject 在此层级中的位置。GameObject 的同级索引改变时，其在 Hierarchy 窗口中的顺序也会改变。这对于有意排列 GameObject 子对象的顺序很有用，例如使用 Layout Group 组件时。Layout Group 也会按照索引重新排列组的视觉顺序。有关 Layout Group 的更多信息，请参阅 AutoLayout。要读取 GameObject 的同级索引，请参阅 Transform.GetSiblingIndex。

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







