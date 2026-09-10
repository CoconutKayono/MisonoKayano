# URP 的包示例参考

> 原文：[Package samples reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/package-sample-urp-package-samples.html)

URP 提供以下包示例：

- **URP Package Samples**：一组示例着色器、C# 脚本和其他资产，可用于构建或增强应用程序。
- **URP RenderGraph Samples**：一组使用渲染图系统的示例自定义渲染通道。

有关安装包示例的信息，请参阅 [[03-在 URP 中导入包示例]]。

## URP Package Samples

URP Package Samples 是 URP 的一个包示例，包含示例着色器、C# 脚本和其他资产，您可以在此基础上构建，借此学习功能，或直接在应用程序中使用。有关导入信息，请参阅 [[03-在 URP 中导入包示例]]。

每个示例都使用自己的 [[../../../08-通用渲染管线参考/01-URP 通用渲染管线资源参考]]。如果要构建示例场景，请将示例的 URP 资源添加到 Graphics 设置中；否则 Unity 可能会剥离示例使用的着色器或渲染通道。

### Camera Stacking

`URP Package Samples/CameraStacking` 文件夹包含 Camera Stacking 示例。

| 示例 | 描述 |
| --- | --- |
| **混合视野 (Mixed field of view)** | `CameraStacking/MixedFOV` 演示如何在第一人称应用程序中使用 Camera Stacking，防止角色装备物品裁剪进环境；环境 Camera 和装备物品 Camera 也可以使用不同视野。 |
| **分屏 (Split screen)** | `CameraStacking/SplitScreenPPUI` 演示如何创建分屏 Camera 设置，使每个屏幕都有自己的 Camera Stack；还演示如何对世界空间和屏幕空间 Camera UI 应用后期处理。 |
| **3D 天空盒 (3D skybox)** | `CameraStacking/3D Skybox` 使用 Camera Stacking 将微型环境变换为天空盒。叠加 Camera 渲染微型城市和行星，并绘制主 Camera 未绘制的像素；配合脚本转换后，微型环境会以全尺寸显示在主 Camera 视图背景中。 |

### Decals

`URP Package Samples/Decals` 文件夹包含贴花示例。

| 示例 | 描述 |
| --- | --- |
| **模糊阴影 (Blob shadows)** | `Decals/BlobShadow` 使用 Decal Projector 组件在角色下方投射阴影。此方法比阴影贴图消耗更少资源，适合低端设备。 |
| **油漆泼溅 (Paint splat)** | `Decals/PaintSplat` 使用 WorldSpaceUV Sub Graph 和 Simple Noise Shader Graph 节点创建程序化贴花；噪点使用 Decal Projector 组件的世界位置。 |
| **代理光照 (Proxy lighting)** | `Decals/ProxyLighting` 基于**模糊阴影**示例，并使用 Decal Projector 添加代理聚光灯，修改投影器体积内表面的发射。**注意**：为展示光照模拟范围，此示例禁用了正常实时光照。 |

### Lens Flares

`URP Package Samples/LensFlares` 文件夹包含镜头光晕示例。

| 示例 | 描述 |
| --- | --- |
| **太阳光晕 (Sun flare)** | `LensFlares/SunFlare` 演示如何使用 Lens Flare 组件为场景中的主方向光添加镜头光晕效果。 |
| **镜头光晕展厅 (Lens flare showroom)** | `LensFlares/LensFlareShowroom` 用于创作镜头光晕：在 Hierarchy 中选择 **Lens Flare** GameObject；在组件中将 LensFlareDataSRP 资产分配给 **Lens Flare Data**；更改组件和数据属性，并在 Game View 中查看。**注意**：若文本框挡住视线，请禁用场景中的 Canvas。 |

### Lighting

`URP Package Samples/Lighting` 文件夹包含光照示例。

| 示例 | 描述 |
| --- | --- |
| **反射探针 (Reflection probes)** | `Lighting/Reflection Probes` 使用反射探针为反射球体 GameObject 创建反射贴图，展示 **Probe Blending** 和 **Box Projection** 如何改变场景反射。 |

### Renderer Features

`URP Package Samples/RendererFeatures` 文件夹包含 [[../../../07-在 URP 中自定义渲染和后期处理/02-通过 URP 中的渲染器功能添加预构建效果/01-向 URP 渲染器添加渲染器功能]] 示例。

