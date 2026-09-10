# 不进行 Scene Reload 进入 Play mode

> 原文：[Enter Play mode without scene reload](https://docs.unity3d.com/6000.7/Documentation/Manual/scene-reloading.html)

默认情况下，进入 Play mode 时会开启 Scene Reload。这意味着进入 Play mode 时，Unity 会销毁所有现有的 Scene GameObject，并从磁盘重新加载 Scene。随着项目变得越来越复杂，从按下 **Play** 按钮到 Scene 在 Editor 中完全加载之间所需的时间会增加。

关闭 Scene Reload 后，该过程耗时更短。Unity 不再从磁盘重新加载 Scene，而只会重置 Scene 中被修改的内容。Unity 仍会调用相同的[事件函数](https://docs.unity3d.com/6000.7/Documentation/Manual/event-functions.html)，例如 `OnEnable`、`OnDisable` 和 `OnDestroy`，就像 Scene 刚刚加载一样。

## 进入 Play mode 时关闭 Scene Reload 的影响

当你[关闭 Scene Reload](https://docs.unity3d.com/6000.7/Documentation/Manual/configurable-enter-play-mode.html#configure-play-mode) 后，在 Editor 中启动应用所需的时间不再代表构建版本的启动时间。如果要精确调试或分析项目启动时发生的事情，应启用 Scene Reload，以便更准确地还原构建版本中的真实加载时间和过程。

除此之外，关闭 Scene Reload 对项目的影响应该很小。但是，由于 Scene Reload 与 Domain Reload 紧密相关，仍有一些重要差异：

- Unity 不会重新创建现有对象或调用构造函数，这意味着非序列化字段会保留它们在 Play mode 期间被赋予的值，并在返回 Edit mode 时继续保留。这适用于所有脚本类型的字段，包括 `MonoBehaviour`、`ScriptableObject` 和你自己的自定义 C# 类型。有关不同上下文中哪些内容会被序列化的详细信息，请参阅 [Serialization rules](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-rules.html)。

  > **Note**：`private` 字段不会作为常规构建流程的一部分进行序列化，但会作为 Editor[脚本热重载](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-how-unity-uses.html#hot-reload)的一部分进行序列化。这就是为什么即使进入 Play mode 时 Scene Reload 和 Domain Reload 都关闭，你在 Play mode 中修改的 `private` 字段仍可能在退出 Play mode 时重置为原始值。

- Unity 会在 Domain Reload 期间将数组和 `List` 类型的 `private`、`internal` 字段中的 `null` 转换为空数组或 `List` 对象；对于运行时（非 Editor）脚本，它们会保持非 `null`。
- 使用 [`[ExecuteInEditMode]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ExecuteInEditMode.html) 或 [`[ExecuteAlways]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ExecuteAlways.html) Attribute 修饰的脚本不会收到 `OnDestroy` 或 `Awake` 调用。在 Edit mode 中，这些脚本可能会修改自身字段，或修改其他 runtime 脚本的字段。为降低这种影响，可以在 `OnEnable` 回调中初始化受影响的字段，并将代码放在检查 [`EditorApplication.isPlaying`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/EditorApplication-isPlaying.html) 值的条件中。有关此方法的示例，以及分离 Play mode 和 Edit mode 代码的重要性的更多上下文，请参阅 [`[ExecuteAlways]` API 描述](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ExecuteAlways.html)。

有关关闭 Scene Reload 时跳过的事件的更多细节，请参阅 [[02-Domain和Scene重载执行顺序参考]]。

## 其他资源

- [[01-配置Unity进入Play Mode]]
- [[03-不进行Domain Reload进入Play Mode]]
- [[02-Domain和Scene重载执行顺序参考]]

---

## 文档导航

- 上一页：[[03-不进行Domain Reload进入Play Mode]]
- 目录：[[00-代码和场景重载]]
- 下一页：[[../06-脚本序列化/00-脚本序列化]]
