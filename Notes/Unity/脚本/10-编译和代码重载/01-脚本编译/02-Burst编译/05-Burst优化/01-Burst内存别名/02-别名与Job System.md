# 别名与 Job System

> 原文：[Aliasing and the job system](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/aliasing-job-system.html)

Unity 的 Job System infrastructure 对 Job struct 中哪些内容可以存在别名有一些限制：

- 作为 Job struct 成员、带有 `[NativeContainer]` attribute 的 struct（例如 `NativeArray` 和 `NativeSlice`）彼此之间不存在别名。
- 带有 `[NativeDisableContainerSafetyRestriction]` attribute 的 Job struct 成员可以与其他成员存在别名，因为此 attribute 明确选择允许这种别名。
- 指向带有 `[NativeContainer]` attribute 的 struct 的指针不能出现在其他带有 `[NativeContainer]` attribute 的 struct 中。例如，不能使用 `NativeArray<NativeSlice<T>>`。
- Job struct 默认是 `[NoAlias]` struct，即不允许 struct 的地址与其成员别名。

可以对 Job struct 及其成员使用实验性 `[Alias]` attribute，退出这些 aliasing 保证。该 attribute 受 `UNITY_BURST_EXPERIMENTAL_ALIAS_ATTRIBUTE` preprocessor define 控制。

下面的 Job 示例展示了这些限制在实践中的工作方式：

```csharp
[BurstCompile]
private struct MyJob : IJob
{
    public NativeArray<float> a;
    public NativeArray<float> b;
    public NativeSlice<int> c;

    [NativeDisableContainerSafetyRestriction]
    public NativeArray<byte> d;

    public void Execute() { ... }
}
```

`a`、`b` 和 `c` 彼此之间不存在别名。

`d` 可以与 `a`、`b` 或 `c` 存在别名。

> **提示**：如果熟悉 C/C++ 的 Type Based Alias Analysis（TBAA），可能会认为 `d` 与 `a`、`b` 或 `c` 类型不同，所以不应存在别名。然而在 C# 中，指针没有“指向不同类型就不会别名”的假设。因此，系统假设 `d` 可以与 `a`、`b` 或 `c` 存在别名。

## 其他资源

- [[00-Burst内存别名]]
- [[03-声明无别名指针和结构体]]
- [[../../../../../11-代码优化/03-Job System/00-Job System]]

---

## 文档导航

- 上一页：[[01-内存别名简介]]
- 目录：[[00-Burst内存别名]]
- 下一页：[[03-声明无别名指针和结构体]]
