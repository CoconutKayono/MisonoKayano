# 在 URP 中的渲染图形系统中创建纹理

> 原文：[Create a temporary texture for a single frame in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-create-a-texture.html)


要在渲染图形系统中创建纹理，请使用 `UniversalRenderer.CreateRenderGraphTexture` API。

通用渲染管线 (URP) 优化渲染图时，如果最终帧不使用纹理，则可能无法创建纹理，从而减少渲染通道使用的内存和带宽。有关 URP 如何优化渲染图的更多信息，请参阅[[01-URP 中的渲染图系统简介]]。

有关在多个帧或多个摄像机上使用纹理的更多信息，例如在项目中导入的纹理资源，请参阅[[03-将纹理导入 URP 中的渲染图系统]]。

## 创建纹理

要创建纹理，请在 `ScriptableRenderPass` 类的 `RecordRenderGraph` 方法中执行以下步骤：

1. 创建具有所需纹理属性的 [RenderTextureDescriptor](https://docs.unity3d.com/ScriptReference/RenderTextureDescriptor.html) 对象。
2. 使用 [UniversalRenderer.CreateRenderGraphTexture](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.UniversalRenderer.html#UnityEngine_Rendering_Universal_UniversalRenderer_CreateRenderGraphTexture_UnityEngine_Rendering_RenderGraphModule_RenderGraph_UnityEngine_RenderTextureDescriptor_System_String_System_Boolean_UnityEngine_FilterMode_UnityEngine_TextureWrapMode_) 方法来创建纹理并返回纹理句柄。

例如，以下命令会创建与屏幕大小相同的纹理。

```
RenderTextureDescriptor textureProperties = new RenderTextureDescriptor(Screen.width, Screen.height, RenderTextureFormat.Default, 0);
TextureHandle textureHandle = UniversalRenderer.CreateRenderGraphTexture(renderGraph, textureProperties, "My texture", false);
```

然后，您可以在同一个自定义渲染通道中[[01-在 URP 中的渲染通道中使用纹理]]。

只有当前摄像机能够访问纹理。要在其他地方（例如从另一个摄像机或自定义渲染代码中）访问纹理，请改用[[03-将纹理导入 URP 中的渲染图系统]]。

渲染图系统管理使用 `CreateRenderGraphTexture` 创建的纹理的生命周期，因此在完成这些纹理后，无需手动释放它们使用的内存。

### 示例

以下可编程渲染器功能包含一个示例渲染通道，用于创建纹理并将其清除为黄色。有关将渲染通道添加到渲染管线的更多信息，请参阅[[01-在 URP 中创建可编程渲染器功能]]。

使用[帧调试器](https://docs.unity3d.com/2023.3/Documentation/Manual/frame-debugger-window.html)检查渲染通道添加的纹理。

```
using UnityEngine;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering;

public class CreateYellowTextureFeature : ScriptableRendererFeature
{
    CreateYellowTexture customPass;

    public override void Create()
    {
        customPass = new CreateYellowTexture();
        customPass.renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderer.EnqueuePass(customPass);
    }

    class CreateYellowTexture : ScriptableRenderPass
    {
        class PassData
        {
            internal TextureHandle cameraColorTexture;
        }

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Create yellow texture", out var passData))
            {
                // Create texture properties that match the screen size
                RenderTextureDescriptor textureProperties = new RenderTextureDescriptor(Screen.width, Screen.height, RenderTextureFormat.Default, 0);

                // Create a temporary texture
                TextureHandle texture = UniversalRenderer.CreateRenderGraphTexture(renderGraph, textureProperties, "My texture", false);

                // Set the texture as the render target
                builder.SetRenderAttachment(texture, 0, AccessFlags.Write);
    
                builder.AllowPassCulling(false);

                builder.SetRenderFunc((PassData data, RasterGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData data, RasterGraphContext context)
        {          
            // Clear the render target to yellow
            context.cmd.ClearRenderTarget(true, true, Color.yellow);            
        }
    }

}
```

有关另一个示例，请参阅[[03-在 URP 中导入包示例]]中名为 **OutputTexture** 的示例。

## 其他资源

- [[03-将纹理导入 URP 中的渲染图系统]]
- [[01-从 URP 中的当前帧获取数据]]
- [纹理 (Textures)](https://docs.unity3d.com/Manual/Textures.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
TextureDesc textureDesc = resourceData.activeColorTexture.GetDescriptor(renderGraph);
TextureHandle textureHandle = renderGraph.CreateTexture(textureDesc);
```

### 官方代码片段 2

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering;

public class CreateYellowTextureFeature : ScriptableRendererFeature
{
    CreateYellowTexture customPass;

    public override void Create()
    {
        customPass = new CreateYellowTexture();
        customPass.renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderer.EnqueuePass(customPass);
    }

    class CreateYellowTexture : ScriptableRenderPass
    {
        class PassData
        {
            public TextureHandle cameraColorTexture;
        }

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
        {
            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Create yellow texture", out var passData))
            {
                // Get the frame data
                UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();

                // Create texture properties that match the screen size
                TextureDesc textureDesc = resourceData.activeColorTexture.GetDescriptor(renderGraph);
                textureDesc.msaaSamples = MSAASamples.None;

                // Create a temporary texture
                TextureHandle texture = renderGraph.CreateTexture(textureDesc);

                // Set the texture as the render target
                builder.SetRenderAttachment(texture, 0, AccessFlags.Write);
    
                // Make sure the render graph system keeps the render pass, even if it's not used in the final frame.
                // Don't use this in production code, because it prevents the render graph system from removing the render pass if it's not needed.
                builder.AllowPassCulling(false);

                builder.SetRenderFunc(static (PassData data, RasterGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData data, RasterGraphContext context)
        {          
            // Clear the render target to yellow
            context.cmd.ClearRenderTarget(true, true, Color.yellow);            
        }
    }

}
```

---

## 文档导航

- 上一页：[[01-在 URP 中的渲染通道中使用纹理]]
- 目录：[[00-URP 中的 Render Graph 系统中的纹理]]
- 下一页：[[00-在 URP 中的渲染通道之间传输纹理]]
