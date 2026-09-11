# URP 的通用渲染器资源参考

> 原文：[Universal Renderer asset reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html)

本页介绍 URP 通用渲染器 (URP Universal Renderer) 设置。

有关 URP 中渲染的更多信息，另请参阅[[01-通用渲染管线中的渲染]]。

## 如何查找通用渲染器资源

要查找 URP 资源正在使用的通用渲染器资源，请执行以下操作：

1. 选择一个 URP 资源。
2. 在渲染器列表 (Renderer List) 部分中，单击某个渲染器项或某个渲染器旁边的垂直省略号图标 (⋮)。

![如何查找通用渲染器资源](find-renderer.png)

如何查找通用渲染器资源

## 属性

### 过滤

此部分包含用于定义渲染器绘制哪些层的属性。

| 属性 | 描述 |
| --- | --- |
| **Prepass Layer Mask** | GameObject 必须分配到的层，以便影响任何预通道。 |
| **Opaque Layer Mask** | 不透明 GameObject 必须分配到的层，以便进行渲染。 |
| **Transparent Layer Mask** | 透明 GameObject 必须分配到的层，以便进行渲染。 |

### 渲染

此部分包含与渲染相关的属性。

| 属性 | 描述 |
| --- | --- |
| **Rendering Path** | 选择渲染路径。<br>选项：<br>- **Forward**：前向渲染路径。<br>- **Forward+**：[Forward+ 渲染路径](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/forward-rendering-paths.html)。<br>- **Deferred**：[[00-URP 中的延迟渲染路径]]。<br>- **Deferred+**：[Deferred+ 渲染路径](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/deferred-rendering-path-landing.html)。 |
| **Depth Priming Mode** | 跳过绘制重叠的像素，以加快渲染速度。Unity 使用深度纹理检查哪些像素重叠。渲染性能的提升取决于重叠像素的数量以及像素着色器的复杂性。<br><br>**注意**：如果使用自定义着色器，除非添加带有 `DepthOnly` 和 `DepthNormals` 标签的通道 (Pass)，否则 Unity 会将不透明对象渲染为不可见。有关更多信息，请参阅 [仅在着色器中写入深度](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-depth-only.html)。<br><br>选项如下：<br>- **Disabled**：不执行深度引导。<br>- **Auto**：仅当渲染管线中已存在深度预通道时才执行深度引导。Android、iOS 和 Apple TV 平台不支持此设置。<br>- **Forced**：如果渲染管线中尚不存在深度预通道，则添加一个深度预通道并执行深度引导。添加深度预通道会影响内存和性能。<br><br>**注意**：如果使用[[00-URP 中的延迟渲染路径]]或[[06-在通用渲染管线中添加抗锯齿]]，或者在运行时使用基于图块的延迟渲染 (TBDR) 的移动设备，则不支持深度引导。 |
| **Accurate G-buffer normals** | 指示是否使用更耗费资源的法线编码/解码方法来提高视觉质量。<br><br>仅当**渲染路径 (Rendering Path)** 设置为**延迟 (Deferred)** 时，此属性才可用。 |
| **Depth Texture Mode** | 指定在渲染管线中将场景深度复制到深度纹理的阶段。选项有：<br>- **After Opaques**：URP 在不透明渲染通道之后复制场景深度。<br>- **After Transparents**：URP 在透明渲染通道之后复制场景深度。<br>- **Force Prepass**：URP 执行深度预通道以生成场景深度纹理。<br><br>**注意**：在移动设备上，**After Transparents** 选项可以显著改善内存带宽。这是因为 Copy Depth 通道会导致渲染目标在不透明通道和透明通道之间切换。发生这种情况时，Unity 会将颜色缓冲区 (Color Buffer) 的内容存储在主内存中，然后在 Copy Depth 通道完成后再次加载。启用 MSAA 后，影响会显著增加，因为 Unity 还必须将 MSAA 数据与颜色缓冲区一起存储和加载。 |
| **Tile-Only Mode** | 在 UI 中显示所有需要非无内存中间纹理 (non-memoryless intermediate textures) 的属性的警告，并防止 Unity 在运行时使用被标记的功能。这会影响 **Camera**、**Universal Render Pipeline Asset** 和 **Universal Renderer** 中的目标属性。<br><br>使用此选项可在渲染过程中减少基于图块的架构（例如大多数移动设备和 XR 设备）的 GPU 带宽。 |

### 原生渲染通道

此部分包含与 URP 的原生渲染通道 API (Native RenderPass API) 相关的属性。

| 属性 | 描述 |
| --- | --- |
| **Native RenderPass** | 指示是否使用 URP 的原生渲染通道 API (Native RenderPass API)。启用后，URP 使用此 API 来构建渲染通道。因此，您可以在自定义 URP 着色器中使用[可编程混合](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-framebuffer-fetch.html)。有关渲染通道 (RenderPass API) 的更多信息，请参阅 [ScriptableRenderContext.BeginRenderPass](https://docs.unity3d.com/ScriptReference/Rendering.ScriptableRenderContext.BeginRenderPass.html)。<br><br>**注意**：启用此属性对 OpenGL ES 没有影响。 |

### 阴影

此部分包含与渲染阴影相关的属性。

| 属性 | 描述 |
| --- | --- |
| **Transparent Receive Shadows** | 启用此选项后，Unity 会在透明对象上绘制阴影。 |

### 后期处理

| 属性 | 描述 |
| --- | --- |
| **Enabled** | 启用场景中的后期处理效果。如果禁用，Unity 会从构建中排除后期处理渲染通道、着色器和纹理。 |
| **Data** | 选择渲染器用于后期处理的资源。仅当启用 **Enabled** 时，此属性才可用。 |

### 覆盖

此部分包含该渲染器覆盖的渲染管线属性。

#### 模板

选中此复选框后，渲染器将处理模板缓冲区值。

![URP 通用渲染器模板覆盖](urp-universal-renderer-stencil-on.png)

URP 通用渲染器模板覆盖

有关 Unity 如何使用模板缓冲区的更多信息，请参阅 [ShaderLab：模板](https://docs.unity3d.com/Manual/SL-Stencil.html)。

在 URP 中，可以使用模板缓冲区的位 0 到 3 来自定义渲染效果。这意味着可以使用模板指数 0 到 15。

### 兼容性

此部分包含与向后兼容性相关的设置。

| 属性 | 描述 |
| --- | --- |
| **Intermediate Texture** | 此属性允许您强制 URP 通过中间纹理进行渲染。<br>选项：<br>- **Auto**：URP 使用 `ScriptableRenderPass.ConfigureInput` 方法提供的信息来自动确定是否需要通过中间纹理进行渲染。<br>- **Always**：强制通过中间纹理进行渲染。仅当与不使用 `ScriptableRenderPass.ConfigureInput` 声明其输入的渲染器功能兼容时，才使用此选项。使用此选项可能会对某些平台产生重大性能影响。 |

### 渲染器功能

此部分包含分配给选定渲染器的渲染器功能列表。

有关如何添加渲染器功能的信息，请参阅[[01-向 URP 渲染器添加渲染器功能]]。

URP 包含名为[[03-URP 的渲染对象渲染器功能 (Render Objects Renderer Feature) 参考]]的预构建渲染器功能。

> **注意**：如果启用 **On-Tile Validation**，Unity 会禁用渲染器功能。

---

## 文档导航

- 上一页：[[01-URP 通用渲染管线资源参考]]
- 目录：[[00-通用渲染管线参考]]
- 下一页：[[03-URP 的图形设置窗口参考]]
