# Navigation Options（导航选项）

| 属性                 | 功能                                         |
| ------------------ | ------------------------------------------ |
| **Navigation**（导航） | 导航选项决定运行模式下 UI 元素的导航控制方式。                  |
| **None**（无）        | 不进行键盘导航，同时确保控件不会因点击/触摸而获得焦点。               |
| **Horizontal**（水平） | 水平方向导航。                                    |
| **Vertical**（垂直）   | 垂直方向导航。                                    |
| **Automatic**（自动）  | 自动导航。                                      |
| **Explicit**（显式）   | 在此模式下，可以针对不同的方向键显式指定控件导航到的目标。              |
| **Visualize**（可视化） | 选择 Visualize 后，可以在场景窗口中直观地看到你所设置的导航连接。见下文。 |

![UI_SelectableNavigationExplicit.png](Unity/UI/UGUI/Unity%20User%20Manual/images/UI_SelectableNavigationExplicit.png)

![GUIVisualizeNavigation.png](Unity/UI/UGUI/Unity%20User%20Manual/images/GUIVisualizeNavigation.png)

场景窗口中显示的可视化导航连接

在上述可视化模式下，箭头表示这一组控件作为一个整体时焦点切换的设置方式。也就是说，对于每个单独的 UI 控件，你都可以看到：当该控件获得焦点时，用户按下某个方向键后，下一个获得焦点的会是哪个 UI 控件。例如在上图所示的示例中，如果 “button” 获得焦点，用户按下右方向键，那么第一个（左侧的）垂直滑动条（slider）将获得焦点。请注意，垂直滑动条无法通过上/下方向键移出焦点，因为这些按键用于控制滑动条的值；水平滑动条与左/右方向键的情况同理。

相关文档：[Selectable（可选择基类）](Selectable-中文文档.md) · [Transition Options（过渡选项）](TransitionOptions-中文文档.md)
