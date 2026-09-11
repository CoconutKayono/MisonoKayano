# 从 URP 中的当前帧获取数据

> 原文：[Get data from the current frame in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/accessing-frame-data.html)


您可以获取通用渲染管线 (URP) 为当前帧创建的纹理，例如活动颜色缓冲区或 G 缓冲区纹理，并在渲染通道中使用它们。

这些纹理称为帧数据、资源数据或帧资源。本文档将这些纹理称为帧数据。

某些纹理可能不存在于帧数据中，具体取决于用于将自定义渲染通道插入到 URP 帧渲染循环中的注入点。有关何时存在哪些纹理的更多信息，请参阅[[04-URP 的注入点参考]]。

## 获取帧数据

覆盖 `RecordRenderGraph` 方法时，帧数据位于 URP 提供的 `ContextContainer` 对象中。

按照以下步骤获取帧数据中的纹理的句柄：

1. 使用 `ContextContainer` 对象的 `Get` 方法，将所有帧数据作为 `UniversalResourceData` 对象获取。 例如： `public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext) { using (var builder = renderGraph.AddRasterRenderPass<PassData>("Get frame data", out var passData)) { UniversalResourceData frameData = frameContext.Get<UniversalResourceData>(); } }`
2. 获取帧数据中的纹理的手柄。 例如，以下方法获取活动颜色纹理的句柄： `TextureHandle activeColorTexture = frameData.activeColorTexture;`

然后，就可以读取和写入纹理了。请参阅[[01-在 URP 中的渲染通道中使用纹理]]。

纹理句柄仅对当前帧中的当前渲染图有效。

可以使用 [ConfigureInput](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.ScriptableRenderPass.html#UnityEngine_Rendering_Universal_ScriptableRenderPass_ConfigureInput_UnityEngine_Rendering_Universal_ScriptableRenderPassInput_) API 确保 URP 在帧数据中生成所需的纹理。

## 示例

有关完整示例，请参阅[[03-在 URP 中导入包示例]]名为 **TextureReference w. FrameData** 的示例。

## 其他资源

- [[04-URP 的帧数据纹理参考]]
- [[01-通用渲染管线中的渲染]]
- [[00-通用渲染管线基础知识]]
- [[00-URP 中的延迟渲染路径]]


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameContext)
{
    using (var builder = renderGraph.AddRasterRenderPass<PassData>("Get frame data", out var passData))
    {
        UniversalResourceData frameData = frameContext.Get<UniversalResourceData>();
    }
}
```

### 官方代码片段 2

```csharp
TextureHandle activeColorTexture = frameData.activeColorTexture;
```

---

## 文档导航

- 上一页：[[00-URP 中的渲染图系统中的帧数据]]
- 目录：[[00-URP 中的渲染图系统中的帧数据]]
- 下一页：[[02-在 URP 中获取先前帧的数据]]
