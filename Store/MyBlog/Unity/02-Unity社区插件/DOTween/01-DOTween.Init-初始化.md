# DOTween.Init

DOTween 有两种初始化方式：

- **自动初始化**：如果什么都不做，首次创建补间时会以默认参数自动完成初始化。
    
- **手动初始化（推荐）**：在创建任何补间之前，主动调用一次 `DOTween.Init()`，后续重复调用无效。

无论采用哪种方式，初始化之后你依然可以随时通过 `DOTween` 的全局设置调整各项参数。

另外，`Init` 方法还支持链式追加 `SetCapacity`，用于预设 `Tweener` 和 `Sequence` 的初始最大容量，效果等同于提前调用 `DOTween.SetTweensCapacity`。

```cs
static DOTween.Init(bool recycleAllByDefault = false, bool useSafeMode = true, LogBehaviour logBehaviour = LogBehaviour.ErrorsOnly)
```

`DOTween.Init` 用于手动初始化 DOTween，可接受三个可选参数：`recycleAllByDefault`、`useSafeMode` 和 `logBehaviour`。各参数作用如下：

- **recycleAllByDefault**  
  若为 `TRUE`，则所有新建补间默认标记为“可回收”。被 Kill 时不会销毁，而是进入对象池等待复用，从而减少 GC 分配。需注意，被 Kill 的补间可能正被重用，若持有引用易引发混乱。若希望 Kill 时自动清空引用，可配合 `OnKill` 回调：

  ```csharp
  .OnKill(() => myTweenReference = null)
  ```
  
  此后也可通过 `DOTween.defaultRecyclable` 属性全局修改，或用 `SetRecyclable` 对单个补间单独设置。

- **useSafeMode**  
  若为 `TRUE`，运行速度稍慢但更安全，能自动处理目标对象在动画中途被销毁等异常。  
  警告：在 iOS 上，安全模式仅在托管剥离级别设为 “Strip Assemblies” 或脚本调用优化设为 “Slow and Safe” 时有效；在 Windows 10 WSA 平台上，若选用 Master Configuration 与 .NET 后端则会失效。

- **logBehaviour**  
  控制日志输出级别：仅错误、错误与警告，或完整信息。

调用时若**不传任何参数**，`DOTween.Init()` 会直接使用你在 DOTween Utility Panel 中配置的偏好值；传入的参数则会覆盖这些偏好。初始化后仍可随时通过全局设置调整。

```csharp
// 使用 Utility Panel 中的偏好初始化
DOTween.Init();

// 自定义参数初始化，并同时预设 Tween/Sequence 最大容量
DOTween.Init(true, true, LogBehaviour.Verbose).SetCapacity(200, 10);
```

