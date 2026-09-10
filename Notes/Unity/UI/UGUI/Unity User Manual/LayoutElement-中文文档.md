# Layout Element（布局元素）

> 来源：[Unity UGUI 2.6 — Layout Element](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-LayoutElement.html)  
> 官方源文件：[uGUI/Documentation~/script-LayoutElement.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/script-LayoutElement.md)  
> 整理日期：2026-09-05

如果需要覆盖布局元素的最小尺寸、首选尺寸或可伸缩尺寸，可以向 GameObject 添加 **Layout Element** 组件。

## 布局控制器如何分配空间

布局控制器按照下面的顺序为布局元素分配宽度或高度：

1. 首先分配最小尺寸（**Min Width**、**Min Height**）。
2. 如果有足够的可用空间，再分配首选尺寸（**Preferred Width**、**Preferred Height**）。
3. 如果仍有额外空间，最后按照可伸缩尺寸（**Flexible Width**、**Flexible Height**）分配剩余空间。

有关最小、首选和可伸缩尺寸的完整说明，请参阅 [自动布局](UIAutoLayout-中文文档.md)。

## 属性

![Layout Element Inspector](UI_LayoutElementInspector.png)

启用某个宽度或高度属性后，该属性右侧会出现数值输入框，可以输入准确的宽度或高度。**Min** 和 **Preferred** 使用普通单位；**Flexible** 使用相对单位。

| 属性 | 说明 |
| --- | --- |
| **Ignore Layout** | 启用后，布局系统会忽略此布局元素。 |
| **Min Width** | 指定布局元素的最小宽度。 |
| **Min Height** | 指定布局元素的最小高度。 |
| **Max Width** | 指定布局元素的最大宽度。 |
| **Max Height** | 指定布局元素的最大高度。 |
| **Preferred Width** | 指定布局元素在分配额外宽度之前的首选宽度。 |
| **Preferred Height** | 指定布局元素在分配额外高度之前的首选高度。 |
| **Flexible Width** | 定义此元素相对于同级元素应占用的额外可用宽度比例。 |
| **Flexible Height** | 定义此元素相对于同级元素应占用的额外可用高度比例。 |
| **Layout Priority** | 此组件的布局优先级。当同一个 GameObject 上有多个组件提供布局属性（例如 Image 和 Layout Element）时，布局系统使用 **Layout Priority** 最高的组件的属性值。如果优先级相同，则每个属性分别取这些组件中的最高值。 |

## 说明

Layout Element 可以覆盖一个或多个布局属性。勾选想要覆盖的属性，然后输入覆盖值即可。未勾选的属性仍由同一个 GameObject 上的其他布局元素组件提供，例如 Text、Image 或 Layout Group。

最小尺寸、最大尺寸和首选尺寸使用普通单位；可伸缩尺寸使用相对单位。如果任意布局元素的可伸缩尺寸大于 0，布局控制器就会尝试填满全部可用空间。同级元素之间的相对可伸缩尺寸决定各自分到的比例。实际项目中，**Flexible Width** 和 **Flexible Height** 最常见的值是 0 或 1。

同时指定首选尺寸和可伸缩尺寸在某些情况下很有用。布局控制器只有在所有首选尺寸都分配完之后，才会分配可伸缩尺寸。因此，只指定可伸缩尺寸而不指定首选尺寸的元素，会先保持在最小尺寸，等其他元素达到首选尺寸后才开始利用剩余空间增长。若同时指定首选尺寸，它就能先与其他元素一起增长到首选尺寸，之后再继续分配额外空间。

## 使用要点

- 用 **Preferred Width/Height** 给按钮、提示框或卡片设置稳定的目标尺寸。
- 用 **Flexible Width/Height** 让某个子元素在布局组中吸收剩余空间。
- 如果希望某个子元素不参与父级布局，启用 **Ignore Layout**。
- 若同一对象同时有 Text、Image、Layout Group 等组件，使用 **Layout Priority** 明确哪个组件提供布局数据。
