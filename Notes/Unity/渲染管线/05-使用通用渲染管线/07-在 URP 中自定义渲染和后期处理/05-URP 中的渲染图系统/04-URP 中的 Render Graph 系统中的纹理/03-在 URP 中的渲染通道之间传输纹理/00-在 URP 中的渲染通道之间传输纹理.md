# 在 URP 中的渲染通道之间传输纹理

> 原文：[Use a texture in multiple render passes in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-pass-textures-between-passes.html)


您可以在渲染通道之间传输纹理，例如，如果需要在一个渲染通道中创建纹理并在后面的渲染通道中读取该纹理。

使用以下方法在渲染通道之间传输纹理：


还可以将纹理存储在渲染通道外部，例如作为[可编程渲染器功能](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/scriptable-renderer-features/scriptable-renderer-features-landing.html)中的 `TextureHandle`。

如果需要确保纹理在多个帧之间可用，或确保多个摄像机可以访问纹理，请改为参阅[[03-将纹理导入 URP 中的渲染图系统]]。



## 将纹理添加到帧数据

您可以将纹理添加到[[../../05-URP 中的渲染图系统中的帧数据/01-从 URP 中的当前帧获取数据]]，以便在后面的渲染通道中获取纹理。

请遵循以下步骤：

1. 创建一个继承 [ContextItem](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.ContextItem.html) 并包含一个纹理句柄字段的类。 例如： `public class MyCustomData : ContextItem { public TextureHandle textureToTransfer; }`
2. 必须在类中实现 `Reset()` 方法，以便在帧重置时重置纹理。 例如： `public class MyCustomData : ContextItem { public TextureHandle textureToTransfer; public override void Reset() { textureToTransfer = TextureHandle.nullHandle; } }`
3. 在 `RecordRenderGraph` 方法中，将类的实例添加到帧数据。 例如： `public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext) { using (var builder = renderGraph.AddRasterRenderPass<PassData>("Get frame data", out var passData)) { UniversalResourceData resourceData = frameContext.Get<UniversalResourceData>(); var customData = contextData.Create<MyCustomData>(); } }`
4. 将纹理句柄设置为纹理。 例如： `// Create texture properties that match the screen RenderTextureDescriptor textureProperties = new RenderTextureDescriptor(Screen.width, Screen.height, RenderTextureFormat.Default, 0); // Create the texture TextureHandle texture = UniversalRenderer.CreateRenderGraphTexture(renderGraph, textureProperties, "My texture", false); // Set the texture in the custom data instance customData.textureToTransfer = texture;`

在后面的渲染通道中，在 `RecordRenderGraph` 方法中，您可以获取您的自定义数据并获取您的纹理：

例如：

```
// Get the custom data
MyCustomData fetchedData = frameData.Get<MyCustomData>();

// Get the texture
TextureHandle customTexture = customData.textureToTransfer;
```

有关帧数据的更多信息，请参阅[[../../05-URP 中的渲染图系统中的帧数据/01-从 URP 中的当前帧获取数据]]。

### 示例

下面的示例会添加一个包含纹理的 `CustomData` 类。第一个渲染通道将纹理清除为黄色，第二个渲染通道获取黄色纹理并在其上绘制三角形。

```
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
                RenderTextureDescriptor textureProperties = new RenderTextureDescriptor(Screen.width, Screen.height, RenderTextureFormat.Default, 0);
                TextureHandle texture = UniversalRenderer.CreateRenderGraphTexture(renderGraph, textureProperties, "My texture", false);
                CustomData customData = frameContext.Create<CustomData>();
                customData.newTextureForFrameData = texture;
                builder.SetRenderAttachment(texture, 0, AccessFlags.Write);
    
                builder.AllowPassCulling(false);

                builder.SetRenderFunc((PassData data, RasterGraphContext context) => ExecutePass(data, context));
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

                builder.AllowPassCulling(false);

                builder.SetRenderFunc((PassData data, RasterGraphContext context) => ExecutePass(data, context));
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



## 将纹理设置为全局纹理

如果需要使用纹理作为游戏对象上着色器的输入，可将纹理设置为全局纹理。全局纹理可用于所有着色器和渲染通道。

将纹理设置为全局纹理会使渲染变慢。请参阅 [SetGlobalTexture](https://docs.unity3d.com/ScriptReference/Shader.SetGlobalTexture.html)。

不要使用[[../../10-在渲染图渲染通道中使用兼容性模式 API]]和 `CommandBuffer.SetGlobal` 来将纹理设置为全局纹理，因为这可能会导致错误。

要设置全局纹理，请在 `RecordRenderGraph` 方法中使用 [SetGlobalTextureAfterPass](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.RenderGraphModule.IBaseRenderGraphBuilder.html#UnityEngine_Rendering_RenderGraphModule_IBaseRenderGraphBuilder_SetGlobalTextureAfterPass_UnityEngine_Rendering_RenderGraphModule_TextureHandle__System_Int32_) 方法。

例如：

```
// Allocate a global shader texture called _GlobalTexture
private int globalTextureID = Shader.PropertyToID("_GlobalTexture")

using (var builder = renderGraph.AddRasterRenderPass<PassData>("MyPass", out var passData)){

    // Set a texture to the global texture
    builder.SetGlobalTextureAfterPass(texture, globalTextureID);
}
```

如果尚未调用 `SetRenderFunc`，则还必须添加空的渲染函数。例如：

```
    builder.SetRenderFunc((PassData data, RasterGraphContext context) => { });
```

您现在可以执行以下操作：

- 使用 `UseGlobalTexture()` 或 `UseAllGlobalTextures()` API 访问不同渲染通道中的纹理。
- 在场景中的任何材质上使用纹理。

---


## 目录

| 页面 | 说明 |
| --- | --- |
| [[01-将纹理添加到 URP 帧数据]] | Add a texture to the frame data in URP |
| [[02-在 URP 中创建全局纹理]] | Create a texture as a global texture in URP |
| [[03-将纹理导入 URP 中的渲染图系统]] | Import a texture into the render graph system in URP |

## 文档导航

- 上一页：[[../02-在 URP 中的渲染图形系统中创建纹理]]
- 目录：
- 下一页：[[01-将纹理添加到 URP 帧数据]]
