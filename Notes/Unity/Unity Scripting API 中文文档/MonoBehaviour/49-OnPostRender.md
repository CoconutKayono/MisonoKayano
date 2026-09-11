> 原文：[MonoBehaviour.OnPostRender](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPostRender.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnPostRender

## 声明

~~~csharp
public void OnPostRender(...);
~~~

## 描述

摄像机完成场景渲染后调用。

## 示例

~~~csharp
using UnityEngine;

// A script that when attached to the camera, makes the resulting
// colors inverted. See its effect in play mode.
public class ExampleClass :  MonoBehaviour 
{
    private  Material  mat;

    // Will be called from camera after regular rendering is done.
    public void OnPostRender()
    {
        if (!mat)
        {
            // Unity has a built-in shader that is useful for drawing
            // simple colored things. In this case, we just want to use
            // a blend mode that inverts destination colors.
            var shader =  Shader.Find ("Hidden/Internal-Colored");
            mat = new  Material (shader);
            mat.hideFlags =  HideFlags.HideAndDontSave ;
            // Set blend mode to invert destination colors.
            mat.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.OneMinusDstColor);
            mat.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.Zero);
            // Turn off backface culling, depth writes, depth test.
            mat.SetInt("_Cull", (int)UnityEngine.Rendering.CullMode.Off);
            mat.SetInt("_ZWrite", 0);
            mat.SetInt("_ZTest", (int)UnityEngine.Rendering.CompareFunction.Always);
        }

         GL.PushMatrix ();
         GL.LoadOrtho ();

        // activate the first shader pass (in this case we know it is the only pass)
        mat.SetPass(0);
        // draw a quad over whole screen
         GL.Begin ( GL.QUADS );
         GL.Vertex3 (0, 0, 0);
         GL.Vertex3 (1, 0, 0);
         GL.Vertex3 (1, 1, 0);
         GL.Vertex3 (0, 1, 0);
         GL.End ();

         GL.PopMatrix ();
    }
}
~~~

## 相关资源

- [Camera.onPostRender](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Camera-onPostRender.html)
- [MonoBehaviour.OnPreRender](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPreRender.html)
- [MonoBehaviour.OnPreCull](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnPreCull.html)
- [CommandBuffer](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CommandBuffer.html)
- [Extending the Built-in Render Pipeline using CommandBuffers](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/../Manual/GraphicsCommandBuffers.html)
- [WaitForEndOfFrame](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitForEndOfFrame.html)

---

## 文档导航

- 上一页：[[48-OnParticleUpdateJobScheduled]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[50-OnPreCull]]






