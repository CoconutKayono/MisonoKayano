> 原文：[MonoBehaviour.OnRenderObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnRenderObject.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnRenderObject

## 声明

~~~csharp
public void OnRenderObject(...);
~~~

## 描述

在渲染对象时调用。

## 示例

~~~csharp
using System.Collections;
using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    public  Mesh  mainMesh;
    public  Mesh  miniMapMesh;

    void OnRenderObject()
    {
        // Render different meshes for the object depending on whether
        // the main camera or minimap camera is viewing.
        if (Camera.current.name == "MiniMapcam")
        {
             Graphics.DrawMeshNow (miniMapMesh, transform.position, transform.rotation);
        }
        else
        {
             Graphics.DrawMeshNow (mainMesh, transform.position, transform.rotation);
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[52-OnRenderImage]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[54-OnTransformChildrenChanged]]





