# Burst 菜单参考

> 原文：[Burst menu reference](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/editor-burst-menu.html)

使用 Burst 菜单中的设置控制 Burst 在 Unity Editor 中的工作方式。这些设置只控制 Editor 中的 Burst 编译。要配置 Player 构建中的 Burst 编译，请参阅 [[08-Burst AOT设置参考]]。

要访问 Burst 菜单，请转到 **Jobs > Burst**。可用设置如下：

| 设置 | 功能 |
| --- | --- |
| **Enable Compilation** | 启用 Burst 编译。启用后，Burst 会编译带有 `[BurstCompile]` 属性的 Job 和 Burst 自定义委托。 |
| **Enable Safety Checks** | 选择 Burst 应使用的安全检查。更多信息请参阅 [[#Enable Safety Checks 设置]]。 |
| Off | 禁用所有 Burst Job 和函数指针的安全检查。只有在希望从 Editor 内捕获的数据中获得更真实的性能分析结果时才使用此设置。重新加载 Editor 时，此设置始终会重置为 **On**。 |
| On | 对使用集合容器的代码启用安全检查（例如 `NativeArray<T>`）。检查包括 Job 数据依赖关系和容器索引越界。这是默认设置。 |
| Force On | 即使 Job 和函数指针设置了 `DisableSafetyChecks = true`，也强制启用安全检查。使用此设置可以排除安全检查本应捕获的问题。 |
| **Synchronous Compilation** | 启用 Burst 同步编译。更多信息请参阅 [同步编译](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-synchronous.html)。 |
| **Native Debug Mode Compilation** | 启用后，停用 Burst 编译的所有代码上的优化。这使得使用 Native Debugger 调试更加容易。更多信息请参阅 [[10-调试和性能分析工具#Native 调试]]。 |
| **Show Timings** | 启用后，将 Editor 中 JIT 编译 Job 所需的时间记录到 Console。更多信息请参阅 [[#Show Timings 设置]]。 |
| **Open Inspector** | 打开 [[11-Burst Inspector窗口参考]]。 |

## Enable Safety Checks 设置

要禁用 Burst 的安全检查代码，请使用 [`DisableSafetyChecks`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Burst.BurstCompileAttribute.DisableSafetyChecks.html)。这样可以生成更快的代码，但必须确保以安全方式使用容器。

要对 Job 或函数指针禁用安全检查，请将 `DisableSafetyChecks` 设置为 `true`：

```csharp
[BurstCompile(DisableSafetyChecks = true)]
public struct MyJob : IJob
{
    // ...
}
```

如果在 Editor 中将 **Enable Safety Checks** 设置为 **On**，Burst 会忽略代码中明确标记的 `DisableSafetyChecks = true`，并在检查代码时对其进行安全检查。选择 **Force On** 可让 Burst 检查所有代码，包括标记了 `DisableSafetyChecks = true` 的代码。

## Show Timings 设置

启用 **Show Timings** 设置后，Unity 会在 Console 窗口中为 Burst 编译的每个入口点库记录一条输出。Burst 会将编译批处理为每个程序集包含若干方法的单元，并将多个入口点组合到同一个编译任务中。如果要通过 [Unity Discussions](https://forum.unity.com/forums/burst.629/) 向 Burst 编译器团队报告编译时间异常值，此输出会很有用。

Unity 将 Burst 的输出拆分为以下主要部分：

- 方法发现（Burst 确定需要编译的内容）。
- 前端（Burst 将 C# IL 转换为 LLVM IR 模块）。
- 中端（Burst 特化、优化并清理模块）。
- 后端（Burst 将 LLVM IR 模块转换为原生 DLL）。

前端和优化器的编译时间与 Burst 需要编译的操作数量成线性关系。函数和指令越多，编译时间越长。泛型函数越多，前端性能计时越高，因为泛型解析具有不可忽略的成本。

后端的编译时间随模块中的入口点数量增加而增加。这是因为每个入口点都位于自己的原生目标文件中。

如果优化器耗时过长，可以使用 `[BurstCompile(OptimizeFor = OptimizeFor.FastCompilation)]`，它会减少优化但显著加快编译。请在更改前后分别分析 Job，确认这种权衡适合该入口点。

## 其他资源

- [[11-Burst Inspector窗口参考]]
- [Job system](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system.html)


---

## 文档导航

- 上一页：[[11-Burst Inspector窗口参考]]
- 目录：[[00-Burst编译]]
- 下一页：[[13-Burst Editor窗口参考]]
