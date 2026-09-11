# 在 URP 中选择渲染路径

> 原文：[Choose a rendering path in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-paths-comparison.html)


应根据项目类型以及目标硬件，确定哪种[[01-URP 中渲染路径简介]]最适合您的通用渲染管线 (URP) 项目。

如果场景中的光源不多，或者在移动平台或低端平台上进行渲染，请使用默认的前向渲染路径，因为 Unity 会限制光源数量和每像素光源数量。

在以下情况下选择 Forward+ 渲染路径：

- 场景中有许多光源，而延迟渲染路径在构建的平台上渲染速度太慢。
- 您需要混合 2 个以上反射探头。
- 您可以使用 [Entities 包](https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/index.html)。

在以下情况下选择延迟渲染路径：

- 无需使用[渲染层](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/rendering-layers.html)。如果在延迟渲染路径中使用渲染层，URP 会渲染额外的 G 缓冲区渲染目标，这可能会影响性能。
- 不需要精确的地形混合。有关更多信息，请参阅[[04-延迟渲染路径简介]]。

避免将具有 Subtractive 或 Shadowmask [Lighting Mode](https://docs.unity3d.com/6000.7/Documentation/Manual/lighting-mode-landing.html) 的光源与延迟渲染路径一起使用，因为这些光源仅针对前向渲染路径进行了优化。

在以下情况下，Unity 会回退到不同的渲染路径：

- 如果选择延迟渲染路径，但着色器不支持延迟着色。Unity 在渲染结束时使用前向渲染路径渲染游戏对象。
- 如果您构建所针对的目标设备上的 GPU 不支持您选择的渲染路径。Unity 回退到不同的渲染路径。

## 渲染路径比较

下表显示了 URP 中的渲染路径之间的差异。

| **功能** | **前向** | **Forward+** | **延迟** |
| --- | --- | --- | --- |
| 移动平台性能 | 性能影响低。 | 性能影响低。 | 性能影响高，因为 Unity 会添加额外的渲染通道来渲染 G 缓冲区。 |
| 每对象渲染通道数 | 1 | 1 | 1 |
| [每对象实时光源数](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting/light-limits-in-urp.html) | 9 | 无限制 | 对于不透明对象无限制；对于透明对象为 9。 |
| [每摄像机实时光源数](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting/light-limits-in-urp.html) | 最多 257 个，具体取决于平台。 | 最多 256 个，具体取决于平台；Forward+ 以相同方式处理主光源和附加光源，因此每个摄像机的限制减少一个光源。 | 最多 257 个光源，具体取决于平台。 |
| 每顶点光源 | 是 | 否 | 否 |
| 禁用主光源 | 是 | 否 | 否 |
| 每个像素法线 | 准确，不进行编码。 | 准确，不进行编码。 | 法线经过编码，精度较低；也可以选择更准确但较慢的法线。 |
| [[06-在通用渲染管线中添加抗锯齿]] | 是 | 是 | 否 |
| 摄像机叠加 | 是 | 是 | 是，但基础摄像机使用延迟渲染路径，叠加摄像机使用前向渲染路径。 |

## 其他资源

- [URP 中的光源限制](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting/light-limits-in-urp.html)
- [逐像素和逐顶点光源](https://docs.unity3d.com/6000.7/Documentation/Manual/PerPixelLights.html)
- [[01-URP 中渲染路径简介]]

---

## 文档导航

- 上一页：[[01-URP 中渲染路径简介]]
- 目录：[[00-URP 中的渲染路径]]
- 下一页：[[03-在 URP 中设置渲染路径]]
