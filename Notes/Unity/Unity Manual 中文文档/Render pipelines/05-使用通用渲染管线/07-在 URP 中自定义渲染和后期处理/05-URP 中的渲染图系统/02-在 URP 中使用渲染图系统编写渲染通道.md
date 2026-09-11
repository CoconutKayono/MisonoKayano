# 在 URP 中使用渲染图系统编写渲染通道

> 原文：[Write a render pass using the render graph system in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-write-render-pass.html)


本页介绍如何使用渲染图系统编写渲染通道。

为了举例说明，页面使用示例渲染通道将摄像机的活动颜色纹理复制到目标纹理。为了简化代码，此示例不使用帧中其他位置的目标纹理。您可以使用帧调试器检查其内容。

## 声明渲染通道

将渲染通道声明为继承自 [ScriptableRenderPass](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.ScriptableRenderPass.html) 类的类。

## 声明渲染通道使用的资源

在渲染通道中，声明一个包含渲染通道使用的资源的类。

资源可以是常规 C# 变量和渲染图资源引用。渲染图系统可以在渲染代码执行期间访问此数据结构。确保仅声明渲染通道使用的变量。添加不必要的变量可能会降低性能。

```
class PassData
{
    internal TextureHandle copySourceTexture;
}
```

[RecordRenderGraph](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.RenderObjectsPass.html#UnityEngine_Rendering_Universal_RenderObjectsPass_RecordRenderGraph_) 方法填充数据，渲染图将其作为参数传递给渲染函数。

## 声明一个渲染函数，用于为渲染通道生成渲染命令

声明一个渲染函数，用于为渲染通道生成渲染命令。在此示例中，[RecordRenderGraph](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.RenderObjectsPass.html#UnityEngine_Rendering_Universal_RenderObjectsPass_RecordRenderGraph_) 方法进一步指示渲染图使用一个使用 `SetRenderFunc` 方法的函数。

```
static void ExecutePass(PassData data, RasterGraphContext context)
{
    // Records a rendering command to copy, or blit, the contents of the source texture
    // to the color render target of the render pass.
    // The RecordRenderGraph method sets the destination texture as the render target
    // with the UseTextureFragment method.
    Blitter.BlitTexture(context.cmd, data.copySourceTexture,
        new Vector4(1, 1, 0, 0), 0, false);
}
```

## 实现 RecordRenderGraph 方法

使用 [RecordRenderGraph](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.RenderObjectsPass.html#UnityEngine_Rendering_Universal_RenderObjectsPass_RecordRenderGraph_) 方法可在渲染图系统中添加和配置一个或多个渲染通道。

Unity 在渲染图配置步骤中调用此方法，并允许您注册用于渲染图执行的相关通道和资源。使用此方法可实现自定义渲染。

在 [RecordRenderGraph](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.RenderObjectsPass.html#UnityEngine_Rendering_Universal_RenderObjectsPass_RecordRenderGraph_) 方法中，可以声明渲染通道输入和输出，但不向命令缓冲区添加命令。

以下部分介绍 [RecordRenderGraph](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.RenderObjectsPass.html#UnityEngine_Rendering_Universal_RenderObjectsPass_RecordRenderGraph_) 方法的主要内容并提供示例实现。

## 渲染图构建器变量添加帧资源

`builder` 变量是 `IRasterRenderGraphBuilder` 接口的实例。此变量是用于配置与渲染通道相关信息的入口点。

[UniversalResourceData](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.UniversalResourceData.html) 类包含 URP 使用的所有纹理资源，包括摄像机的活动颜色和深度纹理。

[UniversalCameraData](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.UniversalCameraData.html) 类包含与当前活动摄像机相关的数据。

出于演示目的，此示例创建一个临时目标纹理。`UniversalRenderer.CreateRenderGraphTexture` 是调用 `RenderGraph.CreateTexture` 方法的 helper 方法。

```
TextureHandle destination =
    UniversalRenderer.CreateRenderGraphTexture(renderGraph, desc, "CopyTexture", false);
```

`builder.UseTexture` 方法声明此渲染通道使用源纹理作为只读输入：

```
builder.UseTexture(passData.copySourceTexture);
```

在此示例中，`builder.SetRenderAttachment` 方法声明此渲染通道使用临时目标纹理作为其颜色渲染目标。此声明类似于可在兼容性模式下使用的 `cmd.SetRenderTarget` API（不含渲染图 API）。

`SetRenderFunc` 方法将 `ExecutePass` 方法设置为执行渲染通道时渲染图形调用的渲染函数。此示例使用 lambda 表达式来避免内存分配。

```
builder.SetRenderFunc((PassData data, RasterGraphContext context) => ExecutePass(data, context));
```

[RecordRenderGraph](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.RenderObjectsPass.html#UnityEngine_Rendering_Universal_RenderObjectsPass_RecordRenderGraph_) 方法的完整示例如下：

```
// This method adds and configures one or more render passes in the render graph.
// This process includes declaring their inputs and outputs,
// but does not include adding commands to command buffers.
public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
{
    string passName = "Copy To Debug Texture";

    // Add a raster render pass to the render graph. The PassData type parameter determines
    // the type of the passData output variable.
    using (var builder = renderGraph.AddRasterRenderPass<PassData>(passName,
        out var passData))
    {
        // UniversalResourceData contains all the texture references used by URP,
        // including the active color and depth textures of the camera.
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();

        // Populate passData with the data needed by the rendering function
        // of the render pass.
        // Use the camera's active color texture
        // as the source texture for the copy operation.
        passData.copySourceTexture = resourceData.activeColorTexture;

        // Create a destination texture for the copy operation based on the settings,
        // such as dimensions, of the textures that the camera uses.
        // Set msaaSamples to 1 to get a non-multisampled destination texture.
        // Set depthBufferBits to 0 to ensure that the CreateRenderGraphTexture method
        // creates a color texture and not a depth texture.
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        RenderTextureDescriptor desc = cameraData.cameraTargetDescriptor;
        desc.msaaSamples = 1;
        desc.depthBufferBits = 0;

        // For demonstrative purposes, this sample creates a temporary destination texture.
        // UniversalRenderer.CreateRenderGraphTexture is a helper method
        // that calls the RenderGraph.CreateTexture method.
        // Using a RenderTextureDescriptor instance instead of a TextureDesc instance
        // simplifies your code.
        TextureHandle destination =
            UniversalRenderer.CreateRenderGraphTexture(renderGraph, desc,
                "CopyTexture", false);

        // Declare that this render pass uses the source texture as a read-only input.
        builder.UseTexture(passData.copySourceTexture);

        // Declare that this render pass uses the temporary destination texture
        // as its color render target.
        // This is similar to cmd.SetRenderTarget prior to the RenderGraph API.
        builder.SetRenderAttachment(destination, 0);

        // RenderGraph automatically determines that it can remove this render pass
        // because its results, which are stored in the temporary destination texture,
        // are not used by other passes.
        // For demonstrative purposes, this sample turns off this behavior to make sure
        // that render graph executes the render pass. 
        builder.AllowPassCulling(false);

        // Set the ExecutePass method as the rendering function that render graph calls
        // for the render pass. 
        // This sample uses a lambda expression to avoid memory allocations.
        builder.SetRenderFunc((PassData data, RasterGraphContext context)
            => ExecutePass(data, context));
    }
}
```

## 将可编程渲染通道实例注入渲染器

要将可编程渲染通道实例注入渲染器，请使用渲染器功能实现中的 `AddRenderPasses` 方法。URP 每帧都会调用 `AddRenderPasses` 方法，每个摄像机调用一次。

```
public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
{
    renderer.EnqueuePass(m_CopyRenderPass);
}
```

## 其他资源

- [完整的可编程渲染器功能示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/create-custom-renderer-feature.html)
- [在兼容性模式下编写可编程渲染通道](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/write-a-scriptable-render-pass.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
class PassData
{
    public TextureHandle copySourceTexture;
}
```

### 官方代码片段 2

```csharp
static void ExecutePass(PassData data, RasterGraphContext context)
{
    // Records a rendering command to copy, or blit, the contents of the source texture
    // to the color render target of the render pass.
    Blitter.BlitTexture(context.cmd, data.copySourceTexture,
        new Vector4(1, 1, 0, 0), 0, false);
}
```

### 官方代码片段 3

```csharp
builder.SetRenderFunc(static (PassData data, RasterGraphContext context) => ExecutePass(data, context));
```

### 官方代码片段 4

```csharp
// This method adds and configures one or more render passes in the render graph.
// This process includes declaring their inputs and outputs,
// but does not include adding commands to command buffers.
public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
{
    string passName = "Copy To Debug Texture";

    // Add a raster render pass to the render graph. The PassData type parameter determines
    // the type of the passData output variable.
    using (var builder = renderGraph.AddRasterRenderPass<PassData>(passName,
        out var passData))
    {
        // UniversalResourceData contains all the texture references used by URP,
        // including the active color and depth textures of the camera.
        UniversalResourceData frameData = frameContext.Get<UniversalResourceData>();

        // Populate passData with the data needed by the rendering function
        // of the render pass.
        // Use the camera's active color texture
        // as the source texture for the copy operation.
        passData.copySourceTexture = frameData.activeColorTexture;

        // Create a destination texture for the copy operation based on the settings,
        // such as dimensions, of the textures that the camera uses.
        // Set depthBufferBits to 0 to ensure that the CreateRenderGraphTexture method
        // creates a color texture and not a depth texture.
        TextureDesc desc = frameData.cameraDepthTexture.GetDescriptor(renderGraph);
        desc.depthBufferBits = 0;
        TextureHandle destination = renderGraph.CreateTexture(desc);

        // Declare that this render pass uses the source texture as a read-only input.
        builder.UseTexture(passData.copySourceTexture);

        // Declare that this render pass uses the temporary destination texture
        // as its color render target.
        // This is similar to cmd.SetRenderTarget prior to the RenderGraph API.
        builder.SetRenderAttachment(destination, 0);

        // Make sure the render graph system keeps the render pass, even if it's not used in the final frame.
        // Don't use this in production code, because it prevents the render graph system from removing the render pass if it's not needed. 
        builder.AllowPassCulling(false);

        // Set the ExecutePass method as the rendering function that render graph calls
        // for the render pass. 
        // This sample uses a lambda expression to avoid memory allocations.
        builder.SetRenderFunc(static (PassData data, RasterGraphContext context)
            => ExecutePass(data, context));
    }
}
```

---

## 文档导航

- 上一页：[[01-URP 中的渲染图系统简介]]
- 目录：[[00-URP 中的渲染图系统]]
- 下一页：[[03-在 URP 中使用渲染图系统执行 Blit]]
