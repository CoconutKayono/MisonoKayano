# Graphic 类

创建新的 Graphic 类型时，所有应从此类派生的 UI 组件的基类。

## 继承关系

`object` → `MonoBehaviour` → `UIBehaviour` → `Graphic` → `MaskableGraphic`、`RaycastReceiver`

## 实现的接口

`ICanvasElement`

## 继承的成员

- `UIBehaviour.Awake()`
- `UIBehaviour.Start()`
- `UIBehaviour.IsActive()`
- `UIBehaviour.OnCanvasGroupChanged()`
- `UIBehaviour.IsDestroyed()`

命名空间：`UnityEngine.UI`

程序集：`UnityEngine.UI.dll`

## 语法

```csharp
[DisallowMultipleComponent]
[RequireComponent(typeof(RectTransform))]
[ExecuteAlways]
public abstract class Graphic : UIBehaviour, ICanvasElement
```

## 构造函数

### Graphic()

声明：

```csharp
protected Graphic()
```

## 字段

### m_CachedMesh

声明：

```csharp
[NonSerialized]
protected Mesh m_CachedMesh
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Mesh` | |

### m_CachedUvs

声明：

```csharp
[NonSerialized]
protected Vector2[] m_CachedUvs
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Vector2[]` | |

### m_Material

声明：

```csharp
[FormerlySerializedAs("m_Mat")]
[SerializeField]
protected Material m_Material
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Material` | |

### m_OnDirtyLayoutCallback

声明：

```csharp
[NonSerialized]
protected UnityAction m_OnDirtyLayoutCallback
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `UnityAction` | |

### m_OnDirtyMaterialCallback

声明：

```csharp
[NonSerialized]
protected UnityAction m_OnDirtyMaterialCallback
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `UnityAction` | |

### m_OnDirtyVertsCallback

声明：

```csharp
[NonSerialized]
protected UnityAction m_OnDirtyVertsCallback
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `UnityAction` | |

### m_SkipLayoutUpdate

声明：

```csharp
[NonSerialized]
protected bool m_SkipLayoutUpdate
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### m_SkipMaterialUpdate

声明：

