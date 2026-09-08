# 让 UI 元素适配内容大小（Making UI Elements Fit the Size of Their Content）

通常，使用 Rect Transform 定位 UI 元素时，其位置和大小都是手动指定的（也可以选择让它随父级 Rect Transform 拉伸）。

不过，有时你希望矩形能够根据 UI 元素的内容自动调整大小。这可以通过添加名为 **Content Size Fitter**（内容尺寸适配器）的组件来实现。

## 适配文本大小（Fit to Size of Text）

要使带有 Text 组件的 Rect Transform 适配文本内容，请在同一游戏对象（拥有 Text 组件的那个）上添加 Content Size Fitter 组件，然后将 **Horizontal Fit**（水平适配）和 **Vertical Fit**（垂直适配）两个下拉选项都设置为 **Preferred**（首选）。

## 原理是什么？（How Does It Work?）

这里发生的事情是：Text 组件充当 **Layout Element**（布局元素），能够提供其最小尺寸（minimum size）和首选尺寸（preferred size）的信息。在手动布局中，这些信息不会被使用。Content Size Fitter 是一种 **Layout Controller**（布局控制器），它会监听 Layout Element 提供的布局信息，并据此控制 Rect Transform 的大小。

## 记住轴心点（Remember the Pivot）

当 UI 元素自动调整大小以适应内容时，应特别注意 Rect Transform 的**轴心点**（pivot）。元素调整大小时，轴心点保持不动，因此通过设置轴心点位置，可以控制元素向哪个方向扩展或收缩。例如，如果轴心点在中心，元素会向所有方向均匀扩展；如果轴心点在左上角，元素会向右和向下扩展。

## 让带子文本的 UI 元素适配大小（Fit to Size of UI Element with Child Text）

如果你有一个 UI 元素（例如 Button），它带有背景图片和一个包含 Text 组件的子游戏对象，你可能会希望整个 UI 元素适配文本的大小——也许还要加上一些内边距（padding）。

为此，首先在 UI 元素上添加 **Horizontal Layout Group**（水平布局组），再添加 Content Size Fitter。将 Horizontal Fit、Vertical Fit（或两者）设置为 Preferred。可以使用 Horizontal Layout Group 的 **Padding**（内边距）属性来添加和调整内边距。

为什么要用 Horizontal Layout Group？用 **Vertical Layout Group**（垂直布局组）也可以——只要组内只有一个子对象，两者产生的结果相同。

## 原理是什么？（How Does It Work?）

Horizontal（或 Vertical）Layout Group 同时充当 Layout Controller 和 Layout Element。首先，它监听组内子对象（本例中即子 Text）提供的布局信息；然后确定组需要多大（最小尺寸和首选尺寸）才能容纳所有子对象，并以 Layout Element 的身份提供这些最小/首选尺寸信息。

Content Size Fitter 监听同一游戏对象上任何 Layout Element 提供的布局信息——本例中来自 Horizontal（或 Vertical）Layout Group。根据其设置，它据此控制 Rect Transform 的大小。

一旦 Rect Transform 的大小确定，Horizontal（或 Vertical）Layout Group 就会根据可用空间来定位和调整其子对象的大小。关于它如何控制子对象位置和大小的更多信息，请参见 [Horizontal Layout Group](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-HorizontalLayoutGroup.html) 页面。

## 让布局组的子元素分别适配各自内容（Make Children of a Layout Group Fit Their Respective Sizes）

如果你有一个 Layout Group（水平或垂直），希望组内每个 UI 元素都适配各自的内容，该怎么办？

你不能在每个子元素上都放一个 Content Size Fitter。原因是：Content Size Fitter 想要控制自己的 Rect Transform，而父级 Layout Group 也想控制子元素的 Rect Transform，这会产生冲突，导致未定义行为。

不过也没有必要这么做。父级 Layout Group 本身就能让每个子元素适配内容大小。你需要做的是关闭 Layout Group 上的 **Child Force Expand**（子元素强制扩展）开关。如果子元素本身也是 Layout Group，可能还需要关闭它们的 Child Force Expand 开关。

一旦子元素不再以弹性宽度（flexible width）扩展，就可以在 Layout Group 中使用 **Child Alignment**（子元素对齐）设置来指定它们的对齐方式。

如果你希望某些子元素扩展以填满额外的可用空间，而其他子元素不扩展，该怎么办？只需在要扩展的子元素上添加 **Layout Element** 组件，并启用这些 Layout Element 上的 **Flexible Width**（弹性宽度）或 **Flexible Height**（弹性高度）属性。父级 Layout Group 仍应关闭 Child Force Expand 开关，否则所有子元素都会弹性扩展。

## 原理是什么？（How Does It Work?）

一个游戏对象可以有多个组件，各自提供关于最小、首选和弹性尺寸的布局信息。一个优先级系统决定哪些值生效。Layout Element 组件的优先级高于 Text、Image 和 Layout Group 组件，因此可以用它来覆盖它们提供的任何布局信息值。

当 Layout Group 监听子元素提供的布局信息时，它会考虑被覆盖后的弹性尺寸。然后在控制子元素大小时，不会让它们超过首选尺寸。但是，如果 Layout Group 启用了 Child Force Expand 选项，它总是会让所有子元素的弹性尺寸至少为 1。

## 更多信息（More Information）

本页介绍了几个常见用例的解决方案。有关自动布局系统的更深入说明，请参见 [UI Auto Layout](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/UIAutoLayout.html) 页面。
