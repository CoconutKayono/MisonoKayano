> 原文：[MonoBehaviour.OnMouseDrag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseDrag.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnMouseDrag

## 声明

~~~csharp
public void OnMouseDrag(...);
~~~

## 描述

用户在 Collider 上按住鼠标按钮并拖动时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  Renderer  rend;

    void Start()
    {
        rend = GetComponent< Renderer >();
    }

    void OnMouseDrag()
    {
        rend.material.color -=  Color.white  *  Time.deltaTime ;
    }
}
~~~

---

## 文档导航

- 上一页：[[38-OnMouseDown]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[40-OnMouseEnter]]





