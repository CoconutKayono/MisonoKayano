# UGUI 推荐结构与命名规范：Window、Widget 和代码控制对象

> 适用范围：Unity UGUI 项目中的界面层级、Prefab 组织、Widget 结构和对象命名  
> 相关文档：[UICanvas-中文文档](UICanvas-中文文档.md)  
> 相关文档：[UIAutoLayout-中文文档](UIAutoLayout-中文文档.md)  
> 整理日期：2026-09-07

## 一、先给出推荐结论

建议把 UGUI 拆成四个层次：

```text
场景级 UI 根节点
└── UIRoot
    ├── WindowLayer       主窗口层
    ├── PopupLayer        弹窗层
    ├── GuideLayer        新手引导、遮罩层
    ├── ToastLayer        Toast、飘字、提示层
    └── TopLayer          始终显示在最上方的 UI
```

Prefab 内部再按照下面的规则组织：

```text
Window       = 可独立打开、关闭、切换的主窗口
Widget       = 可复用的小组件，负责局部显示和交互
Control      = Button、Image、Text、Toggle 等基础控件
Container    = 只负责布局和分组的空节点
```

最重要的一条原则是：

> `Window` 负责页面级生命周期，`Widget` 负责局部功能，基础控件负责具体交互；不要让每个 Widget 都变成一个小型 Window，也不要让 Window 直接管理所有深层子控件的细节。

## 二、Window 和 Widget 的职责边界

### Window：主窗口

Window 通常满足以下特征：

- 可以被 UI 管理器独立打开和关闭；
- 有明确的进入、显示、退出生命周期；
- 通常占据 WindowLayer 中的一整个页面区域；
- 可以处理返回、关闭、暂停输入、窗口切换等页面级逻辑；
- 可以包含多个 Widget；
- 一般制作成独立 Prefab。

典型名称：

```text
LoginWindow
MainMenuWindow
InventoryWindow
SettingsWindow
ConfirmDialogWindow
```

### Widget：可复用的小组件

Widget 通常满足以下特征：

- 只负责一小块 UI 的显示和交互；
- 可以被一个或多个 Window 复用；
- 通常通过 `Bind`、`Refresh` 或 `SetData` 接收数据；
- 不直接决定自己应该显示在哪个 WindowLayer；
- 不应该依赖全局 UI 单例来打开任意窗口；
- 可以制作成独立 Prefab，也可以作为 Window 的子节点。

典型名称：

```text
TopBarWidget
PlayerInfoWidget
InventoryItemWidget
QuestItemWidget
TabWidget
ConfirmButtonWidget
```

### 不要把 Widget 和 Window 混用

下面这些情况通常应该是 Window，而不是 Widget：

- 有自己的打开/关闭动画；
- 需要加入窗口栈或处理返回键；
- 会遮挡整个页面；
- 需要控制输入焦点和页面级导航；
- 由 UIManager 单独管理。

下面这些情况通常应该是 Widget，而不是 Window：

- 背包中的一格物品；
- 一个 Tab 按钮；
- 窗口顶部的标题栏；
- 一个玩家头像和名字组合；
- 一个进度条、血条或属性条；
- 一个可复用的列表项。

## 三、场景中的推荐 UGUI 根结构

建议场景中只保留一个主要的 Screen Space Canvas，除非有明确的排序、渲染隔离或性能需求。

```text
Scene
├── EventSystem
│   ├── EventSystem
│   └── StandaloneInputModule 或 InputSystemUIInputModule
├── UIRoot
│   ├── WindowLayer
│   ├── PopupLayer
│   ├── GuideLayer
│   ├── ToastLayer
│   └── TopLayer
└── 其他游戏对象
```

### UIRoot 应该挂什么组件

`UIRoot` 是全局 Canvas，推荐挂载：

| 组件 | 是否推荐 | 作用 |
| --- | --- | --- |
| **Rect Transform** | Unity 自动添加 | 作为 UI 根节点的 Rect Transform。 |
| **Canvas** | 必须 | 设置 Render Mode、Sort Order 等。一般使用 Screen Space - Overlay 或 Screen Space - Camera。 |
| **Canvas Scaler** | 推荐 | 统一处理不同分辨率下的 UI 缩放。常用 `Scale With Screen Size`。 |
| **Graphic Raycaster** | 需要交互时保留 | 检测 Button、Toggle 等 UI 的指针事件。纯展示 UI 可以考虑关闭。 |
| **UIRoot.cs** | 可选 | 负责初始化层级、注册窗口层或提供根节点引用。 |

