# 可视组件（Visual Components）

> 来源：[Unity UGUI 2.6 — Visual Components](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/UIVisualComponents.html)  
> 官方源文件：[uGUI/Documentation~/UIVisualComponents.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/UIVisualComponents.md)  
> 整理日期：2026-09-05

随着 UI 系统的引入，Unity 增加了一些用于创建 GUI 特定功能的组件。本节介绍这些组件的基础用法。

## Text（文本）

![Text Inspector](UI_TextInspector.png)

Text 组件也称为 Label，包含用于输入要显示文字的 Text 区域。可以设置：

- 字体、字体样式和字体大小；
- 是否启用 Rich Text；
- 文本对齐方式；
- 水平和垂直溢出行为，用于控制文字大于矩形宽度或高度时的处理方式；
- Best Fit，使文本自动调整大小以适应可用空间。

## Image（图像）

![Image Inspector](UI_ImageInspector.png)

Image 由 Rect Transform 和 Image 组件组成。可以在 Target Graphic 字段中为 Image 指定 Sprite，并在 Color 字段中设置颜色，也可以为 Image 应用材质。

Image Type 字段决定 Sprite 的显示方式：

- **Simple**：等比例缩放整个 Sprite。
- **Sliced**：使用 3×3 Sprite 分割，使调整尺寸时不会拉伸角落，只拉伸中心部分。
- **Tiled**：与 Sliced 类似，但会平铺（重复）中心部分，而不是拉伸它。如果 Sprite 完全没有边框，则整个 Sprite 都会平铺。
- **Filled**：显示方式与 Simple 类似，但会从指定的起点，沿指定方向、方法和数量逐渐填充 Sprite。

选择 Simple 或 Filled 时会出现 **Set Native Size** 选项，它会将图像恢复为原始 Sprite 尺寸。

将 Texture Type 设置为 **Sprite (2D / UI)**，即可将图像导入为 UI Sprite。与旧 GUI Sprite 相比，Sprite 具有额外的导入设置，最大区别是增加了 Sprite Editor。Sprite Editor 支持对图像进行 **9-slicing**，将图像分成 9 个区域，从而在调整 Sprite 尺寸时避免拉伸或扭曲角落。

![Sprite Editor](UI_SpriteEditor.png)

## Raw Image（原始图像）

Image 组件接收 Sprite，而 Raw Image 接收 Texture（没有边框等 Sprite 信息）。除非确有需要，否则通常应使用 Image，因为它适用于绝大多数情况。

## Mask（遮罩）

Mask 不是可见的 UI 控件，而是修改子控件外观的一种方式。Mask 会将子元素限制在父元素形状之内：如果子元素比父元素大，则只有落在父元素内部的部分可见。

## Raycast Receiver（射线接收器）

![Raycast Receiver Editor](UI_RaycastReceiverEditor.png)

Raycast Receiver 是一个非可视组件，用于接收 Graphic Raycaster 发出的射线，以检测或阻止点击、触摸等指针事件。它可以在 Canvas 上定义无需渲染可见几何体的交互区域，相比使用透明 Image 性能更好。

可以通过 **Raycast Target** 属性启用或禁用输入拦截，并使用 **Raycast Padding** 相对于 RectTransform 边界调整命中检测区域。

## Effects（效果）

可视组件还可以应用一些简单效果，例如投影或轮廓。更多信息参见 [UI Effects](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/comp-UIEffects.html)。

