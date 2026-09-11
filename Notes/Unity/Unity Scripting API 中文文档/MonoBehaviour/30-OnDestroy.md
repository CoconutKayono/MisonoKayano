> 原文：[MonoBehaviour.OnDestroy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDestroy.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnDestroy

## 声明

~~~csharp
public void OnDestroy(...);
~~~

## 描述

当 MonoBehaviour 将被销毁时调用。

## 示例

~~~csharp
// ExampleClass1 includes a button to switch scene, which calls OnDestroy and then switches to
// ExampleClass2. Once ExampleClass2 is active, OnDestroy will be called when the application closes. 
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class ExampleClass1 :  MonoBehaviour 
{
    private float timePass = 0.0f;
    private int updateCount = 0;

    void Start()
    {
         Debug.Log ("Start1");
    }

    // code that generates a message every second
    void  Update ()
    {
        timePass +=  Time.deltaTime ;

        if (timePass > 1.0f)
        {
            timePass = 0.0f;
             Debug.Log ("Update1: " + updateCount);
            updateCount = updateCount + 1;
        }
    }

    void OnGUI()
    {
        if ( GUI.Button (new  Rect (10, 10, 250, 60), "Change to scene2"))
        {
             Debug.Log ("Exit1");
             SceneManager.LoadScene (1);
        }
    }

    // generate a message before the Start() function
    void OnEnable()
    {
         Debug.Log ("OnEnable1");
    }

    // generate a message when the game shuts down or switches to another  Scene 
    // or switched to ExampleClass2
    void OnDestroy()
    {
         Debug.Log ("OnDestroy1");
    }
}
~~~

~~~csharp
using UnityEngine;
using UnityEngine.UI;

public class ExampleClass2 :  MonoBehaviour 
{
    void Start()
    {
         Debug.Log ("Start2");
    }

    void OnEnable()
    {
         Debug.Log ("OnEnable2");
    }

    // generate a message when the game shuts down
    void OnDestroy()
    {
         Debug.Log ("OnDestroy2");
    }
}
~~~

## 相关资源

- [MonoBehaviour.OnDisable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDisable.html)

---

## 文档导航

- 上一页：[[29-OnControllerColliderHit]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[31-OnDisable]]




