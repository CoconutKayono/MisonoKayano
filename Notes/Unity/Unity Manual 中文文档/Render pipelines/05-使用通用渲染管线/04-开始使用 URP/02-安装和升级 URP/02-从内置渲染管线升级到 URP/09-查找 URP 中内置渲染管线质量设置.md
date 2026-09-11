# 查找 URP 中内置渲染管线质量设置

> 原文：[Built-In Render Pipeline quality settings in URP reference](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/birp-onboarding/quality-settings-location.html)


URP 将其质量设置拆分到项目设置和 URP 资源中，以便在项目的质量级别中实现更好的通用性。因此，项目设置 (Project Settings) 的**质量 (Quality)** 部分中列出的部分内置渲染管线 (BiRP) 设置已移动或更改，或不再存在。

下表描述了内置渲染器在项目设置 (Project Settings) 的**质量 (Quality)** 部分中列出的所有设置，以及设置现位于 URP 中的位置。

## Rendering 部分

| **BiRP 设置** | **URP 设置** |
| --- | --- |
| **Render Pipeline Asset** | **项目设置 (Project Settings)** > **质量 (Quality)** > **渲染 (Rendering)** > **渲染管线资源 (Render Pipeline Asset)** |
| **Pixel Light Count** | 在 URP 中，每个对象的最大实时光源数量取决于所使用的渲染路径。有关更多信息，请参阅 [[01-URP 中渲染路径简介]]。<br><br>要设置每个对象的光源数量，请使用 **URP 资源 (URP Asset)** > **光照 (Lighting)** > **其他光源 (Additional Lights)** > **每像素 (Per Pixel)** > **每对象限制 (Per Object Limit)**。 |
| **Anti-aliasing** | URP 中有两种抗锯齿：在 URP 资源中控制多重采样抗锯齿 (MSAA)，以及根据每个摄像机控制其他抗锯齿类型。有关更多信息，请参阅 [[06-在通用渲染管线中添加抗锯齿]]。<br><br>控制 MSAA：**URP 资源 (URP Asset)** > **质量 (Quality)** > **抗锯齿 (Anti-aliasing (MSAA))**。<br><br>控制其他抗锯齿类型：**摄像机 (Camera)** > **渲染 (Rendering)** > **抗锯齿 (Anti-aliasing)**。 |
| **Realtime Reflection Probes** | **项目设置 (Project Settings)** > **质量 (Quality)** > **渲染 (Rendering)** > **实时反射探针 (Realtime Reflection Probes)** |
| **Resolution Scaling Fixed DPI Factor** | 此属性在 URP 中仍位于原位置。URP 还支持使用 Upscaler 处理 URP 资源中的分辨率缩放。<br><br>固定 DPI 因子：**项目设置 (Project Settings)** > **质量 (Quality)** > **渲染 (Rendering)** > **分辨率缩放固定 DPI 因子 (Resolution Scaling Fixed DPI Factor)**。<br><br>URP 资源中的分辨率缩放：**URP 资源 (URP Asset)** > **质量 (Quality)** > **渲染缩放 (Render Scale)** 和 **升级过滤器 (Upscaling Filter)**。 |
| **VSync Count** | **项目设置 (Project Settings)** > **质量 (Quality)** > **渲染 (Rendering)** > **垂直同步计数 (VSync Count)** |

## Textures 部分

| **BiRP 设置** | **URP 设置** |
| --- | --- |
| **Global Mipmap Limit** | **项目设置 (Project Settings)** > **质量 (Quality)** > **纹理 (Textures)** > **全局 Mipmap 限制 (Global Mipmap Limit)** |
| **Anisotropic Textures** | **项目设置 (Project Settings)** > **质量 (Quality)** > **纹理 (Textures)** > **各向异性纹理 (Anisotropic Textures)** |
| **Mipmap Streaming** | **项目设置 (Project Settings)** > **质量 (Quality)** > **纹理 (Textures)** > **Mipmap Streaming** |

## Particles 部分

| **BiRP 设置** | **URP 设置** |
| --- | --- |
| **Soft Particles** | 要启用软粒子，请在相关粒子着色器中使用着色器关键字 `_SOFTPARTICLES_ON`。 |
| **Particle Raycast Budget** | **项目设置 (Project Settings)** > **质量 (Quality)** > **粒子 (Particles)** > **粒子射线投射预算 (Particle Raycast Budget)** |

## Terrain 部分

| **BiRP 设置** | **URP 设置** |
| --- | --- |
| **Billboards Face Camera Position** | **项目设置 (Project Settings)** > **质量 (Quality)** > **地形 (Terrain)** > **Billboards 正面摄像机位置 (Billboards Face Camera Position)** |
| **Use Legacy Details Distribution** | **项目设置 (Project Settings)** > **质量 (Quality)** > **地形 (Terrain)** > **使用旧版详细信息分布 (Use Legacy Details Distribution)** |

