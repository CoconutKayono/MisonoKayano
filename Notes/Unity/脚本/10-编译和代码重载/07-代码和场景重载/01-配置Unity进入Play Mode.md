# 配置 Unity 进入 Play mode 的方式

> 原文：[Configuring how Unity enters Play mode](https://docs.unity3d.com/6000.7/Documentation/Manual/configurable-enter-play-mode.html)

通过从 Edit mode 切换到 Play mode 来测试应用，是 Unity 的核心功能之一。你可以通过 Toolbar 中的 **Play** 按钮，直接在 Editor 内运行项目。

Play mode 用于尽可能真实地预览应用对用户的行为。默认情况下，Unity 在进入 Play mode 时会重载 Scene。有关关闭 Scene Reload 的影响，以及如何在代码中进行补偿的信息，请参阅 [[04-不进行Scene Reload进入Play Mode]]。

默认情况下，Unity 在进入 Play mode 时不会重载 scripting domain 来重置应用状态，但你可以[配置 Unity 执行 Domain Reload](#configure-play-mode)。有关关闭 Domain Reload 的影响，以及如何在代码中进行补偿的信息，请参阅 [[03-不进行Domain Reload进入Play Mode]]。

> **Note**：建议保持 Domain Reload 关闭，以提高开发迭代速度，并为 Unity 采用不包含 Domain Reload 概念的 CoreCLR runtime 做准备。

Scene Reload 和 Domain Reload 都需要时间，而且脚本和 Scene 越复杂，执行所需的时间就越长。当你频繁修改并预览变化时，等待进入 Play mode 所累积的时间会显著拖慢开发过程。

为了优先提高开发迭代速度，而不是确保 Play mode 模拟的准确性，Unity 提供了在进入 Play mode 时关闭 Domain Reload 和 Scene Reload 的功能。

下面的图示概括了关闭 Domain Reload 和 Scene Reload 的影响：

![关闭 Domain Reload 和 Scene Reload 设置的影响](图片/EnterPlayModeDiagram.svg)

图：关闭 Domain Reload 和 Scene Reload 设置的影响。

有关关闭 Domain Reload 和 Scene Reload 的影响的更多细节，请参阅 [[02-Domain和Scene重载执行顺序参考]]。

<a id="configure-play-mode"></a>

## 配置 Play mode 设置

要配置 Editor 进入 Play mode 的方式：

1. 打开 [Project Settings 窗口](https://docs.unity3d.com/6000.7/Documentation/Manual/comp-ManagerGroup.html)（**Edit > Project Settings**）。
2. 点击 **Editor** 选项卡。
3. 在 **Enter Play Mode Settings** 区域的 **When entering Play Mode** 下拉菜单中，选择以下选项之一：

   - **Reload Domain and Scene**。
   - **Reload Scene only**。这是默认选项。
   - **Reload Domain only**。
   - **Do not reload Domain or Scene**。

## 其他资源

- [Project Settings 窗口](https://docs.unity3d.com/6000.7/Documentation/Manual/comp-ManagerGroup.html)
- [Editor Project Settings](https://docs.unity3d.com/6000.7/Documentation/Manual/class-EditorManager.html)
- [Toolbar](https://docs.unity3d.com/6000.7/Documentation/Manual/Toolbar.html)
- [[03-不进行Domain Reload进入Play Mode]]
- [[04-不进行Scene Reload进入Play Mode]]

---

## 文档导航

- 上一页：[[00-代码和场景重载]]
- 目录：[[00-代码和场景重载]]
- 下一页：[[02-Domain和Scene重载执行顺序参考]]
