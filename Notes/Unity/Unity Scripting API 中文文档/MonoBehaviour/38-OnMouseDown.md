> 原文：[MonoBehaviour.OnMouseDown](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseDown.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnMouseDown

## 声明

~~~csharp
public void OnMouseDown(...);
~~~

## 描述

用户在 Collider 上按下鼠标按钮时调用。

## 示例

~~~csharp
using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    void OnMouseDown()
    {
        // Destroy the gameObject after clicking on it
        Destroy(gameObject);
    }
}
~~~

---

## 文档导航

- 上一页：[[37-OnJointBreak2D]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[39-OnMouseDrag]]





