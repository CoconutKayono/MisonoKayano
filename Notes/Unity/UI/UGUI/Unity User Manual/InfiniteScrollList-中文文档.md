# Unity 无限滚动列表：ScrollRect + UI 单元复用

> 相关组件：[ScrollRect（Unity UGUI）](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-ScrollRect.html)  
> 相关文档：[UIInteractionComponents-中文文档](UIInteractionComponents-中文文档.md)  
> 相关文档：[UIAutoLayout-中文文档](UIAutoLayout-中文文档.md)  
> 整理日期：2026-09-05

在 Unity 中，“无限滚动列表”通常有三种不同需求：

1. **大数据列表**：数据可能有几万条，但屏幕上只显示几十条。重点是虚拟化和 UI 单元复用。
2. **分页列表**：滚动到接近底部时，请求下一页数据并追加到列表。
3. **循环列表**：滚动到末尾后又回到开头，数据重复播放，常见于轮播图或循环选项。

本文实现第 1 种，并给出第 2、3 种的扩展思路。核心原则是：**数据可以很多，但实例化的 Item 数量只保持在“可视数量 + 少量缓冲”**。

## 一、为什么不能把所有 Item 都 Instantiate

最直接的做法是：每条数据创建一个 UI Prefab，再让 Vertical Layout Group 排列它们。当数据量达到几千或几万时，会出现：

- GameObject、Transform、Text、Image 等组件数量过多；
- Canvas 重建和布局计算耗时增加；
- 滚动时产生明显卡顿；
- 内存占用持续增长；
- 首次打开列表耗时过长。

虚拟列表只创建可视区域所需的 Item。例如，视口能显示 10 行，就创建大约 12～14 个 Item。滚动时只修改这些 Item 当前绑定的数据和位置。

## 二、场景层级与 Inspector 设置

推荐的层级结构：

```text
Canvas
└── Scroll View（ScrollRect）
    ├── Viewport（RectTransform + Mask 或 RectMask2D）
    │   └── Content（RectTransform）
    └── Scrollbar（可选）
```

设置要点：

### Scroll View

- 添加或使用 `ScrollRect` 组件；
- **Viewport** 指向 `Viewport`；
- **Content** 指向 `Content`；
- 只启用需要的方向，例如纵向列表只启用 **Vertical**；
- **Movement Type** 可使用 `Clamped`，避免拖到内容边界之外；
- 需要弹性拖拽时可以使用 `Elastic`，但要留意回弹过程中的复用刷新。

### Viewport

- 添加 `RectMask2D` 或 `Mask`，裁剪视口外的 Item；
- 不要在 Viewport 上放 Layout Group；
- Viewport 的尺寸决定可视 Item 数量。

### Content

将 Content 的 Rect Transform 设置为：

- Anchor Min：`(0, 1)`；
- Anchor Max：`(1, 1)`；
- Pivot：`(0.5, 1)`；
- Anchored Position：通常为 `(0, 0)`；
- 横向通过锚点拉伸，纵向高度由脚本设置。

为了让脚本精确控制 Item 位置，Content 下不要再使用 `Vertical Layout Group`、`Content Size Fitter` 来同时驱动同一批 Item。自动布局组件和手动复用脚本同时控制 Rect Transform，容易产生布局竞争。

## 三、制作可复用 Item Prefab

Item Prefab 只负责显示一条数据，例如：

```text
ListItem
├── Icon（Image，可选）
├── Title（Text 或 TextMeshPro，可选）
└── Button（可选）
```

Item 的 Rect Transform 建议使用固定高度，例如 `80`，并让宽度跟随 Content。固定高度可以直接通过索引计算位置，性能和实现复杂度都比较稳定。

下面的示例使用 UGUI 的 `Text`，如果项目使用 TextMeshPro，只需把字段替换为 `TMP_Text` 并添加 `using TMPro;`。

```csharp
using UnityEngine;
using UnityEngine.UI;

public sealed class LoopScrollItemView : MonoBehaviour
{
    [SerializeField] private Text title;

    public void Bind(int index, string value)
    {
        if (title != null)
        {
            title.text = $"{index}: {value}";
        }

        // 在这里更新图标、按钮状态、颜色等内容。
    }
}
```

## 四、固定高度虚拟列表实现

