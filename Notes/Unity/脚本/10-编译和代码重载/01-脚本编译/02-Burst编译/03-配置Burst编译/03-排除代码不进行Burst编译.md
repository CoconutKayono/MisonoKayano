# 排除代码不进行 Burst 编译

> 原文：[Excluding code from Burst compilation](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-burstdiscard.html)

默认情况下，Burst 会编译使用 `[BurstCompile]` Attribute 修饰的 Job 中的所有方法。但有些方法不适合进行 Burst 编译。例如，使用 Managed Object 进行日志记录，或检查只在 Managed 环境中有效的内容的方法，只能在 .NET Runtime 中运行。

在这种情况下，可以将 [`[BurstDiscard]` Attribute](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Burst.BurstDiscardAttribute.html) 添加到方法或属性上，将其排除在 Burst 编译之外：

```csharp
[BurstCompile]
public struct MyJob : IJob
{
    public void Execute()
    {
        // 仅在完整的 .NET Runtime 中运行
        // 使用 [BurstCompile] Attribute 编译此 Job 时，此方法调用会被丢弃
        MethodToDiscard();
    }

    [BurstDiscard]
    private static void MethodToDiscard(int arg)
    {
        Debug.Log($"This is a test: {arg}");
    }
}
```

> 注意：带有 `[BurstDiscard]` 的方法不能有返回值。

可以使用 `ref` 或 `out` 参数来指示代码当前运行在 Burst 还是 Managed 环境中：

```csharp
[BurstDiscard]
private static void SetIfManaged(ref bool b) => b = false;

private static bool IsBurst()
{
    var b = true;
    SetIfManaged(ref b);
    return b;
}
```

## 其他资源

- [`[BurstDiscard]` Attribute API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Burst.BurstDiscardAttribute.html)
- [[01-标记代码进行Burst编译]]

---

## 文档导航

- 上一页：[[02-为程序集定义Burst选项]]
- 目录：[[00-配置Burst编译]]
- 下一页：[[04-泛型Job支持]]