| 示例 | 描述 |
| --- | --- |
| **环境光遮蔽 (Ambient occlusion)** | `RendererFeatures/AmbientOcclusion` 使用 Renderer Feature 将屏幕空间环境光遮蔽 (SSAO) 添加到 URP；参考 `SSAO_Renderer` 资源了解设置。 |
| **故障效果 (Glitch effect)** | `RendererFeatures/GlitchEffect` 使用 Render Objects Render Feature 和 Scene Color Shader Graph 节点绘制带故障效果的 GameObject；参考 `Glitch_Renderer` 资源了解设置。 |
| **保留帧 (Keep frame)** | `RendererFeatures/KeepFrame` 使用自定义 Renderer Feature 在帧之间保留帧颜色，从简单粒子系统创建漩涡效果。**注意**：效果仅在 Play Mode 中可见。 |
| **遮挡效果 (Occlusion effect)** | `RendererFeatures/OcclusionEffect` 使用 Render Objects Renderer Feature 绘制被遮挡几何体；无需代码，`OcclusionEffect_Renderer` 资源已完成设置。 |
| **轨迹效果 (Trail effect)** | `RendererFeatures/TrailEffect` 在附加 Camera 上使用**保留帧**示例的 Renderer Feature 创建轨迹贴图；附加 Camera 将深度绘制到 RenderTexture，`Sand_Graph` 着色器采样贴图并移动地面顶点。 |

### Shaders

`URP Package Samples/Shaders` 文件夹包含着色器示例。

| 示例 | 描述 |
| --- | --- |
| **Lit** | `Shaders/Lit` 演示 Lit 着色器的不同属性如何影响几何体表面；其中的材质和纹理可作为在 URP 中设置材质的参考。 |

## URP RenderGraph Samples

安装 **Render Graph Samples** 后，`URPRenderGraphSamples` 文件夹包含使用渲染图系统的 Scriptable Renderer Features 示例。

使用示例：在 **Project** 窗口选择项目使用的 URP Renderer，在 **Inspector** 窗口选择 **Add Renderer Feature**，然后选择要使用的示例。有关更多信息，请参阅[向 URP Renderer 添加 Renderer Feature](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/intro-to-renderer-features.html)。使用 Render Graph Viewer 可视化渲染通道序列；部分示例仅用于 API 演示，不会在 Game 或 Scene 视图中产生可见输出，但可用 Frame Debugger 查看输出。

| 示例 | 描述 |
| --- | --- |
| **Blit** | 将活动颜色纹理复制到新纹理。 |
| **BlitWithFrameData** | 演示如何使用 frameData 和多个 ScriptableRenderPass 处理 Blit 操作。 |
| **BlitWithMaterial** | 将活动 CameraColor Blit 到新纹理；演示使用材质执行 Blit，并用 ResourceData 避免再 Blit 回活动颜色目标。此示例用于 API 演示。 |
| **Compute** | 展示如何将计算着色器与 RenderGraph 一起使用。 |
| **ComputeInOutRendererFeature** | 展示如何使用 RenderGraph 运行多个计算通道，并将第一个输出作为第二个输入。 |
| **Culling** | 使用剔除结果渲染与指定层关联的场景几何体，用于 API 演示。 |
| **FramebufferFetch** | 使用自定义材质和 framebuffer fetch 将上一通道目标复制到新纹理，用于 API 演示。 |
| **GBufferVisualization** | 在 GBuffer 组件不是全局组件时，在 RenderPass 中使用这些组件。 |
| **GlobalGBuffers** | 将 GBuffer 组件设置为全局变量（自身不渲染内容），使后续通道能够访问它们。 |
| **MRT** | 演示在 URP RenderGraph 中使用 Multiple Render Targets (MRT)，适用于通道需要写入超过 4 个数据通道的情况。 |
| **OutputTexture** | 使用 RenderGraph 输出特定纹理，演示按名称将纹理附加到材质，以及按正确顺序执行时合并两个渲染通道。 |
| **RendererList** | 清除当前活动颜色纹理，然后渲染与层遮罩关联的场景几何体。 |
| **TextureReferenceWithFrameData** | 在 frameData 中创建 TextureReference ContextItem，保存供后续通道使用的引用，避免额外 Blit 往返复制到 Camera 颜色附件。 |
| **UnsafePass** | 将活动颜色纹理复制到新纹理，然后将源纹理降采样两次，用于 API 演示。 |

---

## 文档导航

- 上一页：[[03-在 URP 中导入包示例]]
- 目录：[[00-创建 URP 项目]]
- 下一页：[[../02-从内置渲染管线升级到 URP/00-从内置渲染管线升级到 URP]]