将下面的脚本挂到 `Scroll View` 或单独的列表控制器 GameObject 上，然后把 `ScrollRect`、`Viewport`、`Content` 和 `Item Prefab` 拖入 Inspector。

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public sealed class VirtualVerticalList : MonoBehaviour
{
    [Header("引用")]
    [SerializeField] private ScrollRect scrollRect;
    [SerializeField] private RectTransform viewport;
    [SerializeField] private RectTransform content;
    [SerializeField] private LoopScrollItemView itemPrefab;

    [Header("布局")]
    [SerializeField] private float itemHeight = 80f;
    [SerializeField] private float spacing = 8f;
    [SerializeField] private float paddingTop = 16f;
    [SerializeField] private float paddingBottom = 16f;
    [SerializeField] private int extraPoolItems = 2;

    private readonly List<LoopScrollItemView> pool =
        new List<LoopScrollItemView>();
    private readonly List<string> items = new List<string>();

    private int firstVisibleIndex = -1;
    private int poolSize;

    private float ItemExtent
    {
        get { return itemHeight + spacing; }
    }

    private void OnEnable()
    {
        if (scrollRect != null)
        {
            scrollRect.onValueChanged.AddListener(OnScrollChanged);
        }
    }

    private void OnDisable()
    {
        if (scrollRect != null)
        {
            scrollRect.onValueChanged.RemoveListener(OnScrollChanged);
        }
    }

    public void SetItems(IList<string> source)
    {
        items.Clear();

        if (source != null)
        {
            items.AddRange(source);
        }

        Rebuild();
    }

    public void SetItemCount(int count)
    {
        items.Clear();

        for (int i = 0; i < Mathf.Max(0, count); i++)
        {
            items.Add($"Item {i}");
        }

        Rebuild();
    }

    private void Rebuild()
    {
        if (scrollRect == null || viewport == null ||
            content == null || itemPrefab == null || itemHeight <= 0f)
        {
            Debug.LogError("VirtualVerticalList 的引用或尺寸未设置。", this);
            return;
        }

        for (int i = 0; i < pool.Count; i++)
        {
            if (pool[i] != null)
            {
                Destroy(pool[i].gameObject);
            }
        }

        pool.Clear();

        poolSize = Mathf.CeilToInt(viewport.rect.height / ItemExtent)
                   + Mathf.Max(0, extraPoolItems);
        poolSize = Mathf.Max(1, poolSize);

        for (int i = 0; i < poolSize; i++)
        {
            LoopScrollItemView view = Instantiate(itemPrefab, content);
            RectTransform itemRect = view.transform as RectTransform;

            itemRect.anchorMin = new Vector2(0f, 1f);
            itemRect.anchorMax = new Vector2(1f, 1f);
            itemRect.pivot = new Vector2(0.5f, 1f);
            itemRect.sizeDelta = new Vector2(0f, itemHeight);

            pool.Add(view);
        }

        content.SetSizeWithCurrentAnchors(
            RectTransform.Axis.Vertical, GetContentHeight());

        content.anchoredPosition = new Vector2(
            content.anchoredPosition.x, 0f);
        firstVisibleIndex = -1;
        RefreshVisibleItems(true);
    }

    private float GetContentHeight()
    {
        if (items.Count == 0)
        {
            return paddingTop + paddingBottom;
        }

        return paddingTop + paddingBottom
               + itemHeight * items.Count
               + spacing * (items.Count - 1);
    }

    private void OnScrollChanged(Vector2 _)
    {
        RefreshVisibleItems(false);
    }

    private void RefreshVisibleItems(bool force)
    {
        if (pool.Count == 0)
        {
            return;
        }

        float scrollOffset = Mathf.Max(0f, content.anchoredPosition.y);
        int first = Mathf.FloorToInt(
            Mathf.Max(0f, scrollOffset - paddingTop) / ItemExtent);
        first = Mathf.Clamp(first, 0, Mathf.Max(0, items.Count - 1));

        if (!force && first == firstVisibleIndex)
        {
            return;
        }

        firstVisibleIndex = first;

        for (int i = 0; i < pool.Count; i++)
        {
            int dataIndex = first + i;
            LoopScrollItemView view = pool[i];
            bool shouldShow = dataIndex >= 0 && dataIndex < items.Count;

            view.gameObject.SetActive(shouldShow);

            if (!shouldShow)
            {
                continue;
            }

            RectTransform itemRect = view.transform as RectTransform;
            itemRect.anchoredPosition = new Vector2(
                0f, -paddingTop - dataIndex * ItemExtent);
            view.Bind(dataIndex, items[dataIndex]);
        }
    }
}
```

## 五、脚本的核心计算

假设：

- 每个 Item 高度为 `itemHeight`；
- Item 间距为 `spacing`；
- 单元高度步长为 `itemHeight + spacing`；
- Content 顶部为坐标原点。

第 `index` 个 Item 的纵坐标为：

```text
y = -paddingTop - index × (itemHeight + spacing)
```

Content 的总高度为：

```text
paddingTop + paddingBottom
+ itemCount × itemHeight
+ (itemCount - 1) × spacing
```

滚动时，根据 Content 的 `anchoredPosition.y` 计算第一个可能出现在视口中的数据索引，然后把池中的 Item 依次绑定到 `firstIndex`、`firstIndex + 1`、`firstIndex + 2`……。

因此，列表的时间和内存开销主要与可视 Item 数量相关，而不是与数据总量相关。

## 六、使用示例

```csharp
using System.Collections.Generic;
using UnityEngine;

