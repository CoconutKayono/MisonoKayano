# Text 类

## 继承关系

`object` → `Graphic` → `MaskableGraphic` → `Text`

## 实现的接口

`ICanvasElement`、`IClippable`、`IMaskable`、`IMaterialModifier`、`ILayoutElement`

## 继承的成员

- `MaskableGraphic.m_ShouldRecalculateStencil`
- `MaskableGraphic.m_MaskMaterial`
- `MaskableGraphic.onCullStateChanged`
- `MaskableGraphic.maskable`
- `MaskableGraphic.isMaskingGraphic`

命名空间：`UnityEngine.UI`

程序集：`UnityEngine.UI.dll`

## 语法

```csharp
[RequireComponent(typeof(CanvasRenderer))]
[AddComponentMenu("UI (Canvas)/Legacy/Text", 100)]
public class Text : MaskableGraphic, ICanvasElement, IClippable, IMaskable, IMaterialModifier, ILayoutElement
```

## 构造函数

### Text()

声明：

```csharp
protected Text()
```

## 字段

### m_DisableFontTextureRebuiltCallback

声明：

```csharp
[NonSerialized]
protected bool m_DisableFontTextureRebuiltCallback
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### m_Text

声明：

```csharp
[TextArea(3, 10)]
[SerializeField]
protected string m_Text
```

字段值：

| 类型       | 说明  |
| -------- | --- |
| `string` |     |

## 属性

### alignByGeometry

使用字形几何范围（glyph extents）而非字形度量（glyph metrics）来执行水平对齐。

声明：

```csharp
public bool alignByGeometry { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

备注：

这样可以获得更好的左右对齐效果，但在尝试将多个字体（例如专用轮廓字体）叠加在一起时，可能会导致定位不正确。

### alignment

文本在其 `RectTransform` 中的定位方式。

声明：

```csharp
public TextAnchor alignment { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `TextAnchor` | |

备注：

这是 Text 相对于其 RectTransform 的定位。你可以通过脚本更改它，也可以在 Text 组件的 Inspector 中使用 Alignment（对齐）部分的按钮进行更改。

示例：

```csharp
//Create a Text GameObject by going to __Create__>__UI__>__Text__. Attach this script to the GameObject to see it working.

using UnityEngine;
using UnityEngine.UI;

public class UITextAlignment : MonoBehaviour
{
    Text m_Text;

    void Start()
    {
        //Fetch the Text Component
        m_Text = GetComponent<Text>();
        //Switch the Text alignment to the middle
        m_Text.alignment = TextAnchor.MiddleCenter;
    }

//This is a legacy function used for an instant demonstration. See the <a href="https://unity3d.com/learn/tutorials/s/user-interface-ui">UI Tutorials pages </a> and [[wiki:UISystem|UI Section]] of the manual for more information on creating your own buttons etc.
    void OnGUI()
    {
        //Press this Button to change the Text alignment to the lower right
        if (GUI.Button(new Rect(0, 0, 100, 40), "Lower Right"))
        {
            m_Text.alignment = TextAnchor.LowerRight;
        }

        //Press this Button to change the Text alignment to the upper left
        if (GUI.Button(new Rect(150, 0, 100, 40), "Upper Left"))
        {
            m_Text.alignment = TextAnchor.UpperLeft;
        }
    }
}
```

### cachedTextGenerator

用于生成可见文本的缓存 `TextGenerator`。

声明：

```csharp
public TextGenerator cachedTextGenerator { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `TextGenerator` | |

### cachedTextGeneratorForLayout

确定布局时使用的缓存 `TextGenerator`。

声明：

```csharp
public TextGenerator cachedTextGeneratorForLayout { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `TextGenerator` | |

### flexibleHeight

当有多余可用空间时，此布局元素应获得的额外相对高度。

声明：

```csharp
public virtual float flexibleHeight { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

示例：

```csharp

using UnityEngine;
                        using System.Collections;
                        using UnityEngine.UI; // Required when using UI elements.

                        public class ExampleClass : MonoBehaviour
                        {
                            public Transform MyContentPanel;

                            //Sets the flexible height on on all children in the content panel.
                            public void Start()
                            {
                                //Assign all the children of the content panel to an array.
                                LayoutElement[] myLayoutElements = MyContentPanel.GetComponentsInChildren<LayoutElement>();

                                //For each child in the array change its LayoutElement's flexible height to 100.
                                foreach (LayoutElement element in myLayoutElements)
                                {
                                    element.flexibleHeight = 100f;
                                }
                            }
                        }

```

### flexibleWidth

当有多余可用空间时，此布局元素应获得的额外相对宽度。

声明：

```csharp
public virtual float flexibleWidth { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

备注：

将 `preferredWidth` 设为 -1 可移除优先宽度。

示例：

```csharp

using UnityEngine;
                        using System.Collections;
                        using UnityEngine.UI; // Required when using UI elements.

                        public class ExampleClass : MonoBehaviour
                        {
                            public Transform MyContentPanel;

                            //Sets the flexible height on on all children in the content panel.
                            public void Start()
                            {
                                //Assign all the children of the content panel to an array.
                                LayoutElement[] myLayoutElements = MyContentPanel.GetComponentsInChildren<LayoutElement>();

                                //For each child in the array change its LayoutElement's flexible width to 200.
                                foreach (LayoutElement element in myLayoutElements)
                                {
                                    element.flexibleWidth = 200f;
                                }
                            }
                        }

```

### font

文本使用的字体。

声明：

```csharp
public Font font { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Font` | |

备注：

这是 Text 组件使用的字体。用它来更改或获取 Text 的字体。网上有很多免费字体。

示例：

```csharp
//Create a new Text GameObject by going to Create>UI>Text in the Editor. Attach this script to the Text GameObject. Then, choose or click and drag your own font into the Font section in the Inspector window.

using UnityEngine;
using UnityEngine.UI;

public class TextFontExample : MonoBehaviour
{
    Text m_Text;
    //Attach your own Font in the Inspector
    public Font m_Font;

    void Start()
    {
        //Fetch the Text component from the GameObject
        m_Text = GetComponent<Text>();
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.Space))
        {
            //Change the Text Font to the Font attached in the Inspector
            m_Text.font = m_Font;
            //Change the Text to the message below
            m_Text.text = "My Font Changed!";
        }
    }
}
```

### fontSize

字体应渲染的大小。度量单位为磅（Points）。

声明：

```csharp
public int fontSize { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `int` | |

备注：

这是 Text 的字体大小，用于获取或更改字体大小。更改字体大小时，请记得考虑 Text 的 RectTransform：字号过大或文本过长时，可能放不进某些矩形尺寸，从而不会显示在场景中。注意：不同字体之间的磅值大小并不一致。

示例：

```csharp
//For this script to work, create a new Text GameObject by going to Create>U>Text. Attach the script to the Text GameObject. Make sure the GameObject has a RectTransform component.

using UnityEngine;
using UnityEngine.UI;

public class Example : MonoBehaviour
{
    Text m_Text;
    RectTransform m_RectTransform;

    void Start()
    {
        //Fetch the Text and RectTransform components from the GameObject
        m_Text = GetComponent<Text>();
        m_RectTransform = GetComponent<RectTransform>();
    }

    void Update()
    {
        //Press the space key to change the Font size
        if (Input.GetKey(KeyCode.Space))
        {
            changeFontSize();
        }
    }

    void changeFontSize()
    {
        //Change the Font Size to 16
        m_Text.fontSize = 30;

        //Change the RectTransform size to allow larger fonts and sentences
        m_RectTransform.sizeDelta = new Vector2(m_Text.fontSize * 10, 100);

        //Change the m_Text text to the message below
        m_Text.text = "I changed my Font size!";
    }
}
```

### fontStyle

Text 的文本使用的字体样式。

声明：

```csharp
public FontStyle fontStyle { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `FontStyle` | |

### horizontalOverflow

水平溢出模式。

声明：

```csharp
public HorizontalWrapMode horizontalOverflow { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `HorizontalWrapMode` | |

备注：

设置为 `HorizontalWrapMode.Overflow` 时，文本可以超出 Text 图形的水平边界；设置为 `HorizontalWrapMode.Wrap` 时，文本将自动换行以适配边界。

### layoutPriority

此组件的布局优先级。

声明：

```csharp
public virtual int layoutPriority { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `int` | |

备注：

如果同一 GameObject 上的多个组件实现了 `ILayoutElement` 接口，则返回较高优先级值的组件所提供的值优先；但小于零的值会被忽略。这样一来，组件可以只覆盖选定的属性，而把其余值保持为 -1 或其它小于零的值。

### lineSpacing

行距，以字体行高的倍率表示。值为 1 时产生正常行距。

声明：

```csharp
public float lineSpacing { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### mainTexture

Text 使用的纹理来自字体。

声明：

```csharp
public override Texture mainTexture { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Texture` | |

重写：

`Graphic.mainTexture`

### maxHeight

此布局元素可分配到的最大高度。

声明：

```csharp
public virtual float maxHeight { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### maxWidth

此布局元素可分配到的最大宽度。

声明：

```csharp
public virtual float maxWidth { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### minHeight

此布局元素可分配到的最小高度。

声明：

```csharp
public virtual float minHeight { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### minWidth

此布局元素可分配到的最小宽度。

声明：

```csharp
public virtual float minWidth { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### pixelsPerUnit

提供有关字体如何缩放以适应屏幕的信息。

声明：

```csharp
public float pixelsPerUnit { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

备注：

对于动态字体，该值等同于 Canvas 的缩放因子。对于非动态字体，该值根据请求的文本大小和字体本身的大小计算得出。

### preferredHeight

当有可用空间时，此布局元素应具有的首选高度。

声明：

```csharp
public virtual float preferredHeight { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

备注：

将 `PreferredHeight` 设为 -1 可移除该尺寸。

### preferredWidth

当有可用空间时，此布局元素应具有的首选宽度。

声明：

```csharp
public virtual float preferredWidth { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

备注：

将 `PreferredWidth` 设为 -1 可移除该尺寸。

### resizeTextForBestFit

是否允许文本自动调整大小。

声明：

```csharp
public bool resizeTextForBestFit { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### resizeTextMaxSize

文本允许的最大大小。1 = 无限大。

声明：

```csharp
public int resizeTextMaxSize { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `int` | |

### resizeTextMinSize

文本允许的最小大小。

声明：

```csharp
public int resizeTextMinSize { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `int` | |

### supportRichText

此 Text 是否支持富文本。

声明：

```csharp
public bool supportRichText { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### text

Text 正在显示的文本。

声明：

```csharp
public virtual string text { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `string` | |

备注：

这是 Text 组件的字符串值，用于读取或编辑 Text 中显示的文本。

示例：

```csharp
using UnityEngine;
using UnityEngine.UI;

public class Example : MonoBehaviour
{
    public Text m_MyText;

    void Start()
    {
        //Text sets your text to say this message
        m_MyText.text = "This is my text";
    }

    void Update()
    {
        //Press the space key to change the Text message
        if (Input.GetKey(KeyCode.Space))
        {
            m_MyText.text = "My text has now changed.";
        }
    }
}
```

### verticalOverflow

垂直溢出模式。

声明：

```csharp
public VerticalWrapMode verticalOverflow { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `VerticalWrapMode` | |

## 方法

### CalculateLayoutInputHorizontal()

调用此方法后，布局的水平输入属性应返回最新值；调用时，子级应已具备最新的水平布局输入。

声明：

```csharp
public virtual void CalculateLayoutInputHorizontal()
```

### CalculateLayoutInputVertical()

调用此方法后，布局的垂直输入属性应返回最新值；调用时，子级应已具备最新的垂直布局输入。

声明：

```csharp
public virtual void CalculateLayoutInputVertical()
```

### FontTextureChanged()

当与字体关联的纹理被修改时，由 `FontUpdateTracker` 调用。

声明：

```csharp
public void FontTextureChanged()
```

### GetGenerationSettings(Vector2)

用于填充文本生成设置的便捷函数。

声明：

```csharp
public TextGenerationSettings GetGenerationSettings(Vector2 extents)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Vector2` | `extents` | 文本可以绘制的范围。 |

返回值：

| 类型 | 说明 |
| --- | --- |
| `TextGenerationSettings` | 生成的设置。 |

### GetTextAnchorPivot(TextAnchor)

用于确定锚点向量偏移的便捷函数。

声明：

```csharp
public static Vector2 GetTextAnchorPivot(TextAnchor anchor)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `TextAnchor` | `anchor` | |

返回值：

| 类型 | 说明 |
| --- | --- |
| `Vector2` | |

### OnDisable()

清除引用。

声明：

```csharp
protected override void OnDisable()
```

重写：

`MaskableGraphic.OnDisable()`

### OnEnable()

将 Graphic 和 Canvas 标记为脏（dirty）。

声明：

```csharp
protected override void OnEnable()
```

重写：

`MaskableGraphic.OnEnable()`

### OnPopulateMesh(VertexHelper)

当 UI 元素需要生成顶点时调用的回调函数。填充顶点缓冲区数据。

声明：

```csharp
protected override void OnPopulateMesh(VertexHelper toFill)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `VertexHelper` | `toFill` | |

重写：

`Graphic.OnPopulateMesh(VertexHelper)`

备注：

例如，Text、UI.Image 和 RawImage 使用它来生成各自场景所需的顶点。

### OnRebuildRequested()

仅限编辑器的回调，当 Graphic 需要重建时由 Unity 发出。目前在资源被重新导入时发送。

声明：

```csharp
public override void OnRebuildRequested()
```

重写：

`Graphic.OnRebuildRequested()`

### OnValidate()

声明：

```csharp
protected override void OnValidate()
```

重写：

`MaskableGraphic.OnValidate()`

### Reset()

声明：

```csharp
protected override void Reset()
```

重写：

`Graphic.Reset()`

### UpdateGeometry()

调用此方法可将 Graphic 的几何体更新到 CanvasRenderer。

声明：

```csharp
protected override void UpdateGeometry()
```

重写：

`Graphic.UpdateGeometry()`

## 实现的接口

- `ICanvasElement`
- `IClippable`
- `IMaskable`
- `IMaterialModifier`
- `ILayoutElement`

---

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
