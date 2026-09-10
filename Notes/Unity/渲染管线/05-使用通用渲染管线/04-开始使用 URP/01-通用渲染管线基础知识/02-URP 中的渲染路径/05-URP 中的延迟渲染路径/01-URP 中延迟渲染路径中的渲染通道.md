# URP 中延迟渲染路径中的渲染通道

> 原文：[Render passes in the Deferred and Deferred+ rendering paths in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/render-passes-deferred.html)


下表列出了延迟渲染路径使用的渲染通道。

| **渲染事件** | **渲染事件后发生的渲染通道** | **描述** |
| --- | --- | --- |
| **BeforeRendering** | - | - |
| **BeforeRenderingShadows** | - | - |
| **AfterRenderingShadows** | - | - |
| **BeforeRenderingPrePasses** | **DepthPrepass** 或 **DepthPrepass** 和 **DepthNormalPrepass**。 | Unity 在前向通道中渲染的材质在预通道中渲染深度和法线纹理。 |
| **AfterRenderingPrePasses** | - | - |
| **BeforeRenderingGbuffer** | **GBufferPass** | 渲染 G 缓冲区，然后复制 G 缓冲区深度纹理。 |
| **AfterRenderingGbuffer** | **SSAO** | 计算屏幕空间环境光遮挡 (SSAO) 纹理。仅当您[启用 SSAO](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing-ssao.html) 并禁用 **After Opaque** 时，Unity 才会在此处计算。 |
| **BeforeRenderingDeferredLights** | **延迟通道** | 延迟渲染。Unity 在此渲染通道期间使用 SSAO 纹理（如果已创建）。 |
| **AfterRenderingDeferredLights** | - | - |
| **BeforeRenderingOpaques** | - | 渲染不透明仅前向材质。 |
| **AfterRenderingOpaques** | - | 计算和混合屏幕空间环境光遮挡 (SSAO) 纹理。仅当您[启用 SSAO](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing-ssao.html) 并启用 **After Opaque** 时，Unity 才会在此处计算此属性。 |
| **BeforeRenderingSkybox** | - | - |
| **AfterRenderingSkybox** | - | - |
| **BeforeRenderingTransparents** | - | - |
| **AfterRenderingTransparents** | - | - |
| **BeforeRenderingPostProcessing** | - | - |
| **AfterRenderingPostProcessing** | - | - |
| **AfterRendering** | - | - |

有关渲染事件的完整列表以及自定义渲染通道的注入点，请参阅 [[../../../../07-在 URP 中自定义渲染和后期处理/06-在 URP 中将可编程渲染通道添加到帧渲染循环/04-URP 的注入点参考]]。

## 源代码参考

下表列出了位于 `com.unity.render-pipelines.universal` 文件夹中的文件，其中包含与延迟渲染路径相关的代码。

| **文件路径** | **描述** |
| --- | --- |
| `Runtime\DeferredLights.cs` | 处理延迟渲染路径的主类。 |
| `Runtime\Passes\GBufferPass.cs` | G 缓冲区通道的 `ScriptableRenderPass`。 |
| `Runtime\Passes\DeferredPass.cs` | 延迟着色通道的 `ScriptableRenderPass`。 |
| `Shaders\Utils\Deferred.hlsl` | 用于延迟着色的实用程序函数。 |
| `Shaders\Utils\StencilDeferred.shader` | 用于延迟着色的着色器资源。 |
| `Shaders\Utils\UnityGBuffer.hlsl` | 用于存储和从 G 缓冲区加载材质属性的实用程序函数。 |

## 其他资源

- [[../../../../07-在 URP 中自定义渲染和后期处理/00-在 URP 中自定义渲染和后期处理]]

---

## 文档导航

- 上一页：[[00-URP 中的延迟渲染路径]]
- 目录：[[00-URP 中的延迟渲染路径]]
- 下一页：[[02-URP 中延迟渲染路径中的 G 缓冲区布局]]