`EventSystem` 不要放进 `UIRoot` 的 Canvas 层级中。它是场景级输入对象，应与 `UIRoot` 平级。

### Layer 节点应该挂什么组件

下面这些 Layer 一般只需要：

| 节点 | 组件 |
| --- | --- |
| `WindowLayer` | Rect Transform |
| `PopupLayer` | Rect Transform |
| `GuideLayer` | Rect Transform |
| `ToastLayer` | Rect Transform |
| `TopLayer` | Rect Transform |

不要为了让一个 Layer 能被找到，就额外给它添加 Image、Canvas 或 Graphic Raycaster。层级节点只承担组织作用。

如果某一层确实需要独立排序，可以有意添加一个嵌套 Canvas，并设置 **Override Sorting**。但不要给每个 Window 和 Widget 默认添加 Canvas，否则会增加 Canvas 管理和重建成本。

## 四、命名规范

### 1. Window 和 Widget 的命名

Window 和 Widget 使用语义名称加类型后缀：

```text
InventoryWindow
SettingsWindow
PlayerInfoWidget
InventoryItemWidget
TabWidget
```

类名、Prefab 名和根节点名尽量保持一致：

```text
Assets/UI/Window/InventoryWindow.prefab
Assets/UI/Window/InventoryWindow.cs

Assets/UI/Widget/InventoryItemWidget.prefab
Assets/UI/Widget/InventoryItemWidget.cs
```

这样可以通过 Prefab 名直接找到脚本，也方便代码和资源管理工具按名称匹配。

### 2. 基础控件前缀

对于需要在代码中引用的基础控件，使用类型前缀。推荐使用下面的表：

| Unity 类型 | 推荐前缀 | 示例 |
| --- | --- | --- |
| `Button` | `Btn_` | `Btn_Close`、`Btn_Confirm` |
| `Image` | `Img_` | `Img_Icon`、`Img_Background` |
| `RawImage` | `RawImg_` | `RawImg_Preview` |
| `Text` / `TMP_Text` | `Txt_` | `Txt_Title`、`Txt_Count` |
| `Toggle` | `Tgl_` | `Tgl_Sound` |
| `ToggleGroup` | `TglGrp_` | `TglGrp_Tabs` |
| `Slider` | `Sld_` | `Sld_Volume` |
| `Scrollbar` | `ScrBar_` | `ScrBar_List` |
| `ScrollRect` | `Scr_` | `Scr_Inventory` |
| `Dropdown` / `TMP_Dropdown` | `Drop_` | `Drop_Quality` |
| `InputField` / `TMP_InputField` | `Inp_` | `Inp_Search` |
| `CanvasGroup` | `Cg_` | `Cg_Window` |
| `Animator` | `Anim_` | `Anim_Transition` |
| `LayoutGroup` | `Layout_` | `Layout_Content` |
| `Mask` / `RectMask2D` | `Mask_` | `Mask_Viewport` |

### 3. 空节点和布局节点命名

不需要代码引用的空节点不必强行加类型前缀，优先使用语义名称：

```text
Header
Content
Footer
Viewport
ItemRoot
IconArea
ActionArea
```

如果空节点需要被代码引用，或者项目希望所有节点都能快速识别，可以使用：

```text
Root_Content
Root_Item
Grp_Actions
Layer_Window
```

建议不要把所有节点都命名成 `Go_xxx`。UI 层级的主要目的是表达视觉结构，只有需要脚本引用的对象才使用强类型前缀。

### 4. 脚本字段命名

GameObject 名称和 C# 字段名称可以保持同一语义，但字段使用 C# 风格：

```csharp
[SerializeField] private Button _btnClose;
[SerializeField] private Image _imgIcon;
[SerializeField] private TMP_Text _txtName;
[SerializeField] private CanvasGroup _cgWindow;
```

不要在运行时大量使用 `transform.Find("Btn_Close")` 或 `GetComponentInChildren<T>()` 查找控件。推荐直接通过 `[SerializeField]` 拖拽引用，Prefab 结构变化时更容易在 Inspector 中发现引用问题。

## 五、Widget 到底应该挂什么组件

这是最容易混乱的地方。推荐把 Widget 分成三种类型。

### 类型 A：纯显示 Widget

例如玩家头像、货币显示、静态标题栏。

