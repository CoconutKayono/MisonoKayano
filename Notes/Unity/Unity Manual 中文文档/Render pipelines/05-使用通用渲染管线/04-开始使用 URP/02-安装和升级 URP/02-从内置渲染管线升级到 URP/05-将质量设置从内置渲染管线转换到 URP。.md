# 将质量设置从内置渲染管线转换到 URP。

> 原文：[Match the quality level performance of the Built-In Render Pipeline in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/birp-onboarding/quality-presets.html)


本页面提供了 **Low** 和 **High** 质量级别的推荐 URP 图形[质量级别](https://docs.unity3d.com/6000.7/Documentation/Manual/class-QualitySettings.html)设置。这些设置与内置渲染管线中等效默认预设的性能大致匹配。

URP 会更改许多功能和设置的实现，因此它们对性能的影响通常与内置渲染管线等效方案不同。将项目从内置渲染管线升级为 URP 时，现有质量级别可能会提供不同的性能级别，因此可能需要为项目更新或创建新的质量级别。您可以使用此页面上的值作为起点。

本页面分为两个部分：

- 项目设置中的质量设置。
- URP 资源中的质量设置。

> **注意**：在 URP 中，许多质量级别设置已从 Project Settings 窗口移到 URP 资源。有关在 URP 项目中何处可以找到这些设置的更多信息，请参阅[[09-查找 URP 中内置渲染管线质量设置]]。

## 项目设置

您可以在**项目设置 (Project Settings)** > **质量 (Quality)** 中更改以下设置。

| 设置 | “Low”预设值 | “High”预设值 |
| --- | --- | --- |
| **渲染 (Rendering)** |  |  |
| Real-time Reflection Probes | 否 | 是 |
| Resolution Scaling Fixed DPI Factor | 1 | 1 |
| VSync Count | 不同步 | 每个 V 空白 |
| **纹理 (Textures)** |  |  |
| Global Mipmap Limit | 半分辨率 | 全分辨率 |
| Anisotropic Textures | 禁用 | 禁用 |
| Texture Streaming | 否 | 否 |
| **粒子 (Particles)** |  |  |
| Particle Raycast Budget | 16 | 256 |
| **地形 (Terrain)** |  |  |
| Billboards Face Camera Position | 否 | 是 |
| **阴影 (Shadows)** |  |  |
| Shadowmask Mode | 阴影遮罩 | 距离阴影遮罩 |
| **异步资源上传 (Async Asset Upload)** |  |  |
| Time Slice | 2 | 2 |
| Buffer Size | 16 | 16 |
| Persistent Buffer | 是 | 是 |
| **细节级别 (Level of Detail)** |  |  |
| LOD Bias | 0.4 | 1 |
| Maximum LOD level | 0 | 0 |
| **网格 (Meshes)** |  |  |
| Skin Weights | 4 块骨骼 | 无限制 |

## URP 资源

您可以在任何 [[01-URP 通用渲染管线资源参考]]中更改以下设置。

| **设置** | **“Low”预设值** | **“High”预设值** |
| --- | --- | --- |
| **Rendering** |  |  |
|  |  |  |
| Depth Texture | 否 | 否 |
| Opaque Texture | 否 | 否 |
| Terrain Holes | 是 | 是 |
| **Quality** |  |  |
|  |  |  |
| HDR | 是 | 是 |
| Anti Aliasing (MSAA) | 禁用 | 2x |
| Render Scale | 1 | 1 |
| **Lighting** |  |  |
|  |  |  |
| Main Light | 每像素 | 每像素 |
| Cast Shadows | 否 | 是 |
| Shadows Resolution | 不适用 | 2048 |
| Additional Lights | 禁用 | 每像素 |
| Per Object Limit | 不适用 | 4 |
| Cast Shadows | 不适用 | 是 |
| Shadow Atlas Resolution | 不适用 | 2048 |
| Shadow Resolution Tiers | 不适用 |  |
| Low | 不适用 | 512 |
| Medium | 不适用 | 1024 |
| High | 不适用 | 2048 |
| Cookie Atlas Resolution | 不适用 | 2048 |
| Cookie Atlas Format | 不适用 | 高彩色 |
| Reflection Probes |  |  |
|  |  |  |
| Probe Blending | 否 | 是 |
| Box Projection | 否 | 否 |
| **Shadows** |  |  |
|  |  |  |
| Max Distance | 不适用 | 50 |
| Cascade Count | 不适用 | 3 |
| Split 1 | 不适用 | 12.5 |
| Split 2 | 不适用 | 33.8 |
| Last Border | 不适用 | 3.8 |
| Working Unit | 不适用 | 指标 |
| Depth Bias | 不适用 | 1 |
| Normal Bias | 不适用 | 1 |
| Soft Shadows | 不适用 | 是 |
| **Post-processing** |  |  |
|  |  |  |
| Grading Mode | 低动态范围 | 低动态范围 |
| LUT Size | 16 | 32 |
| Fast sRGB/Linear Conversion | 否 | 否 |

## 其他资源

- [[09-查找 URP 中内置渲染管线质量设置]]
- [[01-URP 通用渲染管线资源参考]]

---

## 文档导航

- 上一页：[[04-升级自定义着色器以实现 URP 兼容性]]
- 目录：[[00-从内置渲染管线升级到 URP]]
- 下一页：[[06-使用渲染管线转换器转换资源]]
