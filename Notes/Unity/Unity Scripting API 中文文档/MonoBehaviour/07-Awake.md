> 原文：[MonoBehaviour.Awake](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.Awake.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).Awake

## 声明

~~~csharp
public void Awake(...);
~~~

## 描述

在脚本实例加载时调用。

## 示例

~~~csharp
using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    private  GameObject  target;

    void Awake()
    {
        target =  GameObject.FindWithTag ("Player");
    }
}
~~~

~~~csharp
using UnityEngine;

// Make sure that Cube1 is assigned this script and is inactive at the start of the game.

public class Example1 :  MonoBehaviour 
{
    void Awake()
    {
        // Prints first
         Debug.Log ("Example1.Awake() was called");
    }

    void Start()
    {
        // Prints second
         Debug.Log ("Example1.Start() was called");
    }

    void  Update ()
    {
        if ( Input.GetKeyDown ("b"))
        {
            // Prints Last if "b" is pressed
             Debug.Log ("b key was pressed");
        }
    }
}
~~~

~~~csharp
using UnityEngine;

public class Example2 :  MonoBehaviour 
{
    // Assign Cube1 to this variable GO before running the example
    public  GameObject  GO;

    void Awake()
    {
         Debug.Log ("Example2.Awake() was called");
    }

    void Start()
    {
         Debug.Log ("Example2.Start() was called");
    }

    // track if Cube1 was already activated
    private bool activateGO = true;

    void  Update ()
    {
        if (activateGO == true)
        {
            if ( Input.GetKeyDown ("space"))
            {
                 Debug.Log ("space key was pressed");
                GO.SetActive(true);
                activateGO = false;
            }
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[06-useGUILayout]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[08-CancelInvoke]]