```text
PlayerInfoWidget
├── Img_Avatar
├── Txt_PlayerName
└── Txt_Level
```

根节点 `PlayerInfoWidget` 推荐组件：

| 组件 | 是否需要 | 说明 |
| --- | --- | --- |
| **Rect Transform** | 必须 | 所有 UI 节点都会有。 |
| **PlayerInfoWidget.cs** | 推荐 | 负责绑定头像、名字和等级。 |
| **CanvasGroup** | 按需 | 需要整体隐藏、淡入淡出或控制透明度时添加。 |
| **LayoutElement** | 按需 | 父级 Layout Group 需要读取该 Widget 的最小/首选/可伸缩尺寸时添加。 |
| **Image** | 通常不需要 | 只有 Widget 根节点本身需要背景或接收点击时才添加。 |
| **Button** | 通常不需要 | 只有整个 Widget 都是一个点击区域时才添加。 |

子节点组件：

- `Img_Avatar`：`RectTransform` + `Image`；
- `Txt_PlayerName`：`RectTransform` + `TMP_Text`；
- `Txt_Level`：`RectTransform` + `TMP_Text`；
- 纯显示 Image/Text 的 **Raycast Target** 通常关闭，避免挡住下层按钮。

### 类型 B：复合交互 Widget

例如背包物品格、任务项、好友项、排行榜项。

```text
InventoryItemWidget
├── Img_Background
├── Img_Icon
├── Txt_Name
├── Txt_Count
├── Img_Selected
└── Btn_Click
    └── Txt_Hint
```

根节点 `InventoryItemWidget` 推荐组件：

| 组件 | 作用 |
| --- | --- |
| **Rect Transform** | 定义 Widget 在父级布局中的位置和尺寸。 |
| **InventoryItemWidget.cs** | 接收物品数据，刷新图标、名字、数量和选中状态。 |
| **CanvasGroup** | 控制禁用、半透明、整体淡出等状态。 |
| **LayoutElement** | 当它作为列表项被 Layout Group 管理时，提供首选高度或宽度。 |

根节点通常不挂 `Button`。真正的点击组件放在 `Btn_Click` 上：

| GameObject | 组件 |
| --- | --- |
| `Img_Background` | Rect Transform + Image，通常关闭 Raycast Target |
| `Img_Icon` | Rect Transform + Image，关闭 Raycast Target |
| `Txt_Name` | Rect Transform + TMP_Text，关闭 Raycast Target |
| `Txt_Count` | Rect Transform + TMP_Text，关闭 Raycast Target |
| `Img_Selected` | Rect Transform + Image，关闭 Raycast Target，默认隐藏 |
| `Btn_Click` | Rect Transform + Image + Button |
| `Txt_Hint` | Rect Transform + TMP_Text，关闭 Raycast Target |

这样可以把所有装饰图形设置为不拦截射线，只让 `Btn_Click` 负责点击。代码只需要监听一个明确的 Button。

### 类型 C：布局型 Widget

例如顶部栏、筛选栏、分页栏或一组 Tab。

```text
FilterBarWidget
├── Drop_Category
├── Inp_Search
├── Tgl_OnlyOwned
└── Btn_Reset
```

根节点 `FilterBarWidget` 推荐组件：

- `RectTransform`；
- `FilterBarWidget.cs`；
- `HorizontalLayoutGroup` 或 `GridLayoutGroup`，如果它负责排列自己的子控件；
- `LayoutElement`，如果它需要向父级布局报告尺寸；
- `ContentSizeFitter` 只有在确实需要根据内容调整自身尺寸时添加，不要和父级 Layout Group 同时争夺同一方向的尺寸。

`FilterBarWidget` 不需要 Canvas、Graphic Raycaster 或 EventSystem。输入事件由最外层的 UIRoot Canvas 处理。

## 六、一个推荐的 Window 示例：InventoryWindow

下面用背包窗口展示完整结构。这个结构适合大多数“窗口 + 顶部栏 + 内容区 + 底部操作栏”的页面。

```text
InventoryWindow
├── Img_Background
├── TopBarWidget
│   ├── Txt_Title
│   └── Btn_Close
├── FilterBarWidget
│   ├── Drop_Category
│   ├── Inp_Search
│   └── Btn_Reset
├── Scr_ItemList
│   └── Viewport
│       └── Content
│           └── InventoryItemWidget（Prefab 实例）
└── BottomBar
    ├── Txt_SelectedCount
    └── Btn_Confirm
```

