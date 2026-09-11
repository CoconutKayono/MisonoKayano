# URP 中的 HDRP 质量设置参考

> 原文：[HDRP quality settings in URP reference](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/hdrp-quality-settings-urp-reference.html)

下表列出 High Definition Render Pipeline（HDRP）项目 **Project Settings > Quality** 部分中的设置，以及 Universal Render Pipeline（URP）中位置相似的设置。

> [!NOTE]
> 并非所有 HDRP 质量设置在 URP 中都有对应项。有关 URP 设置，请参阅 [[01-URP 通用渲染管线资源参考]] 和 [[02-URP 的通用渲染器资源参考]]。

| HDRP 设置 | URP 设置 |
| --- | --- |
| **Rendering > Color Buffer Format** | URP asset > **Quality > HDR Precision** |
| **Rendering > Lit Shader Mode** | Universal Renderer asset > **Rendering > Rendering Path** |
| **Rendering > Terrain Holes** | URP asset > **Rendering > Terrain Holes** |
| **Rendering > GPU Resident Drawer** | URP asset > **Rendering > GPU Resident Drawer** |
| **Rendering > Decals** | Universal Renderer asset > **Renderer Features > Decal Render Feature** |
| **Rendering > Dynamic Resolution** | URP asset > **Quality > Render Scale**、**Camera > Output > Dynamic Resolution**，以及 URP asset > **Quality > Upscaling Filter**。请参阅 [Dynamic resolution](https://docs.unity3d.com/6000.7/Documentation/Manual/DynamicResolution-landing.html)。 |
| **Lighting > Screen Space Ambient Occlusion** | Universal Renderer asset > **Renderer Features > Screen Space Ambient Occlusion Render Feature** |
| **Lighting > Light Layers** | URP asset > **Lighting > Use Rendering Layers** |
| **Lighting > Light Probe Lighting** | URP asset > **Lighting > Light Probe System** |
| **Lighting > Cookies** | URP asset > **Lighting > Additional Lights > Cookie Atlas Resolution**，以及 **Cookie Atlas Format** |
| **Lighting > Reflections** | URP asset > **Lighting > Reflection Probes** |
| **Lighting > Shadows** | URP asset > **Lighting > Additional Lights**，以及 URP asset > **Shadows** |
| **Post Processing** | URP asset > **Post Processing** |
| **Volumes** | URP asset > **Volumes** |

## 其他资源

- [[01-URP 通用渲染管线资源参考]]
- [[01-从 HDRP 迁移到 URP 的工作流]]

---

## 文档导航

- 上一页：[[05-将 HDRP 光照转换为 URP]]
- 目录：[[00-安装和升级 URP]]
- 下一页：无
