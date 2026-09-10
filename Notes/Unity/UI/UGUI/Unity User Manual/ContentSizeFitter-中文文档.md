# Content Size Fitter（内容尺寸适配器）

> 来源：[Unity UGUI 2.6 — Content Size Fitter](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-ContentSizeFitter.html)  
> 官方源文件：[uGUI/Documentation~/script-ContentSizeFitter.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/script-ContentSizeFitter.md)  
> 整理日期：2026-09-05

**Content Size Fitter** 是一种布局控制器，用于控制其所在 GameObject 的 Rect Transform 尺寸。尺寸由同一个 GameObject 上的布局元素组件提供的最小尺寸或首选尺寸决定；这些组件可以是 Image、Text、Layout Group 或 Layout Element。

## 属性

![Content Size Fitter Inspector](UI_ContentSizeFitterInspector.png)

| 属性 | 说明 |
| --- | --- |
| **Horizontal Fit** | 决定宽度如何控制。 |
| └ **Unconstrained** | 不根据布局元素驱动宽度。 |
| └ **Min Size** | 根据布局元素的最小宽度驱动宽度。 |
| └ **Preferred Size** | 根据布局元素的首选宽度驱动宽度。 |
| └ **Clamped** | 使布局元素的宽度保持在最小值和最大值范围内；此模式不会驱动宽度。 |
| **Vertical Fit** | 决定高度如何控制。 |
| └ **Unconstrained** | 不根据布局元素驱动高度。 |
| └ **Min Size** | 根据布局元素的最小高度驱动高度。 |
| └ **Preferred Size** | 根据布局元素的首选高度驱动高度。 |
| └ **Clamped** | 使布局元素的高度保持在最小值和最大值范围内；此模式不会驱动高度。 |

> 上表按 UGUI 2.6 官方页面列出的选项翻译。**Clamped** 表示在最小值和最大值之间限制尺寸，而不是直接驱动尺寸。

## 工作方式

Content Size Fitter 读取同一个 GameObject 上布局元素组件提供的尺寸信息，然后根据 **Horizontal Fit** 和 **Vertical Fit** 设置控制自身的 Rect Transform。比如，带有 Text 组件的对象可以将两个方向都设置为 **Preferred Size**，让矩形自动包住文本内容。

Rect Transform 被调整尺寸时，变化会围绕 Pivot 发生。因此，Pivot 也决定了元素向哪个方向展开或收缩：

- Pivot 在中心时，矩形会向四周均匀扩展；
- Pivot 在左上角时，矩形会向右下方扩展；
- 将 Pivot 放在希望固定不动的边或角上，可以控制适配内容时的展开方向。

## 常见组合

### 让文本背景适配文本

在带有 Text 组件的 GameObject 上添加 Content Size Fitter，将 Horizontal Fit 和 Vertical Fit 设为 **Preferred Size**。如果需要边距，可以在父对象上使用 Layout Group，并通过 Padding 增加内边距。

### 与 Layout Group 配合

Layout Group 会根据子元素的布局信息计算自己的尺寸，Content Size Fitter 再根据 Layout Group 提供的尺寸调整 Rect Transform。这可以实现“背景包住内容”的效果。

### 避免布局控制冲突

不要在 Layout Group 的子元素上普遍添加 Content Size Fitter。Content Size Fitter 想控制子元素自己的 Rect Transform，而父级 Layout Group 也想控制该 Rect Transform，二者会互相冲突并产生未定义行为。通常应该让父级 Layout Group 通过 **Child Force Expand**、Child Alignment 以及子元素的 Layout Element 来完成尺寸分配。
