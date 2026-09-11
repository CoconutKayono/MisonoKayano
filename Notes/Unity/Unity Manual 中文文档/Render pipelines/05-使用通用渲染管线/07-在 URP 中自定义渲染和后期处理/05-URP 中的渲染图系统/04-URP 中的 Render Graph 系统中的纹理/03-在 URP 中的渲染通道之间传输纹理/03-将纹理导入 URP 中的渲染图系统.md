# 将纹理导入 URP 中的渲染图系统

> 原文：[Import a texture into the render graph system in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-import-a-texture.html)


在渲染通道中，[[02-在 URP 中的渲染图形系统中创建纹理]]时，渲染图系统会处理纹理的创建和处置。此过程意味着纹理可能不存在于下一帧中，其他摄像机可能无法使用。

要确保纹理在帧和摄像机之间可用，请使用 `ImportTexture` API 将其导入渲染图系统。

如果使用在渲染图系统外部创建的纹理，则可以导入纹理。例如，可以创建指向项目中的纹理（例如[纹理资源](https://docs.unity3d.com/Manual/ImportingTextures.html)）的渲染纹理，并将其用作渲染通道的输入。

渲染图系统不会管理导入纹理的生命周期。因此，以下几点适用：

- 必须以释放完成后使用的内存。
- URP 无法剔除使用导入纹理的渲染通道。因此，渲染可能会更慢。

有关 `RTHandle` API 的更多信息，请参阅[使用 RTHandle 系统](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/manual/rthandle-system-using.html)。

## 导入纹理

要导入纹理，请在 `ScriptableRenderPass` 类的 `RecordRenderGraph` 方法中执行以下步骤：

1. 使用 [RTHandle](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.RTHandle.html) API 创建渲染纹理手柄。 例如： `private RTHandle renderTextureHandle;`
2. 创建具有所需纹理属性的 [RenderTextureDescriptor](https://docs.unity3d.com/ScriptReference/RenderTextureDescriptor.html) 对象。 例如： `RenderTextureDescriptor textureProperties = new RenderTextureDescriptor(Screen.width, Screen.height, RenderTextureFormat.Default, 0);`
3. 使用 [ReAllocateIfNeeded](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.ShadowUtils.html#UnityEngine_Rendering_Universal_ShadowUtils_ShadowRTReAllocateIfNeeded_UnityEngine_Rendering_RTHandle__System_Int32_System_Int32_System_Int32_System_Int32_System_Single_System_String_) 方法可以创建渲染纹理并将其附加到渲染纹理句柄。仅当渲染纹理句柄为 null 或渲染纹理具有与渲染纹理描述符不同的属性时，此方法才会创建渲染纹理。 例如： `RenderingUtils.ReAllocateIfNeeded(ref renderTextureHandle, textureProperties, FilterMode.Bilinear, TextureWrapMode.Clamp, name: "My render texture" );`
4. 导入纹理，将 `RTHandle` 对象转换为渲染图系统可以使用的 `TextureHandle` 对象。  例如： `TextureHandle texture = renderGraph.ImportTexture(renderTextureHandle);`

然后，您可以使用 `TextureHandle` 对象来[[01-在 URP 中的渲染通道中使用纹理]]。

## 从项目导入纹理

要从项目导入纹理，例如附加到材质的导入纹理，请遵循以下步骤：

1. 使用 [RTHandles.Alloc](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.RTHandles.html#UnityEngine_Rendering_RTHandles_Alloc_UnityEngine_RenderTexture_) API 可从外部纹理创建渲染纹理句柄。 例如： `RTHandle renderTexture = RTHandles.Alloc(texture);`
2. 导入纹理，将 `RTHandle` 对象转换为渲染图系统可以使用的 `TextureHandle` 对象。 例如： `TextureHandle textureHandle = renderGraph.ImportTexture(renderTexture);`

然后，您可以使用 `TextureHandle` 对象来[[01-在 URP 中的渲染通道中使用纹理]]。



## 处置渲染纹理

在渲染通道结束时，必须使用 `Dispose` 方法释放渲染纹理使用的内存。

```
public void Dispose()
{
    renderTexture.Release();
}
```

## 示例

以下可编程渲染器功能包含将纹理资源复制到临时纹理的渲染通道示例。要使用此示例，请遵循以下步骤：

1. 将此编程渲染器功能添加到 URP 资源中。请参阅[[01-在 URP 中创建可编程渲染器功能]]。
2. 在 URP 资源的 Inspector 窗口中，向 **Texture To Use** 属性添加纹理。
3. 使用[帧调试器 (Frame Debugger)](https://docs.unity3d.com/2023.3/Documentation/Manual/frame-debugger-window.html) 检查渲染通道添加的纹理。

```
using UnityEngine;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering;

public class BlitFromExternalTexture : ScriptableRendererFeature
{
    // The texture to use as input 
    public Texture2D textureToUse;

    BlitFromTexture customPass;

    public override void Create()
    {
        // Create an instance of the render pass, and pass in the input texture 
        customPass = new BlitFromTexture(textureToUse);

        customPass.renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderer.EnqueuePass(customPass);
    }

    class BlitFromTexture : ScriptableRenderPass
    {
        class PassData
        {
            internal TextureHandle textureToRead;
        }

        private Texture2D texturePassedIn;

        public BlitFromTexture(Texture2D textureIn)
        {
            // In the render pass's constructor, set the input texture
            texturePassedIn = textureIn;
        }

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Copy texture", out var passData))
            {
                // Create a temporary texture and set it as the render target
                RenderTextureDescriptor textureProperties = new RenderTextureDescriptor(Screen.width, Screen.height, RenderTextureFormat.Default, 0);
                TextureHandle texture = UniversalRenderer.CreateRenderGraphTexture(renderGraph, textureProperties, "My texture", false);
                builder.SetRenderAttachment(texture, 0, AccessFlags.Write);

                // Create a render texture from the input texture
                RTHandle rtHandle = RTHandles.Alloc(texturePassedIn);

                // Create a texture handle that the shader graph system can use
                TextureHandle textureToRead = renderGraph.ImportTexture(rtHandle);

                // Add the texture to the pass data
                passData.textureToRead = textureToRead;

                // Set the texture as readable
                builder.UseTexture(passData.textureToRead, AccessFlags.Read);

                builder.AllowPassCulling(false);

                builder.SetRenderFunc((PassData data, RasterGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData data, RasterGraphContext context)
        {          
            // Copy the imported texture to the render target
            Blitter.BlitTexture(context.cmd, data.textureToRead, new Vector4(0.8f,0.6f,0,0), 0, false);
        }
    }
}
```

## 其他资源

- [纹理 (Textures)](https://docs.unity3d.com/Manual/Textures.html)
- [渲染纹理资源](https://docs.unity3d.com/Manual/class-RenderTexture.html)
- [自定义渲染纹理资源](https://docs.unity3d.com/Manual/class-CustomRenderTexture.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering;

public class BlitFromExternalTexture : ScriptableRendererFeature
{
    // The texture to use as input 
    public Texture2D textureToUse;

    BlitFromTexture customPass;

    public override void Create()
    {
        // Create an instance of the render pass, and pass in the input texture 
        customPass = new BlitFromTexture(textureToUse);

        customPass.renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderer.EnqueuePass(customPass);
    }

    class BlitFromTexture : ScriptableRenderPass
    {
        class PassData
        {
            internal TextureHandle textureToRead;
        }

        private Texture2D texturePassedIn;

        public BlitFromTexture(Texture2D textureIn)
        {
            // In the render pass's constructor, set the input texture
            texturePassedIn = textureIn;
        }

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Copy texture", out var passData))
            {
                // Create a temporary texture and set it as the render target
                RenderTextureDescriptor textureProperties = new RenderTextureDescriptor(Screen.width, Screen.height, RenderTextureFormat.Default, 0);
                TextureHandle texture = UniversalRenderer.CreateRenderGraphTexture(renderGraph, textureProperties, "My texture", false);
                builder.SetRenderAttachment(texture, 0, AccessFlags.Write);

                // Create a render texture from the input texture
                RTHandle rtHandle = RTHandles.Alloc(texturePassedIn);

                // Create a texture handle that the render graph system can use
                TextureHandle textureToRead = renderGraph.ImportTexture(rtHandle);

                // Add the texture to the pass data
                passData.textureToRead = textureToRead;

                // Set the texture as readable
                builder.UseTexture(passData.textureToRead, AccessFlags.Read);

                builder.AllowPassCulling(false);

                builder.SetRenderFunc((PassData data, RasterGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData data, RasterGraphContext context)
        {          
            // Copy the imported texture to the render target
            Blitter.BlitTexture(context.cmd, data.textureToRead, new Vector4(0.8f,0.6f,0,0), 0, false);

            // Dispose of the texture
            RTHandles.Release(data.textureToRead);
        }
    }
}
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
private RTHandle renderTextureHandle;
```

### 官方代码片段 2

```csharp
RenderingUtils.ReAllocateIfNeeded(ref renderTextureHandle, textureProperties, FilterMode.Bilinear, TextureWrapMode.Clamp, name: "My render texture" );
```

### 官方代码片段 3

```csharp
TextureHandle texture = renderGraph.ImportTexture(renderTextureHandle);
```

### 官方代码片段 4

```csharp
RTHandle renderTexture = RTHandles.Alloc(texture);
```

### 官方代码片段 5

```csharp
TextureHandle textureHandle = renderGraph.ImportTexture(renderTexture);
```

---

## 文档导航

- 上一页：[[02-在 URP 中创建全局纹理]]
- 目录：[[00-在 URP 中的渲染通道之间传输纹理]]
- 下一页：[[00-URP 中的渲染图系统中的帧数据]]