## Shadows 部分

| **BiRP 设置** | **URP 设置** |
| --- | --- |
| **Shadowmask Mode** | **项目设置 (Project Settings)** > **质量 (Quality)** > **阴影 (Shadows)** > **阴影遮罩模式 (Shadowmask Mode)** |
| **Shadows** | 在 URP 中，可以分别启用场景主光源和其他光源的阴影。主光源：**URP 资源 (URP Asset)** > **光照 (Lighting)** > **主光源 (Main Light)** > **投射阴影 (Cast Shadows)**。其他光源：**URP 资源 (URP Asset)** > **光照 (Lighting)** > **其他光源 (Additional Lights)** > **投射阴影 (Cast Shadows)**。<br><br>启用阴影后不再选择阴影类型。要使用柔和阴影，请启用 **URP 资源 (URP Asset)** > **阴影 (Shadows)** > **柔和阴影 (Soft Shadows)**，然后选择适当的质量级别。 |
| **Shadow Resolution** | 可以为主光源和其他光源分别设置阴影分辨率。其他光源使用具有 Low、Medium 和 High 三个层级的阴影图集。<br><br>主光源：**URP 资源 (URP Asset)** > **光照 (Lighting)** > **主光源 (Main Light)** > **阴影分辨率 (Shadow Resolution)**。<br><br>其他光源：**URP 资源 (URP Asset)** > **光照 (Lighting)** > **其他光源 (Additional Lights)** > **阴影图集分辨率 (Shadow Atlas Resolution)** 和 **阴影分辨率层级 (Shadow Resolution Tiers)**。 |
| **Shadow Projection** | URP 仅支持 Stable Fit Shadow Projection。 |
| **Shadow Distance** | **URP 资源 (URP Asset)** > **阴影 (Shadows)** > **最大距离 (Max Distance)** |
| **Shadow Near Plane Offset** | 没有等效设置，因为 URP 的阴影系统不使用此属性。 |
| **Shadow Cascades** | **URP 资源 (URP Asset)** > **阴影 (Shadows)** > **级联数量 (Cascade Count)** |
| **Cascade Splits** | 阴影级联拆分由基于级联数量的动态属性控制。URP 资源在拆分值下方以多段条形图呈现级联拆分，每个分段表示给定拆分的大小。<br><br>使用 **URP 资源 (URP Asset)** > **阴影 (Shadows)** > **级联数量 (Cascade Count)** > **拆分 1 (Split 1)**、**拆分 2 (Split 2)**、**拆分 3 (Split 3)** 和 **最后边框 (Last Border)** 控制大小。 |

## Async Asset Upload 部分

| **BiRP 设置** | **URP 设置** |
| --- | --- |
| **Time Slice** | **项目设置 (Project Settings)** > **质量 (Quality)** > **异步资源上传 (Async Asset Upload)** > **时间片 (Time Slice)** |
| **Buffer Size** | **项目设置 (Project Settings)** > **质量 (Quality)** > **异步资源上传 (Async Asset Upload)** > **缓冲区大小 (Buffer Size)** |
| **Persistent Buffer** | **项目设置 (Project Settings)** > **质量 (Quality)** > **异步资源上传 (Async Asset Upload)** > **持久缓冲区 (Persistent Buffer)** |

## Level of Detail 部分

| **BiRP 设置** | **URP 设置** |
| --- | --- |
| **LOD Group Bias** | **项目设置 (Project Settings)** > **质量 (Quality)** > **细节级别 (Level of Detail)** > **LOD Group Bias** |
| **Maximum LOD Group Level** | **项目设置 (Project Settings)** > **质量 (Quality)** > **细节级别 (Level of Detail)** > **Maximum LOD Group Level** |
| **LOD Cross Fade** | **URP 资源 (URP Asset)** > **质量 (Quality)** > **LOD 交叉淡化 (LOD Cross Fade)**。<br><br>**注意**：URP 为 LOD Cross Fade 提供 Bayer、Blue Noise 和 2x2 Stencil 三个选项；这些选项都不同于内置渲染管线使用的 Dither。 |

## Meshes 部分

| **BiRP 设置** | **URP 设置** |
| --- | --- |
| **Skin Weights** | **项目设置 (Project Settings)** > **质量 (Quality)** > **网格 (Meshes)** > **蒙皮权重 (Skin Weights)** |

## 其他资源

- [[05-将质量设置从内置渲染管线转换到 URP。]]
- [[01-URP 通用渲染管线资源参考]]
- [URP 中的阴影](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Shadows-in-URP.html)

---

## 文档导航

- 上一页：[[08-使用渲染管线转换器将着色器转换为 URP]]
- 目录：[[00-从内置渲染管线升级到 URP]]
- 下一页：[[00-从 HDRP 迁移到 URP]]
