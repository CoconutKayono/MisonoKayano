# URP 的图形设置窗口参考

> 原文：[Graphics settings window reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-global-settings.html)

如果项目安装了通用渲染管线 (URP) 包，Unity 会在**项目设置 (Project Settings)** > **图形 (Graphics)** > **管线特定设置 (Pipeline Specific Settings)** > **URP** 中显示 URP 特定的图形设置。

本部分包含以下设置，可让您为 URP 定义整个项目的设置。

您也可以添加自己的设置。有关更多信息，请参阅可编程渲染管线 (SRP) 核心手册中的[添加自定义设置](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/manual/add-custom-graphics-settings)。

## 体积配置文件

使用此部分可为所有场景使用的默认体积分配和编辑[体积配置文件 (Volume Profile)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Volume-Profile.html)。有关更多信息，请参阅[了解体积 (Understand Volumes)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Volumes.html)。

| 属性 | 描述 |
| --- | --- |
| **Default Profile** | 设置全局默认体积所使用的[体积配置文件 (Volume Profile)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Volume-Profile.html)。无法将 **Default Profile** 设置为 **None**。 |

URP 会显示所有可能的[体积覆盖 (Volume Overrides)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/VolumeOverrides.html) 的全部属性。要编辑或覆盖这些属性，请使用[某质量等级的全局体积](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/set-up-a-volume.html#configure-the-global-volume-for-a-quality-level)或[创建一个体积](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/set-up-a-volume.html#add-a-volume)。

## 光照

| 属性 | 描述 |
| --- | --- |
| **Use Bicubic Lightmap Sampling** | 通过平滑锐利或锯齿状的边缘（尤其是阴影边缘）来提高光照贴图的视觉保真度。启用此属性可能会降低低端平台上的性能。 |
| **Probe Volume Disable Streaming Assets** | 启用后，URP 使用[流媒体资源](https://docs.unity3d.com/6000.7/Documentation/Manual/StreamingAssets.html)来优化[自适应探针体积 (Adaptive Probe Volumes)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/probevolumes.html)。如果使用与流媒体资源不兼容的资源包 (Asset Bundle) 和可寻址资源 (Addressables)，请禁用此设置。 |
| **Use Reflection Probe Rotation** | 当反射探针 (Reflection Probe) 未与世界坐标轴对齐时，改善反射效果。在低端平台上，此设置可能会降低性能。 |

## 其他着色器剥离设置

此部分中的复选框定义在构建 Player 时 Unity 会剥离哪些着色器变体。

| 属性 | 描述 |
| --- | --- |
| **Export Shader Variants** | 在构建项目时输出两个包含着色器编译信息的日志文件。有关更多信息，请参阅[减少 URP 中的着色器变体](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shader-stripping-landing.html)。 |
| **Shader Variant Log Level** | 选择在构建 Unity 项目时 Unity 保存到日志中的着色器变体信息。<br>选项：<br>• **Disabled**：Unity 不保存任何着色器变体信息。<br>• **Only SRP Shaders**：Unity 仅保存 URP 着色器的着色器变体信息。<br>• **All Shaders**：Unity 保存每种着色器类型的着色器变体信息。 |
| **Strip Runtime Debug Shaders** | 启用后，Unity 会在构建 Player 时剥离所有运行时调试着色器。这会缩短构建时间，但会阻止在 Player 构建中使用渲染调试器 (Rendering Debugger)。禁用后，除非在[Player 设置](https://docs.unity3d.com/6000.7/Documentation/Manual/class-PlayerSettings.html)中将 **Managed Code Variant** 设置为 **Debug** 或 **Checked**，否则 Unity 会剥离这些着色器。 |
| **Strip Unused Post Processing Variants** | 启用后，Unity 假定 Player 不会在运行时创建新的[体积配置文件 (Volume Profiles)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Volume-Profile.html)。基于这一假设，Unity 只保留现有[体积配置文件 (Volume Profiles)](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Volume-Profile.html) 使用的着色器变体，并剥离所有其他变体。即使项目中的场景不使用这些配置文件，Unity 仍会保留体积配置文件中使用的着色器变体。 |
| **Strip Unused Variants** | 启用后，Unity 会以更高效的方式执行着色器剥离。如果项目使用以下 URP 功能，此选项会将 Player 中的着色器变体数量减少为原来的一半：<br><br>• Rendering Layers<br>• Native Render Pass<br>• Reflection Probe Blending<br>• Reflection Probe Box Projection<br>• SSAO Renderer Feature<br>• Decal Renderer Feature<br>• 某些后期处理效果<br><br>仅当在 Player 中发现问题时才禁用此选项。 |
| **Strip 2D Unused Variants** | 启用后，Unity 会分析构建中包含的场景，只保留这些场景使用的 2D 光照着色器变体，然后剥离所有其他 2D 光照着色器变体。禁用后，Unity 会保留所有 2D 光照着色器变体。此设置默认处于禁用状态。 |
| **Strip Screen Coord Override Variants** | 启用后，Unity 会在 Player 构建中剥离屏幕坐标覆盖着色器变体。 |

## 渲染图系统

使用此部分可启用、禁用或配置渲染图系统。有关更多信息，请参阅[[00-URP 中的渲染图系统]]。

| 属性 | 描述 |
| --- | --- |
| **Enable Compilation Caching** | 启用后，URP 会尽可能使用前一帧编译的渲染图，而不是再次编译渲染图。这会加快渲染速度。 |
| **Enable Validity Checks** | 启用后，URP 会在编辑器中，以及在[Player 设置](https://docs.unity3d.com/6000.7/Documentation/Manual/class-PlayerSettings.html)中将 **Managed Code Variant** 设置为 **Debug** 或 **Checked** 的构建中验证渲染图的各个方面。当 **Managed Code Variant** 设置为 **Instrumented** 或 **Release** 时，**Enable Validity Checks** 在构建中不起作用。 |

## VRS - 运行时资源

使用此部分可配置可变速率着色 (Variable Rate Shading, VRS)。

| 属性 | 描述 |
| --- | --- |
| **Texture Compute Shader** | 设置计算着色器。在可变速率着色期间，[`ColorMaskTextureToShadingRateImage`](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.4/api/UnityEngine.Rendering.Vrs.html#UnityEngine_Rendering_Vrs_ColorMaskTextureToShadingRateImage_UnityEngine_Rendering_RenderGraphModule_RenderGraph_UnityEngine_Rendering_RTHandle_UnityEngine_Rendering_RTHandle_System_Boolean_) API 使用此计算着色器将颜色转换为着色速率值。默认值是内置的 `VrsTexture` 计算着色器。 |
| **Visualization Shader** | 设置着色器。在渲染调试器窗口等可视化界面中，[`ShadingRateImageToColorMaskTexture`](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.4/api/UnityEngine.Rendering.Vrs.html#UnityEngine_Rendering_Vrs_ShadingRateImageToColorMaskTexture_UnityEngine_Rendering_RenderGraphModule_RenderGraph_UnityEngine_Rendering_RenderGraphModule_TextureHandle__UnityEngine_Rendering_RenderGraphModule_TextureHandle__) API 使用此着色器将着色速率值转换为颜色。默认值是内置的 `VrsVisualization` 着色器。 |
| **Visualization Lookup Table** | 设置 **Visualization Shader** 用于将着色速率值转换为显示颜色的颜色映射。 |
| **Conversion Lookup Table** | 设置 **Texture Compute Shader** 用于将输入颜色映射到对应着色速率值的查找表。 |

---

## 文档导航

- 上一页：[[02-URP 的通用渲染器资源参考]]
- 目录：[[00-通用渲染管线参考]]
- 下一页：[[06-使用高清渲染管线资源]]