```csharp
[NonSerialized]
protected bool m_SkipMaterialUpdate
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### s_DefaultUI

声明：

```csharp
protected static Material s_DefaultUI
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Material` | |

### s_Mesh

声明：

```csharp
protected static Mesh s_Mesh
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Mesh` | |

### s_WhiteTexture

声明：

```csharp
protected static Texture2D s_WhiteTexture
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Texture2D` | |

## 属性

### canvas

此 Graphic 正在渲染到的 Canvas 的引用。

声明：

```csharp
public Canvas canvas { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Canvas` | |

备注：

如果 Graphic 在具有多个 Canvas 的层级结构中使用，将使用最靠近根节点的 Canvas。

### canvasRenderer

由此 Graphic 填充的 `CanvasRenderer` 的引用。

声明：

```csharp
public CanvasRenderer canvasRenderer { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `CanvasRenderer` | |

### color

Graphic 的基本颜色。

声明：

```csharp
public virtual Color color { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Color` | |

备注：

内置 UI 组件将此属性用作它们的顶点颜色。用它来获取或更改视觉 UI 元素（例如 Image）的颜色。

示例：

```csharp
//Place this script on a GameObject with a Graphic component attached e.g. a visual UI element (Image).

using UnityEngine;
using UnityEngine.UI;

public class Example : MonoBehaviour
{
    Graphic m_Graphic;
    Color m_MyColor;

    void Start()
    {
        //Fetch the Graphic from the GameObject
        m_Graphic = GetComponent<Graphic>();
        //Create a new Color that starts as red
        m_MyColor = Color.red;
        //Change the Graphic Color to the new Color
        m_Graphic.color = m_MyColor;
    }

    // Update is called once per frame
    void Update()
    {
        //When the mouse button is clicked, change the Graphic Color
        if (Input.GetKey(KeyCode.Mouse0))
        {
            //Change the Color over time between blue and red while the mouse button is pressed
            m_MyColor = Color.Lerp(Color.red, Color.blue, Mathf.PingPong(Time.time, 1));
        }
        //Change the Graphic Color to the new Color
        m_Graphic.color = m_MyColor;
    }
}
```

### defaultGraphicMaterial

如果未指定显式材质，用于绘制 UI 元素的默认材质。

声明：

```csharp
public static Material defaultGraphicMaterial { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Material` | |

### defaultMaterial

返回 Graphic 的默认材质。

声明：

```csharp
public virtual Material defaultMaterial { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Material` | |

### depth

Graphic 的绝对深度，用于渲染和事件——从最低到最高。

声明：

```csharp
public int depth { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `int` | |

示例：

深度是相对于第一个根 Canvas 的。

Canvas → Graphic - 1 → Graphic - 2 → 嵌套 Canvas → Graphic - 3 → Graphic - 4 → Graphic - 5

该值用于确定绘制和事件的顺序。

### mainTexture

Graphic 的纹理（只读）。

声明：

```csharp
public virtual Texture mainTexture { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Texture` | |

备注：

这是传递给 CanvasRenderer、Material，再到 Shader 的 `_MainTex` 的纹理。

实现自己的 Graphic 时，可以重写此属性来控制哪些纹理通过 UI 渲染管线。

请注意，Unity 会尝试将 UI 元素批量合批以提高性能，因此理想的做法是使用图集来减少 draw call 的数量。

### material

用户设置的材质。

声明：

```csharp
public virtual Material material { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Material` | |

### materialForRendering

将发送用于渲染的材质（只读）。

声明：

```csharp
public virtual Material materialForRendering { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Material` | |

备注：

这是实际发送到 CanvasRenderer 的材质。默认情况下它与 `Graphic.material` 相同。扩展 Graphic 时，你可以重写此属性，向 CanvasRenderer 发送与 `Graphic.material` 设置的不同材质。如果你想以非破坏性方式修改用户设置的材质，这会很有用。

### raycastPadding

应用于遮罩的边距：X = 左，Y = 下，Z = 右，W = 上。

声明：

```csharp
public Vector4 raycastPadding { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Vector4` | |

### raycastTarget

此 Graphic 是否应被视为射线投射（raycasting）的目标？

声明：

```csharp
public virtual bool raycastTarget { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### rectTransform

Graphic 使用的 RectTransform 组件。为速度而缓存。

声明：

```csharp
public RectTransform rectTransform { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `RectTransform` | |

### useLegacyMeshGeneration

声明：

```csharp
[Obsolete("useLegacyMeshGeneration is deprecated now that the legacy mesh generation is no longer supported.")]
protected bool useLegacyMeshGeneration { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### workerMesh

声明：

```csharp
protected static Mesh workerMesh { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Mesh` | |

## 方法

### CrossFadeAlpha(float, float, bool)

补间与此 Graphic 关联的 CanvasRenderer 颜色的 alpha。

声明：

```csharp
public virtual void CrossFadeAlpha(float alpha, float duration, bool ignoreTimeScale)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `float` | `alpha` | 目标 alpha。 |
| `float` | `duration` | 补间的持续时间（秒）。 |
| `bool` | `ignoreTimeScale` | 是否应忽略 `Time.scale`？ |

### CrossFadeColor(Color, float, bool, bool)

补间与此 Graphic 关联的 CanvasRenderer 颜色。

声明：

```csharp
public virtual void CrossFadeColor(Color targetColor, float duration, bool ignoreTimeScale, bool useAlpha)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Color` | `targetColor` | 目标颜色。 |
| `float` | `duration` | 补间持续时间。 |
| `bool` | `ignoreTimeScale` | 是否应忽略 `Time.scale`？ |
| `bool` | `useAlpha` | 是否也应补间 alpha 通道？ |

### CrossFadeColor(Color, float, bool, bool, bool)

补间与此 Graphic 关联的 CanvasRenderer 颜色。

声明：

```csharp
public virtual void CrossFadeColor(Color targetColor, float duration, bool ignoreTimeScale, bool useAlpha, bool useRGB)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Color` | `targetColor` | 目标颜色。 |
| `float` | `duration` | 补间持续时间。 |
| `bool` | `ignoreTimeScale` | 是否应忽略 `Time.scale`？ |
| `bool` | `useAlpha` | 是否也应补间 alpha 通道？ |
| `bool` | `useRGB` | 使用颜色还是 alpha 进行补间。 |

### GetPixelAdjustedRect()

返回最接近 Graphic RectTransform 的像素完美（pixel perfect）Rect。

声明：

```csharp
public Rect GetPixelAdjustedRect()
```

返回值：

| 类型 | 说明 |
| --- | --- |
| `Rect` | 一个像素完美的 Rect。 |

备注：

注意：仅当 Graphic 的根 Canvas 处于屏幕空间（Screen Space）时，此结果才准确。

### GraphicUpdateComplete()

当此 `ICanvasElement` 完成 Graphic 重建时发送的回调。

声明：

```csharp
public virtual void GraphicUpdateComplete()
```

### LayoutComplete()

当此 `ICanvasElement` 完成布局时发送的回调。

声明：

```csharp
public virtual void LayoutComplete()
```

### OnBeforeTransformParentChanged()

声明：

```csharp
protected override void OnBeforeTransformParentChanged()
```

重写：

`UIBehaviour.OnBeforeTransformParentChanged()`

### OnCanvasHierarchyChanged()

当父 Canvas 的状态发生改变时调用。

声明：

```csharp
protected override void OnCanvasHierarchyChanged()
```

重写：

`UIBehaviour.OnCanvasHierarchyChanged()`

### OnCullingChanged()

当 `CanvasRenderer.cull` 被修改时，必须调用此方法。

声明：

```csharp
public virtual void OnCullingChanged()
```

备注：

此方法可用于执行之前因 Graphic 被剔除（culled）而跳过的操作。

### OnDestroy()

声明：

```csharp
protected override void OnDestroy()
```

重写：

`UIBehaviour.OnDestroy()`

### OnDidApplyAnimationProperties()

声明：

```csharp
protected override void OnDidApplyAnimationProperties()
```

重写：

`UIBehaviour.OnDidApplyAnimationProperties()`

### OnDisable()

清除引用。

声明：

```csharp
protected override void OnDisable()
```

重写：

`UIBehaviour.OnDisable()`

### OnEnable()

将 Graphic 和 Canvas 标记为已发生更改。

声明：

```csharp
protected override void OnEnable()
```

重写：

`UIBehaviour.OnEnable()`

### OnPopulateMesh(Mesh)

当 UI 元素需要生成顶点时调用的回调函数。填充顶点缓冲区数据。

声明：

```csharp
[Obsolete("Use OnPopulateMesh(VertexHelper vh) instead.", true)]
protected virtual void OnPopulateMesh(Mesh m)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Mesh` | `m` | 要用 UI 数据填充的网格。 |

备注：

例如，Text、UI.Image 和 RawImage 使用它来生成各自用例专用的顶点。

### OnPopulateMesh(VertexHelper)

当 UI 元素需要生成顶点时调用的回调函数。填充顶点缓冲区数据。

声明：

```csharp
protected virtual void OnPopulateMesh(VertexHelper vh)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `VertexHelper` | `vh` | VertexHelper 工具。 |

备注：

例如，Text、UI.Image 和 RawImage 使用它来生成各自用例专用的顶点。

### OnRebuildRequested()

仅限编辑器的回调，当 Graphic 需要重建时由 Unity 发出。目前在资源被重新导入时发送。

声明：

```csharp
public virtual void OnRebuildRequested()
```

### OnRectTransformDimensionsChange()

当关联的 RectTransform 尺寸发生改变时调用此回调。它总是在 Awake、OnEnable 或 Start 之前调用。该调用也会对所有子 RectTransform 进行，无论它们的尺寸是否改变（这取决于它们的锚定方式）。

声明：

```csharp
protected override void OnRectTransformDimensionsChange()
```

重写：

`UIBehaviour.OnRectTransformDimensionsChange()`

### OnTransformParentChanged()

声明：

```csharp
protected override void OnTransformParentChanged()
```

重写：

`UIBehaviour.OnTransformParentChanged()`

### OnValidate()

声明：

```csharp
protected override void OnValidate()
```

重写：

`UIBehaviour.OnValidate()`

### PixelAdjustPoint(Vector2)

将给定像素调整为像素完美。

声明：

```csharp
public Vector2 PixelAdjustPoint(Vector2 point)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Vector2` | `point` | 局部空间坐标点。 |

返回值：

| 类型 | 说明 |
| --- | --- |
| `Vector2` | 像素完美调整后的点。 |

备注：

注意：仅当 Graphic 的根 Canvas 处于屏幕空间时，此结果才准确。

### Raycast(Vector2, Camera)

当 GraphicRaycaster 向场景投射射线时，它会做两件事。首先，使用元素的 RectTransform 矩形过滤元素。然后使用此 Raycast 函数确定射线命中的元素。

声明：

```csharp
public virtual bool Raycast(Vector2 sp, Camera eventCamera)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Vector2` | `sp` | 正在测试的屏幕坐标点。 |
| `Camera` | `eventCamera` | 用于测试的相机。 |

返回值：

| 类型 | 说明 |
| --- | --- |
| `bool` | 如果提供的点是 GraphicRaycaster 射线投射的有效位置，则为 True。 |

### Raycast(Vector2, Camera, bool)

当 GraphicRaycaster 向场景投射射线时，它首先根据元素的 RectTransform 矩形过滤元素，然后使用此 Raycast 函数确定哪些元素被命中。

声明：

```csharp
protected bool Raycast(Vector2 sp, Camera eventCamera, bool ignoreMasks)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Vector2` | `sp` | 正在测试的屏幕坐标点。 |
| `Camera` | `eventCamera` | 用于测试的相机。 |
| `bool` | `ignoreMasks` | 如果为 true，则忽略遮罩，遮罩不会阻止射线投射。 |

返回值：

| 类型 | 说明 |
| --- | --- |
| `bool` | 如果提供的点是 GraphicRaycaster 射线投射的有效位置，则为 True。 |

### Rebuild(CanvasUpdate)

在 PreRender 周期重建 Graphic 的几何体及其材质。

声明：

```csharp
public virtual void Rebuild(CanvasUpdate update)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `CanvasUpdate` | `update` | 渲染 CanvasUpdate 周期的当前步骤。 |

备注：

有关 Canvas 更新周期的更多详细信息，请参见 `CanvasUpdateRegistry`。

### RegisterDirtyLayoutCallback(UnityAction)

添加监听器，以便在 Graphic 的布局被标记为脏（dirty）时接收通知。

声明：

```csharp
public void RegisterDirtyLayoutCallback(UnityAction action)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `UnityAction` | `action` | 被调用时要调用的方法。 |

### RegisterDirtyMaterialCallback(UnityAction)

添加监听器，以便在 Graphic 的材质被标记为脏时接收通知。

声明：

```csharp
public void RegisterDirtyMaterialCallback(UnityAction action)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `UnityAction` | `action` | 被调用时要调用的方法。 |

### RegisterDirtyVerticesCallback(UnityAction)

添加监听器，以便在 Graphic 的顶点被标记为脏时接收通知。

声明：

```csharp
public void RegisterDirtyVerticesCallback(UnityAction action)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `UnityAction` | `action` | 被调用时要调用的方法。 |

### Reset()

声明：

```csharp
protected override void Reset()
```

重写：

`UIBehaviour.Reset()`

### SetAllDirty()

将 Graphic 的所有属性标记为脏并需要重建。将 Layout（布局）、Vertices（顶点）和 Materials（材质）都标记为脏。

声明：

```csharp
public virtual void SetAllDirty()
```

### SetLayoutDirty()

将布局标记为脏并需要重建。

声明：

```csharp
public virtual void SetLayoutDirty()
```

备注：

如果注册了任何元素，则发送 `OnDirtyLayoutCallback` 通知。参见 `RegisterDirtyLayoutCallback`。

### SetMaterialDirty()

将材质标记为脏并需要重建。

声明：

```csharp
public virtual void SetMaterialDirty()
```

备注：

如果注册了任何元素，则发送 `OnDirtyMaterialCallback` 通知。参见 `RegisterDirtyMaterialCallback`。

### SetNativeSize()

使 Graphic 具有其内容的原生大小。

声明：

```csharp
public virtual void SetNativeSize()
```

### SetRaycastDirty()

声明：

```csharp
public void SetRaycastDirty()
```

### SetVerticesDirty()

将顶点标记为脏并需要重建。

声明：

```csharp
public virtual void SetVerticesDirty()
```

备注：

如果注册了任何元素，则发送 `OnDirtyVertsCallback` 通知。参见 `RegisterDirtyVerticesCallback`。

### UnregisterDirtyLayoutCallback(UnityAction)

移除接收 Graphic 布局变脏通知的监听器。

声明：

```csharp
public void UnregisterDirtyLayoutCallback(UnityAction action)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `UnityAction` | `action` | 被调用时要调用的方法。 |

### UnregisterDirtyMaterialCallback(UnityAction)

移除接收 Graphic 材质变脏通知的监听器。

声明：

```csharp
public void UnregisterDirtyMaterialCallback(UnityAction action)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `UnityAction` | `action` | 被调用时要调用的方法。 |

### UnregisterDirtyVerticesCallback(UnityAction)

移除接收 Graphic 顶点变脏通知的监听器。

声明：

```csharp
public void UnregisterDirtyVerticesCallback(UnityAction action)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `UnityAction` | `action` | 被调用时要调用的方法。 |

### UpdateGeometry()

调用以将 Graphic 的几何体更新到 CanvasRenderer 上。

声明：

```csharp
protected virtual void UpdateGeometry()
```

### UpdateMaterial()

调用以将 Graphic 的材质更新到 CanvasRenderer 上。

声明：

```csharp
protected virtual void UpdateMaterial()
```

## 实现的接口

- `ICanvasElement`

---

相关文档：[[UnityEngine-UI-Text-中文文档]]、[[UnityEngine-UI-Image-中文文档]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
