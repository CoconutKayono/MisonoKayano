# Play Mode 中的 Burst 编译

> 原文：[Burst compilation in Play mode](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-synchronous.html)

当你[构建项目](https://docs.unity3d.com/6000.7/Documentation/Manual/building-and-publishing.html)时，Burst 会将所有受支持的代码提前（AOT）编译为 Native Library，Unity 会将该库随应用一起发布。

在 Editor 的 Play Mode 中预览应用时，Burst 提供以下编译模式：

- **Asynchronous**：标记为进行 Burst 编译的代码部分，在等待 Burst 编译完成期间，可以在 .NET Runtime 中作为 Managed、即时（JIT）编译的代码运行。这是默认行为。
- **Synchronous**：标记为进行 Burst 编译的代码部分只能作为 Burst 编译的 Native Code 运行，应用必须等待 Burst 编译完成。

## 同步编译

要在 Play Mode 中强制进行同步编译，请将 [`CompileSynchronously`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Burst.BurstCompileAttribute.CompileSynchronously.html) 属性设置为 `true`：

```csharp
[BurstCompile(CompileSynchronously = true)]
public struct MyJob : IJob
{
    // ...
}
```

等待同步编译会影响当前正在运行的帧，可能造成卡顿并使应用无响应。只建议在以下情况下使用同步编译：

- 如果有一个只运行一次的长时间 Job。编译后代码的性能提升可能超过同步编译带来的负面影响。
- 如果正在分析 Burst Job，并希望测试 Burst 编译器生成的代码。此时应进行预热，以丢弃 Job 首次调用的计时数据，因为分析数据包含编译时间，会使结果失真。
- 帮助调试 Managed 代码与 Burst 编译代码之间的差异。

## 其他资源

- [[01-标记代码进行Burst编译]]
- [[04-泛型Job支持]]

---

## 文档导航

- 上一页：[[04-泛型Job支持]]
- 目录：[[00-配置Burst编译]]
- 下一页：[[06-编译警告参考]]
