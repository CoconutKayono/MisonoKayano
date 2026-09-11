> 原文：[GameObject.activeInHierarchy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-activeInHierarchy.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).activeInHierarchy

## 声明

~~~csharp
public bool activeInHierarchy;
~~~

## 描述

GameObject 在 Scene 层级中的激活状态。激活时为 true，未激活时为 false。（只读）

如果对象及其所有父对象的 [GameObject.activeSelf](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-activeSelf.html) 都是 true，则 GameObject 在场景层级中处于激活状态。如果某个父对象的 GameObject.activeSelf 为 false，即使对象自身的 GameObject.activeSelf 为 true，该 GameObject 在场景层级中也不处于激活状态。

GameObject.activeInHierarchy 变为 false 会触发附加脚本的 [MonoBehaviour.OnDisable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDisable.html)。GameObject.activeInHierarchy 变为 true 会触发 [MonoBehaviour.OnEnable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnEnable.html)。

~~~csharp
// 此脚本展示 activeInHierarchy 如何随 GameObject 父对象的激活状态变化。
using UnityEngine;

public class ActiveInHierarchyExample : MonoBehaviour
{
    // 在 Inspector 中附加这些对象。
    public GameObject m_ParentObject, m_ChildObject;

    // 用于获取切换数据。
    bool m_Activate;

    void Start()
    {
        // 停用父 GameObject 并设置切换值。
        m_Activate = false;
    }

    void Update()
    {
        // 根据切换值激活附加的 GameObject。
        m_ParentObject.SetActive(m_Activate);
    }

    void OnGUI()
    {
        // 使用此切换激活或停用父 GameObject。
        m_Activate = GUI.Toggle(
            new Rect(10, 10, 100, 30),
            m_Activate,
            "Activate Parent GameObject");

        if (GUI.changed)
        {
            // 将 GameObject 的激活状态输出到控制台。
            Debug.Log("Child GameObject Active : " + m_ChildObject.activeInHierarchy);
        }
    }
}
~~~

停用的父 GameObject 的子对象可能仍会根据 GameObject.activeSelf 处于激活状态，尽管它们在场景中不可见。GameObject.activeInHierarchy 是检查 GameObject 是否因父对象状态而实际停用的可靠方式。

~~~csharp
// 此脚本展示 activeInHierarchy 与 activeSelf 的区别。
// 使用切换改变父子 GameObject 的激活状态，并输出子对象状态。
using UnityEngine;

public class ActiveInHierarchyExample : MonoBehaviour
{
    public GameObject m_ParentObject, m_ChildObject;

    // 用于获取切换数据。
    bool m_ActivateParent, m_ActivateChild;

    // 用于判断是否需要更新控制台输出。
    bool m_HierarchyOutput, m_SelfOutput;

    void Start()
    {
        // 停用父、子 GameObject 和切换值。
        m_ActivateParent = false;
        m_ActivateChild = false;

        // 允许脚本将当前 GameObject 状态输出到控制台。
        m_HierarchyOutput = false;
        m_SelfOutput = false;
    }

    void Update()
    {
        m_ParentObject.SetActive(m_ActivateParent);
        m_ChildObject.SetActive(m_ActivateChild);

        if (m_HierarchyOutput == false)
        {
            Debug.Log("Object Active : " + m_ChildObject.activeInHierarchy);
            m_HierarchyOutput = true;
        }

        if (m_ChildObject.activeSelf && m_SelfOutput == false)
        {
            Debug.Log("Child Active, parent might not be");
            m_SelfOutput = true;
        }
    }

    void OnGUI()
    {
        m_ActivateParent = GUI.Toggle(
            new Rect(10, 10, 100, 30),
            m_ActivateParent,
            "Activate Parent GameObject");

        m_ActivateChild = GUI.Toggle(
            new Rect(10, 40, 100, 30),
            m_ActivateChild,
            "Activate Child GameObject");

        if (GUI.changed)
        {
            m_SelfOutput = false;
            m_HierarchyOutput = false;
        }
    }
}
~~~

## 示例

~~~csharp
//This script shows how the activeInHierarchy state changes depending on the active state of the  GameObject ’s parent

using UnityEngine;

public class ActiveInHierarchyExample :  MonoBehaviour 
{
    //Attach these in the Inspector
    public  GameObject  m_ParentObject, m_ChildObject;
    //Use this for getting the toggle data
    bool m_Activate;

    void Start()
    {
        //Deactivate parent  GameObject  and toggle
        m_Activate = false;
    }

    void  Update ()
    {
        //Activate the  GameObject  you attach depending on the toggle output
        m_ParentObject.SetActive(m_Activate);
    }

    void OnGUI()
    {
        //Switch this toggle to activate and deactivate the parent  GameObject 
        m_Activate =  GUI.Toggle (new  Rect (10, 10, 100, 30), m_Activate, "Activate Parent  GameObject ");

        if ( GUI.changed )
        {
            //Output the status of the  GameObject 's active state in the console
             Debug.Log ("Child  GameObject  Active : " + m_ChildObject.activeInHierarchy);
        }
    }
}
~~~

~~~csharp
//This script shows how activeInHierarchy differs from activeSelf. Use the toggle  to alter the parent and child  GameObject ’s active states. This makes it output the child  GameObject ’s state in the console.
//It also shows how activeSelf outputs that the child  GameObject  is active when the parent is not, while the activeInHierarchy lists the child  GameObject  as inactive.


using UnityEngine;

public class ActiveInHierarchyExample :  MonoBehaviour 
{
    public  GameObject  m_ParentObject, m_ChildObject;
    //Use this for getting the toggle data
    bool m_ActivateParent, m_ActivateChild;
    //Use these for deciding if console is needing updated
    bool m_HierarchyOutput, m_SelfOutput;

    void Start()
    {
        //Deactivate parent and child GameObjects and toggles
        m_ActivateParent = false;
        m_ActivateChild = false;
        //Ables script to output current state of  GameObject  to console
        m_HierarchyOutput = false;
        m_SelfOutput = false;
    }

    void  Update ()
    {
        //Activates the  GameObject  you attach depending on the toggle output
        m_ParentObject.SetActive(m_ActivateParent);
        m_ChildObject.SetActive(m_ActivateChild);

        //Find out if the  GameObject  is active in the Game and checks if this state has been output to the console
        if (m_HierarchyOutput == false)
        {
            //Output the state of the  GameObject ’s activity if it hasn't already been output
             Debug.Log ("Object Active : " + m_ChildObject.activeInHierarchy);
            //The state of the  GameObject  is output already, so no need to do it again
            m_HierarchyOutput = true;
        }
        //Check to see if the assigned  GameObject  is active despite parent  GameObject 's status
        if (m_ChildObject.activeSelf && m_SelfOutput == false)
        {
            //Output the message if the  GameObject  is still active
             Debug.Log ("Child Active, parent might not be");
            //You no longer need to output the message
            m_SelfOutput = true;
        }
    }

    void OnGUI()
    {
        //Switch this toggle to activate and deactivate the parent  GameObject 
        m_ActivateParent =  GUI.Toggle (new  Rect (10, 10, 100, 30), m_ActivateParent, "Activate Parent  GameObject ");
        //Switch this toggle to activate and deactivate the child  GameObject 
        m_ActivateChild =  GUI.Toggle (new  Rect (10, 40, 100, 30), m_ActivateChild, "Activate Child  GameObject ");


        //If a change is detected with the toggle, the console outputs updates
        if ( GUI.changed )
        {
            m_SelfOutput = false;
            m_HierarchyOutput = false;
        }
    }
}
~~~

