> 原文：[MonoBehaviour.OnPreCull](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPreCull.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnPreCull

## 声明

~~~csharp
public void OnPreCull(...);
~~~

## 描述

摄像机剔除场景前调用。

## 示例

~~~csharp
// Attach this to the same  GameObject  as a  Camera  component.
// This script inverts the view of the  Camera , so that everything rendered by it is flipped

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
     Camera  cam;

    void Start()
    {
        cam = GetComponent< Camera >();
    }

    void OnPreCull()
    {
        cam.ResetWorldToCameraMatrix();
        cam.ResetProjectionMatrix();
        cam.projectionMatrix = cam.projectionMatrix *  Matrix4x4.Scale (new  Vector3 (1, -1, 1));
    }

    void OnPreRender()
    {
         GL.invertCulling  = true;
    }

    void OnPostRender()
    {
         GL.invertCulling  = false;
    }
}
~~~

## 相关资源

- [Camera.onPreCull](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Camera-onPreCull.html)
- [MonoBehaviour.OnPreRender](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPreRender.html)
- [MonoBehaviour.OnPostRender](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPostRender.html)
- [CommandBuffer](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CommandBuffer.html)
- [Extending the Built-in Render Pipeline using CommandBuffers](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/../Manual/GraphicsCommandBuffers.html)

---

## 文档导航

- 上一页：[[49-OnPostRender]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[51-OnPreRender]]






