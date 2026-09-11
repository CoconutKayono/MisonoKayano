# 在 URP 中获取先前帧的数据

> 原文：[Get data from previous frames in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-get-previous-frames.html)


要在通用渲染管线 (URP) 中获取摄像机渲染的先前帧，请使用 [UniversalCameraData.historyManager](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/api/UnityEngine.Rendering.Universal.UniversalCameraData.html) API。这些纹理有时称为历史纹理或历史缓冲区。

这些帧是 GPU 渲染管线的输出，因此它们不包括 GPU 渲染后发生的任何处理，例如后期处理效果。

要从可编程渲染通道外部获取先前的帧，请参阅。

请遵循以下步骤：

1. 在 `RecordRenderGraph` 方法中，从 `ContextContainer` 对象获取 `UniversalCameraData` 对象。例如： `public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext) { UniversalCameraData cameraData = frameContext.Get<UniversalCameraData>(); }`
2. 要请求访问渲染历史记录中的颜色纹理或深度纹理，请使用 `RequestAccess` API。例如： `// Request access to the color textures cameraData.historyManager.RequestAccess<RawColorHistory>();` 请改用 `RawDepthHistory` 来请求访问深度纹理。
3. 获取先前的纹理之一。例如： `// Get the previous textures RawColorHistory history = cameraData.historyManager.GetHistoryForRead<RawColorHistory>(); // Get the first texture, which the camera rendered in the previous frame RTHandle historyTexture = history?.GetPreviousTexture(0);`
4. 将纹理转换为渲染图系统可以使用的句柄。例如： `passData.historyTexture = renderGraph.ImportTexture(historyTexture);`

然后，您可以在渲染通道中读取纹理。

有关使用 `historyManager` API 的更多信息，请参阅 [UniversalCameraData.historyManager](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/api/UnityEngine.Rendering.Universal.UniversalCameraData.html)。

## 示例

以下是可编程渲染器功能，可创建材质并使用先前帧作为材质的纹理。

要使用该示例，请遵循以下步骤：

1. 创建一个 URP 着色器，以对名为 `_BaseMap` 的纹理进行采样。有关示例，请参阅[绘制纹理](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-unlit-texture.html)。
2. 从着色器创建材质。
3. 创建一个名为 `RenderLastFrameInMaterial.cs` 的 C# 新脚本，将以下代码粘贴到其中，然后保存文件。
4. 在活动 URP 渲染器中，[[01-向 URP 渲染器添加渲染器功能]]。
5. 在活动 URP 渲染器的**检视面板 (Inspector)** 窗口中，在可编程渲染器功能（在步骤 4 中添加）的**渲染材质中的最后一帧 (Render Last Frame In Material)** 部分中，将在步骤 2 中创建的材质分配给**对象材质 (Object Material)** 字段。

```
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;
public class RenderLastFrameInMaterial : ScriptableRendererFeature
{
    public Material objectMaterial;
    CustomRenderPass renderLastFrame;

    public override void Create()
    {
        renderLastFrame = new CustomRenderPass();
        renderLastFrame.renderPassEvent = RenderPassEvent.BeforeRenderingOpaques;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderLastFrame.passMaterial = objectMaterial;
        renderer.EnqueuePass(renderLastFrame);
    }

    class CustomRenderPass : ScriptableRenderPass
    {
        public Material passMaterial;

        public class PassData
        {
            internal Material material;
            internal TextureHandle historyTexture;
        }

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer contextData)
        {
            UniversalCameraData cameraData = contextData.Get<UniversalCameraData>();

            // Return if the history manager isn't available
            // For example, there are no history textures during the first frame
            if (cameraData.historyManager == null) { return; }
  
            // Request access to the color and depth textures
            cameraData.historyManager.RequestAccess<RawColorHistory>();

            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Get last frame", out var passData))
            {
                UniversalResourceData resourceData = contextData.Get<UniversalResourceData>();

                // Set the render graph to render to the active color texture
                builder.SetRenderAttachment(resourceData.activeColorTexture, 0, AccessFlags.Write);

                // Add the material to the pass data
                passData.material = passMaterial;
                
                // Get the color texture the camera rendered to in the previous frame
                RawColorHistory history = cameraData.historyManager.GetHistoryForRead<RawColorHistory>();
                RTHandle historyTexture = history?.GetPreviousTexture(0);
                passData.historyTexture = renderGraph.ImportTexture(historyTexture);

                builder.SetRenderFunc(static (PassData data, RasterGraphContext context) =>
                {
                    // Set the material to use the texture
                    data.material.SetTexture("_BaseMap", data.historyTexture);
                });
            }
        }
    }
}
```



