# 交互组件（Interaction Components）

> 来源：[Unity UGUI 2.6 — Interaction Components](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/UIInteractionComponents.html)  
> 官方源文件：[uGUI/Documentation~/UIInteractionComponents.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/UIInteractionComponents.md)  
> 整理日期：2026-09-05

本节介绍 UI 系统中负责交互的组件，包括鼠标或触摸事件，以及键盘或控制器输入。这些交互组件本身不可见，必须与一个或多个[可视组件](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/UIVisualComponents.html)组合使用，才能正常工作。

## 通用功能

大多数交互组件有一些共同点。它们属于 Selectable，这意味着它们共享以下内置功能：

- 可视化 Normal、Highlighted、Pressed、Disabled 等状态之间的过渡；
- 使用键盘或控制器导航到其他 Selectable。

这些共享功能在 [Selectable](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Selectable.html) 页面中说明。

交互组件至少包含一个 UnityEvent，用于定义用户以特定方式操作组件时要执行的行为。UI 系统会捕获并记录从绑定到 UnityEvent 的代码中传播出来的异常。

## Button（按钮）

Button 有一个 **OnClick** UnityEvent，用于定义被单击时执行的行为。

![Button 示例](UI_ButtonExample.png)

更多信息参见 [Button](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Button.html)。

## Toggle（开关）

Toggle 有一个 **Is On** 复选框，用于决定当前处于开启还是关闭状态。用户单击 Toggle 时，该值会翻转，也可以相应地显示或隐藏可视勾选标记。

Toggle 还提供 **OnValueChanged** UnityEvent，用于定义值改变时执行的行为。

![Toggle 示例](UI_ToggleExample.png)

更多信息参见 [Toggle](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Toggle.html)。

## Toggle Group（开关组）

Toggle Group 可用于将一组 Toggle 组成互斥集合。同一组中的 Toggle 被限制为同时只能选择一个：选择其中一个会自动取消选择其他 Toggle。

![Toggle Group 示例](UI_ToggleGroupExample.png)

更多信息参见 [Toggle Group](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-ToggleGroup.html)。

## Slider（滑动条）

Slider 有一个十进制 **Value**，用户可以在最小值和最大值之间拖动它。Slider 可以水平或垂直显示，并提供 **OnValueChanged** UnityEvent，用于定义值改变时执行的行为。

![Slider 示例](UI_SliderExample.png)

更多信息参见 [Slider](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Slider.html)。

## Scrollbar（滚动条）

Scrollbar 的 **Value** 是 0 到 1 之间的十进制数。用户拖动滚动条时，该值会相应改变。

Scrollbar 通常与 Scroll Rect 和 Mask 配合使用来创建滚动视图。它还具有 0 到 1 之间的 **Size** 值，用于决定滑块占整个滚动条长度的比例。另一个组件通常会控制这个值，用于表示滚动视图中当前可见内容所占的比例；Scroll Rect 可以自动完成这项工作。

Scrollbar 可以水平或垂直显示，也提供 **OnValueChanged** UnityEvent。

![Scrollbar 示例](UI_ScrollbarExample.png)

更多信息参见 [Scrollbar](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Scrollbar.html)。

## Dropdown（下拉框）

Dropdown 提供一个选项列表供用户选择。每个选项都可以指定文字，也可以选择性地指定图像；选项既可以在 Inspector 中设置，也可以通过代码动态设置。

Dropdown 提供 **OnValueChanged** UnityEvent，用于定义当前选项改变时执行的行为。

![Dropdown 示例](UI_DropdownExample.png)

更多信息参见 [Dropdown](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Dropdown.html)。

## Input Field（输入框）

Input Field 用于让用户编辑 Text Element 的内容。它提供 UnityEvent 来定义文本内容改变时执行的行为，也提供另一个 UnityEvent 来定义用户完成编辑时执行的行为。

更多信息参见 [Input Field](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-InputField.html)。

## Scroll Rect（滚动视图）

当内容占用空间很大、但需要在一个较小区域中显示时，可以使用 Scroll Rect。Scroll Rect 提供滚动这些内容的功能。

通常会将 Scroll Rect 与 Mask 组合使用来创建滚动视图，使 Scroll Rect 内的可滚动内容之外的部分不可见。还可以额外搭配一个或两个 Scrollbar，让用户通过拖动滚动条水平或垂直滚动。

更多信息参见 [Scroll Rect](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-ScrollRect.html)。

