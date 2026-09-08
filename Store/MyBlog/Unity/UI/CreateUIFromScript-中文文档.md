# 通过脚本创建 UI 元素（Creating UI Elements from Scripting）

> 来源：[Unity UGUI 2.6 — Creating UI Elements from Scripting](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/HOWTO-UICreateFromScripting.html)  
> 官方源文件：[uGUI/Documentation~/HOWTO-UICreateFromScripting.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/HOWTO-UICreateFromScripting.md)  
> 整理日期：2026-09-05

如果你正在创建一个动态 UI，其中 UI 元素会根据用户操作或游戏中的其他操作而出现、消失或变化，你可能需要编写一个脚本，基于自定义逻辑实例化（instantiate）新的 UI 元素。

## 创建 UI 元素的预制件（Creating a Prefab of the UI Element）

为了能够方便地动态实例化 UI 元素，第一步是为你想要实例化的 UI 元素类型创建一个预制件（prefab）。先在场景中把 UI 元素设置成你想要的外观，然后把它拖到 Project 视图中，使其成为预制件。

例如，按钮的预制件可以是一个带 Image 组件和 Button 组件的游戏对象，以及一个带 Text 组件的子游戏对象。根据你的需求，设置可能有所不同。

你可能会疑惑，为什么我们没有提供创建各种控件的 API 方法（包括视觉表现等一切）。原因是：例如一个按钮可以有无穷多种设置方式。它用图片、文本，还是两者都用？也许还要多张图片？文本的字体、颜色、字号和对齐方式是什么？图片应该使用哪个（些）精灵（sprite）？通过让你制作预制件并实例化它，你可以完全按照想要的方式设置它。而且，如果你以后想改变 UI 的外观和感觉，只需修改预制件，改动就会反映到你的 UI 中，包括动态创建的 UI。

## 实例化 UI 元素（Instantiating the UI Element）

UI 元素的预制件像平常一样使用 `Instantiate` 方法实例化。为实例化的 UI 元素设置父对象时，建议使用 `Transform.SetParent` 方法，并将 `worldPositionStays` 参数设为 `false`。

## 定位 UI 元素（Positioning the UI Element）

UI 元素通常使用其 Rect Transform 来定位。如果 UI 元素是 Layout Group 的子对象，它会被自动定位，可以跳过定位步骤。

定位 Rect Transform 时，最好先确定它是否具有（或应该具有）拉伸（stretching）行为。当 `anchorMin` 和 `anchorMax` 属性不完全相同时，就会发生拉伸行为。

对于非拉伸的 Rect Transform，最简单的方法是通过设置 `anchoredPosition` 和 `sizeDelta` 属性来定位。`anchoredPosition` 指定轴心点（pivot）相对于锚点（anchors）的位置；在没有拉伸的情况下，`sizeDelta` 就是尺寸本身。

对于拉伸的 Rect Transform，使用 `offsetMin` 和 `offsetMax` 属性来定位会更简单。`offsetMin` 属性指定矩形左下角相对于左下锚点的位置；`offsetMax` 属性指定矩形右上角相对于右上锚点的位置。

## 自定义 UI 元素（Customizing the UI Element）

如果你要动态实例化多个 UI 元素，不太可能希望它们看起来都一样、行为也都一样。无论是菜单中的按钮、库存中的物品还是其他东西，你都可能希望各个项目有不同的文本或图片，并在交互时执行不同的操作。

要做到这一点，需要获取各个组件并修改它们的属性。请参阅 Image 和 Text 组件的脚本参考，以及如何在脚本中处理 UnityEvents。
