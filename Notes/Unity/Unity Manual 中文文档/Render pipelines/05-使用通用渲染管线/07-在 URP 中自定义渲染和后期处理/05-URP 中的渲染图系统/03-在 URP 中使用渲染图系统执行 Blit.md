# 在 URP 中使用渲染图系统执行 Blit

> 原文：[Blit using the render graph system in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-blit.html)


要在通用渲染管线（URP）的渲染图系统中将一张纹理 Blit 到另一张纹理，请使用 [AddBlitPass](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.3/api/UnityEngine.Rendering.RenderGraphModule.Util.RenderGraphUtils.html#UnityEngine_Rendering_RenderGraphModule_Util_RenderGraphUtils_AddBlitPass_UnityEngine_Rendering_RenderGraphModule_RenderGraph_UnityEngine_Rendering_RenderGraphModule_Util_RenderGraphUtils_BlitMaterialParameters_System_String_System_Boolean_) API。该 API 会自动生成渲染通道，因此不需要使用 `AddRasterRenderPass` 等方法。

请按以下步骤操作：

1. 要创建可用于 Blit 渲染通道的着色器和材质，请从主菜单选择 **Assets** > **Create** > **Shader** > **SRP Blit Shader**，然后从该着色器创建材质。如果改用 Shader Graph，请参阅[创建低代码自定义后期处理效果](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing/post-processing-custom-effect-low-code.html)。有关在 URP 中编写着色器的更多信息，请参阅[在 URP 中编写自定义着色器](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-custom-shaders-urp.html)。
2. 在渲染通道脚本中添加 `using UnityEngine.Rendering.RenderGraphModule.Util`。
3. 在渲染通道中为 Blit 材质创建字段。例如：`public class MyBlitPass : ScriptableRenderPass { Material blitMaterial; }`
4. 设置要执行 Blit 的源纹理和目标纹理。例如：`TextureHandle sourceTexture = renderGraph.CreateTexture(sourceTextureProperties); TextureHandle destinationTexture = renderGraph.CreateTexture(destinationTextureProperties);` 更多信息请参阅 [[01-从 URP 中的当前帧获取数据]] 和 [[02-在 URP 中的渲染图形系统中创建纹理]]。
5. 要为 Blit 操作设置材质、纹理和着色器通道，请创建 [RenderGraphUtils.BlitMaterialParameters](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.3/api/UnityEngine.Rendering.RenderGraphModule.Util.RenderGraphUtils.BlitMaterialParameters.html) 对象。例如：`// Create a BlitMaterialParameters object with the blit material, source texture, destination texture, and shader pass to use. var blitParams = new RenderGraphUtils.BlitMaterialParameters(blitMaterial, sourceTexture, destinationTexture, 0);`
6. 要添加 Blit 通道，请使用 Blit 参数调用 [AddBlitPass](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.3/api/UnityEngine.Rendering.RenderGraphModule.Util.RenderGraphUtils.html#UnityEngine_Rendering_RenderGraphModule_Util_RenderGraphUtils_AddBlitPass_UnityEngine_Rendering_RenderGraphModule_RenderGraph_UnityEngine_Rendering_RenderGraphModule_Util_RenderGraphUtils_BlitMaterialParameters_System_String_System_Boolean_) 方法。例如：`renderGraph.AddBlitPass(blitParams, "Pass created with AddBlitPass");`

完整示例请参阅 [[03-在 URP 中导入包示例]]中的渲染图示例 **BlitWithMaterial**。

如果将 `AddBlitPass` 与默认材质结合使用，Unity 可能改用 `AddCopyPass` API，以优化渲染通道，使其从 GPU 的片上内存而不是显存访问帧缓冲区。此过程有时称为帧缓冲区获取。有关更多信息，请参阅 [AddCopyPass](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.3/api/UnityEngine.Rendering.RenderGraphModule.Util.RenderGraphUtils.html#UnityEngine_Rendering_RenderGraphModule_Util_RenderGraphUtils_AddCopyPass_UnityEngine_Rendering_RenderGraphModule_RenderGraph_UnityEngine_Rendering_RenderGraphModule_TextureHandle_UnityEngine_Rendering_RenderGraphModule_TextureHandle_System_String_System_Boolean_) API。

## 避免回 Blit

执行 Blit 后，通常会将目标纹理再次 Blit 回活动颜色纹理。但在渲染图系统中，可以改为更新帧数据，使其指向目标纹理，从而只需执行一次 Blit。例如：

```cs
// Set the camera color as the destination texture you blitted to.
frameData.cameraColor = destinationTexture;
```

更多信息请参阅 [[09-优化渲染图]]。

## 其他资源

- [从 GPU 内存获取当前帧缓冲区](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-framebuffer-fetch.html)
- [[00-URP 中的渲染图系统]]
- [[03-在 URP 中导入包示例]]：参阅使用 **AddCopyPass** 的 **Blit** 示例。


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
// Create a BlitMaterialParameters object with the blit material, source texture, destination texture, and shader pass to use.
var blitParams = new RenderGraphUtils.BlitMaterialParameters(sourceTexture, destinationTexture, blitMaterial, 0);
```

### 官方代码片段 2

```csharp
using (var builder = renderGraph.AddBlitPass(blitParams, "Pass created with AddBlitPass", returnBuilder: true))
{
    // Use the builder variable to customize the render pass here.
}
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
public class MyBlitPass : ScriptableRenderPass
{
    Material blitMaterial;
}
```

### 官方代码片段 2

```csharp
TextureHandle sourceTexture = renderGraph.CreateTexture(sourceTextureProperties);
TextureHandle destinationTexture = renderGraph.CreateTexture(destinationTextureProperties);
```

### 官方代码片段 3

```csharp
renderGraph.AddBlitPass(blitParams, "Pass created with AddBlitPass");
```

---

## 文档导航

- 上一页：[[02-在 URP 中使用渲染图系统编写渲染通道]]
- 目录：[[00-URP 中的渲染图系统]]
- 下一页：[[00-URP 中的 Render Graph 系统中的纹理]]
