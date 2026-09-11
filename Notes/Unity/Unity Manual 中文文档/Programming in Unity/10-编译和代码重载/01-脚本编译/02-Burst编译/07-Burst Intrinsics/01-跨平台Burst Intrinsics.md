# 跨平台 Burst Intrinsics

> 原文：[Cross-platform Burst intrinsics](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics-common.html)

`Unity.Burst.Intrinsics.Common` Intrinsics 用于实现 Burst 所支持硬件目标之间共享的功能。

## Pause

`Unity.Burst.Intrinsics.Common.Pause` 是一种请求 CPU 暂停当前线程的 Intrinsic。在 x86 上它映射为 `pause`，在 ARM 上映射为 `yield`。

可以使用它停止因争用原子访问而产生的自旋锁，从而减少该代码段中的争用和功耗。

## Prefetch

`Unity.Burst.Intrinsics.Common.Prefetch` 是一种 Intrinsic，用于向 Burst 提示应将某个内存位置预取到缓存中。

## umul128

使用 `Unity.Burst.Intrinsics.Common.umul128` Intrinsic 可以访问 128 位无符号乘法。这类乘法适用于哈希函数。在 x86 和 ARM 目标上，它与硬件指令一一对应。

## InterlockedAnd 与 InterlockedOr

`Unity.Burst.Intrinsics.Common.InterlockedAnd` 和 `Unity.Burst.Intrinsics.Common.InterlockedOr` 是提供原子 and/or 操作的 Intrinsics，适用于 `int`、`uint`、`long` 和 `ulong` 类型。

## 相关资源

- [Unity.Burst.Intrinsics.Common API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Burst.Intrinsics.Common.html)
- [[03-处理器特定SIMD扩展]]
- [[02-Burst Arm Neon Intrinsics参考]]

---

## 文档导航

- 上一页：[[00-Burst Intrinsics]]
- 目录：[[00-Burst Intrinsics]]
- 下一页：[[03-处理器特定SIMD扩展]]
