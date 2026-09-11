# URP 通用渲染管线资源参考

> 原文：[Universal Render Pipeline asset reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/universalrp-asset.html)

在 URP 资源中，可以配置以下设置：

- **Rendering**
- **Quality**
- **Lighting**
- **Shadows**
- **Post-processing**
- **Volumes**
- **Adaptive Performance**

**注意：**如果启用了实验性 2D 渲染器（菜单：**图形设置 (Graphics Settings)** > 在**可编写脚本的渲染管线设置 (Scriptable Render Pipeline Settings)** 下添加 2D 渲染器资源），URP 资源中与 3D 渲染相关的一些选项不会影响最终应用程序或游戏。

### Rendering

**Rendering** 设置控制渲染管线帧的核心部分。

| 属性 | 描述 |
| --- | --- |
| **Depth Texture** | 启用 URP 创建 `_CameraDepthTexture`。然后，URP 默认会将此[深度纹理](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-DepthTextures.html)用于场景中的所有 Camera。您可以在[[01-Camera Inspector窗口参考]]中为单个 Camera 覆盖此设置。<br><br>**注意**：如果启用[On-Tile Validation](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html#rendering)，Unity 会禁用此选项。 |
| **Opaque Texture** | 启用此选项，为场景中的所有 Camera 默认创建 `_CameraOpaqueTexture`。其工作方式类似于内置渲染管线中的 [GrabPass](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-GrabPass.html)。<br><br>**Opaque Texture** 会在 URP 渲染透明网格之前立即提供场景快照。您可以在透明 Shader 中使用它来创建毛玻璃、水折射或热浪等效果。您可以在[[01-Camera Inspector窗口参考]]中为单个 Camera 覆盖此设置。<br><br>**注意**：如果启用[On-Tile Validation](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html#rendering)，Unity 会禁用此选项。 |
| **Opaque Downsampling** | 将不透明纹理的采样模式设置为以下选项之一：<br>**None**：以与 Camera 相同的分辨率生成不透明通道的副本。<br>**2x Bilinear**：使用双线性过滤生成半分辨率图像。<br>**4x Box**：使用盒式过滤生成四分之一分辨率图像，从而产生柔和的模糊副本。<br>**4x Bilinear**：使用双线性过滤生成四分之一分辨率图像。 |
| **Terrain Holes** | 如果禁用此选项，URP 会在为 Unity Player 构建时移除所有 Terrain hole Shader 变体，从而缩短构建时间。 |
| **GPU Resident Drawer** | GPU Resident Drawer 会自动使用 [BatchRendererGroup](https://docs.unity3d.com/6000.7/Documentation/Manual/batch-renderer-group.html) API，通过 GPU 实例化绘制 GameObject。更多信息请参阅[使用 GPU Resident Drawer](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/gpu-resident-drawer.html)。<br><br>可用选项：<br>**Disabled**：Unity 不会自动使用 GPU 实例化绘制 GameObject。<br>**Instanced Drawing**：Unity 会自动使用 GPU 实例化绘制 GameObject。 |
| **Small-Mesh Screen-Percentage** | 设置 Unity 用于剔除小型 GameObject 的屏幕百分比，以加快渲染。Unity 会剔除占据屏幕比例小于此值的 GameObject。<br><br>如果使用自己的[细节级别 (LOD) 网格](https://docs.unity3d.com/6000.7/Documentation/Manual/LevelOfDetail.html)，此设置可能不起作用。<br><br>将值设置为 0 可停止 Unity 剔除小型 GameObject。<br><br>若要防止 Unity 剔除某个占据屏幕空间小于此值的 GameObject，请打开该 GameObject 的**检视面板 (Inspector)**窗口并添加 **Disallow Small Mesh Culling** 组件。 |
| **GPU Occlusion Culling** | 启用后，当 GameObject 被其他 GameObject 遮挡时，Unity 使用 GPU 而不是 CPU 将其排除在渲染之外。更多信息请参阅[[10-URP中的GPU遮挡剔除]]。<br><br>**注意**：如果启用[On-Tile Validation](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html#rendering)，Unity 会禁用此选项。 |
| **SRP Batcher** | 只有打开**更多 (⋮)**菜单并选择**显示所有高级属性 (Show All Advanced Properties)**后，此属性才可用。<br><br>启用 SRP Batcher。当许多不同材质使用同一个 Shader 时，此选项很有用。SRP Batcher 是一个可以加速 CPU 渲染而不影响 GPU 性能的内部循环。使用 SRP Batcher 时，它会替代 SRP 渲染代码的内部循环。<br><br>**注意**：如果项目中的资源或 Shader 未针对 SRP Batcher 优化，则在低性能设备上，禁用 SRP Batcher 可能会获得更好的性能。 |
| **Debug Level** | 设置渲染管线生成的调试信息级别。<br><br>可用选项：<br>**Disabled**：禁用调试。这是默认值。<br>**Profiling**：使渲染管线提供详细信息标签，可在 FrameDebugger 中找到这些标签。 |
| **Shader Variant Log Level** | 设置 Unity 完成构建时要显示的 Shader Stripping 和 Shader Variant 信息级别。<br><br>可用选项：<br>**Disabled**：Unity 不记录任何内容。<br>**Only Universal**：Unity 记录所有 [URP Shader](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shaders-in-universalrp.html) 的信息。<br>**All**：Unity 记录构建中所有 Shader 的信息。<br><br>构建完成后，可以在 Console 面板中检查这些信息。 |
| **Store Actions** | 只有打开**更多 (⋮)**菜单并选择**显示所有高级属性 (Show All Advanced Properties)**后，此属性才可用。<br><br>定义 Unity 丢弃还是存储 DrawObjects Pass 的渲染目标。<br><br>可用选项：<br>**Auto**：Unity 默认使用 **Discard**，检测到任何注入的 Pass 时则回退到 **Store**。<br>**Discard**：Unity 丢弃之后不会再次使用的渲染 Pass 的渲染目标，从而降低内存带宽。<br>**Store**：Unity 存储每个 Pass 的所有渲染目标。在移动设备和基于区块的 GPU 上，**Store** 会显著增加内存带宽。 |

### Quality

这些设置控制 URP 的质量等级。您可以在此降低低端硬件上的性能开销，或改善高端硬件上的图形效果。

**提示：**如果要为不同硬件使用不同设置，可以在多个通用渲染管线资源中配置这些设置，然后根据需要切换资源。

| 属性 | 子属性 | 描述 |
| --- | --- | --- |
| **HDR** | — | 启用后，默认允许场景中的每个 Camera 使用高动态范围 (HDR) 渲染。使用 HDR 时，图像最亮部分的值可以大于 1。<br><br>这会提供更宽的光强范围，使光照更逼真，例如即使有明亮光源，也能分辨细节并减少饱和度。如果需要宽范围光照或使用[泛光](https://docs.unity3d.com/6000.7/Documentation/Manual/PostProcessing-Bloom.html)效果，此选项很有用。<br><br>如果目标是低端硬件，可以禁用此选项以跳过 HDR 计算并提升性能。您可以在 Camera Inspector 中为单个 Camera 覆盖此设置。<br><br>**注意**：如果启用[On-Tile Validation](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html#rendering)，Unity 会禁用此选项。 |
| — | **HDR Precision** | 只有打开**更多 (⋮)**菜单并选择**显示所有高级属性 (Show All Advanced Properties)**后，此属性才可用。<br><br>HDR 渲染中 Camera 颜色缓冲区的精度。64 位精度可以避免条带伪影，但需要更高的带宽，并且可能使采样变慢。默认值为 32 位。 |
| **Anti Aliasing (MSAA)** | — | 渲染时默认对场景中的每个 Camera 使用[多重采样抗锯齿](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/anti-aliasing.html#msaa)。这会柔化几何体边缘，使其不会出现锯齿或闪烁。在下拉菜单中选择每像素采样数：**2x**、**4x** 或 **8x**。采样数越多，对象边缘越平滑。<br><br>如果想跳过 MSAA 计算，或 2D 游戏不需要此类计算，请选择 **Disabled**。您可以在 Camera Inspector 中为单个 Camera 覆盖此设置。<br><br>**注意**：在不支持 [StoreAndResolve](https://docs.unity3d.com/ScriptReference/Rendering.RenderBufferStoreAction.StoreAndResolve.html) 存储操作的移动平台上，如果在 URP 资源中选择 **Opaque Texture**，Unity 会在运行时忽略 **Anti Aliasing (MSAA)** 属性，就像该属性设置为 **Disabled** 一样。<br><br>**注意**：如果启用[On-Tile Validation](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html#rendering)，Unity 会禁用此选项。 |
| **Render Scale** | — | 此滑动条缩放渲染目标分辨率，而不是当前设备的分辨率。需要出于性能原因以较低分辨率渲染，或需要放大渲染以改善质量时，可以使用此属性。<br><br>**注意**：此属性只缩放游戏渲染，UI 渲染仍使用设备的原生分辨率。<br><br>**注意**：在某些平台上，如果启用[On-Tile Validation](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html#rendering)，Unity 会禁用此选项。 |
| **Upscaling Filter** | — | 选择 Unity 执行放大时使用的图像滤镜。Render Scale 值小于 1.0 时，Unity 会执行放大。<br><br>**注意**：如果启用[On-Tile Validation](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html#rendering)，Unity 会禁用此选项。 |
| — | **Automatic** | Unity 根据 Render Scale 值和当前屏幕分辨率选择一种过滤选项。如果可以进行整数缩放，Unity 选择 **Nearest-Neighbor**；否则选择 **Bilinear**。 |
| — | **Bilinear** | Unity 使用图形 API 提供的双线性或线性过滤。 |
| — | **Nearest-Neighbor** | Unity 使用图形 API 提供的最近邻或点采样过滤。<br><br>**注意**：启用 **Post-processing** 时，**Nearest-Neighbour** 滤镜不起作用。 |
| — | **FidelityFX Super Resolution 1.0** | Unity 使用 AMD FidelityFX Super Resolution 1.0 (FSR) 技术执行放大。<br><br>与大多数其他 Upscaling Filter 选项不同，此滤镜在 Render Scale 值为 1.0 时仍保持启用。即使没有发生缩放，此滤镜也可以改善图像质量；在启用动态分辨率缩放时，还可以减弱 0.99 与 1.0 缩放值之间的过渡。<br><br>**注意**：此滤镜仅支持 Unity Shader Model 4.5 或更高版本的设备。在不支持 Unity Shader Model 4.5 的设备上，Unity 改用 **Automatic**。 |
| — | **Override FSR Sharpness** | 选择 FSR 滤镜时，Unity 会显示此复选框。选中后，可以指定 FSR 锐化 Pass 的强度。 |
| — | **FSR Sharpness** | 指定 FSR 锐化 Pass 的强度。值为 0.0 时不锐化，值为 1.0 时锐度最大。<br><br>**注意**：FSR 不是当前活动的放大滤镜时，此选项不起作用。 |
| — | **Spatial-Temporal Post-Processing (STP) 1.0** | 使用 Spatial Temporal Post-Processing (STP) 技术执行放大。选择此选项会强制将[[01-STP Upscaler简介]]中的 **Anti-Aliasing** 设置为 **Temporal Anti-aliasing (TAA)**。<br><br>即使没有缩放，此设置也能改善图像质量，因此 Render Scale 为 1.0 时仍保持启用。<br><br>**注意**：此设置仅支持支持计算着色器的非 GLES 设备。在不支持的设备上，Unity 使用 **Automatic**。 |
| **LOD Cross Fade** | — | 使用此属性启用或禁用 LOD 交叉淡化。禁用后，URP 会在构建 Unity Player 时移除所有 LOD 交叉淡化 Shader 变体，从而缩短构建时间。 |
| **LOD Cross Fade Dithering Type** | — | 当 [LOD 组](https://docs.unity3d.com/6000.7/Documentation/Manual/class-LODGroup.html)的 **Fade Mode** 设置为 **Cross Fade** 时，Unity 使用 Alpha 测试或模板测试渲染 Renderer 的 LOD 网格，并在它们之间进行交叉淡化。此属性定义 LOD 交叉淡化的抖动模式。<br><br>可用选项：<br>**Bayer Matrix**：性能优于 **Blue Noise**，但具有重复图案。<br>**Blue Noise**：使用预计算的蓝噪声纹理，外观优于 **Bayer Matrix**，但性能开销略高。<br>**2x2 Stencil**：Unity 使用模板缓冲区中的第 4 位和第 8 位应用 2 × 2 抖动模式，而不是 Alpha 测试。此设置会显著减少 Shader 变体数量。更多信息请参阅[减少 URP 中的 Shader 变体](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shader-stripping-landing.html)。 |

### Lighting

这些设置会影响场景中的光源。

如果禁用其中某些设置，相关[关键字](https://docs.unity3d.com/6000.7/Documentation/Manual/shader-keywords)会从[Shader 变量中剥离](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shader-stripping-landing.html)。如果确定游戏或应用不会使用某些设置，可以禁用它们来提升性能并缩短构建时间。

| 属性 | 子属性 | 描述 |
| --- | --- | --- |
| **Main Light** | — | 这些设置会影响场景中的主[方向光](https://docs.unity3d.com/6000.7/Documentation/Manual/Lighting.html)。您可以在 Lighting Inspector 中将某个光源指定为 Sun Source，从而选择它作为主光源。如果没有指定 Sun Source，URP 会将场景中最亮的方向光视为主光源。<br><br>您可以在 [Pixel Lighting](https://docs.unity3d.com/6000.7/Documentation/Manual/LightPerformance.html) 与 **None** 之间选择。如果选择 **None**，即使设置了 Sun Source，URP 也不会渲染主光源。 |
| — | **Cast Shadows** | 选中此复选框，使主光源在场景中投射阴影。 |
| — | **Shadow Resolution** | 控制主光源阴影贴图的纹理大小。高分辨率可以提供更清晰、更详细的阴影。如果内存或渲染时间有限，请尝试降低分辨率。 |
| **Light Probe System** | — | 选择此 URP 资源使用的光照探针系统。<br><br>可用选项：<br>**Light Probe Groups (Legacy)**：使用与内置渲染管线相同的[光照探针组系统](https://docs.unity3d.com/6000.7/Documentation/Manual/class-LightProbeGroup.html)。<br>**Adaptive Probe Volumes**：使用 [Adaptive Probe Volumes](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/probevolumes.html)。 |
| **Memory Budget** | — | 限制存储烘焙全局光照数据的纹理宽度和高度，这决定 Unity 为存储烘焙 Adaptive Probe Volume 数据预留的内存量。这些纹理具有固定深度。<br><br>可用选项：**Memory Budget Low**、**Memory Budget Medium**、**Memory Budget High**。 |
| **SH Bands** | — | 确定 Unity 用于存储探针数据的[球谐函数 (SH) 频段](https://docs.unity3d.com/6000.7/Documentation/Manual/LightProbes-TechnicalInformation.html)。L2 提供更精确的结果，但需要更多系统资源。<br><br>可用选项：**Spherical Harmonics L1**、**Spherical Harmonics L2**。 |
| **Enable Streaming** | — | 启用后，在运行时将 Adaptive Probe Volume 数据从 CPU 内存流式传输到 GPU 内存。更多信息请参阅[优化 Adaptive Probe Volume 数据的加载](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/probevolumes-streaming.html)。 |
| **Estimated GPU Memory Cost** | — | 指示项目中 Adaptive Probe Volumes 使用的纹理数据量。 |
| **Additional Lights** | — | 在此选择用于补充主光源的附加光源。可以选择 [Per Vertex](https://docs.unity3d.com/6000.7/Documentation/Manual/LightPerformance.html)、[Per Pixel](https://docs.unity3d.com/6000.7/Documentation/Manual/LightPerformance.html) 或 **Disabled**。 |
| — | **Per Object Limit** | 设置每个 GameObject 可受影响的附加光源数量上限。如果选择 Forward+ 渲染路径，Unity 会忽略此设置。 |
| — | **Cast Shadows** | 选中此复选框，使附加光源在场景中投射阴影。 |
| — | **Shadow Atlas Resolution** | 控制附加光源投射定向阴影的纹理大小。这是一个最多可容纳 16 张阴影贴图的 Sprite Atlas。高分辨率可以提供更清晰、更详细的阴影。如果内存或渲染时间有限，请尝试降低分辨率。 |
| — | **Shadow Resolution Tiers** | 设置附加光源在不同层级投射的阴影分辨率。分辨率必须为 128 或更大，并会四舍五入到下一个 2 的幂。<br><br>**注意**：仅当为 Additional Lights 启用 **Cast Shadows** 属性时，此属性才可见。 |
| — | **Cookie Atlas Resolution** | 附加光源使用的 Cookie Atlas 大小。所有附加光源都会打包到单个 Cookie Atlas 中。<br><br>仅当启用 **Light Cookies** 属性时，此属性才可见。 |
| — | **Cookie Atlas Format** | 附加光源 Cookie Atlas 的格式。所有附加光源都会打包到单个 Cookie Atlas 中。<br><br>可用选项：**Grayscale Low**、**Grayscale High**、**Color Low**、**Color High**、**Color HDR**。<br><br>仅当启用 **Light Cookies** 属性时，此属性才可见。 |
| **Reflection Probes** | — | 使用这些属性控制反射探针设置。 |
| — | **Probe Blending** | 平滑反射探针之间的过渡。更多信息请参阅[反射探针混合](https://docs.unity3d.com/6000.7/Documentation/Manual/blend-reflection-probes-birp.html)。 |
| — | **Probe Atlas Blending** | 启用后，反射探针会添加到 Forward Plus 数据网格，并组合到单个 Atlas 纹理中。在同时使用 Forward Plus 和 GPU Resident Drawer 时，默认使用此 Atlas。此属性仅适用于选择 Forward+ 渲染路径的情况，并且仅当启用 **Probe Blending** 时可见。 |
| — | **Box Projection** | 根据对象在探针盒体中的位置在对象上创建反射，同时仍使用单个探针作为反射源。更多信息请参阅[高级反射探针功能](https://docs.unity3d.com/6000.7/Documentation/Manual/AdvancedRefProbe.html)。 |
| **Mixed Lighting** | — | 只有打开**更多 (⋮)**菜单并选择**显示所有高级属性 (Show All Advanced Properties)**后，此属性才可用。启用 Mixed Lighting 后，管线会在构建中包含混合光照 Shader 变体。 |
| **Use Rendering Layers** | — | 只有打开**更多 (⋮)**菜单并选择**显示所有高级属性 (Show All Advanced Properties)**后，此属性才可用。选中后，可以配置某些 Light，使其只影响特定的 GameObject。更多信息请参阅[渲染层](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/rendering-layers.html)。 |
| **Light Cookies** | — | 只有打开**更多 (⋮)**菜单并选择**显示所有高级属性 (Show All Advanced Properties)**后，此属性才可用。启用光照 Cookie，并为附加光源启用 **Cookie Atlas Resolution** 和 **Cookie Atlas Format**。 |
| **SH Evaluation Mode** | — | 只有打开**更多 (⋮)**菜单并选择**显示所有高级属性 (Show All Advanced Properties)**后，此属性才可用。定义球谐函数 (SH) 光照评估类型。<br><br>可用选项：<br>**Auto**：Unity 自动选择模式。<br>**Per Vertex**：逐顶点评估光照。<br>**Mixed**：部分逐顶点、部分逐像素评估光照。<br>**Per Pixel**：逐像素评估光照。 |

### Shadows

这些设置可以配置阴影的外观和行为，在视觉质量与性能之间取得平衡。

**Shadows** 部分具有以下属性。

| 属性 | 子属性 | 描述 |
| --- | --- | --- |
| **Max Distance** | — | Unity 渲染阴影时，阴影与 Camera 之间的最大距离。Unity 不会渲染超出此距离的阴影。<br><br>**注意**：无论 **Working Unit** 属性的值如何，此属性都使用公制单位。 |
| **Working Unit** | — | Unity 衡量阴影级联距离时使用的单位。 |
| **Cascade Count** | — | 阴影级联的数量。使用阴影级联可以避免靠近 Camera 的阴影过于粗糙，并将阴影分辨率保持在合理的较低值。更多信息请参阅[阴影级联](https://docs.unity3d.com/6000.7/Documentation/Manual/shadow-cascades.html)文档。增加级联数量会降低性能。级联设置仅影响主光源。 |
| — | **Split 1** | 级联 1 结束、级联 2 开始的距离。 |
| — | **Split 2** | 级联 2 结束、级联 3 开始的距离。 |
| — | **Split 3** | 级联 3 结束、级联 4 开始的距离。 |
| — | **Last Border** | Unity 淡出阴影的区域大小。Unity 会在 `Max Distance - Last Border` 的距离处开始淡出阴影，并在 **Max Distance** 处将阴影淡化为零。 |
| — | **Depth Bias** | 使用此设置减少[阴影暗斑](https://docs.unity3d.com/6000.7/Documentation/Manual/ShadowPerformance.html)。 |
| — | **Normal Bias** | 使用此设置减少[阴影暗斑](https://docs.unity3d.com/6000.7/Documentation/Manual/ShadowPerformance.html)。 |
| — | **Soft Shadows** | 选中此复选框，对阴影贴图执行额外处理，使其外观更平滑。<br><br>**性能影响**：对使用基于区块的渲染的平台（例如移动平台和不受约束的 XR 平台）影响很大。禁用后，Unity 使用默认硬件过滤对阴影贴图采样一次。 |
| — | **Quality** | 选择柔和阴影处理的质量级别。<br><br>可用选项：<br>**Low**：适合移动平台的质量与性能平衡。过滤方法：4 个 PCF 抽头。<br>**Medium**：适合桌面平台的质量与性能平衡。过滤方法：5×5 帐篷过滤器。这是默认值。<br>**High**：最佳质量，但性能影响更高。过滤方法：7×7 帐篷过滤器。 |
| **Conservative Enclosing Sphere** | — | 只有打开**更多 (⋮)**菜单并选择**显示所有高级属性 (Show All Advanced Properties)**后，此属性才可用。启用后，可以改善阴影视锥体剔除，并防止 Unity 过度剔除阴影级联角落中的阴影。<br><br>仅出于兼容以前 Unity 版本创建的现有项目的目的禁用此选项。<br><br>如果在现有项目中启用此选项，可能需要调整阴影级联距离，因为包围球的阴影剔除会改变其大小和位置。<br><br>**性能影响**：启用此选项可能提高性能，因为它会尽量减少阴影级联的重叠，从而减少冗余静态阴影投射器的数量。 |

### Post-processing

此部分用于微调全局后期处理设置。

| 属性 | 描述 |
| --- | --- |
| **Grading Mode** | 选择项目使用的[颜色分级](https://docs.unity3d.com/6000.7/Documentation/Manual/PostProcessing-ColorGrading.html)模式。<br>**High Dynamic Range**：最适合类似电影制作流程的高精度分级。Unity 在色调映射之前应用颜色分级。<br>**Low Dynamic Range**：遵循更经典的流程。Unity 在色调映射之后应用有限范围的颜色分级。 |
| **LUT Size** | 设置通用渲染管线用于颜色分级的内部和外部[查找纹理 (LUT)](https://docs.unity3d.com/6000.7/Documentation/Manual/PostProcessing-ColorGrading.html)大小。较大的尺寸提供更高精度，但可能增加性能和内存开销。LUT 大小不能混用，因此应在开始颜色分级流程前确定大小。<br><br>默认值 32 在速度与质量之间提供良好平衡。 |
| **Alpha Processing** | 启用后，URP 后期处理效果会输出正确处理的 Alpha 值。禁用后，URP 会用 1 替换 Alpha 值，从而丢弃 Alpha 通道。渲染目标需要使用包含 Alpha 通道的格式。如果使用 HDR 渲染，请将 **HDR Precision** 设置为 64 位，因为 32 位格式不包含 Alpha 通道。<br><br>**渲染到 Render Texture**<br>如果要将带 Alpha 通道的输出渲染到 Render Texture，请确保 Render Texture 的 **Color Format** 属性包含 Alpha 通道。在渲染带 Alpha 值输出的 Camera 上，将 Environment 部分中的 **Background Type** 设置为 **Solid Color**。这样可以在 Shader 中识别并处理 Alpha 值。<br><br>**限制**<br>在 Camera Stacking 设置中，Overlay Camera 上的后期处理效果仍会影响其下方的所有 Camera。此设置可用于为不在同一 Camera Stack 中的独立 Camera 配置不同后期处理效果，然后使用 Render Texture 和合成 Pass 将它们组合起来。应用后期处理效果时，此功能会保留应用效果之前的 Alpha 值。因此，在对象原始边界之外绘制像素的预构建后期处理效果（例如泛光或景深）可能会在受影响对象周围产生锐利边缘。这不适用于扭曲几何体的效果，例如 Panini 投影或镜头畸变效果；这些效果也会扭曲 Alpha 通道。 |
| **Fast sRGB/Linear Conversions** | 选择此选项，在 sRGB 与线性颜色空间之间转换时使用更快但精度更低的近似函数。 |
| **Data Driven Lens Flare** | 为[镜头光晕](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shared/lens-flare/lens-flare-srp-reference.html)效果分配 URP 所需的 Shader 变体和内存。 |
| **Screen Space Lens Flare** | 为[屏幕空间镜头光晕](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shared/lens-flare/reference-screen-space-lens-flare.html)分配 URP 所需的 Shader 变体和内存。 |

### Volumes

| 属性 | 描述 |
| --- | --- |
| **Volume Update Mode** | 选择 Unity 在运行时如何更新 Volume。<br>**Every Frame**：Unity 每帧更新 Volume。<br>**Via Scripting**：通过脚本触发时，Unity 更新 Volume。在 Editor 中，当不处于 Play 模式时，Unity 仍会每帧更新 Volume。 |
| **Volume Profile** | 设置场景默认使用的 [Volume Profile](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Volume-Profile.html)。更多信息请参阅[了解 Volume](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Volumes.html)。 |

Volume Profile 下方会显示 Volume Override 列表。您可以添加、删除、禁用和启用 Volume Override，并编辑其属性。更多信息请参阅[Volume Override](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/VolumeOverrides.html)。

### Adaptive Performance

如果项目安装了 Adaptive Performance 包，则会出现此部分。**Use Adaptive Performance** 属性可以启用自适应性能功能。

| 属性 | 描述 |
| --- | --- |
| **Use Adaptive Performance** | 选中此复选框以启用自适应性能功能，该功能会在运行时调整渲染质量。启用后，Adaptive Performance 可以覆盖渲染设置，例如阴影和 Decal 的绘制距离，并将其降低到低于您在此资源或单个组件中配置的值。有关 Adaptive Performance 可控制设置的详细信息，请参阅[Adaptive Performance Scalers](https://docs.unity3d.com/6000.7/Documentation/Manual/../adaptive-performance/scalers-reference.html)。 |

### 其他资源

- [[02-创建通用渲染管线资源]]

---

## 文档导航

- 上一页：[[00-通用渲染管线参考]]
- 目录：[[00-通用渲染管线参考]]
- 下一页：[[02-URP 的通用渲染器资源参考]]
