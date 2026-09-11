# Camera Inspector 窗口参考

> 原文：[Camera Inspector window reference for the Built-In Render Pipeline](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Camera.html)

> [!IMPORTANT]
> Built-In Render Pipeline 已弃用，并将在未来版本中变为 obsolete。在整个 Unity 6.7 LTS 生命周期内，它仍受支持，包括 bug 修复和维护。有关迁移信息，请参阅[从 Built-In Render Pipeline 迁移到 URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrading-from-birp.html)和[Render Pipeline 功能比较](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines-feature-comparison.html)。

探索 Camera Component window 中的属性，用于自定义 Camera。

| 属性 | 功能 |
| --- | --- |
| **Clear Flags** | 确定清除屏幕的哪些部分。在使用多台 Camera 绘制不同游戏元素时很有用。 |
| **Background** | 在绘制完视图中的所有元素且没有 skybox 后，应用于剩余屏幕的颜色。 |
| **Culling Mask** | 按 Layer 包含或排除由 Camera 渲染的对象。可以在 Inspector 中为对象分配 Layer。 |
| **Projection** | 切换 Camera 模拟 perspective 的能力。 |
| **Perspective** | Camera 以保留 perspective 的方式渲染对象。 |
| **Orthographic** | Camera 以统一方式渲染对象，不产生 perspective 感。注意：Deferred rendering 不支持 Orthographic mode，始终使用 Forward rendering。 |
| **Size**（选择 Orthographic 时） | Camera 设置为 Orthographic 时的 viewport size。 |
| **FOV Axis**（选择 Perspective 时） | Field of View axis。可选择 **Horizontal** 或 **Vertical**。 |
| **Field of View**（选择 Perspective 时） | Camera 的 view angle，沿 FOV Axis 下拉菜单指定的 axis 以 degree 为单位测量。 |
| **Physical Camera** | 启用 Camera 的 Physical Camera 属性。启用后，Unity 使用 **Focal Length**、**Sensor Size** 和 **Lens Shift** 模拟真实相机属性来计算 Field of View。 |
| **Focal Length** | 设置 Camera sensor 与 lens 之间的距离，单位为毫米。值越低，Field of View 越宽；更改后 Unity 会自动更新 Field of View。 |
| **Sensor Type** | 指定 Camera 要模拟的真实相机格式。选择格式后 Unity 自动设置 Sensor Size X/Y；手动更改 Sensor Size 后自动变为 **Custom**。 |
| **Sensor Size** | 设置 Camera sensor 的大小，单位为毫米。包括 **X**（sensor width）和 **Y**（sensor height）。 |
| **Lens Shift** | 将 lens 从中心水平或垂直移动。值是 sensor size 的倍数，也可以用来修正透视 distortion，或使 Camera frustum 变为 oblique。包括 **X**（horizontal offset）和 **Y**（vertical offset）。 |
| **Gate Fit** | 更改 resolution gate 相对于 film gate 的尺寸。可选择 **Vertical**、**Horizontal**、**Fill**、**Overscan** 或 **None**。 |
| **Clipping Planes** | 设置开始和停止渲染的距离，包括 **Near**（距 Camera 最近的绘制点）和 **Far**（距 Camera 最远的绘制点）。 |
| **Viewport Rect** | 使用 Viewport Coordinates（`0–1`）中的四个值，指定 Camera view 在屏幕上的绘制位置：**X**、**Y**、**W**（Width）和 **H**（Height）。 |
| **Depth** | Camera 在绘制顺序中的位置。值较大的 Camera 会绘制在值较小的 Camera 之上。 |
| **Rendering Path** | 定义 Camera 使用的渲染方法。**Use Player Settings** 使用 Player Settings 中的 Rendering Path；**Vertex Lit** 将所有对象作为 Vertex-Lit 渲染；**Forward** 对每个材质使用一个 pass 渲染所有对象。 |
| **Target Texture** | 指向包含 Camera view 输出的 Render Texture。设置后 Camera 将不能渲染到屏幕。 |
| **Occlusion Culling** | 启用该 Camera 的 Occlusion Culling，使被其他对象（例如墙）遮挡的对象不被渲染。 |
| **Allow HDR** | 为该 Camera 启用 High Dynamic Range rendering。 |
| **Allow MSAA** | 为该 Camera 启用 multi-sample anti-aliasing。 |
| **Allow Dynamic Resolution** | 为该 Camera 启用 Dynamic Resolution rendering。 |
| **Target Display** | 定义渲染到哪个 external device，范围为 1 到 8。 |

## 其他资源

- [[01-Camera Inspector窗口参考|URP Camera Inspector 窗口参考]]
- [[00-使用物理相机模拟真实相机|Physical Camera]]
- [[00-使用遮挡剔除排除隐藏对象|Occlusion Culling]]

---

## 文档导航

- 上一页：[[01-使用Clear Flags设置相机背景]]
- 目录：[[00-Built-In Render Pipeline中的相机]]
- 下一页：[[12-相机故障排查]]
