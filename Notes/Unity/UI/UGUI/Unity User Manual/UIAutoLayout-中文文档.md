# 自动布局（Auto Layout）

> 来源：[Unity UGUI 2.6 — Auto Layout](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/UIAutoLayout.html)  
> 官方源文件：[uGUI/Documentation~/UIAutoLayout.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/UIAutoLayout.md)  
> 整理日期：2026-09-05

Rect Transform 布局系统既能支持多种结构化布局，也能让元素完全自由地摆放。有时需要更规整的布局，这时可以使用自动布局系统：它支持嵌套的水平组、垂直组和网格组，也可以根据内容自动调整元素大小。例如，按钮可以根据文字内容和内边距动态调整到刚好合适的尺寸。

自动布局建立在基础 Rect Transform 布局系统之上，可以只用于部分元素，也可以用于全部元素。

## 理解布局元素

自动布局围绕两类对象工作：布局元素和布局控制器。

布局元素是带有 Rect Transform 的 GameObject（也可以带有其他组件）。它知道自己适合使用多大的空间，但不会直接设置自己的尺寸；布局控制器会读取这些信息并据此计算最终尺寸。布局元素提供以下属性：

- 最小宽度（Minimum width）
- 最小高度（Minimum height）
- 最大宽度（Maximum width）
- 最大高度（Maximum height）
- 首选宽度（Preferred width）
- 首选高度（Preferred height）
- 可伸缩宽度（Flexible width）
- 可伸缩高度（Flexible height）

使用这些信息的布局控制器包括 Content Size Fitter 和各种 Layout Group。布局组给子元素分配尺寸时，基本顺序如下：

1. 先分配最小尺寸。
2. 如果有足够空间，再分配首选尺寸。
3. 如果仍有剩余空间，再分配可伸缩尺寸。

任何带 Rect Transform 的 GameObject 都可以作为布局元素。默认情况下，它的最小、首选和可伸缩尺寸都是 0。某些组件会改变这些布局属性，例如 Image 和 Text 会将首选宽高改为匹配精灵或文字内容。

## Layout Element 组件

如果需要覆盖最小、首选或可伸缩尺寸，可以向 GameObject 添加 Layout Element 组件。

![Layout Element 检查器](UI_LayoutElementInspector.png)

Layout Element 可以覆盖一个或多个布局属性。勾选想要覆盖的属性，然后填写覆盖值。更多字段说明参见 [Layout Element](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-LayoutElement.html)。

## 理解布局控制器

布局控制器是控制一个或多个布局元素（即带 Rect Transform 的 GameObject）的尺寸，并且可能控制其位置的组件。它可以控制：

- 自身布局元素，即组件所在的 GameObject；
- 子布局元素。

同一个组件也可以同时充当布局控制器和布局元素。

### Content Size Fitter

Content Size Fitter 是控制自身布局元素尺寸的布局控制器。最简单的示例是：给带 Text 组件的 GameObject 添加 Content Size Fitter。

![Content Size Fitter 检查器](UI_ContentSizeFitterInspector.png)

将 Horizontal Fit 或 Vertical Fit 设置为 Preferred 后，Rect Transform 会调整宽度或高度以适应 Text 内容。更多信息参见 [Content Size Fitter](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-ContentSizeFitter.html)。

### Aspect Ratio Fitter

Aspect Ratio Fitter 同样控制自身布局元素的尺寸。

![Aspect Ratio Fitter 检查器](UI_AspectRatioFitterInspector.png)

它可以根据宽度调整高度，或根据高度调整宽度；也可以让元素适应父元素内部，或包住整个父元素。Aspect Ratio Fitter 不会考虑最小尺寸、首选尺寸等布局信息。更多信息参见 [Aspect Ratio Fitter](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-AspectRatioFitter.html)。

### Layout Groups

Layout Group 是控制子布局元素尺寸和位置的布局控制器。例如：

