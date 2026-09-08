# Image 类

Image 是 UI 层级结构中带纹理的元素。

## 继承关系

`object` → `Graphic` → `MaskableGraphic` → `Image`

## 实现的接口

`ICanvasElement`、`IClippable`、`IMaskable`、`IMaterialModifier`、`ISerializationCallbackReceiver`、`ILayoutElement`、`ICanvasRaycastFilter`

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
[AddComponentMenu("UI (Canvas)/Image", 11)]
public class Image : MaskableGraphic, ICanvasElement, IClippable, IMaskable, IMaterialModifier, ISerializationCallbackReceiver, ILayoutElement, ICanvasRaycastFilter
```

## 构造函数

### Image()

声明：

```csharp
protected Image()
```

## 字段

### s_ETC1DefaultUI

声明：

```csharp
protected static Material s_ETC1DefaultUI
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Material` | |

## 属性

### alphaHitTestMinimumThreshold

Alpha 阈值：指定像素的 Alpha 值必须达到的最小值，事件才会被视为对该 Image 的一次“命中”。

声明：

```csharp
public float alphaHitTestMinimumThreshold { get; set; }
```

属性值：

| 类型      | 说明  |
| ------- | --- |
| `float` |     |

备注：

Alpha 值低于该阈值时，射线投射（raycast）事件将穿透该 Image。若值为 1，则只有完全不透明的像素才会在 Image 上注册射线投射事件。用于测试的 Alpha 仅取自图片的精灵（Sprite），而 Image 的 `UI.Graphic.color` 中的 Alpha 会被忽略。

`alphaHitTestMinimumThreshold` 默认值为 0；此时 Image 矩形内部的所有射线投射事件均被视为命中。若要使大于 0 的值生效，Image 所使用的 Sprite 必须具有可读的像素。这可以通过在该精灵的高级纹理导入设置（Texture Import Settings）中启用 Read/Write Enabled，并禁用该精灵的图集打包（atlassing）来实现。

示例：

```csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI; // Required when Using UI elements.

public class ExampleClass : MonoBehaviour
{
    public Image theButton;

