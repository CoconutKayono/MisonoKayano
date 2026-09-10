# 泛型 Job 支持

> 原文：[Generic job support](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-generic-jobs.html)

虽然 Burst 支持泛型，但对泛型 Job 或函数指针的支持有限。如果发现某个 Job 在 Editor 中以全速运行，但在构建后的 Player 中没有以全速运行，问题可能与泛型 Job 有关。

下面的示例定义了一个泛型 Job：

```csharp
// 直接使用的泛型 Job
[BurstCompile]
struct MyGenericJob<TData> : IJob where TData : struct {
    public void Execute() { ... }
}
```

也可以按如下方式嵌套泛型 Job：

```csharp
// 嵌套的泛型 Job
public class MyGenericSystem<TData> where TData : struct {
    [BurstCompile]
    struct MyGenericJob  : IJob {
        public void Execute() { ... }
    }

    public void Run()
    {
        var myJob = new MyGenericJob(); // 隐式类型为 MyGenericSystem<TData>.MyGenericJob
        myJob.Schedule();
    }
}
```

经过 Burst 编译的 Job 结构如下：

```csharp
// 直接使用的泛型 Job
var myJob = new MyGenericJob<int>();
myJob.Schedule();

// 嵌套的泛型 Job
var myJobSystem = new MyGenericSystem<float>();
myJobSystem.Run();
```

在这两种情况下，构建 Player 时，Burst 都能检测到需要编译 `MyGenericJob<int>` 和 `MyGenericJob<float>`。这是因为泛型 Job（对于嵌套 Job，则是包围它的类型）使用了完全解析的泛型参数（`int` 和 `float`）。

但是，如果通过泛型参数间接使用这些 Job，Burst 编译器就无法在构建 Player 时检测出需要编译哪些 Job：

```csharp
public static void GenericJobSchedule<TData>() where TData: struct {
    // 泛型参数：泛型参数 TData
    // Burst 编译器在构建独立 Player 时不会检测到此 Job。
    var job = new MyGenericJob<TData>();
    job.Schedule();
}

// 隐式构造的 MyGenericJob<int> 会在 Editor 中以全速 Burst 运行，
// 但在构建独立 Player 时不会被检测到。
GenericJobSchedule<int>();
```

如果在来自类型的泛型参数上下文中声明 Job，也有同样的限制：

```csharp
// 泛型参数 TData
public class SuperJobSystem<TData>
{
    // 泛型参数：泛型参数 TData
    // Burst 编译器在构建独立 Player 时不会检测到此 Job。
    public MyGenericJob<TData> MyJob;
}
```

如果要使用泛型 Job，必须直接使用完全解析的泛型参数（例如 `int`、`MyOtherStruct`）。不能通过泛型参数间接使用它们（例如 `MyGenericJob<TContext>`）。

> 重要：Burst 不支持通过泛型方法调度泛型 Job。

## 函数指针

函数指针受到限制，因为不能通过 Burst 使用泛型 Delegate：

```csharp
public delegate void MyGenericDelegate<T>(ref TData data) where TData: struct;

var myGenericDelegate = new MyGenericDelegate<int>(MyIntDelegateImpl);
// 编译此函数指针会失败。
var myGenericFunctionPointer = BurstCompiler.CompileFunctionPointer<MyGenericDelegate<int>>(myGenericDelegate);
```

此限制源于 .NET Runtime 无法与这类 Delegate 进行互操作。

有关更多信息，请参阅[函数指针](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-function-pointers.html)。

## 其他资源

- [[05-Play Mode中的Burst编译]]
- [Job system](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system.html)

---

## 文档导航

- 上一页：[[03-排除代码不进行Burst编译]]
- 目录：[[00-配置Burst编译]]
- 下一页：[[05-Play Mode中的Burst编译]]
