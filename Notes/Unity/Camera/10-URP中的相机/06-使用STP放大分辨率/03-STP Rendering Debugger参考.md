# STP Rendering Debugger 参考

> 原文：[Spatial-Temporal Post-processing Rendering Debugger reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/stp/stp-debug-views.html)

Spatial-Temporal Post-processing（STP）有六种 debug view。要访问这些视图，请打开 Rendering Debugger 窗口，进入 **Rendering > Map Overlays** 并选择 **STP**。Unity 会显示 **STP Debug Views** 属性，可以从中选择一个 view。

有关如何访问 Rendering Debugger 窗口的信息，请参阅[如何访问 Rendering Debugger](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/rendering-debugger.html)。

## Debug view

| Debug view | 说明 |
| --- | --- |
| **Clipped Input Color** | 显示裁剪到 `0` 和 `1` 之间的 HDR input color。 |
| **Log Input Depth** | 以 logarithmic scale 显示 input depth。 |
| **Reversible Tonemapped Input Color** | 显示使用 reversible tonemapper 映射到 `0–1` 范围的 input color。 |
| **Shaped Absolute Input Motion** | 可视化 input motion vectors。 |
| **Motion Reprojection** | 可视化跨多个 frame 的 reprojected color difference。 |
| **Sensitivity** | 可视化 pixel sensitivities。绿色区域表示 STP 无法预测 motion behavior 的位置，这些区域很可能以降低的视觉质量渲染。当被遮挡对象首次变为可见或发生快速运动时，STP 难以预测 motion。错误的 object motion vectors 也可能造成 motion prediction 问题。红色区域突出显示从 TAA 中排除的 pixels，因此 STP 会有意不预测这些 pixels 的 motion。这有助于避免不必要的 blurring 和 ghosting，尤其是在渲染透明对象时。 |

---

## 文档导航

- 上一页：[[02-启用STP]]
- 目录：[[00-使用STP放大分辨率]]
- 下一页：[[../07-Universal Additional Camera Data]]
