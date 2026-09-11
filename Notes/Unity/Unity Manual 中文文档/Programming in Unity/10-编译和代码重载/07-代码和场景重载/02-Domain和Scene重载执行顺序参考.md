# Domain 和 Scene Reload 执行顺序参考

> 原文：[Domain and scene reload execution order reference](https://docs.unity3d.com/6000.7/Documentation/Manual/configurable-enter-play-mode-details.html)

从较高层次看，进入 Play mode 包含以下主要阶段：

- **Backup current scenes**。仅当 Scene 已被修改时执行。它允许 Unity 在退出 Play mode 时，将 Scene 恢复到开始 Play mode 之前的状态。
- **Domain reload**。如果你已[配置 Unity 在进入 Play mode 时执行 Domain Reload](https://docs.unity3d.com/6000.7/Documentation/Manual/configurable-enter-play-mode.html#configure-play-mode)，Editor 会[重载 Domain](https://docs.unity3d.com/6000.7/Documentation/Manual/domain-reloading.html) 以重置脚本状态。
- **Scene reload**。通过重载 Scene 来重置 Scene 状态。
- **Update scene**。执行两次：一次不进行渲染，另一次进行渲染。

Domain Reload 和 Scene Reload 的组合操作会重置 scripting domain，并模拟应用在 Player 中运行时的启动行为。下图详细说明了 Unity 在 Scene Reload 和 Domain Reload 期间执行的确切步骤，以及在关闭相应重载时跳过的步骤。蓝色表示关闭 Domain Reload 时 Unity 跳过的事件（Domain Reload 默认关闭）；绿色表示关闭 Scene Reload 时 Unity 跳过的事件。

![MonoBehaviour 脚本生命周期中的事件函数](EnterPlayModeEvents.svg)

图：MonoBehaviour 脚本生命周期中的事件函数。关闭 Domain Reload 时跳过的事件函数以蓝色突出显示；关闭 Scene Reload 时跳过的事件函数以绿色突出显示。

## 其他资源

- [[03-不进行Domain Reload进入Play Mode]]
- [[04-不进行Scene Reload进入Play Mode]]

---

## 文档导航

- 上一页：[[01-配置Unity进入Play Mode]]
- 目录：[[00-代码和场景重载]]
- 下一页：[[03-不进行Domain Reload进入Play Mode]]
