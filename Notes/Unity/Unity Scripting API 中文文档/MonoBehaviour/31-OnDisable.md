> 原文：[MonoBehaviour.OnDisable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDisable.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnDisable

## 声明

~~~csharp
public void OnDisable(...);
~~~

## 描述

Behaviour 被禁用时调用。

## 示例

~~~csharp
// Implement OnDisable and OnEnable script functions.
// These functions will be called when the attached  GameObject 
// is activated/deactivated or the script component is enabled/disabled.
// This example also supports running in the  Editor . The  Update  function
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

- [MonoBehaviour.OnEnable](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnEnable.html)

---

## 文档导航

- 上一页：[[30-OnDestroy]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[32-OnDrawGizmos]]




