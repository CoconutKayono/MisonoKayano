# 受支持的事件（Supported Events）

事件系统支持许多事件，并且可以在用户自定义的输入模块中进一步定制。

Standalone Input Module（独立输入模块）和 Touch Input Module（触屏输入模块）支持的事件由接口提供，可以通过在 MonoBehaviour 上实现接口来使用。如果你配置了有效的事件系统，事件将在正确的时间被调用。

| 接口 | 回调方法 | 说明 |
| --- | --- | --- |
| [IPointerEnterHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IPointerEnterHandler.html) | OnPointerEnter | 当指针进入对象时调用 |
| [IPointerExitHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IPointerExitHandler.html) | OnPointerExit | 当指针离开对象时调用 |
| [IPointerDownHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IPointerDownHandler.html) | OnPointerDown | 当指针在对象上按下时调用 |
| [IPointerUpHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IPointerUpHandler.html) | OnPointerUp | 当指针释放时调用（在指针正在点击的 GameObject 上调用） |
| [IPointerClickHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IPointerClickHandler.html) | OnPointerClick | 当指针在同一对象上按下并释放时调用 |
| [IInitializePotentialDragHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IInitializePotentialDragHandler.html) | OnInitializePotentialDrag | 当找到拖拽目标时调用，可用于初始化数值 |
| [IBeginDragHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IBeginDragHandler.html) | OnBeginDrag | 当拖拽即将开始时在拖拽对象上调用 |
| [IDragHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IDragHandler.html) | OnDrag | 当拖拽进行中时在拖拽对象上调用 |
| [IEndDragHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IEndDragHandler.html) | OnEndDrag | 当拖拽完成时在拖拽对象上调用 |
| [IDropHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IDropHandler.html) | OnDrop | 在拖拽结束位置的对象上调用 |
| [IScrollHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IScrollHandler.html) | OnScroll | 当鼠标滚轮滚动时调用 |
| [IUpdateSelectedHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IUpdateSelectedHandler.html) | OnUpdateSelected | 每帧在选中对象上调用 |
| [ISelectHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.ISelectHandler.html) | OnSelect | 当对象成为选中对象时调用 |
| [IDeselectHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IDeselectHandler.html) | OnDeselect | 当选中对象被取消选中时调用 |
| [IMoveHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.IMoveHandler.html) | OnMove | 当发生移动事件时调用（左、右、上、下） |
| [ISubmitHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.ISubmitHandler.html) | OnSubmit | 当按下提交按钮时调用 |
| [ICancelHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.ICancelHandler.html) | OnCancel | 当按下取消按钮时调用 |

---

相关文档：[[00-MessagingSystem-消息系统]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
