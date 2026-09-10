# 开始使用 Burst

> 原文：[Get started with Burst](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/getting-started.html)

可以使用 Burst 编译 Job，也可以编译非 Job C# 类型中的静态方法。要开始在代码中使用 Burst Compiler，请在 Job 或静态方法上添加 `[BurstCompile]` attribute。

有关应在何处以及何时应用 `[BurstCompile]` attribute 的信息，请参阅 [[03-配置Burst编译/01-标记代码进行Burst编译]]。

## 使用 Burst 编译 Job

对于 Job，只需将 `[BurstCompile]` attribute 添加到 Job 声明上，Burst 就会自动编译 Job 内部的所有内容。示例如下：

```csharp
using Unity.Burst;
using Unity.Collections;
using Unity.Jobs;
using UnityEngine;

public class MyBurst2Behavior : MonoBehaviour
{
    void Start()
    {
        var input = new NativeArray<float>(10, Allocator.Persistent);
        var output = new NativeArray<float>(1, Allocator.Persistent);
        for (int i = 0; i < input.Length; i++)
            input[i] = 1.0f * i;

        var job = new MyJob
        {
            Input = input,
            Output = output
        };
        job.Schedule().Complete();

        Debug.Log("The result of the sum is: " + output[0]);
        input.Dispose();
        output.Dispose();
    }

    // Using BurstCompile to compile a Job with Burst

    [BurstCompile]
    private struct MyJob : IJob
    {
        [ReadOnly]
        public NativeArray<float> Input;

        [WriteOnly]
        public NativeArray<float> Output;

        public void Execute()
        {
            float result = 0.0f;
            for (int i = 0; i < Input.Length; i++)
            {
                result += Input[i];
            }
            Output[0] = result;
        }
    }
}
```

## 使用 Burst 编译静态方法

对于静态方法，必须将 `[BurstCompile]` attribute 同时添加到希望 Burst 编译的每个方法，以及父类型的声明上。示例如下：

```csharp
using Unity.Burst;
using Unity.Collections;
using Unity.Jobs;
using UnityEngine;

[BurstCompile]
public static class MyBurstUtilityClass
{
    [BurstCompile]
    public static void BurstCompiled_MultiplyAdd(in float4 mula, in float4 mulb, in float4 add, out float4 result)
    {
        result = mula * mulb + add;
    }
}
```

有关如何从 C# 代码调用这个 Burst 编译的 utility class 及其成员方法，请参阅 [[06-CSharp语言支持/02-调用Burst编译代码]]。

## 限制

Burst 支持大多数 C# expressions 和 statements，但有少数例外。更多信息请参阅 [[06-CSharp语言支持/00-CSharp语言支持]]。

## 编译

Burst 在 Editor 的 Play mode 中对代码进行 just-in-time（JIT）编译，在应用程序运行于 Player 时进行 ahead-of-time（AOT）编译。有关编译的信息，请参阅 [[00-Burst编译]]。

## 命令行选项

可以在命令行向 Unity Editor 传递以下选项来控制 Burst：

- `--burst-disable-compilation`：禁用 Burst。
- `--burst-force-sync-compilation`：强制 Burst 进行同步编译。

更多信息请参阅 [[00-Burst编译]]。

## 其他资源

- [[00-Burst编译]]
- [`[BurstCompile]` attribute API reference](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Burst.BurstCompileAttribute.html)

---

## 文档导航

- 上一页：[[01-Burst简介]]
- 目录：[[00-Burst编译]]
- 下一页：[[03-配置Burst编译/00-配置Burst编译]]
