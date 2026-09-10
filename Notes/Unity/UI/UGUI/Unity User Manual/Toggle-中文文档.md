# Toggle（开关）

**Toggle** 控件是一个复选框，允许用户打开或关闭某个选项。

*（图：一个 Toggle 示例）*

## 属性

| 属性                          | 功能                                                                                                                                                 |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Interactable（可交互）**       | 此组件是否会接受输入？参见 [Interactable](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Selectable.html)。                                  |
| **Transition（过渡）**          | 决定控件在用户操作时如何做出视觉响应的属性。参见 [Transition Options（过渡选项）](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-SelectableTransition.html)。 |
| **Navigation（导航）**          | 决定控件之间切换顺序的属性。参见 [Navigation Options（导航选项）](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-SelectableNavigation.html)。         |
| **Is On（是否开启）**             | Toggle 在开始时是否就处于开启状态？                                                                                                                              |
| **Toggle Transition（开关过渡）** | 当值改变时 Toggle 的图形反应方式。可选值为 *None*（即勾选标记直接出现或消失）和 *Fade*（即勾选标记淡入或淡出）。                                                                                |
| **Graphic（图形）**             | 用于勾选标记的图像。                                                                                                                                         |
| **Group（组）**                | 此 Toggle 所属的 [Toggle Group](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-ToggleGroup.html)（如果有）。                             |

## 事件

| 属性 | 功能 |
| --- | --- |
| **On Value Changed（值更改时）** | 点击 Toggle 时调用的 [UnityEvent](https://docs.unity3d.com/Manual/UnityEvents.html)。该事件可以将当前状态作为 bool 类型的动态参数发送。 |

## 详细信息

Toggle 控件允许用户打开或关闭某个选项。你也可以将多个 Toggle 组合成一个 [Toggle Group](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-ToggleGroup.html)，适用于"同一组选项里同时只能开启一个"的场景。

Toggle 有一个名为 *On Value Changed* 的事件，当用户更改当前值时触发。新值会作为布尔参数传递给事件函数。Toggle 的典型用例包括：

- 打开或关闭某个选项（例如在游戏过程中是否播放音乐）。
- 让用户确认其已阅读法律免责声明。
- 在 Toggle Group 中使用时，从一组选项中选择一个（例如星期几）。

请注意，**Toggle** 是一个父级对象，为子对象提供可点击区域。如果 **Toggle** 没有子对象（或子对象被禁用），则它不可点击。

---

相关文档：[[ToggleGroup-中文文档]]

这个页面是否对你有帮助？请为其评分：
