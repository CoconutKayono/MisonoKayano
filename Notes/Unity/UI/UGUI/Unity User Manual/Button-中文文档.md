# Button（按钮）

**Button**（按钮）控件响应用户的点击，用于启动或确认某项操作。常见的例子包括网页表单上的 *Submit*（提交）和 *Cancel*（取消）按钮。

![UI_ButtonInspector.png](Unity/UI/UGUI/Unity%20User%20Manual/images/UI_ButtonInspector.png)

一个按钮在 Inspector 中的外观。

## 属性（Properties）

| 属性 | 功能 |
| --- | --- |
| **Interactable**（可交互） | 如果希望该按钮接受输入，请启用 **Interactable**。更多细节请参阅 [Interactable](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Selectable.html) 的 API 文档。 |
| **Transition**（过渡） | 决定控件在视觉上如何响应用户操作的属性。请参阅 [过渡选项（Transition Options）](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-SelectableTransition.html)。 |
| **Navigation**（导航） | 决定控件切换顺序的属性。请参阅 [导航选项（Navigation Options）](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-SelectableNavigation.html)。 |

## 事件（Events）

| 属性 | 功能 |
| --- | --- |
| **On Click**（点击） | 当用户点击按钮并释放时，Unity 调用的 [UnityEvent](https://docs.unity3d.com/Manual/UnityEvents.html)。 |

## 详细信息（Details）

按钮被设计为在用户点击并释放时启动某项操作。如果在点击释放之前，鼠标已经移出按钮控件，则该操作不会发生。

按钮只有一个名为 *On Click* 的事件，在用户完成一次点击时触发。典型的使用场景包括：

- 确认某个决定（例如开始游戏或保存游戏）
- 跳转到 GUI 中的子菜单
- 取消正在进行的操作（例如取消下载新场景）
