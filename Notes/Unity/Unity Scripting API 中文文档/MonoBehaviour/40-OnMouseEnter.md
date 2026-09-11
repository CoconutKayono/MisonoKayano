> 原文：[MonoBehaviour.OnMouseEnter](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseEnter.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnMouseEnter

## 声明

~~~csharp
public void OnMouseEnter(...);
~~~

## 描述

鼠标进入 Collider 时调用。

## 示例

~~~csharp
// Change the mesh color in response to mouse actions.

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  Renderer  rend;

    void Start()
    {
        rend = GetComponent< Renderer >();
    }

    // The mesh goes red when the mouse is over it...
    void OnMouseEnter()
    {
        rend.material.color =  Color.red ;
    }

    // ...the red fades out to cyan as the mouse is held over...
    void OnMouseOver()
    {
        rend.material.color -= new  Color (0.1F, 0, 0) *  Time.deltaTime ;
    }

    // ...and the mesh finally turns white when the mouse moves away.
    void OnMouseExit()
    {
        rend.material.color =  Color.white ;
    }
}
~~~

## 相关资源

- [OnMouseOver](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseOver.html)
- [OnMouseExit](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseExit.html)

---

## 文档导航

- 上一页：[[39-OnMouseDrag]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[41-OnMouseExit]]






