# Grid Layout Group（网格布局组）

> 来源：[Unity UGUI 2.6 — Grid Layout Group](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-GridLayoutGroup.html)  
> 官方源文件：[uGUI/Documentation~/script-GridLayoutGroup.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/script-GridLayoutGroup.md)  
> 整理日期：2026-09-05

**Grid Layout Group** 会把子布局元素排列成网格。

![Grid Layout Group Inspector](UI_GridLayoutGroupInspector.png)

## 属性

| 属性 | 说明 |
| --- | --- |
| **Padding** | 布局组边缘内侧的内边距。 |
| **Cell Size** | 组内每个布局元素使用的固定尺寸。 |
| **Spacing** | 网格单元之间的间距。 |
| **Start Corner** | 第一个元素所在的角。 |
| **Start Axis** | 放置元素时使用的主轴。选择 **Horizontal** 时先填满一整行再开始新行；选择 **Vertical** 时先填满一整列再开始新列。 |
| **Child Alignment** | 元素没有填满全部可用空间时使用的对齐方式。 |
| **Constraint** | 将网格限制为固定行数或列数，以帮助自动布局系统计算布局。 |

## 说明

与其他布局组不同，Grid Layout Group 会忽略子元素提供的最小、首选和可伸缩尺寸，而是使用自身 **Cell Size** 属性为所有子元素分配固定尺寸。

## Grid Layout Group 与自动布局

将 Grid Layout Group 用在自动布局系统中时，需要特别注意它与 [Content Size Fitter](ContentSizeFitter-中文文档.md) 的配合。自动布局系统独立计算水平尺寸和垂直尺寸，但网格中的行数取决于列数，列数也取决于行数，二者可能产生矛盾。

对于固定数量的单元格，行数和列数可以有多种组合。使用 **Constraint** 可以告诉布局系统你希望表格固定行数还是固定列数。

### 宽度可伸缩、高度固定

如果希望随着元素增加，网格水平方向扩展而垂直方向保持固定，可以设置：

- Grid Layout Group **Constraint**：**Fixed Row Count**；
- Content Size Fitter **Horizontal Fit**：**Preferred Size**；
- Content Size Fitter **Vertical Fit**：**Preferred Size** 或 **Unconstrained**。

如果 Vertical Fit 使用 **Unconstrained**，需要自行提供足够的网格高度，以容纳指定行数的单元格。

### 宽度固定、高度可伸缩

如果希望网格宽度固定，随着元素增加而垂直扩展，可以设置：

- Grid Layout Group **Constraint**：**Fixed Column Count**；
- Content Size Fitter **Horizontal Fit**：**Preferred Size** 或 **Unconstrained**；
- Content Size Fitter **Vertical Fit**：**Preferred Size**。

如果 Horizontal Fit 使用 **Unconstrained**，需要自行提供足够的网格宽度，以容纳指定列数的单元格。

### 宽度和高度都可伸缩

网格也可以同时让宽度和高度都可伸缩，但此时无法控制具体的行数和列数。网格会尽量让行数和列数接近。可以设置：

- Grid Layout Group **Constraint**：**Flexible**；
- Content Size Fitter **Horizontal Fit**：**Preferred Size**；
- Content Size Fitter **Vertical Fit**：**Preferred Size**。

## 使用建议

Grid Layout Group 适合缩略图、图标面板和固定单元格的物品栏。若每个子元素需要根据文本或图片内容拥有不同尺寸，应改用 Horizontal Layout Group 或 Vertical Layout Group，或者使用嵌套布局组。
