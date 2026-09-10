# 在 URP 中创建全局纹理

> 原文：[Create a texture as a global texture in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-create-global-texture.html)


如果需要将纹理用作 GameObject 上着色器的输入，可以将该纹理设置为全局纹理。全局纹理对所有着色器和渲染通道可用。有关 GameObject 的更多信息，请参阅[游戏对象](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/class-GameObject.html)。

将纹理设置为全局纹理可能会降低渲染速度。请参阅 [SetGlobalTexture](https://docs.unity3d.com/ScriptReference/Shader.SetGlobalTexture.html)。

不要使用 [[../../10-在渲染图渲染通道中使用兼容性模式 API]] 和 `CommandBuffer.SetGlobal` 将纹理设置为全局纹理，因为这可能导致错误。

要设置全局纹理，请在 `RecordRenderGraph` 方法中使用 [SetGlobalTextureAfterPass](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@latest/index.html?subfolder=/api/UnityEngine.Rendering.RenderGraphModule.IBaseRenderGraphBuilder.html%23UnityEngine_Rendering_RenderGraphModule_IBaseRenderGraphBuilder_SetGlobalTextureAfterPass_UnityEngine_Rendering_RenderGraphModule_TextureHandle__System_Int32_) 方法。

例如：

```cs
// Allocate a global shader texture called _GlobalTexture
private int globalTextureID = Shader.PropertyToID("_GlobalTexture")

using (var builder = renderGraph.AddRasterRenderPass<PassData>("MyPass", out var passData)){

    // Set a texture to the global texture
    builder.SetGlobalTextureAfterPass(texture, globalTextureID);
}
```

如果尚未调用 `SetRenderFunc`，还必须添加一个空的渲染函数。例如：

```cs
    builder.SetRenderFunc(static (PassData data, RasterGraphContext context) => { });
```

现在可以执行以下操作：

- 使用 [UseGlobalTexture()](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@latest/index.html?subfolder=/api/UnityEngine.Rendering.RenderGraphModule.IBaseRenderGraphBuilder.html%23UnityEngine_Rendering_RenderGraphModule_IBaseRenderGraphBuilder_UseGlobalTexture_System_Int32_UnityEngine_Rendering_RenderGraphModule_AccessFlags_) 或 [UseAllGlobalTextures()](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@latest/index.html?subfolder=/api/UnityEngine.Rendering.RenderGraphModule.IBaseRenderGraphBuilder.html%23UnityEngine_Rendering_RenderGraphModule_IBaseRenderGraphBuilder_UseAllGlobalTextures_System_Boolean_) API，在其他渲染通道中访问该纹理。
- 通过引用纹理的 [nameID](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Shader.PropertyToID.html)，在场景中的任意材质上使用该纹理。



## 访问全局纹理

在其他渲染通道中，通过纹理的 `nameID` 访问设置为全局纹理的特定纹理（使用 [Shader.PropertyToID](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Shader.PropertyToID.html) 获取）。请根据通道使用全局纹理的方式设置适当的访问标志。

例如：

```cs
    class AccessGlobalTexturePass : ScriptableRenderPass
    {

        // The nameID of the globalTexture you want to use - which you have set in a previous pass
        private int globalTextureID = Shader.PropertyToID("_GlobalTexture")

        class PassData
        {
            // No local pass data needed
        }       

        public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
        {
            using (var builder = renderGraph.AddRasterRenderPass<PassData>("Fetch texture and draw triangle", out var passData))
            {
                
                // Set the inputs and outputs of your pass
                // builder.SetRenderAttachment(/*...*/);
                // builder.UseTexture(/*...*/);

                // Use the global texture in this pass
                builder.UseGlobalTexture(globalTextureID, AccessFlags.Read);

                builder.SetRenderFunc(static (PassData data, RasterGraphContext context) => ExecutePass(data, context));
            }
        }

        static void ExecutePass(PassData data, RasterGraphContext context)
        {
            // ...
        }
    }
```

**注意：** 也可以使用 `builder.UseAllGlobalTextures(true);` 在通道中使用所有全局纹理，而不是使用单个纹理。但这会占用更多内存。

---

## 文档导航

- 上一页：[[01-将纹理添加到 URP 帧数据]]
- 目录：[[00-在 URP 中的渲染通道之间传输纹理]]
- 下一页：[[03-将纹理导入 URP 中的渲染图系统]]
