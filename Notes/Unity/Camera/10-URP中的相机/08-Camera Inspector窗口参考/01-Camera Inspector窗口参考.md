# Camera Inspector 窗口参考

> 原文：[Camera Inspector window reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/camera-component-reference.html)

在 Universal Render Pipeline（URP）中，Unity 会根据 Camera 类型，在 Inspector 中显示 Camera Component 的不同属性。要更改 Camera 类型，请选择 **Render Type**。

Base Camera 显示：**Projection**、**Physical Camera**、**Rendering**、**Stack**、**Environment**、**Output**。Overlay Camera 显示：**Projection**、**Physical Camera**、**Rendering**、**Environment**。

## Projection

| 属性 | 说明 |
| --- | --- |
| **Projection** | 控制 Camera 如何模拟 perspective。**Perspective** 保留 perspective 地渲染对象；**Orthographic** 以统一方式渲染对象，不产生 perspective 感。 |
| **Field of View Axis** | 设置 Unity 测量 Camera field of view 所沿的 axis，可选 **Vertical** 或 **Horizontal**。仅在 Projection 为 Perspective 时显示。 |
| **Field of View** | 设置 Camera view angle 的宽度，沿选定 axis 以 degree 为单位测量。仅在 Projection 为 Perspective 时显示。 |
| **Size** | 设置 Camera viewport size。仅在 Projection 为 Orthographic 时显示。 |
| **Clipping Planes** | 设置开始和停止渲染的距 Camera 距离，包括 **Near**（最近绘制点）和 **Far**（最远绘制点）。 |
| **Physical Camera** | 显示用于模拟 physical camera 的额外属性。Physical Camera 使用 **Focal Length**、**Sensor Size** 和 **Shift** 等真实相机属性计算 Field of View。仅在 Projection 为 Perspective 时可用。 |

选择 **Physical Camera** 后，还会显示[[02-Physical Camera Inspector窗口参考|Physical Camera 属性]]。

## Rendering

| 属性 | 说明 |
| --- | --- |
| **Renderer** | 选择 Camera 使用的 Renderer。 |
| **Post Processing** | 启用 post-processing effect。如果启用 Universal Renderer 的 **On-Tile Validation**，Unity 会禁用此选项。 |
| **Anti-Aliasing** | 选择 Camera 使用的 post-process anti-aliasing 方法。可选 **None**、**Fast Approximate Anti-aliasing (FXAA)**、**Subpixel Morphological Anti-aliasing (SMAA)** 和 **Temporal Anti-aliasing (TAA)**。Camera 仍可同时使用硬件 MSAA，但不能与 TAA 同时使用。该属性仅在 Render Type 为 Base 时显示。 |
| **Quality (SMAA)** | 选择 SMAA quality：**Low**、**Medium** 或 **High**。仅在 Anti-aliasing 选择 SMAA 时显示。Low 与 High 的 resource intensity 差异较小。 |
| **Quality (TAA)** | 选择 TAA quality：**Very Low**、**Low**、**Medium**、**High** 或 **Very High**。仅在 Anti-aliasing 选择 TAA 时显示。 |
| **Contrast Adaptive Sharpening** | 启用高质量 post sharpening，减少 TAA blur。URP Asset 启用 AMD FidelityFX Super Resolution（FSR）或 Scalable Temporal Post-Processing（STP）时，该设置会被覆盖，因为二者都会在 upscaling 过程中处理 sharpening。仅在 TAA 时显示。 |
| **Base Blend Factor** | 设置 history buffer 与当前 frame result 的混合量。值越高，history contribution 越多，anti-aliasing 越好，但 ghosting 风险越高。仅在 TAA 且启用 Inspector 的 Advanced Properties 时显示。 |
| **Jitter Scale** | 设置启用 TAA 时 jitter 的 scale。值越低，visible flickering/jittering 越少，但 anti-aliasing 效果也越弱。仅在 TAA 且启用 Advanced Properties 时显示。 |
| **Mip Bias** | 设置渲染时 texture mipmap selection 的 bias。正值使 texture 更模糊，负值使 texture 更锐利，但更低的值会影响性能。需要 texture mipmaps。仅在 TAA 且启用 Advanced Properties 时显示。 |
| **Variance Clamp Scale** | 设置 Unity 在 color history 错误或不可用时查找附近像素所使用的 color volume 大小。较低值可减少 ghosting 但增加 flickering；较高值减少 flickering，但容易产生 blur 和 ghosting。仅在 TAA 且启用 Advanced Properties 时显示。 |
| **Stop NaNs** | 将 NaN 值替换为黑色像素，避免某些 effect 出错，但此过程开销较大。只有遇到无法修复的 NaN 问题时才启用。必须启用 Post Processing，且仅在 Render Type 为 Base 时可用。 |
| **Dithering** | 对最终 render 应用 8-bit dithering，减少宽渐变和低光区域中的 banding。仅在 Render Type 为 Base 时显示。 |
| **Clear Depth** | 渲染时清除前一台 Camera 的 depth。仅在 Render Type 为 Overlay 时显示。 |
| **Render Shadows** | 启用 shadow rendering。 |
| **Priority** | priority 较高的 Camera 绘制在 priority 较低的 Camera 之上，范围为 `-100` 到 `100`。仅在 Render Type 为 Base 时显示。 |
| **Opaque Texture** | 控制是否创建 `CameraOpaqueTexture`（rendered view 的副本）。可选 **Off**、**On** 或 **Use Pipeline Settings**。仅在 Render Type 为 Base 时显示；启用 On-Tile Validation 时 Unity 禁用此选项。 |
| **Depth Texture** | 控制是否创建 `_CameraDepthTexture`（rendered depth values 的副本）。可选 **Off**、**On** 或 **Use Pipeline Settings**。该 Texture 通常在 `AfterRenderingSkybox` 与 `BeforeRenderingTransparents` 之间设置；使用 depth prepass 时在 `BeforeRenderingOpaques` 设置。启用 On-Tile Validation 时 Unity 禁用此选项。 |
| **Culling Mask** | 选择 Camera 渲染的 Layers。 |
| **Occlusion Culling** | 启用 Occlusion Culling。启用 On-Tile Validation 时 Unity 禁用此选项。 |

