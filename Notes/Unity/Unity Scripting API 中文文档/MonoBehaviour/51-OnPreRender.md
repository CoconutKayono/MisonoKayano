> 原文：[MonoBehaviour.OnPreRender](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPreRender.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnPreRender

## 声明

~~~csharp
public void OnPreRender(...);
~~~

## 描述

摄像机开始渲染场景前调用。

## 示例

~~~csharp
// This script lets you enable/disable fog per camera.
// by enabling or disabling the script in the title of the Inspector
// you can turn fog on or off per camera.

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    private bool revertFogState = false;

    void OnPreRender()
    {
        revertFogState =  RenderSettings.fog ;
         RenderSettings.fog  = enabled;
    }

    void OnPostRender()
    {
         RenderSettings.fog  = revertFogState;
    }
}
~~~

## 相关资源

- [Camera.onPreRender](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Camera-onPreRender.html)
- [MonoBehaviour.OnPreCull](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPreCull.html)
- [MonoBehaviour.OnPostRender](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPostRender.html)
- [CommandBuffer](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CommandBuffer.html)
- [Extending the Built-in Render Pipeline using CommandBuffers](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/../Manual/GraphicsCommandBuffers.html)

---

## 文档导航

- 上一页：[[50-OnPreCull]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[52-OnRenderImage]]