### InventoryWindow 根节点组件

| 组件 | 说明 |
| --- | --- |
| **Rect Transform** | 根节点铺满 WindowLayer。 |
| **CanvasGroup** | 控制窗口整体显示、隐藏和交互状态。 |
| **InventoryWindow.cs** | 页面级逻辑，例如打开、关闭、刷新背包和响应 Widget 事件。 |
| **Animator** | 需要窗口动画时添加；没有动画时不必添加。 |
| **LayoutElement** | 只有当 Window 自己被父级 Layout Group 管理时才需要。 |

### InventoryWindow 子节点组件

| GameObject | 组件 | 说明 |
| --- | --- | --- |
| `Img_Background` | Image | 窗口背景。如果它不需要点击，关闭 Raycast Target。 |
| `TopBarWidget` | RectTransform + TopBarWidget.cs | 可复用的窗口标题栏。 |
| `FilterBarWidget` | RectTransform + LayoutGroup + FilterBarWidget.cs | 筛选、搜索和重置区域。 |
| `Scr_ItemList` | RectTransform + ScrollRect | 控制列表滚动。命名中的 `Scr_` 表示 ScrollRect。 |
| `Viewport` | RectTransform + RectMask2D | 裁剪滚动区域外的内容。 |
| `Content` | RectTransform + VerticalLayoutGroup | 普通小列表可以使用；虚拟列表则由脚本控制尺寸和位置。 |
| `BottomBar` | RectTransform + HorizontalLayoutGroup | 底部操作区域。 |
| `Btn_Close` | Image + Button | 关闭窗口的按钮。 |
| `Btn_Confirm` | Image + Button | 确认操作的按钮。 |

如果使用前文的虚拟列表方案，`Content` 不要再挂 `VerticalLayoutGroup` 或 `ContentSizeFitter` 来驱动同一批列表项，避免布局系统和复用脚本发生冲突。参考 [InfiniteScrollList-中文文档](InfiniteScrollList-中文文档.md)。

## 七、一个推荐的 Widget 示例：InventoryItemWidget

### 1. Prefab 层级

```text
InventoryItemWidget
├── Img_Background
├── Img_Icon
├── Txt_Name
├── Txt_Count
├── Img_Selected
├── Img_Lock
└── Btn_Click
```

### 2. 组件清单

根节点：

```text
InventoryItemWidget
├── RectTransform
├── CanvasGroup
├── LayoutElement
└── InventoryItemWidget.cs
```

子节点：

```text
Img_Background  = RectTransform + Image
Img_Icon        = RectTransform + Image
Txt_Name        = RectTransform + TMP_Text
Txt_Count       = RectTransform + TMP_Text
Img_Selected    = RectTransform + Image
Img_Lock        = RectTransform + Image
Btn_Click       = RectTransform + Image + Button
```

建议设置：

- `Img_Background`、`Img_Icon`、`Txt_Name`、`Txt_Count`、`Img_Selected`、`Img_Lock` 的 **Raycast Target** 关闭；
- `Btn_Click` 的 Image 负责接收射线，Button 负责交互状态；
- `Img_Selected` 和 `Img_Lock` 初始可以禁用，由脚本根据数据状态显示；
- `LayoutElement.preferredHeight` 可以设置为固定列表项高度，例如 `96`；
- Widget 的根节点不要添加 `Canvas`、`GraphicRaycaster` 或 `EventSystem`。

### 3. Widget 脚本示例

下面是一个使用 TextMeshPro 的示例：

```csharp
using System;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public sealed class InventoryItemWidget : MonoBehaviour
{
    [Header("显示")]
    [SerializeField] private Image _imgIcon;
    [SerializeField] private TMP_Text _txtName;
    [SerializeField] private TMP_Text _txtCount;
    [SerializeField] private GameObject _imgSelected;
    [SerializeField] private GameObject _imgLock;

    [Header("交互")]
    [SerializeField] private Button _btnClick;
    [SerializeField] private CanvasGroup _canvasGroup;

    private ItemData _data;
    private Action<ItemData> _onClicked;

    private void Awake()
    {
        _btnClick.onClick.AddListener(OnClick);
    }

    private void OnDestroy()
    {
        _btnClick.onClick.RemoveListener(OnClick);
    }

    public void Bind(ItemData data, Action<ItemData> onClicked)
    {
        _data = data;
        _onClicked = onClicked;

        _imgIcon.sprite = data.Icon;
        _txtName.text = data.Name;
        _txtCount.text = data.Count.ToString();
        _imgSelected.SetActive(data.IsSelected);
        _imgLock.SetActive(data.IsLocked);

        _canvasGroup.alpha = data.IsLocked ? 0.55f : 1f;
        _btnClick.interactable = !data.IsLocked;
    }

    public void Clear()
    {
        _data = null;
        _onClicked = null;
        _imgIcon.sprite = null;
        _txtName.text = string.Empty;
        _txtCount.text = string.Empty;
        _imgSelected.SetActive(false);
        _imgLock.SetActive(false);
        _btnClick.interactable = false;
    }

    private void OnClick()
    {
        if (_data != null)
        {
            _onClicked?.Invoke(_data);
        }
    }
}

[Serializable]
public sealed class ItemData
{
    public Sprite Icon;
    public string Name;
    public int Count;
    public bool IsSelected;
    public bool IsLocked;
}
```