## Stack

> [!NOTE]
> 只有当 **Render Type** 为 **Base** 且 **On-Tile Validation** 禁用时，才会显示此部分。

Camera Stack 可以合成多台 Camera 的结果，由一台 Base Camera 和任意数量的 Overlay Camera 组成。使用 Stack 属性将 Overlay Camera 添加到 Stack，它们会按 Stack 中定义的顺序渲染。有关配置和使用 Camera Stack 的更多信息，请参阅[[../03-多台相机/02-设置Camera Stack|设置 Camera Stack]]。

## Environment

| 属性 | 说明 |
| --- | --- |
| **Background Type** | 控制 Camera Render Loop 开始时如何初始化 color buffer。仅在 Render Type 为 Base 时显示。**Skybox** 使用 Skybox 清除 color buffer；如果没有 Skybox 则回退到 background color。**Solid Color** 使用给定 color 清除，并显示 **Background** 属性。**Uninitialized** 不初始化 color buffer，将 RenderTarget 的 load action 设为 `DontCare`。只有 Camera 或 Camera Stack 会绘制 color buffer 每个像素时才使用，否则未绘制像素行为未定义。TBDR GPU 上可能产生未初始化 tile memory。 |
| **Volumes > Update Mode** | 选择 Unity 如何更新 Volumes：**Every Frame**、**Via Scripting** 或 **Use Pipeline Settings**。 |
| **Volume Mask** | 使用下拉菜单设置定义哪些 Volumes 影响 Camera 的 Layer Mask。 |
| **Volume Trigger** | 分配 Volume system 用于处理 Camera 位置的 Transform。例如 third person view 中，可以设置为角色的 Transform，使 Camera 使用角色进入的 Volumes 的 post-processing 和 Scene 设置。未分配时使用 Camera 自身 Transform。 |

## Output

此部分只有在 **Render Type** 为 **Base** 时显示。

当 Camera 的 Render Type 为 Base 且 Render Target 设置为 Texture 时，Inspector 不显示 **Target Display**、HDR rendering、MSAA 和 Allow Dynamic Resolution，因为这些属性由 Render Texture 决定，可在 Render Texture Asset 中更改。

| 属性 | 说明 |
| --- | --- |
| **Output Texture** | 如果指定，则将 Camera 输出渲染到 RenderTexture；否则渲染到屏幕。 |
| **Target Display** | 选择要渲染到的 external device。 |
| **Target Eye** | 选择 Camera 的 target eye：**Both** 允许所选 Camera 进行 XR rendering；**None** 禁用所选 Camera 的 XR rendering。 |
| **Viewport Rect** | 使用 Viewport Coordinates（`0–1`）中的四个值指定 Camera view 的绘制位置，包括 **X**、**Y**、**W**（Width）和 **H**（Height）。 |
| **HDR Rendering** | 为 Camera 启用 High Dynamic Range rendering。 |
| **MSAA** | 为 Camera 启用 Multisample Anti-aliasing。 |
| **Allow Dynamic Resolution** | 为 Camera 启用 Dynamic Resolution rendering。 |

---

## 文档导航

- 上一页：[[00-Camera Inspector窗口参考]]
- 目录：[[00-Camera Inspector窗口参考]]
- 下一页：[[02-Physical Camera Inspector窗口参考]]
