# IL2CPP 运行时代码检查

> 原文：[IL2CPP runtime code checks](https://docs.unity3d.com/6000.7/Documentation/Manual/il2cpp-runtime-checks.html)

你可以使用 `[Il2CppSetOption]` C# Attribute 及其 `Option` 参数，控制 IL2CPP Compiler 在生成的 C++ 代码中包含哪些安全检查。

`[Il2CppSetOption]` Attribute 不属于标准 Unity Editor 和 Engine 公开 API，但其源代码会作为 Unity 安装内容的一部分单独提供。要使用 `[Il2CppSetOption]` Attribute，请执行以下操作：

1. 在 Unity 版本的安装目录中，Windows 导航到 `Data\il2cpp` 目录，macOS 导航到 `Contents/Frameworks/il2cpp` 目录。
2. 找到 `Il2CppSetOptionAttribute.cs` 源文件。
3. 将源文件复制到项目的 `Assets` 文件夹中。

该 Attribute 支持以下选项：

| 属性 | 描述 | 默认值 |
| --- | --- | --- |
| **Null checks** | 建议保持此选项启用。禁用后，IL2CPP 生成的 C++ 代码不包含 null 检查，也不会抛出托管 `NullReferenceException` 异常。这可以提升运行时性能，但不会阻止代码访问 null 值，可能导致包括崩溃在内的非预期行为。 | Enabled |
| **Array bounds checks** | 建议保持此选项启用。禁用后，IL2CPP 生成的 C++ 代码不包含数组边界检查，也不会抛出托管 `IndexOutOfRangeException` 异常。这可能提升运行时性能，但会允许代码使用无效索引访问数组，可能导致错误行为，包括读写任意内存位置。在大多数情况下，这些内存访问不会立即产生副作用，并可能在没有明显警告的情况下破坏应用状态，使错误极难调试。 | Enabled |
| **Divide by zero checks** | 除非需要执行除零检查，否则请保持此选项禁用。启用后，IL2CPP 生成的 C++ 代码会对整数除法包含除零检查，并在需要时抛出托管 `DivideByZeroException` 异常。禁用后，IL2CPP 不会将整数除法的除零检查写入生成的 C++ 代码。<br><br>这些检查会影响运行时性能。 | Disabled |

以下示例展示如何使用 `[Il2CppSetOption]` Attribute：

```csharp
[Il2CppSetOption(Option.NullChecks, false)]
public static string MethodWithNullChecksDisabled()
{
    var tmp = new object();
    return tmp.ToString();
}
```

你可以将 `[Il2CppSetOption]` 应用于程序集、类型、方法和属性。Unity 使用最接近目标代码的作用域中的 Attribute。

```csharp
[Il2CppSetOption(Option.NullChecks, false)]
public class TypeWithNullChecksDisabled
{
    public static string AnyMethod()
    {
        // Unity doesn’t perform null checks in this method.
        var tmp = new object();
        return tmp.ToString();
    }

    [Il2CppSetOption(Option.NullChecks, true)]
    public static string MethodWithNullChecksEnabled()
    {
        // Unity performs null checks in this method.
        var tmp = new object();
        return tmp.ToString();
    }
}

public class SomeType
{
    [Il2CppSetOption(Option.NullChecks, false)]
    public string PropertyWithNullChecksDisabled
    {
        get
        {
            // Unity doesn't perform null checks here.
            var tmp = new object();
            return tmp.ToString();
        }
        set
        {
            // Unity doesn't perform null checks here.
            value.ToString();
        }
    }

    public string PropertyWithNullChecksDisabledOnGetterOnly
    {
        [Il2CppSetOption(Option.NullChecks, false)]
        get
        {
            // Unity doesn’t perform null checks here.
            var tmp = new object();
            return tmp.ToString();
        }
        set
        {
            // Unity performs null checks here.
            value.ToString();
        }
    }
}
```

## 其他资源

- [[02-IL2CPP托管Stack Trace]]
- [[04-额外IL2CPP编译器参数]]


---

## 文档导航

- 上一页：[[02-IL2CPP托管Stack Trace]]
- 目录：[[00-IL2CPP脚本后端]]
- 下一页：[[04-额外IL2CPP编译器参数]]