- Horizontal Layout Group 将子元素依次水平排列；
- Vertical Layout Group 将子元素依次垂直排列；
- Grid Layout Group 将子元素排列成网格。

布局组不会控制自己的尺寸，而是自身作为一个布局元素，由其他布局控制器控制，或者手动设置尺寸。无论布局组被分配到多大空间，它通常都会根据子元素报告的最小、首选和可伸缩尺寸，尽量为每个子元素分配合适的空间。布局组可以任意嵌套。

更多信息参见 [Horizontal Layout Group](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-HorizontalLayoutGroup.html)、[Vertical Layout Group](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-VerticalLayoutGroup.html) 和 [Grid Layout Group](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-GridLayoutGroup.html)。

## Driven Rect Transform 属性

自动布局中的布局控制器可以自动控制 UI 元素的尺寸和位置，因此不应同时在 Inspector 或 Scene View 中手动编辑这些值。手动修改的值会在下一次布局计算时被布局控制器重置。

Rect Transform 使用“驱动属性”（driven properties）解决这个问题。例如，当 Content Size Fitter 的 Horizontal Fit 设置为 Minimum 或 Preferred 时，它会驱动同一个 GameObject 的 Rect Transform 宽度。Inspector 中的宽度会显示为只读，Rect Transform 顶部也会出现提示，说明有一个或多个属性正由 Content Size Fitter 驱动。

驱动属性还有一个重要作用：布局可能仅因 Game View 的分辨率或尺寸变化而改变。如果这些变化会修改驱动属性，却把修改标记为场景未保存，就会造成不必要的脏场景状态。因此，驱动属性不会保存到场景中，修改它们也不会将场景标记为已修改。

## 技术细节

UGUI 内置了一些自动布局组件，也可以通过实现特定接口来编写自定义布局组件。

### 布局接口

- 实现 `ILayoutElement` 的组件会被自动布局系统视为布局元素。
- 实现 `ILayoutGroup` 的组件应当负责驱动其子元素的 Rect Transform。
- 实现 `ILayoutSelfController` 的组件应当负责驱动自身的 Rect Transform。

### 布局计算顺序

自动布局系统按以下顺序评估并执行布局：

1. 调用 `ILayoutElement` 组件的 `CalculateLayoutInputHorizontal`，计算布局元素的最小、首选和可伸缩宽度。计算采用自底向上的顺序：先计算子元素，再计算父元素，使父元素能够将子元素的信息纳入自己的计算。
2. 调用 `ILayoutController` 组件的 `SetLayoutHorizontal`，计算并设置布局元素的实际宽度。计算采用自顶向下的顺序：先计算父元素，再计算子元素，因为子元素的宽度分配依赖父元素可提供的完整宽度。此步骤完成后，布局元素的 Rect Transform 已得到新的宽度。
3. 调用 `ILayoutElement` 组件的 `CalculateLayoutInputVertical`，计算最小、首选和可伸缩高度，顺序同样是自底向上。
4. 调用 `ILayoutController` 组件的 `SetLayoutVertical`，计算并设置实际高度，顺序同样是自顶向下。此步骤完成后，布局元素的 Rect Transform 已得到新的高度。

由此可见，自动布局先计算宽度，再计算高度。因此，计算出的高度可以依赖宽度，但计算出的宽度不能依赖高度。

### 触发布局重建

当组件属性发生变化、可能导致当前布局失效时，需要重新计算布局。可以调用：

```csharp
LayoutRebuilder.MarkLayoutForRebuild(transform as RectTransform);
```

重建不会立即发生，而是在当前帧结束、即将渲染之前发生。这是为了避免同一帧内重复重建布局，造成不必要的性能开销。

通常应在以下位置触发重建：

- 会改变布局的属性 setter 中；
- `OnEnable` 回调中；
- `OnDisable` 回调中；
- `OnRectTransformDimensionsChange` 回调中；
- `OnValidate` 回调中（仅编辑器需要，运行时不需要）；
- `OnDidApplyAnimationProperties` 回调中。

