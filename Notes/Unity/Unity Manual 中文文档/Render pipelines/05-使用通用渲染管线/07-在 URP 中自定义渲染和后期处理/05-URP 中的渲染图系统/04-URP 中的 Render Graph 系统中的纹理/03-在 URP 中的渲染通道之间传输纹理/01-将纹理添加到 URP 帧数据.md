# 将纹理添加到 URP 的帧数据

> 原文：[Add a texture to the frame data in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-add-texture-to-frame-data.html)


要在同一渲染图中的不同渲染通道之间传递纹理，可以将纹理添加到 [[01-从 URP 中的当前帧获取数据]]。

请按以下步骤操作：

1. 创建继承自 [ContextItem](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.ContextItem.html) 的类，并在其中包含纹理句柄字段。例如：`public class MyCustomData : ContextItem { public TextureHandle textureToTransfer; }`
2. 必须在类中实现 `Reset()` 方法，以便在帧重置时重置纹理。例如：`public class MyCustomData : ContextItem { public TextureHandle textureToTransfer; public override void Reset() { textureToTransfer = TextureHandle.nullHandle; } }`
3. 在 `RecordRenderGraph` 方法中，将类的实例添加到帧数据。例如：`public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext) { using (var builder = renderGraph.AddRasterRenderPass<PassData>("Get frame data", out var passData)) { var customData = frameContext.Create<MyCustomData>(); } }`
4. 将纹理句柄设置为您的纹理。更多信息请参阅 [[01-在 URP 中的渲染通道中使用纹理]]。
5. 在后续渲染通道的 `RecordRenderGraph` 方法中，可以获取自定义数据并检索纹理：

例如：

```cs
// Get the custom data
MyCustomData customData = frameData.Get<MyCustomData>();

// Get the texture
TextureHandle customTexture = customData.textureToTransfer;
```

有关帧数据的更多信息，请参阅 [[01-从 URP 中的当前帧获取数据]]。

## 示例

以下示例添加包含纹理的 `CustomData` 类。第一个渲染通道将纹理清除为黄色，第二个渲染通道获取黄色纹理并在其上绘制三角形。要查看这些渲染通道，请打开[帧调试器](https://docs.unity3d.com/6000.7/Documentation/Manual/FrameDebugger.html)。

```cs
using UnityEngine;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering;

public class AddOwnTextureToFrameData : ScriptableRendererFeature
{
    AddOwnTexturePass customPass1;
    DrawTrianglePass customPass2;

    public override void Create()
    {
        customPass1 = new AddOwnTexturePass();
        customPass2 = new DrawTrianglePass();

        customPass1.renderPassEvent = RenderPassEvent.AfterRenderingOpaques;
        customPass2.renderPassEvent = RenderPassEvent.AfterRenderingOpaques;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderer.EnqueuePass(customPass1);
        renderer.EnqueuePass(customPass2);
    }
    
    // Create the first render pass, which creates a texture and adds it to the frame data
    class AddOwnTexturePass : ScriptableRenderPass
    {

        class PassData
        {
            internal TextureHandle copySourceTexture;
        }

        // Create the custom data class that contains the new texture
        public class CustomData : ContextItem {
            public TextureHandle newTextureForFrameData;

            public override void Reset()
            {
                newTextureForFrameData = TextureHandle.nullHandle;
            }
        }

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Create new texture", out var passData))
            {
                // Create a texture and set it as the render target
                UniversalResourceData frameData = frameContext.Get<UniversalResourceData>();
                TextureDesc textureDesc = frameData.activeColorTexture.GetDescriptor(renderGraph);
                textureDesc.msaaSamples = MSAASamples.None;
                TextureHandle texture = renderGraph.CreateTexture(textureDesc);
                CustomData customData = frameContext.Create<CustomData>();
                customData.newTextureForFrameData = texture;
                builder.SetRenderAttachment(texture, 0, AccessFlags.Write);
    
                // Make sure the render graph system keeps the render pass, even if it's not used in the final frame.
                // Don't use this in production code, because it prevents the render graph system from removing the render pass if it's not needed.
                builder.AllowPassCulling(false);

                builder.SetRenderFunc(static (PassData data, RasterGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData data, RasterGraphContext context)
        {          
            // Clear the render target (the texture) to yellow
            context.cmd.ClearRenderTarget(true, true, Color.yellow);
        }
 
    }

    // Create the second render pass, which fetches the texture and writes to it
    class DrawTrianglePass : ScriptableRenderPass
    {

        class PassData
        {
            // No local pass data needed
        }      

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Fetch texture and draw triangle", out var passData))
            {                                
                // Fetch the yellow texture from the frame data and set it as the render target
                var customData = frameContext.Get<AddOwnTexturePass.CustomData>();
                var customTexture = customData.newTextureForFrameData;
                builder.SetRenderAttachment(customTexture, 0, AccessFlags.Write);

                // Make sure the render graph system keeps the render pass, even if it's not used in the final frame.
                // Don't use this in production code, because it prevents the render graph system from removing the render pass if it's not needed.
                builder.AllowPassCulling(false);

                builder.SetRenderFunc(static (PassData data, RasterGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData data, RasterGraphContext context)
        {          
            // Generate a triangle mesh
            Mesh mesh = new Mesh();
            mesh.vertices = new Vector3[] { new Vector3(0, 0, 0), new Vector3(1, 0, 0), new Vector3(0, 1, 0) };
            mesh.triangles = new int[] { 0, 1, 2 };
            
            // Draw a triangle to the render target (the yellow texture)
            context.cmd.DrawMesh(mesh, Matrix4x4.identity, new Material(Shader.Find("Universal Render Pipeline/Unlit")));
        }
    }
}
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
public class MyCustomData : ContextItem {
    public TextureHandle textureToTransfer;
}
```

### 官方代码片段 2

```csharp
public class MyCustomData : ContextItem {
    public TextureHandle textureToTransfer;

    public override void Reset()
    {
        textureToTransfer = TextureHandle.nullHandle;
    }
}
```

### 官方代码片段 3

```csharp
public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
{
    using (var builder = renderGraph.AddRasterRenderPass<PassData>("Get frame data", out var passData))
    {
        var customData = frameContext.Create<MyCustomData>();
    }
}
```

---

## 文档导航

- 上一页：[[00-在 URP 中的渲染通道之间传输纹理]]
- 目录：[[00-在 URP 中的渲染通道之间传输纹理]]
- 下一页：[[02-在 URP 中创建全局纹理]]
