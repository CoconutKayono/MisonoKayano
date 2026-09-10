# 不进行 Domain Reload 进入 Play mode

> 原文：[Enter Play mode without domain reload](https://docs.unity3d.com/6000.7/Documentation/Manual/domain-reloading.html)

Domain Reload 是 Mono 脚本后端使用的代码重载机制。有关 Unity Editor 何时执行代码重载，以及你的代码如何通过回调接入该过程的信息，请参阅 [[00-代码和场景重载]]。

你可以[配置 Editor 在进入 Play mode 时执行 Domain Reload](https://docs.unity3d.com/6000.7/Documentation/Manual/configurable-enter-play-mode.html#configure-play-mode)，以重置应用状态。在进入 Play mode 之前重置状态通常是理想做法，因为这样应用会像新构建开始运行一样启动。例如，在上一个 Play mode session 中递增的静态计数器，应在下一次运行中再次从零开始。

但是，Domain Reload 也是一个耗时操作。当你频繁在 Edit mode 和 Play mode 之间切换时，它会对迭代时间产生负面影响。因此，Editor 默认不会在进入 Play mode 时执行 Domain Reload。如果保留 Domain Reload 关闭的默认配置，就必须通过其他方式[重置静态状态](#reset-state)。

## 进入 Play mode 且关闭 Domain Reload 的影响

如果保留 Unity 默认的 Domain Reload 关闭设置：

- 非序列化字段会保留它们在 Play mode 期间被赋予的值，并在返回 Edit mode 时继续保留。此规则适用于所有脚本类型的字段，包括 `MonoBehaviour`（包括 Prefab Asset 上的 `MonoBehaviour`）、`ScriptableObject` 和你自己的自定义 C# 类型。有关不同上下文中哪些内容会被序列化的详细信息，请参阅 [Serialization rules](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-rules.html)。
- 静态变量会在不同 Play mode session 之间保留其值。
- 静态事件会在不同 Play mode session 之间保留已注册的订阅者。
- 标记了 [`[ExecuteInEditMode]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ExecuteInEditMode.html) 或 [`[ExecuteAlways]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ExecuteAlways.html) 的脚本不会额外收到 `OnDisable` 或 `OnEnable` 调用。

为了补偿 Play mode session 之间的数据持久性，并以全新的应用状态进入 Play mode，必须[在代码中重置状态](#reset-state)。

有关同时关闭 Domain Reload 和 Scene Reload 的影响，请参阅 [[02-Domain和Scene重载执行顺序参考]]。

<a id="reset-state"></a>

## 从代码重置状态

关闭 Domain Reload 时，[静态字段](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/static-classes-and-static-class-members#static-members)的值以及分配给静态事件的处理程序会在不同 Play mode 运行之间保留。下面的代码示例包含一个静态计数器，每按下任意键一次就递增。

启用 Domain Reload 时，Unity 会在进入 Play mode 时重新初始化这段代码，擦除上一次 Play mode 运行的状态，包括计数器值。关闭 Domain Reload 时，计数器值会从上一次运行中保留。在下一次运行 Play mode 时，计数器从上一次运行结束时的值开始。

```csharp
// Copy-paste this code into a MonoBehaviour script attached to a GameObject in your project.
// Run it with domain reload enabled and then with domain reload disabled and note the different behavior.

using UnityEngine;

public class StaticsReset : MonoBehaviour
{
    // With domain reload disabled this counter won't reset to zero on exiting Play mode
    static int counter = 0;

    void Update()
    {
        if (Input.anyKeyDown)
        {
            counter++;
            Debug.Log("Counter: " + counter);
        }
    }

}
```

你可以通过在 Play mode 进入或退出时编写代码来显式重置计数器，从而修复这一问题。你可以[手动](#manual-static-reset)执行重置，也可以使用静态清理 Attribute，在进入 Play mode 时[自动](#automatic-static-reset)执行重置。

### 手动重置静态状态

你可以分别使用生命周期 Attribute [`[OnEnteringPlayMode]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/OnEnteringPlayModeAttribute.html) 和 [`[OnExitingPlayMode]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/OnExitingPlayModeAttribute.html)，在进入或退出 Play mode 时手动重置静态状态。通常，在退出 Play mode 时重置状态比在进入时重置更高效。以下示例在退出 Play mode 时重置静态计数器：

```csharp
using UnityEngine;

public class ManualStaticsReset : MonoBehaviour
{
    static int counter = 0;

    public static void ResetCounter() => counter = 0;

    // Update is called once per frame
    void Update()
    {
        if (Input.anyKeyDown)
        {
            counter++;
            Debug.Log("Counter: " + counter);
        }
    }


}

public static partial class PlayModeManager
{

    [OnEnteringPlayMode]
    static void Init()
    {
        Debug.Log("Entering Play mode!");
    }


    [OnExitingPlayMode]
    private static void OnExitPlayMode()
    {
        Debug.Log("Resetting counter.");
        // Reset the counter so it starts from 0 on the next Play mode run
        ManualStaticsReset.ResetCounter();
        Debug.Log("Exiting Play mode!");
    }

}
```

如果你的代码除了 Play mode 之外还会在 Edit mode 中执行，就不能依赖在退出 Play mode 时重置。你的代码可能会在 Edit mode 中修改静态变量，因此必须在进入 Play mode 时重置变量。

> **Note**：对于在 Edit mode 中执行的脚本，保持 Domain Reload 关闭会跳过 [`MonoBehaviour.OnDisable`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDisable.html)，而关闭 Scene Reload 会跳过 [`MonoBehaviour.OnDestroy`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDestroy.html)，因此这些方法不适合用来重置此类脚本中的状态。更多信息请参阅 [[02-Domain和Scene重载执行顺序参考]]。

### 自动重置静态状态

[`[AutoStaticsCleanup]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Scripting.LifecycleManagement.AutoStaticsCleanupAttribute.html) 和 [`[NoAutoStaticsCleanup]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Scripting.LifecycleManagement.NoAutoStaticsCleanupAttribute.html) Attribute 使用代码生成，在进入 Play mode 时自动重置静态状态。你可以将它们应用于静态字段，以指定该字段是否应自动重置。

以下示例展示这些 Attribute 的用法：

```csharp
using Unity.Scripting.LifecycleManagement;
using UnityEngine;

public partial class AutomaticStaticsReset : MonoBehaviour
{
    [AutoStaticsCleanup]
    public static int cleanedUpCounter = 0;
    [NoAutoStaticsCleanup]
    public static int counter = 0;
    void Start()
    {
        Debug.Log(cleanedUpCounter); // Counter value is reset each time entering Play Mode
        Debug.Log(counter); // Counter value is only reset on Domain Reload
        cleanedUpCounter++;
        counter++;
    }
}
```

> **Note**：有关应用于不同 C# 类型的具体重置行为，请参阅 [`[AutoStaticsCleanup]` API reference](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Scripting.LifecycleManagement.AutoStaticsCleanupAttribute.html)。

静态自动清理由代码生成和代码分析器支持。应用 `[AutoStaticsCleanup]` 时，代码生成器会生成必要的清理代码。

> **Important**：对于非 `readonly` 字段，代码生成器会捕获内联初始化表达式，并在每次 Play mode transition 时重新求值。例如，`static MyType s_Field = new MyType();` 每次都会得到一个新的 `MyType`，即使你的代码在上一个 Play mode session 中将该字段设置成了 `null`。`readonly` 集合字段是例外：实例会保留，并调用 `Clear()`，因此不会重新求值其初始化表达式。无论哪种情况，生成器都不会重新运行类型的静态构造函数，因此没有通过字段初始化表达式表达的静态设置逻辑，在每个 Editor session 中只运行一次。将这类设置逻辑移到带有 [`[OnEnteringPlayMode]`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/OnEnteringPlayModeAttribute.html) 的方法中；如果不需要清理，则使用 `[NoAutoStaticsCleanup]`。

#### 选择合适的 Attribute

下表提供了常见字段类型应使用哪个 Attribute 的指导。这些是基于典型用法的一般建议；根据具体实现，可能存在需要不同选择的情况。

| 字段类型 | 通常的选择 | 原因 |
| --- | --- | --- |
| Events、delegates | `[AutoStaticsCleanup]` | Event handler 应在不同 Play mode session 之间重置，以避免陈旧引用。 |
| 用户对象的集合（例如 `List<MonoBehaviour>`） | `[AutoStaticsCleanup]` | 用户对象不应跨 Play mode session 持久存在。 |
| ID 生成计数器（例如 `s_NextObjectID`） | `[NoAutoStaticsCleanup]` | 唯一名称生成使用的计数器应保留，以维持不同 Play mode session 之间的唯一性。 |
| 缓存的 UI 资源（`GUIStyle`、`GUIContent`） | `[NoAutoStaticsCleanup]` | 不可变 UI 资源可以安全地重复使用。 |
| 对 Unity 对象的引用（`ScriptableObject`、`MonoBehaviour`） | `[AutoStaticsCleanup]` | Unity 对象应被重置，以获得干净的 Play mode session。 |

静态清理 Attribute 的代码生成默认开启。如果不想使用这些 Attribute，而是希望自行编写清理代码，可以通过[全局配置文件](#global-config)关闭代码生成。

自动静态清理代码分析器会分析程序集中的代码，并提供哪些静态变量需要重置以及如何重置的指导。当 Domain Reload 关闭且没有使用静态清理 Attribute 时，这尤其有用，因为它可以帮助你识别必须手动重置的静态变量。启用 Fast Enter Play Mode（Domain Reload disabled）时，分析器默认启用。你可以使用[全局配置文件](#global-config)按程序集覆盖此设置。

启用后，分析器会发出带有 `UAL` 前缀的警告。下表列出了最常见的警告：

| 代码 | 说明 | 修复方法 |
| --- | --- | --- |
| `UAL0010` | 类型包含需要生命周期 Attribute 的静态成员。每个受影响的成员还会显示 `UAL0013`。 | 为每个成员添加 `[AutoStaticsCleanup]` 或 `[NoAutoStaticsCleanup]`。 |
| `UAL0011` | `[AutoStaticsCleanup]` 或 `[NoAutoStaticsCleanup]` 配置无效。 | 查看编译器消息了解详细信息。 |
| `UAL0012` | 包含自动清理静态成员的类型必须标记为 `partial`，以允许代码生成器注入清理代码。 | 为 class 或 struct 添加 `partial` 关键字。 |
| `UAL0013` | 静态成员必须标记 `[AutoStaticsCleanup]` 或 `[NoAutoStaticsCleanup]`。 | 为成员添加 `[AutoStaticsCleanup]` 或 `[NoAutoStaticsCleanup]`。 |
| `UAL0014` | 带有 `[AutoStaticsCleanup]` 成员的类型拥有显式静态构造函数。 | 删除静态构造函数，将初始化逻辑移到其他位置；或者在不需要清理时改用 `[NoAutoStaticsCleanup]`。 |

### 代码生成和分析配置

你可以使用与程序集位于同一目录的 `.globalconfig` 文件，按程序集配置代码生成和代码分析设置。步骤如下：

1. 在脚本文件夹中创建[程序集定义文件](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definitions-creating.html)。
2. 在同一文件夹中创建 `<assemblyDefinitionName>.globalconfig` 文件。
3. 在 `.globalconfig` 文件中使用以下标志打开或关闭代码生成和代码分析：

| 属性 | 说明 |
| --- | --- |
| `is_global` | 将此文件标记为分析器配置文件。可以省略；但如果存在，该属性必须设置为 `true`。默认值为 `true`。 |
| `build_property.UnityEnableAutoStaticsCleanupCodeGen` | 启用静态自动清理的代码生成。要使用 `[AutoStaticsCleanup]` 和 `[NoAutoStaticsCleanup]` Attribute，必须将其设置为 `true`。默认值为 `true`。 |
| `build_property.UnityEnableAutoStaticsCleanupAnalysis` | 按程序集覆盖静态自动清理的代码分析。启用 Fast Enter Play Mode 时，将其设置为 `false` 可针对特定程序集关闭分析器。Editor Settings 中启用 Fast Enter Play Mode（Domain Reload disabled）时，分析器默认启用，不需要此属性。 |

下面是一个与默认设置对应的 `.globalconfig` 文件示例：

```text
is_global = true # enables Roslyn
build_property.UnityEnableAutoStaticsCleanupCodeGen = true # statics cleanup code generator on
build_property.UnityEnableAutoStaticsCleanupAnalysis = false # disable analyzer for this assembly (overrides Fast Enter Play Mode auto-enable)
```

> **Important**：对于 Package，将 `.globalconfig` 文件放在与 `.asmdef` 文件相同的文件夹中；如果文件不存在，则创建它。对于没有程序集定义的脚本，将文件放在 `Assets/` 下的子文件夹中。如果你满意于代码生成开启、代码分析关闭的默认配置，就不需要创建此文件，可以直接在代码中使用静态清理 Attribute。

## 其他资源

- [Project Settings 窗口](https://docs.unity3d.com/6000.7/Documentation/Manual/comp-ManagerGroup.html)
- [Editor Project Settings](https://docs.unity3d.com/6000.7/Documentation/Manual/class-EditorManager.html)
- [Toolbar](https://docs.unity3d.com/6000.7/Documentation/Manual/Toolbar.html)
- [[04-不进行Scene Reload进入Play Mode]]
- [Configurable Enter Play Mode](https://docs.unity3d.com/6000.7/Documentation/Manual/configurable-enter-play-mode.html)

---

## 文档导航

- 上一页：[[02-Domain和Scene重载执行顺序参考]]
- 目录：[[00-代码和场景重载]]
- 下一页：[[04-不进行Scene Reload进入Play Mode]]
