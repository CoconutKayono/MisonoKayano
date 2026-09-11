> 原文：[MonoBehaviour.OnEnable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnEnable.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnEnable

## 声明

~~~csharp
public void OnEnable(...);
~~~

## 描述

对象启用并处于活动状态时调用。

## 示例

~~~csharp
// Implement OnDisable and OnEnable script functions.
// These functions will be called when the script component
// is enabled.
// This example also supports the  Editor . The  Update  function
// will be called, for example, when the position of the
//  GameObject  is changed.

using UnityEngine;

[ ExecuteInEditMode ]
public class PrintOnOff :  MonoBehaviour 
{
    void OnDisable()
    {
         Debug.Log ("PrintOnDisable: script was disabled");
    }

    void OnEnable()
    {
         Debug.Log ("PrintOnEnable: script was enabled");
    }

    void  Update ()
    {
#if UNITY_EDITOR
         Debug.Log (" Editor  causes this  Update ");
#endif
    }
}
~~~

## 相关资源

- [MonoBehaviour.OnDisable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDisable.html)

---

## 文档导航

- 上一页：[[33-OnDrawGizmosSelected]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[35-OnGUI]]