public sealed class ListDemo : MonoBehaviour
{
    [SerializeField] private VirtualVerticalList list;

    private void Start()
    {
        List<string> data = new List<string>();

        for (int i = 0; i < 10000; i++)
        {
            data.Add($"服务器消息 {i}");
        }

        list.SetItems(data);
    }
}
```

如果数据类型不是 `string`，可以将 `List<string>` 改成自己的数据类型，并把 `LoopScrollItemView.Bind` 改为接收对应的数据对象。例如 `Bind(int index, InventoryItem data)`。

## 七、滚动到底部加载下一页

如果数据来自服务器，不需要一次性准备 10000 条数据。可以先加载第一页，在接近底部时请求下一页：

```csharp
private bool loading;
private int page;

// 将主实现中的 OnScrollChanged 替换为类似逻辑，或在其中调用
// CheckLoadMore()。不要在同一个类中保留两个同签名的方法。
private void CheckLoadMore()
{
    float normalized = scrollRect.verticalNormalizedPosition;
    if (!loading && normalized < 0.1f)
    {
        LoadNextPage();
    }
}

private void LoadNextPage()
{
    loading = true;

    // 这里替换成自己的网络请求或本地异步加载逻辑。
    // List<string> nextPage = repository.LoadPage(page + 1);
    // AppendItems(nextPage);

    page++;
    loading = false;
}
```

实际项目中，`AppendItems` 应该只追加数据并更新 Content 高度，不要销毁并重新创建整个 Item 池，否则滚动位置可能跳动，也会失去复用的意义。还应处理：

- 请求失败和重试；
- 已经没有更多数据；
- 快速拖到底部时避免重复请求；
- 加载指示器和空状态；
- 网络返回顺序与用户滚动顺序不一致。

## 八、如果需要首尾循环的“真正无限列表”

虚拟列表解决的是“大数据量”，它仍然有明确的第一条和最后一条。如果需求是轮播式循环，需要额外定义循环策略：

### 方案 A：索引取模

逻辑数据索引可以通过下面的方式映射到实际数据：

```csharp
int actualIndex = ((virtualIndex % dataCount) + dataCount) % dataCount;
```

这样 `virtualIndex` 可以无限增长，而 `actualIndex` 始终落在真实数据范围内。Item 的显示内容使用 `actualIndex`，位置计算仍然使用 `virtualIndex`。

### 方案 B：滚动到边界时搬移 Content

当 Content 接近顶部或底部时，把它的滚动位置平移一个或多个完整数据周期，同时保持当前可见内容不变。这个方案能避免 Content 的高度无限增大，但需要同步处理：

- ScrollRect 的 `normalizedPosition`；
- 当前选中的 Item；
- 拖拽惯性；
- 鼠标滚轮和手柄导航；
- 首尾边界附近的可视刷新。

如果只是展示排行榜、背包或聊天记录，通常不需要首尾循环；使用本文的虚拟化列表配合分页加载更符合用户对列表位置的预期。

## 九、固定高度与动态高度

本文使用固定高度，因为它能通过一次乘法直接计算索引和位置。如果 Item 高度会因换行文字而变化，需要维护每个 Item 的实际高度或预估高度，并使用前缀和查找第一个可见索引：

```text
prefix[i] = 第 0 到 i-1 个 Item 的累计高度
```

更新某一行高度后，还要修正后续 Item 的位置和 Content 总高度。动态高度虚拟列表更复杂，建议：

- 尽量限制标题行数；
- 先使用预估高度，显示后再校正；
- 避免把 Content Size Fitter、Layout Group 和手动定位同时用于同一层级；
- 或使用经过验证的第三方虚拟列表方案。

## 十、常见问题

### 滚动时 Item 闪烁

确认 Item 只在索引变化时重新绑定，避免每帧重复 Instantiate。绑定数据时应一次性更新标题、图标、按钮状态和选中状态。

### 最后一行显示不完整

检查 Content 高度公式、`paddingBottom`、`itemHeight` 和 `spacing`。Content 高度必须覆盖最后一个 Item 的底部。

### Item 位置整体偏移

确认 Content 的 Pivot 是顶部，Item 的 Pivot 是顶部，并且使用：

```text
y = -paddingTop - index × (itemHeight + spacing)
```

如果使用了底部 Pivot，需要重新推导坐标公式。

### 列表刷新后跳回顶部

这是示例 `Rebuild` 中主动重置滚动位置造成的。搜索结果刷新时可以保存刷新前的 `content.anchoredPosition.y`，更新数据后按数据索引恢复位置；分页追加数据时通常不需要重置位置。

### 能不能继续使用 Vertical Layout Group

可以使用布局系统制作普通的小列表，但本文的虚拟复用方案需要脚本直接控制 Item 的 Rect Transform。不要让 Layout Group、Content Size Fitter 和复用脚本同时驱动同一批 Item 的位置和尺寸。