## 使用脚本获取先前帧的数据

要使用脚本（例如 `MonoBehaviour`）获取先前帧的数据，请执行以下操作：

1. 使用可编程渲染管线 (SRP) Core [RequestAccess](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.IPerFrameHistoryAccessTracker.html#UnityEngine_Rendering_IPerFrameHistoryAccessTracker_RequestAccess__1) API 来请求纹理。
2. 使用 [UniversalAdditionalCameraData.history](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/api/UnityEngine.Rendering.Universal.UniversalAdditionalCameraData.html#UnityEngine_Rendering_Universal_UniversalAdditionalCameraData_history) API 来获取数据。

要确保 Unity 先完成帧的渲染，请使用 [LateUpdate](https://docs.unity3d.com/ScriptReference/MonoBehaviour.LateUpdate.html) 方法中的 `UniversalAdditionalCameraData.history` API。

有关更多信息，请参阅可编程渲染管线 (SRP) Core 包中的以下内容：

- [ICameraHistoryReadAccess](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.ICameraHistoryReadAccess.html)
- [IPerFrameHistoryTracker](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.IPerFrameHistoryAccessTracker.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;
public class RenderLastFrameInMaterial : ScriptableRendererFeature
{
    public Material objectMaterial;
    CustomRenderPass renderLastFrame;

    public override void Create()
    {
        renderLastFrame = new CustomRenderPass();
        renderLastFrame.renderPassEvent = RenderPassEvent.BeforeRenderingOpaques;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderLastFrame.passMaterial = objectMaterial;
        renderer.EnqueuePass(renderLastFrame);
    }

    class CustomRenderPass : ScriptableRenderPass
    {
        public Material passMaterial;

        class PassData
        {
            public Material material;
            public TextureHandle historyTexture;
        }

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer contextData)
        {
            UniversalCameraData cameraData = contextData.Get<UniversalCameraData>();

            // Return if the history manager isn't available
            // For example, there are no history textures during the first frame
            if (cameraData.historyManager == null) { return; }
  
            // Request access to the color and depth textures
            cameraData.historyManager.RequestAccess<RawColorHistory>();

            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Get last frame", out var passData))
            {
                UniversalResourceData resourceData = contextData.Get<UniversalResourceData>();

                // Set the render graph to render to the active color texture
                builder.SetRenderAttachment(resourceData.activeColorTexture, 0, AccessFlags.Write);

                // Add the material to the pass data
                passData.material = passMaterial;
                
                // Get the color texture the camera rendered to in the previous frame
                RawColorHistory history = cameraData.historyManager.GetHistoryForRead<RawColorHistory>();
                RTHandle historyTexture = history?.GetPreviousTexture(0);
                passData.historyTexture = renderGraph.ImportTexture(historyTexture);

                builder.SetRenderFunc(static (PassData data, RasterGraphContext context) =>
                {
                    // Set the material to use the texture
                    data.material.SetTexture("_BaseMap", data.historyTexture);
                });
            }
        }
    }
}
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
{
    UniversalCameraData cameraData = frameContext.Get<UniversalCameraData>();
}
```

### 官方代码片段 2

```csharp
// Request access to the color textures
cameraData.historyManager.RequestAccess<RawColorHistory>();
```

### 官方代码片段 3

```csharp
// Get the previous textures 
RawColorHistory history = cameraData.historyManager.GetHistoryForRead<RawColorHistory>();

// Get the first texture, which the camera rendered in the previous frame
RTHandle historyTexture = history?.GetPreviousTexture(0);
```

---

## 文档导航

- 上一页：[[01-从 URP 中的当前帧获取数据]]
- 目录：[[00-URP 中的渲染图系统中的帧数据]]
- 下一页：[[03-将纹理添加到摄像机历史记录]]