    // Use this for initialization
    void Start()
    {
        theButton.alphaHitTestMinimumThreshold = 0.5f;
    }
}
```

### defaultETC1GraphicMaterial

默认 Canvas 的爱立信纹理压缩 1（ETC1）与 Alpha 材质的缓存。

声明：

```csharp
public static Material defaultETC1GraphicMaterial { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Material` | |

备注：

存储由 `GetETC1SupportedCanvasMaterial()` 返回的、支持 ETC1 的 Canvas 材质。注意：要使用 ETC1 与 Alpha 材质，请务必在 Always Included Shader（始终包含的着色器）列表中指定 `UI/DefaultETC1` 着色器。

### eventAlphaThreshold

声明：

```csharp
[Obsolete("eventAlphaThreshold has been deprecated. Use eventMinimumAlphaThreshold instead (UnityUpgradable) -> alphaHitTestMinimumThreshold", true)]
public float eventAlphaThreshold { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### fillAmount

当 `Image.type` 设置为 `Image.Type.Filled` 时，Image 的显示量。

声明：

```csharp
public float fillAmount { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

备注：

取值范围为 0–1：0 表示不显示任何内容，1 表示显示完整的 Image。

示例：

```csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI; // Required when Using UI elements.

public class Cooldown : MonoBehaviour
{
    public Image cooldown;
    public bool coolingDown;
    public float waitTime = 30.0f;

    // Update is called once per frame
    void Update()
    {
        if (coolingDown == true)
        {
            //Reduce fill amount over 30 seconds
            cooldown.fillAmount -= 1.0f / waitTime * Time.deltaTime;
        }
    }
}
```

### fillCenter

是否渲染平铺（Tiled）或九宫格（Sliced）图片的中心部分。

声明：

```csharp
public bool fillCenter { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

备注：

仅当 `Image.sprite` 具有边框时，此属性才会生效。

示例：

```csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class FillCenterScript : MonoBehaviour
{
    public Image xmasCalenderDoor;

    // removes the center of the image to reveal the image behind it
    void OpenCalendarDoor()
    {
        xmasCalenderDoor.fillCenter = false;
    }
}
```

### fillClockwise

Image 是否应顺时针填充（true）或逆时针填充（false）。

声明：

```csharp
public bool fillClockwise { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

备注：

仅当 `Image.type` 设置为 `Image.Type.Filled`，且 `Image.fillMethod` 设置为任意径向（Radial）方法时，此属性才会生效。

示例：

```csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI; // Required when Using UI elements.

public class FillClockwiseScript : MonoBehaviour
{
    public Image healthCircle;

    // This method sets the direction of the health circle.
    // Clockwise for the Player, Counter Clockwise for the opponent.
    void SetHealthDirection(GameObject target)
    {
        if (target.tag == "Player")
        {
            healthCircle.fillClockwise = true;
        }
        else if (target.tag == "Opponent")
        {
            healthCircle.fillClockwise = false;
        }
    }
}
```

### fillMethod

声明：

```csharp
public Image.FillMethod fillMethod { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Image.FillMethod` | |

### fillOrigin

控制填充过程的起点。不同的填充方法下，该值的含义不同。

声明：

```csharp
public int fillOrigin { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `int` | |

备注：

应根据 `Image.FillMethod` 将值转换为相应的原点类型：`Image.OriginHorizontal`、`Image.OriginVertical`、`Image.Origin90`、`Image.Origin180` 或 `Image.Origin360`。注意：仅当 `Image.type` 设置为 `Image.Type.Filled` 时，此属性才会生效。

示例：

```csharp
using UnityEngine;
using UnityEngine.UI;
using System.Collections;

[RequireComponent(typeof(Image))]
public class ImageOriginCycle : MonoBehaviour
{
    void OnEnable()
    {
        Image image = GetComponent<Image>();
        string fillOriginName = "";

        switch ((Image.FillMethod)image.fillMethod)
        {
            case Image.FillMethod.Horizontal:
                fillOriginName = ((Image.OriginHorizontal)image.fillOrigin).ToString();
                break;
            case Image.FillMethod.Vertical:
                fillOriginName = ((Image.OriginVertical)image.fillOrigin).ToString();
                break;
            case Image.FillMethod.Radial90:

                fillOriginName = ((Image.Origin90)image.fillOrigin).ToString();
                break;
            case Image.FillMethod.Radial180:

                fillOriginName = ((Image.Origin180)image.fillOrigin).ToString();
                break;
            case Image.FillMethod.Radial360:
                fillOriginName = ((Image.Origin360)image.fillOrigin).ToString();
                break;
        }
        Debug.Log(string.Format("{0} is using {1} fill method with the origin on {2}", name, image.fillMethod, fillOriginName));
    }
}
```

### flexibleHeight

参见 `ILayoutElement.flexibleHeight`。

声明：

```csharp
public virtual float flexibleHeight { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### flexibleWidth

参见 `ILayoutElement.flexibleWidth`。

声明：

```csharp
public virtual float flexibleWidth { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### hasBorder

图片的 Sprite 是否具有可用于九宫格的边框。

声明：

```csharp
public bool hasBorder { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### layoutPriority

参见 `ILayoutElement.layoutPriority`。

声明：

```csharp
public virtual int layoutPriority { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `int` | |

### mainTexture

Image 的纹理来自 `UnityEngine.Image`。

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

### material

此 Image 使用的指定材质。若未指定材质，则使用默认材质。

声明：

```csharp
public override Material material { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Material` | |

重写：

`Graphic.material`

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

参见 `ILayoutElement.minHeight`。

声明：

```csharp
public virtual float minHeight { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### minWidth

参见 `ILayoutElement.minWidth`。

声明：

```csharp
public virtual float minWidth { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### multipliedPixelsPerUnit

声明：

```csharp
protected float multipliedPixelsPerUnit { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### overrideSprite

设置一个用于渲染的替代精灵。

声明：

```csharp
public Sprite overrideSprite { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Sprite` | |

备注：

`overrideSprite` 变量允许更换精灵。此更改会立即生效。当不再需要更换后的精灵时，可以将精灵恢复为原始版本——将 `overrideSprite` 设为 `null` 即可。

示例：

注意：下面的脚本示例包含两个按钮。按钮的纹理从 `/Resources/` 文件夹加载（在所示示例中并未使用）。示例代码中添加了两个精灵。`/Example1/` 和 `/Example2/` 是由按钮的 OnClick 函数调用的函数。Example1 调用 `overrideSprite`，Example2 将 `overrideSprite` 设为 `null`。

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class ExampleClass : MonoBehaviour
{
private Sprite sprite1;
private Sprite sprite2;
private Image i;
public void Start()
{
    i = GetComponent<Image>();
    sprite1 = Resources.Load<Sprite>("texture1");
    sprite2 = Resources.Load<Sprite>("texture2");

    i.sprite = sprite1;
}

// Called by a Button OnClick() with ExampleClass.Example1
// Uses overrideSprite to make this change temporary
public void Example1()
{
    i.overrideSprite = sprite2;
}

// Called by a Button OnClick() with ExampleClass.Example2
// Removes the overrideSprite which causes the original sprite to be used again.
public void Example2()
{
    i.overrideSprite = null;
}

}
```

### pixelsPerUnit

声明：

```csharp
public float pixelsPerUnit { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### pixelsPerUnitMultiplier

每单位像素修饰符，用于改变九宫格精灵的生成方式。

声明：

```csharp
public float pixelsPerUnitMultiplier { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### preferredHeight

如果正在渲染精灵，则返回该精灵的大小。对于 Sliced 或 Tiled 精灵，则返回计算出的最小可能大小。

声明：

```csharp
public virtual float preferredHeight { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### preferredWidth

如果正在渲染精灵，则返回该精灵的大小。对于 Sliced 或 Tiled 精灵，则返回计算出的最小可能大小。

声明：

```csharp
public virtual float preferredWidth { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `float` | |

### preserveAspect

此图片是否应保持其 Sprite 的宽高比。

声明：

```csharp
public bool preserveAspect { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### sprite

用于渲染此图片的精灵。

声明：

```csharp
public Sprite sprite { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Sprite` | |

备注：

返回 Image 的源 Sprite。该 Sprite 也可以在 Inspector 中作为 Image 组件的一部分进行查看和更改，也可以通过脚本进行更改。

示例：

```csharp
//Attach this script to an Image GameObject and set its Source Image to the Sprite you would like.
//Press the space key to change the Sprite. Remember to assign a second Sprite in this script's section of the Inspector.

using UnityEngine;
using UnityEngine.UI;

public class Example : MonoBehaviour
{
    Image m_Image;
    //Set this in the Inspector
    public Sprite m_Sprite;

    void Start()
    {
        //Fetch the Image from the GameObject
        m_Image = GetComponent<Image>();
    }

    void Update()
    {
        //Press space to change the Sprite of the Image
        if (Input.GetKey(KeyCode.Space))
        {
            m_Image.sprite = m_Sprite;
        }
    }
}
```

### type

如何显示图片。

声明：

```csharp
public Image.Type type { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Image.Type` | |

备注：

根据预期的用途，Unity 可以以多种不同的方式解释 Image。可用于显示：

- 拉伸以适配 Image 的 RectTransform 的整幅图片。
- 适用于各种装饰性 UI 框及其他矩形元素的九宫格（9-sliced）图片。
- 重复精灵部分区域的平铺图片。
- 部分图片，适用于擦除、淡入淡出、计时器、状态条等。

### useSpriteMesh

允许你指定 UI Image 是使用 TextureImporter 生成的网格显示，还是使用简单的四边形网格显示。

声明：

```csharp
public bool useSpriteMesh { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

备注：

当此属性设置为 false 时，UI Image 使用简单的四边形。当设置为 true 时，UI Image 使用 TextureImporter 生成的精灵网格。如果你想使用基于图像 Alpha 值紧密贴合（tightly fitted）的精灵网格，则应将其设置为 true。注意：如果纹理导入器的 `SpriteMeshType` 属性设置为 `SpriteMeshType.FullRect`，则只会生成四边形，而不会生成紧密贴合的精灵网格，这意味着无论此属性的值如何，该 UI Image 都会以四边形绘制。因此，在启用此属性以使用紧密贴合的精灵网格时，还必须确保纹理导入器的 `SpriteMeshType` 属性设置为 `Tight`。

## 方法

### CalculateLayoutInputHorizontal()

参见 `ILayoutElement.CalculateLayoutInputHorizontal`。

声明：

```csharp
public virtual void CalculateLayoutInputHorizontal()
```

### CalculateLayoutInputVertical()

参见 `ILayoutElement.CalculateLayoutInputVertical`。

声明：

```csharp
public virtual void CalculateLayoutInputVertical()
```

### DisableSpriteOptimizations()

禁用所有自动精灵优化。

声明：

```csharp
public void DisableSpriteOptimizations()
```

备注：

当分配新的 Sprite 时，会自动应用更新优化。

### IsRaycastLocationValid(Vector2, Camera)

计算此图片的射线位置是否为有效的命中位置。会考虑 Alpha 测试阈值。

声明：

```csharp
public virtual bool IsRaycastLocationValid(Vector2 screenPoint, Camera eventCamera)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Vector2` | `screenPoint` | 要检查的屏幕坐标点 |
| `Camera` | `eventCamera` | 用于计算对应坐标的相机 |

返回值：

| 类型 | 说明 |
| --- | --- |
| `bool` | 该位置是否为有效命中 |

备注：

另请参见 `ICanvasRaycastFilter`。

### OnAfterDeserialize()

参见 `ISerializationCallbackReceiver`。

声明：

```csharp
public virtual void OnAfterDeserialize()
```

### OnBeforeSerialize()

参见 `ISerializationCallbackReceiver`。

声明：

```csharp
public virtual void OnBeforeSerialize()
```

### OnCanvasHierarchyChanged()

当父 Canvas 的状态发生改变时调用。

声明：

```csharp
protected override void OnCanvasHierarchyChanged()
```

重写：

`MaskableGraphic.OnCanvasHierarchyChanged()`

### OnDidApplyAnimationProperties()

声明：

```csharp
protected override void OnDidApplyAnimationProperties()
```

重写：

`Graphic.OnDidApplyAnimationProperties()`

### OnDisable()

清除引用。

声明：

```csharp
protected override void OnDisable()
```

重写：

`MaskableGraphic.OnDisable()`

### OnEnable()

将 Graphic 和 Canvas 标记为已发生更改。

声明：

```csharp
protected override void OnEnable()
```

重写：

`MaskableGraphic.OnEnable()`

### OnPopulateMesh(VertexHelper)

更新 UI 渲染器网格。

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

### OnValidate()

声明：

```csharp
protected override void OnValidate()
```

重写：

`MaskableGraphic.OnValidate()`

### SetNativeSize()

调整图像大小以使其像素完美。

声明：

```csharp
public override void SetNativeSize()
```

重写：

`Graphic.SetNativeSize()`

备注：

这意味着将 Image 的 `RectTransform.sizeDelta` 设置为与 Sprite 的尺寸相等。

### UpdateMaterial()

更新渲染器的材质。

声明：

```csharp
protected override void UpdateMaterial()
```

重写：

`Graphic.UpdateMaterial()`

## 实现的接口

- `ICanvasElement`
- `IClippable`
- `IMaskable`
- `IMaterialModifier`
- `ISerializationCallbackReceiver`
- `ILayoutElement`
- `ICanvasRaycastFilter`

---

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
