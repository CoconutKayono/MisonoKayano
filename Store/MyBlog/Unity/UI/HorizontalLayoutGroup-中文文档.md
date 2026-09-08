# Horizontal Layout Group（水平布局组）

> 来源：[Unity UGUI 2.6 — Horizontal Layout Group](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-HorizontalLayoutGroup.html)  
> 官方源文件：[uGUI/Documentation~/script-HorizontalLayoutGroup.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/script-HorizontalLayoutGroup.md)  
> 整理日期：2026-09-05

**Horizontal Layout Group** 会把子布局元素并排放置。每个子元素的宽度根据它报告的最小宽度、首选宽度和可伸缩宽度计算。

## 宽度分配规则

布局组按照以下模型计算和分配宽度：

1. 将所有子布局元素的最小宽度相加，再加上子元素之间的间距，得到布局组的最小宽度。
2. 将所有子布局元素的首选宽度相加，再加上间距，得到布局组的首选宽度。
3. 当布局组处于最小宽度或更窄时，所有子元素都使用各自的最小宽度。
4. 布局组越接近首选宽度，每个子元素就越接近自己的首选宽度。
5. 当布局组宽于首选宽度时，额外空间会根据各子元素的可伸缩宽度按比例分配。

有关最小、首选和可伸缩尺寸的说明，请参阅 [自动布局](UIAutoLayout-中文文档.md)。

## 属性

![Horizontal Layout Group Inspector](images/UI_HorizontalLayoutGroupInspector.png)

| 属性 | 说明 |
| --- | --- |
| **Padding** | 布局组边缘内侧的内边距。 |
| **Spacing** | 子布局元素之间的间距。 |
| **Child Alignment** | 子元素没有填满全部可用空间时使用的对齐方式。 |
| **Control Child Size** | 是否由布局组控制子布局元素的宽度和高度。 |
| **Use Child Scale** | 布局组计算尺寸和排列元素时是否考虑子布局元素的缩放。**Width** 和 **Height** 分别对应子元素 Rect Transform 的 **Scale > X** 和 **Scale > Y**。使用 Animator Controller 不能为这些 Scale 值制作动画。 |
| **Child Force Expand** | 是否强制子布局元素扩展以填充额外的可用空间。 |

## 使用要点

- 水平菜单、按钮栏、工具栏和横向卡片列表通常适合使用 Horizontal Layout Group。
- 希望子元素按自身内容大小排列时，关闭对应方向的 **Child Force Expand**。
- 希望某个子元素吸收剩余空间时，在该子元素上添加 Layout Element，并设置 **Flexible Width**；同时通常应关闭父级的 Child Force Expand。
- **Control Child Size** 决定布局组是否直接控制子元素尺寸；关闭后，布局组仍可负责排列，但不会在对应方向强制设置子元素尺寸。
