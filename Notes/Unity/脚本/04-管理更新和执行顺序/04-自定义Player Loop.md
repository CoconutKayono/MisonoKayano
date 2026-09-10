# 自定义 Player loop

> 原文：[Customizing the Player loop](https://docs.unity3d.com/6000.7/Documentation/Manual/player-loop-customizing.html)

Unity 运行时应用程序会在一个称为 **Player loop** 的连续循环中运行。在 Player loop 的每次迭代期间，Unity 都会调用各种系统来执行渲染、物理模拟和输入处理等任务。

Player loop 中更新的各种系统和子系统按照预先定义的默认顺序调用。你可以使用 [PlayerLoop](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoop.html) API 的静态方法查看和自定义这个顺序。你可以获取默认或当前的 Player loop，插入自己的自定义 Player loop 系统，也可以移除、重新排序或替换现有系统。

你可能出于以下原因自定义 Player loop：

- 作为自定义[更新管理器](https://docs.unity3d.com/6000.7/Documentation/Manual/events-per-frame-optimization.html)的一部分创建自己的托管更新，这可能比 Unity 原生的事件函数具有更高的性能。有关更多信息，请参阅 Unity 博客中的 [10000 Update calls](https://unity.com/blog/engine-platform/10000-update-calls)。
- 针对特定平台优化 Player loop。例如，对于移动游戏，可以移除 Physics、AI 和 XR 更新。
- 在 Edit Mode 或 Play Mode 中创建更新循环的可视化结果，以帮助调试。

## 访问 Player loop

Player loop 由一系列嵌套的 Player loop 系统组成，每个系统都是一个 [PlayerLoopSystem](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoopSystem.html) 结构体。最外层的根 Player loop 系统代表完整的 Player loop，其他 Player loop 系统嵌套在其下方。

在这里，Player loop 系统只是对 Player loop 期间需要更新的内容进行抽象表示。默认系统代表 Audio 和 Input 等 Unity 原生系统，但你也可以从 C# 代码中创建自己的自定义系统。

要访问 Unity 的默认 Player loop，请使用 [PlayerLoop.GetDefaultPlayerLoop](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoop.GetDefaultPlayerLoop.html)。要访问当前生效的 Player loop，请使用 [PlayerLoop.GetCurrentPlayerLoop](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoop.GetCurrentPlayerLoop.html)。除非你使用 [PlayerLoop.SetPlayerLoop](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoop.SetPlayerLoop.html) 应用了新的自定义 Player loop，否则默认 Player loop 和当前 Player loop 会保持一致。

Player loop 中的每个系统都有一个用于标识它的 [PlayerLoopSystem.type](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoopSystem-type.html) 属性。你可以递归遍历 Player loop 系统结构，并打印每个 `type` 属性的 [Name](https://learn.microsoft.com/en-us/dotnet/api/system.reflection.memberinfo.name?view=net-9.0#system-reflection-memberinfo-name)，从而在 Console 中显示 Player loop 的结构。

你也可以像下面的示例一样使用 `type` 属性来识别需要添加、移除或替换的 Player loop 子系统。默认系统的有效类型位于 `UnityEngine.PlayerLoop` 命名空间中。

[PlayerLoop.GetDefaultPlayerLoop](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoop.GetDefaultPlayerLoop.html) API 参考中包含一个示例，用于获取默认 Player loop、遍历嵌套的 Player loop 系统，并打印其 `type` 属性的 `Name`。该代码会生成以下 Console 输出：

```text
ROOT NODE
    TimeUpdate
        WaitForLastPresentationAndUpdateTime
    Initialization
        ProfilerStartFrame
        UpdateCameraMotionVectors
        DirectorSampleTime
        AsyncUploadTimeSlicedUpdate
        SynchronizeInputs
        SynchronizeState
        XREarlyUpdate
    EarlyUpdate
        PollPlayerConnection
        GpuTimestamp
        AnalyticsCoreStatsUpdate
        UnityWebRequestUpdate
        ExecuteMainThreadJobs
        ProcessMouseInWindow
        ClearIntermediateRenderers
        ClearLines
        PresentBeforeUpdate
        ResetFrameStatsAfterPresent
        UpdateAsyncInstantiate
        UpdateAsyncReadbackManager
        UpdateStreamingManager
        UpdateTextureStreamingManager
        UpdatePreloading
        UpdateContentLoading
        RendererNotifyInvisible
        PlayerCleanupCachedData
        UpdateMainGameViewRect
        UpdateCanvasRectTransform
        XRUpdate
        UpdateInputManager
        ProcessRemoteInput
        ScriptRunDelayedStartupFrame
        UpdateKinect
        DeliverIosPlatformEvents
        DispatchEventQueueEvents
        Physics2DEarlyUpdate
        PhysicsResetInterpolatedTransformPosition
        SpriteAtlasManagerUpdate
        PerformanceAnalyticsUpdate
    FixedUpdate
        ClearLines
        NewInputFixedUpdate
        DirectorFixedSampleTime
        AudioFixedUpdate
        ScriptRunBehaviourFixedUpdate
        DirectorFixedUpdate
        LegacyFixedAnimationUpdate
        XRFixedUpdate
        PhysicsFixedUpdate
        Physics2DFixedUpdate
        PhysicsClothFixedUpdate
        DirectorFixedUpdatePostPhysics
        ScriptRunDelayedFixedFrameRate
    PreUpdate
        PhysicsUpdate
        Physics2DUpdate
        PhysicsClothUpdate
        CheckTexFieldInput
        IMGUISendQueuedEvents
        NewInputUpdate
        InputForUIUpdate
        SendMouseEvents
        AIUpdate
        WindUpdate
        UpdateVideo
    Update
        ScriptRunBehaviourUpdate
        ScriptRunDelayedDynamicFrameRate
        ScriptRunDelayedTasks
        DirectorUpdate
    PreLateUpdate
        AIUpdatePostScript
        DirectorUpdateAnimationBegin
        LegacyAnimationUpdate
        DirectorUpdateAnimationEnd
        DirectorDeferredEvaluate
        AccessibilityUpdate
        UIElementsUpdatePanels
        EndGraphicsJobsAfterScriptUpdate
        ConstraintManagerUpdate
        ParticleSystemBeginUpdateAll
        Physics2DLateUpdate
        PhysicsLateUpdate
        ScriptRunBehaviourLateUpdate
    PostLateUpdate
        PlayerSendFrameStarted
        DirectorLateUpdate
        ScriptRunDelayedDynamicFrameRate
        PhysicsSkinnedClothBeginUpdate
        UpdateRectTransform
        PlayerUpdateCanvases
        UIElementsRepaintPanels
        UpdateAudio
        VFXUpdate
        ParticleSystemEndUpdateAll
        EndGraphicsJobsAfterScriptLateUpdate
        UpdateCustomRenderTextures
        XRPostLateUpdate
        UpdateAllRenderers
        UpdateLightProbeProxyVolumes
        EnlightenRuntimeUpdate
        UpdateAllSkinnedMeshes
        ProcessWebSendMessages
        SortingGroupsUpdate
        UpdateVideoTextures
        UpdateVideo
        DirectorRenderImage
        PlayerEmitCanvasGeometry
        UIElementsRenderBatchModeOffscreen
        PhysicsSkinnedClothFinishUpdate
        FinishFrameRendering
        BatchModeUpdate
        PlayerSendFrameComplete
        UpdateCaptureScreenshot
        PresentAfterDraw
        ClearImmediateRenderers
        PlayerSendFramePostPresent
        UpdateResolution
        InputEndFrame
        TriggerEndOfFrameCallbacks
        GUIClearEvents
        ShaderHandleErrors
        ResetInputAxis
        ThreadedLoadingDebug
        ProfilerSynchronizeStats
        MemoryFrameMaintenance
        XRPreEndFrame
        ProfilerEndFrame
        GraphicsWarmupPreloadedShaders
        ObjectDispatcherPostLateUpdate
```

## 将自定义更新插入默认 Player loop

自定义 Player loop 时，推荐且风险最低的方式是将自定义 Player loop 系统插入默认 Player loop。这样可以添加自己的自定义更新逻辑，而不会干扰 Unity 的任何内置系统。

[PlayerLoop.SetPlayerLoop](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoop.SetPlayerLoop.html) API 参考中的代码示例展示了如何在指定位置将自定义 Player loop 系统插入默认 Player loop。在该示例中，`CustomUpdate` 方法的行为定义在 `InsertSystem` 类中。

只需进行以下少量修改，就可以将 `CustomUpdate` 改为一个事件，使 MonoBehaviour 脚本能够订阅该事件并提供自己的更新逻辑：

- 在 `InsertSystem` 类中声明一个 `public static` 事件字段：

```csharp
public static event Action AddCustomUpdate;
```

- 修改 `CustomUpdate` 方法的定义，使其调用这个事件：

```csharp
private static void CustomUpdate() => AddCustomUpdate?.Invoke();
```

之后，任何 MonoBehaviour 脚本都可以按如下方式订阅这个自定义更新：

```csharp
using UnityEngine;

public class CustomUpdateFromEvent : MonoBehaviour
{
    private void OnEnable()
    {
        InsertSystem.AddCustomUpdate += MyCustomUpdate;
    }

    private void Update()
    {
        Debug.Log("Update");
    }

    private void LateUpdate()
    {
        Debug.Log("Late Update");
    }

    private void OnDisable()
    {
        InsertSystem.AddCustomUpdate -= MyCustomUpdate;
    }

    private void MyCustomUpdate()
    {
        Debug.Log("Custom update from an event that your MonoBehaviour scripts can subscribe to.");
    }
}
```

> [!NOTE]
> 传递给 [PlayerLoop.SetPlayerLoop](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoop.SetPlayerLoop.html) 的 Player loop 系统会覆盖当前 Player loop。因此，请确保传递给该方法的循环包含所有希望保留的系统，包括那些没有被替换的系统。如果从头开始创建新的 Player loop 系统，则必须显式地将所有希望保留的系统添加到新循环中。

## 替换 Player loop 中的默认系统

下面的示例使用自定义更新替换 Player loop 中的默认系统。该示例替换的是 `PreUpdate.AIUpdate` 系统，但你可以通过指定其 [PlayerLoopSystem.type](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoopSystem-type.html) 标识符来替换 Player loop 中的任何系统。

默认系统的有效类型可以通过遍历默认 Player loop 获得，上一节的示例展示了这种方式；也可以从 `UnityEngine.PlayerLoop` 命名空间中获取。

> [!IMPORTANT]
> 替换 Player loop 中的系统可能会产生意外后果，因为这会移除该系统的默认功能。请谨慎使用此方法，并且只在确定要用自己的自定义逻辑替换默认功能时使用。

```csharp
using UnityEngine.LowLevel;
using UnityEngine.PlayerLoop;
using UnityEngine;

// Replace an existing system in the Unity Player Loop with a custom update.
public class MyReplacementCustomUpdate { } // Empty class to use as a type identifier for the custom update

public class SystemReplacement
{
    //Run this method on runtime initialization
    [RuntimeInitializeOnLoadMethod]
    private static void AppStart()
    {
        // Retrieve the default Player loop system. Get the current loop instead if the default was already modified previously.
        var defaultSystems = PlayerLoop.GetDefaultPlayerLoop();
        // Create a custom update system to replace an existing one
        var customUpdate = new PlayerLoopSystem()
        {
            updateDelegate = CustomUpdate,
            type = typeof(MyReplacementCustomUpdate)
        };
        // Specify the system to replace as the type parameter, in this case PreUpdate.AIUpdate
        ReplaceSystem<PreUpdate.AIUpdate>(ref defaultSystems, customUpdate);
        PlayerLoop.SetPlayerLoop(defaultSystems);
    }
    // Custom update method that will be called in the Player Loop
    private static void CustomUpdate()
    {
        Debug.Log("Custom update from a replacement system.");
    }

    //Recursively replace a system of type T with a replacement system in the Player Loop
    private static bool ReplaceSystem<T>(ref PlayerLoopSystem system, PlayerLoopSystem replacement)
    {
        if (system.type == typeof(T))
        {
            system = replacement;
            return true;
        }
        if (system.subSystemList != null)
        {
            for (var i = 0; i < system.subSystemList.Length; i++)
            {
                if (ReplaceSystem<T>(ref system.subSystemList[i], replacement))
                {
                    return true;
                }
            }
        }
        return false;
    }
}
```

## 其他资源和示例

- **Documentation**：[事件函数执行顺序](03-事件函数执行顺序.md)
- **Documentation**：[LowLevel.PlayerLoop API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LowLevel.PlayerLoop.html)
- **Documentation**：[10000 Update calls](https://unity.com/blog/engine-platform/10000-update-calls)
- **Community**：[Unity Discussions 中的 LowLevel.PlayerLoop 主题](https://discussions.unity.com/search?expanded=true&q=LowLevel.PlayerLoop%20order%3Alatest_topic)

---

## 文档导航

- 上一篇：[[03-事件函数执行顺序]]
- 所属目录：[[00-管理更新和执行顺序]]
- 下一篇：[[05-使用自定义更新管理器]]
