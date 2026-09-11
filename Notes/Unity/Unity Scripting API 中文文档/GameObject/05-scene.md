> 原文：[GameObject.scene](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-scene.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).scene

## 声明

~~~csharp
public Scene scene;
~~~

## 描述

包含该 GameObject 的 Scene。

~~~csharp
// 输出此 GameObject 所属 Scene 的名称。
using UnityEngine;
using UnityEngine.SceneManagement;

public class Example : MonoBehaviour
{
    void Start()
    {
        Scene scene = gameObject.scene;
        Debug.Log(gameObject.name + " is from the Scene: " + scene.name);
    }
}
~~~

## 示例

~~~csharp
//Output the name of the  Scene  this  GameObject  belongs to

using UnityEngine;
using UnityEngine.SceneManagement;

public class Example :  MonoBehaviour 
{
    void Start()
    {
         Scene  scene = gameObject.scene;
         Debug.Log (gameObject.name + " is from the  Scene : " + scene.name);
    }
}
~~~