> 如果项目使用 UGUI Legacy Text，可以把 `TMP_Text` 替换成 `UnityEngine.UI.Text`。新项目更推荐 TextMeshPro。

### 4. Widget 的生命周期

推荐给 Widget 统一采用下面的生命周期：

```text
Awake       = 注册本地 Button 事件、缓存不变的引用
Bind        = 绑定一条业务数据并刷新显示
Refresh     = 数据变化后刷新当前显示
Clear       = 列表复用或禁用时清空旧数据
OnDestroy   = 注销本地事件
```

列表复用时尤其要注意 `Clear`。如果 Item 被重新绑定但没有清理旧的状态，就可能出现：

- 上一条物品的锁定图标残留；
- 上一条数据的数量没有刷新；
- 旧 Button 回调仍然指向旧数据；
- 选中状态显示在错误的 Item 上。

## 八、Window 脚本和 Widget 脚本如何通信

推荐由 Window 负责组合 Widget，并通过回调、事件或接口接收 Widget 的操作结果：

```text
InventoryWindow
    ├── Bind 数据到 InventoryItemWidget
    ├── 接收 InventoryItemWidget.OnClicked
    ├── 更新当前选中物品
    └── 决定是否打开 ConfirmDialogWindow
```

Widget 不建议直接执行：

```csharp
UIManager.Instance.OpenWindow<ConfirmDialogWindow>();
GameManager.Instance.SelectItem(_data);
```

更推荐：

```csharp
// Widget 只通知外部“用户点击了某个物品”。
_onClicked?.Invoke(_data);

// InventoryWindow 决定接下来打开什么窗口或执行什么业务。
private void OnItemClicked(ItemData data)
{
    // 更新选中项、显示详情、打开确认弹窗等。
}
```

这样 Widget 可以在背包、商店、仓库和奖励窗口中复用，而不需要知道自己被谁使用。

## 九、Window 的推荐生命周期

可以为所有主窗口定义统一的基类：

```csharp
using UnityEngine;

public abstract class UIWindow : MonoBehaviour
{
    [SerializeField] private CanvasGroup _canvasGroup;

    public bool IsOpen { get; private set; }

    public virtual void Open()
    {
        IsOpen = true;
        gameObject.SetActive(true);

        if (_canvasGroup != null)
        {
            _canvasGroup.alpha = 1f;
            _canvasGroup.interactable = true;
            _canvasGroup.blocksRaycasts = true;
        }

        OnOpened();
    }

    public virtual void Close()
    {
        IsOpen = false;

        if (_canvasGroup != null)
        {
            _canvasGroup.interactable = false;
            _canvasGroup.blocksRaycasts = false;
        }

        OnClosed();
        gameObject.SetActive(false);
    }

    protected virtual void OnOpened() { }
    protected virtual void OnClosed() { }
}
```

具体窗口只实现自己的页面逻辑：

```csharp
public sealed class InventoryWindow : UIWindow
{
    protected override void OnOpened()
    {
        // 请求或刷新背包数据，设置默认选中项。
    }

    protected override void OnClosed()
    {
        // 清理临时状态，停止页面级订阅。
    }
}
```

如果窗口有 Animator，可以把 `Close()` 改成播放关闭动画，并在动画结束事件中 `SetActive(false)`。不要让每个 Widget 自己决定整个 Window 的 Active 状态。

## 十、哪些组件应该放在哪一层

