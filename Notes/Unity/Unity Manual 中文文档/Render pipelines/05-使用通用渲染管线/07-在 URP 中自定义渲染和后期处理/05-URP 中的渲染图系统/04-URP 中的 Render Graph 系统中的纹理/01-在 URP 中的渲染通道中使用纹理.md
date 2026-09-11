# 在 URP 中的渲染通道中使用纹理

> 原文：[Read or write to a texture in a render pass in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-read-write-texture.html)


您可以使用渲染图系统 API 将纹理设置为自定义渲染通道的输入或输出，以便对其进行读取或写入。

不能同时读取和写入渲染通道中的同一纹理。有关更多信息，请参阅。

## 将纹理设置为输入

要将纹理设置为自定义渲染通道的输入，请遵循以下步骤：

1. 在 `RecordRenderGraph` 方法中，将纹理句柄字段添加到您的通道使用的数据。 例如： `// Create the data your pass uses public class MyPassData { // Add a texture handle public TextureHandle textureToUse; }`
2. 将纹理句柄设置为您要使用的纹理。 例如： `// Add the texture handle to the data RenderTextureDescriptor textureProperties = new RenderTextureDescriptor(Screen.width, Screen.height, RenderTextureFormat.Default, 0); TextureHandle textureHandle = UniversalRenderer.CreateRenderGraphTexture(renderGraph, textureProperties, "My texture", false); passData.textureToUse = textureHandle;`
3. 调用 [UseTexture](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.RenderGraphModule.IBaseRenderGraphBuilder.html#UnityEngine_Rendering_RenderGraphModule_IBaseRenderGraphBuilder_UseTexture_UnityEngine_Rendering_RenderGraphModule_TextureHandle__UnityEngine_Rendering_RenderGraphModule_AccessFlags_) 方法将纹理设置为输入。 例如： `builder.UseTexture(passData.textureToUse, AccessFlags.Read);`

在 `SetRenderFunc` 方法中，现在可以使用通道数据中的 `TextureHandle` 对象作为 API（如 `Blitter.BlitTexture`）的输入。

## 将纹理设置为渲染目标

要将纹理设置为 `Blit` 等命令的输出，请在 `RecordRenderGraph` 方法中使用 [SetRenderAttachment](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.RenderGraphModule.IRasterRenderGraphBuilder.html#UnityEngine_Rendering_RenderGraphModule_IRasterRenderGraphBuilder_SetRenderAttachment_UnityEngine_Rendering_RenderGraphModule_TextureHandle_System_Int32_UnityEngine_Rendering_RenderGraphModule_AccessFlags_) 方法。默认情况下，`SetRenderAttachment` 方法将纹理设置为只读。

例如，以下命令会创建一个临时纹理并将其设置为渲染通道的渲染目标：

```
// Create texture properties
RenderTextureDescriptor textureProperties = new RenderTextureDescriptor(Screen.width, Screen.height, RenderTextureFormat.Default, 0);

// Create the texture
TextureHandle targetTexture = UniversalRenderer.CreateRenderGraphTexture(renderGraph, textureProperties, "My texture", false);

// Set the texture as the render target
// The second parameter is the index the shader uses to access the texture
builder.SetRenderAttachment(targetTexture, 0);
```

在 `SetRenderFunc` 方法中，现在可以使用 API（例如 `Blitter.BlitTexture`）写入纹理。

无需将纹理添加到通道数据。渲染图系统在执行渲染通道之前，会自动为您设置纹理。

如果需要将对象绘制到渲染目标，请参阅[[06-在 URP 中的渲染图形系统中绘制对象]]以了解更多信息。



## 在渲染通道期间更改渲染目标

在渲染图系统渲染通道期间，无法更改 URP 写入的目标纹理。

您可以改用以下任一方式：

- 创建另一个自定义渲染通道，并在另一个渲染通道期间使用 `builder.SetRenderAttachment` 更改渲染目标。
- 使用 `UnsafePass` API，以便可以在 `SetRenderFunc` 方法中使用 `SetRenderTarget` API。请参阅[[10-在渲染图渲染通道中使用兼容性模式 API]]，以了解更多信息和获取示例。

您可以使用这些方法来读取和写入同一个纹理，方法是先从纹理复制到您创建的临时纹理，然后再复制回来。

如果在具有不同属性的几个纹理之间执行__ blit__“位块传输 (Bit Block Transfer)”的简写。blit 操作是将数据块从内存中的一个位置传输到另一个位置的过程。
如果执行 Blit 操作，渲染可能会很慢，因为 URP 无法将 Blit 合并到单个原生渲染通道中。请改用 `AddUnSafePass` API 和 `SetRenderTarget()` 方法。有关 Blit 术语，请参阅 [Glossary](https://docs.unity3d.com/6000.7/Documentation/Manual/Glossary.html#blit)。

### 示例

请参阅以下内容：

- [[02-在 URP 中使用渲染图系统编写渲染通道]]，以获得创建纹理然后对其执行 blit 操作的示例。
- [[03-将纹理导入 URP 中的渲染图系统]]，以获得将临时纹理设置为渲染目标的示例。


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
builder.SetRenderAttachment(textureHandle, 0);
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
// Create the data your pass uses
public class MyPassData
{
    // Add a texture handle
    public TextureHandle textureToUse;
}
```

### 官方代码片段 2

```csharp
builder.UseTexture(passData.textureToUse, AccessFlags.Read);
```

---

## 文档导航

- 上一页：[[00-URP 中的 Render Graph 系统中的纹理]]
- 目录：[[00-URP 中的 Render Graph 系统中的纹理]]
- 下一页：[[02-在 URP 中的渲染图形系统中创建纹理]]
