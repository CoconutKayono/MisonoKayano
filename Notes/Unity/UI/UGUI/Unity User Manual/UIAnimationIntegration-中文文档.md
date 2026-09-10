# 动画集成（Animation Integration）

> 来源：[Unity UGUI 2.6 — Animation Integration](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/UIAnimationIntegration.html)  
> 官方源文件：[uGUI/Documentation~/UIAnimationIntegration.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/UIAnimationIntegration.md)  
> 整理日期：2026-09-05

Animation 过渡模式可以使用 Unity 动画系统，让控件在每个状态之间的过渡都完全动画化。由于可以同时动画化许多属性，这是最强大的过渡模式。

![Button Inspector 中的动画过渡设置](GUI_ButtonInspectorAnimation.png)

## 使用 Animation 过渡模式

要使用 Animation 过渡模式，需要在控制器元素上附加 Animator 组件。单击 **Auto Generate Animation** 可以自动完成这一步，同时生成一个已配置状态的 Animator Controller；生成的 Animator Controller 需要保存。

新的 Animator Controller 可以立即使用。与大多数 Animator Controller 不同，这个控制器还保存了控制器各状态之间过渡所使用的动画；如果需要，可以继续自定义这些动画。

![生成的 Animator Controller](GUI_ButtonAnimator.png)

例如，选中附加了 Animator Controller 的 Button 后，可以打开 Animation 窗口（**Window > Animation**）编辑按钮各状态的动画。通过 Animation Clip 下拉菜单选择目标动画片段：

- Normal
- Highlighted
- Pressed
- Disabled

![Animation 窗口](GUI_ButtonAnimationWindow.png)

Normal 状态由按钮元素本身的属性值决定，因此可以留空。其他状态最常见的配置是在时间线起点设置一个关键帧。状态之间的过渡动画由 Animator 负责。

例如，要改变按钮在 Highlighted 状态下的宽度，可以在 Animation Clip 下拉菜单中选择 Highlighted，并将播放头放在时间线起点，然后：

1. 单击 **录制（Record）Button**。
2. 在 Inspector 中修改 Button 的宽度。
3. 退出录制模式。

进入 Play Mode 后，将鼠标移到按钮上使其高亮，就可以看到按钮变宽。一个关键帧中可以设置任意数量的属性。多个按钮可以共享同一 Animator Controller，从而共享相同的行为。

UI Animation 过渡模式与 Unity 的旧版 Animation 系统不兼容，只应使用 **Animator** 组件。

