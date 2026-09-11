# 为程序集定义 Burst 选项

> 原文：[Defining Burst options for an assembly](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-burstcompile-assembly.html)

在 assembly 上使用 `[BurstCompile]` attribute，为 assembly 中的所有 Burst Job 和 function pointer 设置选项：

```csharp
[assembly: BurstCompile(CompileSynchronously = true)]
```

例如，如果某个 assembly 只包含需要快速运行的游戏代码，可以使用：

```csharp
[assembly: BurstCompile(OptimizeFor = OptimizeFor.FastCompilation)]
```

这表示 Burst 会尽可能快地编译代码，因此可以更快地迭代游戏代码。同时，其他 assembly 会按照之前的方式编译，因此可以更好地控制 Burst 如何处理代码。

Assembly 级别的 `BurstCompile` attribute 会与 Job 或 function pointer 上的 attribute，以及 Editor 中 Burst 菜单的全局设置共同作用。Burst 按以下顺序确定优先级：

1. **Burst 菜单设置优先**。例如，如果从 Burst 菜单启用了 Native Debug Compilation，Burst 总是以可调试的方式编译代码。
2. Burst 检查 Job 或 function pointer 上的 `BurstCompile` attribute。如果 `BurstCompile` 中设置了 `CompileSynchronously = true`，Burst 就会同步编译。
3. 其余设置取自 assembly 级别的 attribute。

例如：

```csharp
[assembly: BurstCompile(OptimizeFor = OptimizeFor.FastCompilation)]

// This job will be optimized for fast-compilation, because the per-assembly BurstCompile asked for it
[BurstCompile]
struct AJob : IJob
{
    // ...
}

// This job will be optimized for size, because the per-job BurstCompile asked for it
[BurstCompile(OptimizeFor = OptimizeFor.Size)]
struct BJob : IJob
{
    // ...
}
```

## 其他资源

- [[01-标记代码进行Burst编译]]
- [`[BurstCompile]` attribute API reference](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Burst.BurstCompileAttribute.html)

---

## 文档导航

- 上一页：[[01-标记代码进行Burst编译]]
- 目录：[[00-配置Burst编译]]
- 下一页：[[03-排除代码不进行Burst编译]]
