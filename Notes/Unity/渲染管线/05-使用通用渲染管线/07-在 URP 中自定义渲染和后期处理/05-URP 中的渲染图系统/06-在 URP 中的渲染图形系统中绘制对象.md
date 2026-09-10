# 在 URP 中的渲染图形系统中绘制对象

> 原文：[Draw objects in the render graph system in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-draw-objects-in-a-pass.html)


要在使用渲染图系统的自定义渲染通道中绘制对象，请使用 `RendererListHandle` API 创建要绘制的对象列表。

## 创建要绘制的对象列表

请遵循以下步骤：

1. 在 `ScriptableRenderPass` 类中，在用于通道数据的类中，创建一个 [RendererListHandle](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.RenderGraphModule.RendererListHandle.html) 字段。 例如： `private class PassData { public RendererListHandle objectsToDraw; }`
2. 创建一个 [RendererListParams](https://docs.unity3d.com/ScriptReference/Rendering.RendererListParams.html) 对象，其中包含要绘制的对象、绘制设置和剔除数据。有关 `RenderListParams` 对象的更多信息，请参阅[在自定义渲染管线中创建简单渲染循环](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/manual/index.html)。 有关详细示例，请参阅。
3. 在 `RecordRenderGraph` 方法中，使用 [CreateRendererList API](https://docs.unity3d.com/ScriptReference/Rendering.ScriptableRenderContext.CreateRendererList.html) 将 `RendererListParams` 对象转换为渲染图形系统可以使用的句柄。 例如： `RenderListHandle rendererListHandle = renderGraph.CreateRendererList(rendererListParameters);`
4. 在通道数据中设置 `RendererListHandle` 字段。 例如： `passData.objectsToDraw = rendererListHandle;`

## 绘制对象

在通道数据中设置 `RendererListHandle` 后，可以在列表中绘制对象。

请遵循以下步骤：

1. 在 `RecordRenderGraph` 方法中，使用 `UseRendererList` API 告知渲染图系统要使用的对象列表。 例如： `builder.UseRendererList(passData.rendererListHandle);`
2. 设置要将对象绘制到其上的纹理。设置颜色纹理和深度纹理，以便 URP 正确渲染对象。 例如，下面的示例告知 URP 绘制到活动摄像机纹理的颜色纹理和深度纹理。 `UniversalResourceData frameData = frameContext.Get<UniversalResourceData>(); builder.SetRenderAttachment(frameData.activeColorTexture, 0); builder.SetRenderAttachmentDepth(frameData.activeDepthTexture, AccessFlags.Write);`
3. 在 `SetRenderFunc` 方法中，使用 [DrawRendererList](https://docs.unity3d.com/ScriptReference/Rendering.CommandBuffer.DrawRendererList.html) API 绘制渲染器。 例如： `context.cmd.DrawRendererList(passData.rendererListHandle);`



## 示例

以下可编程渲染器功能 (Scriptable Renderer Feature) 使用覆盖材质重新绘制场景中 `Lightmode` 标签设置为 `UniversalForward` 的对象。

[[../06-在 URP 中将可编程渲染通道添加到帧渲染循环/01-在 URP 中创建可编程渲染器功能]]后，请将**要使用的材质 (Material To Use)** 参数设置为任何材质。

```
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;
 
public class DrawObjectsWithOverrideMaterial : ScriptableRendererFeature
{

    DrawObjectsPass drawObjectsPass;
    public Material overrideMaterial;
 
    public override void Create()
    {
        // Create the render pass that draws the objects, and pass in the override material
        drawObjectsPass = new DrawObjectsPass(overrideMaterial);

        // Insert render passes after URP's post-processing render pass
        drawObjectsPass.renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }
 
    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        // Add the render pass to the URP rendering loop
        renderer.EnqueuePass(drawObjectsPass);
    }

    class DrawObjectsPass : ScriptableRenderPass
    {
        private Material materialToUse;

        public DrawObjectsPass(Material overrideMaterial)
        {
            // Set the pass's local copy of the override material 
            materialToUse = overrideMaterial;
        }
       
        private class PassData
        {
            // Create a field to store the list of objects to draw
            public RendererListHandle rendererListHandle;
        }
 
        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Redraw objects", out var passData))
            {
                // Get the data needed to create the list of objects to draw
                UniversalRenderingData renderingData = frameContext.Get<UniversalRenderingData>();
                UniversalCameraData cameraData = frameContext.Get<UniversalCameraData>();
                UniversalLightData lightData = frameContext.Get<UniversalLightData>();
                SortingCriteria sortFlags = cameraData.defaultOpaqueSortFlags;
                RenderQueueRange renderQueueRange = RenderQueueRange.opaque;
                FilteringSettings filterSettings = new FilteringSettings(renderQueueRange, ~0);

                // Redraw only objects that have their LightMode tag set to UniversalForward 
                ShaderTagId shadersToOverride = new ShaderTagId("UniversalForward");

                // Create drawing settings
                DrawingSettings drawSettings = RenderingUtils.CreateDrawingSettings(shadersToOverride, renderingData, cameraData, lightData, sortFlags);

                // Add the override material to the drawing settings
                drawSettings.overrideMaterial = materialToUse;

                // Create the list of objects to draw
                var rendererListParameters = new RendererListParams(renderingData.cullResults, drawSettings, filterSettings);

                // Convert the list to a list handle that the render graph system can use
                passData.rendererListHandle = renderGraph.CreateRendererList(rendererListParameters);
                
                // Set the render target as the color and depth textures of the active camera texture
                UniversalResourceData resourceData = frameContext.Get<UniversalResourceData>();
                builder.UseRendererList(passData.rendererListHandle);
                builder.SetRenderAttachment(resourceData.activeColorTexture, 0);
                builder.SetRenderAttachmentDepth(resourceData.activeDepthTexture, AccessFlags.Write);

                builder.SetRenderFunc((PassData data, RasterGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData data, RasterGraphContext context)
        {
            // Clear the render target to black
            context.cmd.ClearRenderTarget(true, true, Color.black);

            // Draw the objects in the list
            context.cmd.DrawRendererList(data.rendererListHandle);
        }

    }
 
}
```

有关另一个示例，请参阅[[../../04-开始使用 URP/02-安装和升级 URP/01-创建 URP 项目/03-在 URP 中导入包示例]]中名为 **RendererList** 的示例。

## 其他资源

- [[04-URP 中的 Render Graph 系统中的纹理/00-URP 中的 Render Graph 系统中的纹理]]
- [[05-URP 中的渲染图系统中的帧数据/01-从 URP 中的当前帧获取数据]]
- [可编程渲染器功能 (Scriptable Reader Feature)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/scriptable-renderer-features/scriptable-renderer-features-landing.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
RendererListHandle rendererListHandle = renderGraph.CreateRendererList(rendererListParameters);
```

### 官方代码片段 2

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;
 
public class DrawObjectsWithOverrideMaterial : ScriptableRendererFeature
{

    DrawObjectsPass drawObjectsPass;
    public Material overrideMaterial;
 
    public override void Create()
    {
        // Create the render pass that draws the objects, and pass in the override material
        drawObjectsPass = new DrawObjectsPass(overrideMaterial);

        // Insert render passes after URP's post-processing render pass
        drawObjectsPass.renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }
 
    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        // Add the render pass to the URP rendering loop
        renderer.EnqueuePass(drawObjectsPass);
    }

    class DrawObjectsPass : ScriptableRenderPass
    {
        private Material materialToUse;

        public DrawObjectsPass(Material overrideMaterial)
        {
            // Set the pass's local copy of the override material 
            materialToUse = overrideMaterial;
        }
       
        class PassData
        {
            // Create a field to store the list of objects to draw
            public RendererListHandle rendererListHandle;
        }
 
        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Redraw objects", out var passData))
            {
                // Get the data needed to create the list of objects to draw
                UniversalRenderingData renderingData = frameContext.Get<UniversalRenderingData>();
                UniversalCameraData cameraData = frameContext.Get<UniversalCameraData>();
                UniversalLightData lightData = frameContext.Get<UniversalLightData>();
                SortingCriteria sortFlags = cameraData.defaultOpaqueSortFlags;
                RenderQueueRange renderQueueRange = RenderQueueRange.opaque;
                FilteringSettings filterSettings = new FilteringSettings(renderQueueRange, ~0);

                // Redraw only objects that have their LightMode tag set to UniversalForward 
                ShaderTagId shadersToOverride = new ShaderTagId("UniversalForward");

                // Create drawing settings
                DrawingSettings drawSettings = RenderingUtils.CreateDrawingSettings(shadersToOverride, renderingData, cameraData, lightData, sortFlags);

                // Add the override material to the drawing settings
                drawSettings.overrideMaterial = materialToUse;

                // Create the list of objects to draw
                var rendererListParameters = new RendererListParams(renderingData.cullResults, drawSettings, filterSettings);

                // Convert the list to a list handle that the render graph system can use
                passData.rendererListHandle = renderGraph.CreateRendererList(rendererListParameters);
                
                // Set the render target as the color and depth textures of the active camera texture
                UniversalResourceData resourceData = frameContext.Get<UniversalResourceData>();
                builder.UseRendererList(passData.rendererListHandle);
                builder.SetRenderAttachment(resourceData.activeColorTexture, 0);
                builder.SetRenderAttachmentDepth(resourceData.activeDepthTexture, AccessFlags.Write);

                builder.SetRenderFunc(static (PassData data, RasterGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData data, RasterGraphContext context)
        {
            // Clear the render target to black
            context.cmd.ClearRenderTarget(true, true, Color.black);

            // Draw the objects in the list
            context.cmd.DrawRendererList(data.rendererListHandle);
        }

    }
 
}
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
class PassData
{
    public RendererListHandle objectsToDraw;
}
```

### 官方代码片段 2

```csharp
passData.objectsToDraw = rendererListHandle;
```

### 官方代码片段 3

```csharp
UniversalResourceData frameData = frameContext.Get<UniversalResourceData>();
builder.SetRenderAttachment(frameData.activeColorTexture, 0);
builder.SetRenderAttachmentDepth(frameData.activeDepthTexture, AccessFlags.Write);
```

### 官方代码片段 4

```csharp
context.cmd.DrawRendererList(passData.rendererListHandle);
```

---

## 文档导航

- 上一页：[[05-URP 中的渲染图系统中的帧数据/04-URP 的帧数据纹理参考]]
- 目录：[[00-URP 中的渲染图系统]]
- 下一页：[[07-在 URP 的渲染图系统中的计算着色器/00-在 URP 的渲染图系统中的计算着色器]]
