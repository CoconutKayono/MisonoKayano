# 调用 Burst 编译的代码

> 原文：[Calling Burst-compiled code](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-calling-burst-code.html)

可以直接从托管代码调用 Burst 编译的方法。不支持调用泛型方法或声明类型为泛型的方法；除此以外，规则与[函数指针](03-函数指针.md)相同。不过，你不必处理函数指针所需的额外样板代码。

下面的示例展示一个 Burst 编译的工具类。由于它使用结构体，根据[函数指针](03-函数指针.md)的规则，参数按引用传递：

```csharp
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

可以像这样从托管代码使用该方法：

```csharp
public class MyMonoBehaviour : MonoBehaviour
{
    void Start()
    {
        var mula = new float4(1, 2, 3, 4);
        var mulb = new float4(-1,1,-1,1);
        var add = new float4(99,0,0,0);
        MyBurstUtilityClass.BurstCompiled_MultiplyAdd(mula, mulb, add, out var result);
        Debug.Log(result);
    }
}
```

将此脚本附加到对象并运行时，日志中会打印 `float4(98f, 2f, -3f, 4f)`。

## 代码转换

Burst 使用 IL 后处理自动将代码转换为函数指针和调用。更多信息请参阅[函数指针](03-函数指针.md)。

要禁用直接调用转换，请在 `BurstCompile` 选项中添加 `DisableDirectCall = true`。这会阻止后处理器处理该代码：

```csharp
[BurstCompile]
public static class MyBurstUtilityClass
{
    [BurstCompile(DisableDirectCall = true)]
    public static void BurstCompiled_MultiplyAdd(in float4 mula, in float4 mulb, in float4 add, out float4 result)
    {
        result = mula * mulb + add;
    }
}
```

## 相关资源

- [HPC# 概览](01-高性能CSharp简介.md)
- [函数指针](03-函数指针.md)

---

## 文档导航

- 上一页：[[01-高性能CSharp简介]]
- 目录：[[00-CSharp语言支持]]
- 下一页：[[03-函数指针]]
