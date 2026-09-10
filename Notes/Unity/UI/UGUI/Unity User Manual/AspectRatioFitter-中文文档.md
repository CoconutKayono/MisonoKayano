# Aspect Ratio Fitter（宽高比适配器）

> 来源：[Unity UGUI 2.6 — Aspect Ratio Fitter](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-AspectRatioFitter.html)  
> 官方源文件：[uGUI/Documentation~/script-AspectRatioFitter.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/script-AspectRatioFitter.md)  
> 整理日期：2026-09-05

**Aspect Ratio Fitter** 是一种布局控制器，用于控制其所在布局元素的尺寸。它可以根据宽度调整高度、根据高度调整宽度，也可以让元素适配父级矩形内部，或覆盖父级矩形的整个区域。

## 属性

![Aspect Ratio Fitter Inspector](UI_AspectRatioFitterInspector.png)

| 属性 | 说明 |
| --- | --- |
| **Aspect Mode** | 决定如何调整矩形以保持指定宽高比。 |
| └ **None** | 不让矩形适配宽高比。 |
| └ **Width Controls Height** | 根据宽度自动调整高度。 |
| └ **Height Controls Width** | 根据高度自动调整宽度。 |
| └ **Fit In Parent** | 自动调整宽度、高度、位置和锚点，使矩形在保持宽高比的同时适配父级矩形内部。父级矩形中可能有一部分空间不会被覆盖。 |
| └ **Envelope Parent** | 自动调整宽度、高度、位置和锚点，使矩形在保持宽高比的同时覆盖父级的整个区域。矩形可能超出父级边界。 |
| **Aspect Ratio** | 要保持的宽高比，即“宽度 ÷ 高度”。 |

## 工作方式

Aspect Ratio Fitter 不会考虑布局系统提供的最小尺寸、首选尺寸等布局信息。它直接根据 **Aspect Mode** 和 **Aspect Ratio** 控制自身的 Rect Transform，因此应避免让另一个布局控制器同时驱动同一方向的尺寸。

当 Rect Transform 被调整尺寸时，变化会围绕 Pivot 发生。Pivot 可以用来控制矩形的对齐方式。例如，将 Pivot 放在顶部中心，矩形会向左右均匀增长，并只向下增长，从而保持顶部边缘的位置不变。

## 模式选择建议

- 已知宽度，希望高度随比例变化：使用 **Width Controls Height**。
- 已知高度，希望宽度随比例变化：使用 **Height Controls Width**。
- 图片或视频需要完整显示在父级区域内：使用 **Fit In Parent**，可能留下空白区域。
- 背景图需要覆盖父级区域：使用 **Envelope Parent**，边缘可能被裁切或超出父级。
