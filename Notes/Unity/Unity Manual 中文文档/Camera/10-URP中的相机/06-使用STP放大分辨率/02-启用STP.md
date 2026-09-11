# 启用 STP

> 原文：[Enable Spatial-Temporal Post-processing in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/stp/stp-enable.html)

要在 Universal Render Pipeline（URP）中启用 STP：

1. 在 Project 窗口中选择 active URP Asset。
2. 在 Inspector 中进入 **Quality > Upscaling Filter**，选择 **Spatial-Temporal Post-Processing**。

当 **Render Scale** 设置为 **1.0** 时，STP 仍保持 active，因为它会对最终 rendered output 应用 temporal anti-aliasing（TAA）。

> [!NOTE]
> STP 与 URP 中的 **Dynamic Resolution** 不兼容，只能与 **Render Scale** 配合使用。

---

## 文档导航

- 上一页：[[01-STP Upscaler简介]]
- 目录：[[00-使用STP放大分辨率]]
- 下一页：[[03-STP Rendering Debugger参考]]
