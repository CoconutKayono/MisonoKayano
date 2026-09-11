> 原文：[MonoBehaviour.OnMouseUp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseUp.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnMouseUp

## 声明

~~~csharp
public void OnMouseUp(...);
~~~

## 描述

用户在 Collider 上释放鼠标按钮时调用。

## 示例

~~~csharp
// Register when mouse dragging has ended. OnMouseUp is called
// when the mouse button is released.

using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    void OnMouseUp()
    {
        // If the user releases the mouse button while over the  GameObject  with this script attached, output this message
         Debug.Log ("Drag ended!");
    }
}
~~~

## 相关资源

- [OnMouseDown](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseDown.html)
- [OnMouseDrag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseDrag.html)

---

## 文档导航

- 上一页：[[42-OnMouseOver]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[44-OnMouseUpAsButton]]






