# 13. Domain Reload

> 原文：[13. Domain reload](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/domain-reload.html)

## 学习目标

本节将学习如何触发并等待 Domain Reload。

## 简介与动机

当执行会影响项目脚本的操作时，Unity 会执行 Domain Reload。由于 Domain Reload 会重启所有脚本，因此必须通过产生一个 [`WaitForDomainReload`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.WaitForDomainReload.html) 来标记预期中的 Domain Reload。该命令会停止后续代码执行，并在 Domain Reload 完成后恢复执行。

也可以产生一个 [`RecompileScripts`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.RecompileScripts.html) 命令。它与 `WaitForDomainReload` 的作用相同，但会额外执行 `AssetDatabase.Reload()` 调用。两个调用都可以配置为声明脚本编译是否应当成功。

如果测试运行期间发生 Domain Reload，却没有产生这些命令中的任何一个，测试就会失败，并报告发生了意外的 Domain Reload。

## 练习

[sample](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/test-framework-general-introduction.html#import-samples) `13_DomainReload_Solution` 已经准备好了名为 `ScriptAddingTests` 的测试类。

测试中已经实现了两个辅助方法：

- `CreateScript` 创建一个包含 `MyTempScript` 类的 C# 脚本，该类有一个名为 `Verify` 的方法。
- `VerifyScript` 使用反射实例化 `MyTempScript`，并返回 `Verify` 方法的值。预期返回值是字符串 `"OK"`。

执行 `CreateScript` 后，Unity 会在项目中得到一个新的 C# 文件，因此需要重新编译。任务是创建一个测试，调用 `CreateScript`，处理 Domain Reload，然后验证 `VerifyScript` 的输出。

还要记得清理测试产生的文件：删除该文件，并再次编译脚本。建议将清理逻辑放在 `TearDown` 或 `UnityTearDown` 中，这样即使测试失败也会执行。

> **重要**：导入后，必须将 sample 测试文件夹 `Tests_13` 移动到 `Assets` 文件夹中，本练习才能正常运行。

## 提示

- 如果 `RecompileScripts` 因为是 internal API 而不可用，需要将 Unity Test Framework package 升级到 1.1.0 或更高版本。
- 如果使用非 Windows 系统，可能需要修改 `k_fileName` 中的路径，或者使用 C# 的 [`Path.Combine`](https://docs.microsoft.com/en-us/dotnet/api/system.io.path.combine?view=net-6.0)，以获得更好的跨平台兼容性。

## 解决方案

完整解决方案位于 sample `13_DomainReload_Solution` 中。

测试可以实现如下：

```csharp
internal class ScriptAddingTests
{
    private const string k_fileName = @"Assets\\Tests\\TempScript.cs";

    [UnityTest]
    public IEnumerator CreatedScriptIsVerified()
    {
        CreateScript();
        yield return new RecompileScripts();

        var verification = VerifyScript();

        Assert.That(verification, Is.EqualTo("OK"));
    }

    [UnityTearDown]
    public IEnumerator Teardown()
    {
        if (!File.Exists(k_fileName))
        {
            yield break;
        }

        File.Delete(k_fileName);
        yield return new RecompileScripts();
    }

    private void CreateScript()
    {
        File.WriteAllText(k_fileName, @"
        public class MyTempScript {
            public string Verify()
            {
                return ""OK"";
            }
        }");
    }

    private string VerifyScript()
    {
        Type type = Type.GetType("MyTempScript", true);

        object instance = Activator.CreateInstance(type);

        var verifyMethod = type.GetMethod("Verify", BindingFlags.Instance | BindingFlags.Public);

        var verifyResult = verifyMethod.Invoke(instance, new object[0]);
        return verifyResult as string;
    }
}
```

## 其他资源

- [RecompileScripts API 参考](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.RecompileScripts.html)
- [WaitForDomainReload API 参考](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.WaitForDomainReload.html)

---

## 文档导航

- 上一页：[[11-构建时设置和清理]]
- 目录：[[00-Unity Test Framework通用简介]]
- 下一页：[[13-保留测试状态]]
