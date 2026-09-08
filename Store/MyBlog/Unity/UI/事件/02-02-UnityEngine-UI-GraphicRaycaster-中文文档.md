# GraphicRaycaster 类

## 继承关系

`object` → `UIBehaviour` → `BaseRaycaster` → `GraphicRaycaster`

## 继承的成员

- `BaseRaycaster.priority`
- `BaseRaycaster.rootRaycaster`
- `BaseRaycaster.ToString()`
- `BaseRaycaster.OnEnable()`
- `BaseRaycaster.OnDisable()`

命名空间：`UnityEngine.UI`

程序集：`UnityEngine.UI.dll`

## 语法

```csharp
[AddComponentMenu("Event/Graphic Raycaster")]
[RequireComponent(typeof(Canvas))]
public class GraphicRaycaster : BaseRaycaster
```

## 构造函数

### GraphicRaycaster()

声明：

```csharp
protected GraphicRaycaster()
```

## 字段

### kNoEventMaskSet

声明：

```csharp
protected const int kNoEventMaskSet = -1
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `int` | |

### m_BlockingMask

声明：

```csharp
[SerializeField]
protected LayerMask m_BlockingMask
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `LayerMask` | |

## 属性

### blockingMask

通过 LayerMask 指定的对象类型，用于判断它们是否阻挡图形射线投射。

声明：

```csharp
public LayerMask blockingMask { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `LayerMask` | |

### blockingObjects

用于判断是否阻挡图形射线投射的对象类型。

声明：

```csharp
public GraphicRaycaster.BlockingObjects blockingObjects { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `GraphicRaycaster.BlockingObjects` | |

### eventCamera

将为此射线发射器（Raycaster）生成射线的摄像机。

声明：

```csharp
public override Camera eventCamera { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `Camera` | 如果摄像机模式为 ScreenSpaceOverlay（屏幕空间-覆盖），或为 ScreenSpaceCamera（屏幕空间-摄像机）但未指定摄像机，则返回 null；如果 `canvas.worldCanvas` 不为 null 则返回它；否则返回 `Camera.main`。 |

重写：

`BaseRaycaster.eventCamera`

### ignoreReversedGraphics

是否检查背向射线发射器的 Graphic 的射线投射。

声明：

```csharp
public bool ignoreReversedGraphics { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

### renderOrderPriority

基于渲染顺序的射线发射器优先级。

声明：

```csharp
public override int renderOrderPriority { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `int` | 渲染顺序优先级。 |

重写：

`BaseRaycaster.renderOrderPriority`

### sortOrderPriority

基于排序顺序的射线发射器优先级。

声明：

```csharp
public override int sortOrderPriority { get; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `int` | 排序顺序优先级。 |

重写：

`BaseRaycaster.sortOrderPriority`

## 方法

### Raycast(PointerEventData, List<RaycastResult>)

对与 Canvas 关联的图形列表执行射线投射。

声明：

```csharp
public override void Raycast(PointerEventData eventData, List<RaycastResult> resultAppendList)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `PointerEventData` | `eventData` | 当前事件数据。 |
| `List<RaycastResult>` | `resultAppendList` | 用于追加命中对象结果的列表。 |

重写：

`BaseRaycaster.Raycast(PointerEventData, List<RaycastResult>)`

---

相关文档：[[UnityEngine-UI-Graphic-中文文档]]、[[UnityEngine-UI-Image-中文文档]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