| 组件 | 推荐层级 | 原因 |
| --- | --- | --- |
| `Canvas` | UIRoot 或明确需要独立排序的特殊层 | 不要每个 Widget 都创建 Canvas。 |
| `CanvasScaler` | UIRoot | 全局统一缩放。 |
| `GraphicRaycaster` | UIRoot | 统一处理 Screen Space UI 事件。 |
| `EventSystem` | 场景根节点 | 它不是 Canvas 的子组件。 |
| `CanvasGroup` | Window 根、需要整体控制的 Widget 根 | 控制整体 alpha、交互和射线阻挡。 |
| `ScrollRect` | 负责滚动的 Window 或列表 Widget | 不要让每个列表项拥有 ScrollRect。 |
| `LayoutGroup` | 负责排列子元素的 Container 或布局型 Widget | 只由一个系统负责同一方向的尺寸和位置。 |
| `ContentSizeFitter` | 需要根据内容改变自身尺寸的节点 | 避免与父级 Layout Group 同时控制同一方向。 |
| `Button` | 实际可点击的控件节点 | 通常和 Image 放在同一个 `Btn_` 节点上。 |
| `Image` | 视觉背景、图标或按钮目标图形 | 纯装饰节点通常关闭 Raycast Target。 |
| `Animator` | Window 根或需要独立动画的 Widget 根 | 没有动画需求时不添加。 |

## 十一、推荐的目录结构

```text
Assets/UI/
├── Common/
│   ├── UIRoot.prefab
│   ├── UIWindow.cs
│   └── UIManager.cs
├── Window/
│   ├── InventoryWindow/
│   │   ├── InventoryWindow.prefab
│   │   └── InventoryWindow.cs
│   ├── SettingsWindow/
│   │   ├── SettingsWindow.prefab
│   │   └── SettingsWindow.cs
│   └── ConfirmDialogWindow/
│       ├── ConfirmDialogWindow.prefab
│       └── ConfirmDialogWindow.cs
├── Widget/
│   ├── TopBarWidget/
│   │   ├── TopBarWidget.prefab
│   │   └── TopBarWidget.cs
│   ├── InventoryItemWidget/
│   │   ├── InventoryItemWidget.prefab
│   │   └── InventoryItemWidget.cs
│   └── PlayerInfoWidget/
│       ├── PlayerInfoWidget.prefab
│       └── PlayerInfoWidget.cs
├── Texture/
├── Sprite/
└── Font/
```

如果项目规模较小，也可以直接把脚本和 Prefab 放在 `Assets/UI/Window`、`Assets/UI/Widget` 下，不必为了目录层级过度拆分。

## 十二、最终推荐示例

```text
UIRoot
├── WindowLayer
│   └── InventoryWindow
│       ├── Img_Background        [Image]
│       ├── TopBarWidget          [TopBarWidget.cs]
│       │   ├── Txt_Title         [TMP_Text]
│       │   └── Btn_Close          [Image + Button]
│       ├── FilterBarWidget       [FilterBarWidget.cs + LayoutGroup]
│       │   ├── Drop_Category      [TMP_Dropdown]
│       │   ├── Inp_Search         [TMP_InputField]
│       │   └── Btn_Reset          [Image + Button]
│       ├── Scr_ItemList           [ScrollRect]
│       │   └── Viewport           [RectMask2D]
│       │       └── Content
│       │           └── InventoryItemWidget [CanvasGroup + LayoutElement + 脚本]
│       │               ├── Img_Background [Image]
│       │               ├── Img_Icon       [Image]
│       │               ├── Txt_Name       [TMP_Text]
│       │               ├── Txt_Count      [TMP_Text]
│       │               └── Btn_Click      [Image + Button]
│       └── BottomBar
│           └── Btn_Confirm              [Image + Button]
├── PopupLayer
├── GuideLayer
├── ToastLayer
└── TopLayer
```

这套结构的核心特点是：

1. `UIRoot` 统一持有 Canvas、CanvasScaler 和 GraphicRaycaster；
2. `Window` 负责页面级生命周期；
3. `Widget` 负责局部显示、数据绑定和局部交互；
4. `Btn_`、`Img_`、`Txt_` 等前缀只用于快速识别和脚本引用；
5. 空节点只承担布局，不随意添加视觉或事件组件；
6. 一个 Rect Transform 的位置和尺寸尽量只交给一个系统控制；
7. Widget 通过回调或事件通知 Window，不直接依赖全局窗口管理器；
8. 纯装饰 Image/Text 关闭 Raycast Target，减少无意义的 UI 射线命中。
