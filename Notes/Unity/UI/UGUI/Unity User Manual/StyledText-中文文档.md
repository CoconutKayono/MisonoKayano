# 富文本（Rich Text）

> 来源：[Unity UGUI 2.6 — Rich Text](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/StyledText.html)  
> 官方源文件：[uGUI/Documentation~/StyledText.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/StyledText.md)  
> 整理日期：2026-09-05

UI 元素和文本网格中的文字可以包含多种字体样式和字号。UGUI 和旧版 GUI 系统都支持富文本。Text、GUIStyle、GUIText 和 TextMesh 类都有 **Rich Text** 设置，用于指示 Unity 在文字中查找标记标签。

`Debug.Log` 也可以使用这些标签来增强代码产生的错误报告。标签不会直接显示出来，而是表示应用到文字上的样式变化。

## 标记格式

富文本标记系统受 HTML 启发，但并不追求与标准 HTML 严格兼容。基本方式是将一段文字包在一对匹配的标签中：

```text
We are <b>not</b> amused.
```

标签是放在尖括号 `<` 和 `>` 中的文字。开标签放在文字段落的开头，标签内的文字是标签名（示例中为 `b`）。段落末尾放置闭标签，闭标签的名称与开标签相同，但前面加 `/`。

每个开标签都必须有对应的闭标签。如果不闭合开标签，Unity 会将其作为普通文字渲染。标签本身不会直接显示给用户，而是被解释为对其中文字进行样式处理的指令。上例中的 `b` 标签会让 `not` 以粗体显示。

![粗体富文本效果](StyleTextBold.png)

包含标签及其包围文字的标记段落称为一个元素。

## 嵌套元素

可以将一个元素嵌套在另一个元素中，从而对同一段文字应用多个样式：

```text
We are <b><i>definitely not</i></b> amused
```

`<i>` 标签应用斜体，因此显示效果为 “We are definitely not amused”。闭标签的顺序与开标签相反，因为内部标签不一定覆盖最外层元素的全部文字。

![粗体与斜体嵌套效果 1](StyleTextBoldItalic1.png)

例如：

```text
We are <b>absolutely <i>definitely</i> not</b> amused
```

显示为 “We are absolutely definitely not amused”，其中 `absolutely definitely not` 为粗体，`definitely` 同时为斜体。

![粗体与斜体嵌套效果 2](StyleTextBoldItalic2.png)

## 标签参数

有些标签只有开和关两种效果，另一些标签则允许变化。例如，`color` 标签需要知道要应用什么颜色。这样的信息通过参数加入标签：

```text
We are <color=green>green</color> with envy
```

![绿色富文本效果](StyleTextColorGreen.png)

结束标签不包含参数值。参数值可以用引号包裹，但不是必须的。标签参数不能包含空格，因此以下写法无效：

```text
We are <color = green>green</color> with envy
```

原因是 `=` 两侧存在空格。

## 支持的标签

以下标签是 Unity 支持的全部样式标签。

| 标签 | 说明 | 示例 | 注意 |
| --- | --- | --- | --- |
| `b` | 以粗体渲染文字。 | `We are <b>not</b> amused.` | — |
| `i` | 以斜体渲染文字。 | `We are <i>usually</i> not amused.` | — |
| `size` | 根据参数值设置文字大小，单位为像素。 | `We are <size=50>largely</size> unaffected.` | `Debug.Log` 也支持，但字号过大时，窗口标题栏和 Console 的行距可能看起来异常。 |
| `color` | 根据参数值设置文字颜色。 | `We are <color=#ff0000ff>colorfully</color> amused` | 支持 HTML 风格的 `#rrggbbaa` 十六进制值，也支持颜色名称。 |
| `material` | 仅对文本网格有用。根据参数指定的材质渲染文字片段；参数是 Inspector 中 Text Mesh 材质数组的索引。 | `We are <material=2>texturally</material> amused` | — |
| `quad` | 仅对文本网格有用。将图像内嵌到文字中。 | `<quad material=1 size=20 x=0.1 y=0.1 width=0.5 height=0.5 />` | 它是自闭合标签，不包围文字；末尾使用 `/` 表示结束。参数分别指定材质、图像高度，以及图像中要显示的矩形区域。 |

### color 标签的十六进制值

颜色可以用传统 HTML 格式指定：`#rrggbbaa`，其中每两个十六进制数字分别表示红、绿、蓝和 Alpha（透明度）。例如，完全不透明的青色为 `#00ffffff`。十六进制数字不区分大小写，`#FF0000` 与 `#ff0000` 等价。

颜色名称更易读，但可用颜色范围有限，并且默认始终为完全不透明，例如：

```text
<color=cyan>some text</color>
```

## 支持的颜色

以下颜色名称可以替代 `<color>` 标签中的十六进制值。

| 颜色名 | 十六进制值 | 色板 |
| --- | --- | --- |
| `aqua`（同 `cyan`） | `#00ffffff` | ![cyan](CyanSwatch.png) |
| `black` | `#000000ff` | ![black](BlackSwatch.png) |
| `blue` | `#0000ffff` | ![blue](BlueSwatch.png) |
| `brown` | `#a52a2aff` | ![brown](BrownSwatch.png) |
| `cyan`（同 `aqua`） | `#00ffffff` | ![cyan](CyanSwatch.png) |
| `darkblue` | `#0000a0ff` | ![darkblue](DarkblueSwatch.png) |
| `fuchsia`（同 `magenta`） | `#ff00ffff` | ![magenta](MagentaSwatch.png) |
| `green` | `#008000ff` | ![green](GreenSwatch.png) |
| `grey` | `#808080ff` | ![grey](GreySwatch.png) |
| `lightblue` | `#add8e6ff` | ![lightblue](LightblueSwatch.png) |
| `lime` | `#00ff00ff` | ![lime](LimeSwatch.png) |
| `magenta`（同 `fuchsia`） | `#ff00ffff` | ![magenta](MagentaSwatch.png) |
| `maroon` | `#800000ff` | ![maroon](MaroonSwatch.png) |
| `navy` | `#000080ff` | ![navy](NavySwatch.png) |
| `olive` | `#808000ff` | ![olive](OliveSwatch.png) |
| `orange` | `#ffa500ff` | ![orange](OrangeSwatch.png) |
| `purple` | `#800080ff` | ![purple](PurpleSwatch.png) |
| `red` | `#ff0000ff` | ![red](RedSwatch.png) |
| `silver` | `#c0c0c0ff` | ![silver](SilverSwatch.png) |
| `teal` | `#008080ff` | ![teal](TealSwatch.png) |
| `white` | `#ffffffff` | ![white](WhiteSwatch.png) |
| `yellow` | `#ffff00ff` | ![yellow](YellowSwatch.png) |

## Editor GUI

编辑器 GUI 系统默认禁用富文本，但可以使用自定义 GUIStyle 显式启用。将 `richText` 属性设置为 `true`，然后将样式传给对应的 GUI 函数：

```csharp
GUIStyle style = new GUIStyle();
style.richText = true;
GUILayout.Label("<size=30>Some <color=yellow>RICH</color> text</size>", style);
```
