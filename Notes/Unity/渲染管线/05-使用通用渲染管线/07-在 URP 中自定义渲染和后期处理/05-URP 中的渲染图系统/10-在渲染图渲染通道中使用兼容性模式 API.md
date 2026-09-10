# 在渲染图渲染通道中使用兼容性模式 API

> 原文：[Use the CommandBuffer interface in a render graph](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-unsafe-pass.html)


您可以使用渲染图 `AddUnsafePass` API 来在渲染图系统渲染通道中使用兼容性模式 API，例如 `SetRenderTarget`。

如果使用 `AddUnsafePass` API，则适用以下几点：

- 不能在 `RecordRenderGraph` 方法中使用 `SetRenderAttachment` 方法。请改为在 `SetRenderFunc` 方法中使用 `SetRenderTarget`。
- 渲染可能会较慢，因为 URP 无法优化渲染通道。例如，如果渲染通道写入活动颜色缓冲区，URP 无法检测后面的渲染通道是否写入同一缓冲区。因此，URP 无法合并两个渲染通道，GPU 会不必要地在内存中和内存外传输缓冲区。

## 创建不安全的渲染通道

要创建不安全的渲染通道，请遵循以下步骤：

1. 在 `RecordRenderGraph` 方法中，使用 `AddUnsafePass` 方法而不是 `AddRasterRenderPass` 方法。 例如： `using (var builder = renderGraph.AddUnsafePass<PassData>("My unsafe render pass", out var passData))`
2. 调用 `SetRenderFunc` 方法时，使用 `UnsafeGraphContext` 类型而不是 `RasterGraphContext`。 例如： `builder.SetRenderFunc( (PassData passData, UnsafeGraphContext context) => ExecutePass(passData, context) );`
3. 如果渲染通道写入纹理，必须将纹理添加为通道数据类中的字段。 例如： `private class PassData { internal TextureHandle textureToWriteTo; }`
4. 如果渲染通道写入纹理，还必须使用 `UseTexture` 方法将纹理设置为可写。 例如： `builder.UseTexture(passData.textureToWriteTo, AccessFlags.Write);`

您现在可以在 `SetRenderFunc` 方法中使用兼容性模式 API 了。

## 示例

下面的示例在渲染通道期间使用兼容性模式 `SetRenderTarget` API 将渲染目标设置为活动颜色缓冲区，然后使用其表面法线作为颜色来绘制对象。

```
using UnityEngine;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class DrawNormalsToActiveColorTexture : ScriptableRendererFeature
{

    DrawNormalsPass unsafePass;

    public override void Create()
    {
        unsafePass = new DrawNormalsPass();
        unsafePass.renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderer.EnqueuePass(unsafePass);
    }

    class DrawNormalsPass : ScriptableRenderPass
    {
        private class PassData
        {
            internal TextureHandle activeColorBuffer;
            internal TextureHandle cameraNormalsTexture;
        }

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddUnsafePass<PassData>("Draw normals", out var passData))
            {
                // Make sure URP generates the normals texture
                ConfigureInput(ScriptableRenderPassInput.Normal);

                // Get the frame data
                UniversalResourceData resourceData = frameContext.Get<UniversalResourceData>();

                // Add the active color buffer to our pass data, and set it as writeable 
                passData.activeColorBuffer = resourceData.activeColorTexture;
                builder.UseTexture(passData.activeColorBuffer, AccessFlags.Write);                

                // Add the camera normals texture to our pass data 
                passData.cameraNormalsTexture = resourceData.cameraNormalsTexture;
                builder.UseTexture(passData.cameraNormalsTexture);

                builder.AllowPassCulling(false);

                builder.SetRenderFunc((PassData data, UnsafeGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData passData, UnsafeGraphContext context)
        {
            // Create a command buffer for a list of rendering methods
            CommandBuffer unsafeCommandBuffer = CommandBufferHelpers.GetNativeCommandBuffer(context.cmd);

            // Add a command to set the render target to the active color buffer so URP draws to it
            context.cmd.SetRenderTarget(passData.activeColorBuffer);

            // Add a command to copy the camera normals texture to the render target
            Blitter.BlitTexture(unsafeCommandBuffer, passData.cameraNormalsTexture, new Vector4(1, 1, 0, 0), 0, false);
        }

    }

}
```

有关另一个示例，请参阅[[../../04-开始使用 URP/02-安装和升级 URP/01-创建 URP 项目/03-在 URP 中导入包示例]]中名为 **UnsafePass** 的示例。


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
builder.SetRenderFunc(
    static (PassData passData, UnsafeGraphContext context) => ExecutePass(passData, context)
);
```

### 官方代码片段 2

```csharp
class PassData
{
    public TextureHandle textureToWriteTo;
}
```

### 官方代码片段 3

```csharp
using UnityEngine;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class DrawNormalsToActiveColorTexture : ScriptableRendererFeature
{

    DrawNormalsPass unsafePass;

    public override void Create()
    {
        unsafePass = new DrawNormalsPass();
        unsafePass.renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderer.EnqueuePass(unsafePass);
    }

    class DrawNormalsPass : ScriptableRenderPass
    {
        class PassData
        {
            public TextureHandle activeColorBuffer;
            public TextureHandle cameraNormalsTexture;
        }

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddUnsafePass<PassData>("Draw normals", out var passData))
            {
                // Make sure URP generates the normals texture
                ConfigureInput(ScriptableRenderPassInput.Normal);

                // Get the frame data
                UniversalResourceData resourceData = frameContext.Get<UniversalResourceData>();

                // Add the active color buffer to our pass data, and set it as writeable 
                passData.activeColorBuffer = resourceData.activeColorTexture;
                builder.UseTexture(passData.activeColorBuffer, AccessFlags.Write);                

                // Add the camera normals texture to our pass data 
                passData.cameraNormalsTexture = resourceData.cameraNormalsTexture;
                builder.UseTexture(passData.cameraNormalsTexture);

                // Make sure the render graph system keeps the render pass, even if it's not used in the final frame.
                // Don't use this in production code, because it prevents the render graph system from removing the render pass if it's not needed.
                builder.AllowPassCulling(false);

                builder.SetRenderFunc(static (PassData data, UnsafeGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData passData, UnsafeGraphContext context)
        {
            // Create a command buffer for a list of rendering methods
            CommandBuffer unsafeCommandBuffer = CommandBufferHelpers.GetNativeCommandBuffer(context.cmd);

            // Add a command to set the render target to the active color buffer so URP draws to it
            context.cmd.SetRenderTarget(passData.activeColorBuffer);

            // Add a command to copy the camera normals texture to the render target
            Blitter.BlitTexture(unsafeCommandBuffer, passData.cameraNormalsTexture, new Vector4(1, 1, 0, 0), 0, false);
        }

    }

}
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
using (var builder = renderGraph.AddUnsafePass<PassData>("My unsafe render pass", out var passData))
```

### 官方代码片段 2

```csharp
builder.UseTexture(passData.textureToWriteTo, AccessFlags.Write);
```

---

## 文档导航

- 上一页：[[09-优化渲染图]]
- 目录：[[00-URP 中的渲染图系统]]
- 下一页：[[11-URP 的渲染图查看器 (Render Graph Viewer) 窗口参考]]
