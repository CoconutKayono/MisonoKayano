# Selectable（可选择基类）

**Selectable** 类是所有交互组件的基类，负责处理这些组件共有的属性。

| 属性 | 功能 |
| --- | --- |
| **Interactable**（可交互） | 决定该组件是否接受输入。当设置为 false 时，交互被禁用，过渡状态（transition state）将变为禁用状态（disabled）。 |
| **Transition**（过渡） | 在 Selectable 组件中，根据组件当前所处的状态，提供了若干[过渡选项（Transition Options）](TransitionOptions-中文文档.md)。不同的状态包括：正常（normal）、高亮（highlighted）、按下（pressed）和禁用（disabled）。 |
| **Navigation**（导航） | 还提供了一些[导航选项（Navigation Options）](NavigationOptions-中文文档.md)，用于控制控件之间的键盘导航方式。 |

相关文档：[过渡选项（Transition Options）](TransitionOptions-中文文档.md) · [导航选项（Navigation Options）](NavigationOptions-中文文档.md)
