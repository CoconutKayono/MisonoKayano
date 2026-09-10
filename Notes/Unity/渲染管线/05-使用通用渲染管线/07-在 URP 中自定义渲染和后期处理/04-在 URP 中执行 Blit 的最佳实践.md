# 在 URP 中执行 Blit 的最佳实践

> 原文：[Blit in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customize/blit-overview.html)


Blit 操作是将来源纹理复制到目标纹理的过程。

本页概述了在 URP 中执行__ Blit__“位块传输 (Bit Block Transfer)”的简写。blit 操作是将数据块从内存中的一个位置传输到另一个位置的过程。
介绍在 URP 中执行 Blit 操作的不同方法，以及编写自定义渲染通道时应遵循的最佳实践。有关 Blit 术语，请参阅 [Glossary](https://docs.unity3d.com/6000.7/Documentation/Manual/Glossary.html#blit)。

## 旧版 CommandBuffer.Blit API

请避免在 URP 项目中使用 [CommandBuffer.Blit](https://docs.unity3d.com/2022.1/Documentation/ScriptReference/Rendering.CommandBuffer.Blit.html) API。

[CommandBuffer.Blit](https://docs.unity3d.com/2022.1/Documentation/ScriptReference/Rendering.CommandBuffer.Blit.html) API 为旧版 API。它隐式运行与更改状态、绑定纹理和设置渲染目标相关的额外操作。这些操作发生在 SRP 项目的后台，对用户来说并不透明。

该 API 与 URP__ XR__虚拟现实（VR）、增强现实（AR）和混合现实（MR）应用的泛指术语。支持这些形式的交互式应用程序的设备可被称为 XR 设备。[更多信息](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customize/XR.html)
该 API 与 [XR](https://docs.unity3d.com/6000.7/Documentation/Manual/Glossary.html#XR) 集成存在兼容性问题。使用 `cmd.Blit` 可能会隐式启用或禁用扩展现实着色器关键字，而这会破坏扩展现实 SPI 渲染。

[CommandBuffer.Blit](https://docs.unity3d.com/2022.1/Documentation/ScriptReference/Rendering.CommandBuffer.Blit.html) API 与 `NativeRenderPass` 和 `RenderGraph` 不兼容。

类似的考虑因素也适用于任何内部依赖于`cmd.Blit` 的实用程序或封装器，`RenderingUtils.Blit` 就是其中一个示例。

## SRP Blitter API

在 URP 项目中使用 [Blitter API](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@13.1/api/UnityEngine.Rendering.Blitter.html)。此 API 不依赖旧版逻辑，与扩展现实、原生渲染通道和其他 SRP API 兼容。

## 自定义全屏 Blit 示例

[如何在兼容模式下于 URP 中执行全屏 Blit](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/how-to-fullscreen-blit.html) 示例展示了如何创建可执行全屏 Blit 的自定义渲染器功能。该示例适用于扩展现实，并且与 SRP API 兼容。


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
{
    Blitter.BlitCameraTexture(commandBuffer, sourceTexture, destinationTexture, materialToUse, passNumber);
}
```

### 官方代码片段 2

```csharp
using UnityEngine.Rendering.RenderGraphModule.Util;

...

    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData) {

        // Set up the source texture, destination texture, material, and shader pass number for the blit
        RenderGraphUtils.BlitMaterialParameters parameters = new(sourceTexture, destinationTexture, materialToUse, passNumber);

        // Add the blit pass
        renderGraph.AddBlitPass(parameters, passName: "My Blit Pass");
    }
```

---

## 文档导航

- 上一页：[[03-URP 中的自定义渲染通道工作流程]]
- 目录：[[00-在 URP 中自定义渲染和后期处理]]
- 下一页：[[05-URP 中的渲染图系统/00-URP 中的渲染图系统]]
