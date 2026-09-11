# 修改 Player 构建参考

> 原文：[Modifying a Player build for tests](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-attribute-testplayerbuildmodifier.html)

可以在特定平台的独立 Player 中运行 Play Mode 测试。[TestPlayerBuildModifier](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEditor.TestTools.TestPlayerBuildModifierAttribute.html) 属性提供多个可配置选项，用于控制为运行测试而构建的 Player 的属性。

## 修改 Play Mode 测试的 Player 构建选项

可以修改测试 Player 的 [BuildPlayerOptions](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildPlayerOptions.html)，以便在运行 Play Mode 测试时实现自定义行为。修改构建选项可以改变构建输出位置，也可以改变 [BuildOptions](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildOptions.html)。

要修改 BuildPlayerOptions，请执行以下操作：

- 实现 ITestPlayerBuildModifier。
- 在程序集级别的 TestPlayerBuildModifier 属性中引用该实现类型。

下面的示例演示了这一过程：

~~~csharp
using UnityEditor;
using UnityEditor.TestTools;

[assembly:TestPlayerBuildModifier(typeof(BuildModifier))]
public class BuildModifier : ITestPlayerBuildModifier
{
    public BuildPlayerOptions ModifyOptions(BuildPlayerOptions playerOptions)
    {
        if (playerOptions.target == BuildTarget.iOS)
        {
            playerOptions.options |= BuildOptions.SymlinkLibraries; // Enable symlink libraries when running on iOS
        }
        
        playerOptions.options |= BuildOptions.AllowDebugging; // Enable allow Debugging flag on the test Player.
        return playerOptions;
    }
}
~~~

> **注意：** 构建 Player 时，会包含所有已加载程序集中的 TestPlayerBuildModifier 属性，而不受当前使用的测试筛选器影响。由于实现引用 UnityEditor 命名空间，通常应在仅限 Editor 的程序集中实现代码，因为其他程序集无法使用 UnityEditor 命名空间。

## 构建 Player 但不运行测试

可以使用 Unity Editor 构建包含测试的 Player，但不[运行测试](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/workflow-run-playmode-test-standalone.html)。例如，这样可以在另一台机器上运行 Player。此时，需要修改 Player 的构建方式，并实现自定义的测试结果处理方式。

可以使用 TestPlayerBuildModifier 将 BuildOptions 设置为把 Player 构建到特定位置，但不运行它。结合 [[02-构建时设置和清理#prebuildsetup-and-postbuildcleanup|PostBuildCleanup]]，可以在构建完成后自动退出 Editor。下面的示例演示了这一过程：

~~~csharp
using System;
using System.IO;
using System.Linq;
using Tests;
using UnityEditor;
using UnityEditor.TestTools;
using UnityEngine;
using UnityEngine.TestTools;

[assembly:TestPlayerBuildModifier(typeof(HeadlessPlayModeSetup))]
[assembly:PostBuildCleanup(typeof(HeadlessPlayModeSetup))]

namespace Tests
{
    public class HeadlessPlayModeSetup : ITestPlayerBuildModifier, IPostBuildCleanup
    {
        private static bool s_RunningPlayerTests;
        public BuildPlayerOptions ModifyOptions(BuildPlayerOptions playerOptions)
        {
            // Do not launch the player after the build completes.
            playerOptions.options &= ~BuildOptions.AutoRunPlayer;

            // Set the headlessBuildLocation to the output directory you desire. It does not need to be inside the project.
            var headlessBuildLocation = Path.GetFullPath(Path.Combine(Application.dataPath, ".//..//PlayModeTestPlayer"));
            var fileName = Path.GetFileName(playerOptions.locationPathName);
            if (!string.IsNullOrEmpty(fileName))
            {
                headlessBuildLocation = Path.Combine(headlessBuildLocation, fileName);
            }
            playerOptions.locationPathName = headlessBuildLocation;

            // Instruct the cleanup to exit the Editor if the run came from the command line. 
            // The variable is static because the cleanup is being invoked in a new instance of the class.
            s_RunningPlayerTests = true;
            return playerOptions;
        }

        public void Cleanup()
        {
            if (s_RunningPlayerTests && IsRunningTestsFromCommandLine())
            {
                // Exit the Editor on the next update, allowing for other PostBuildCleanup steps to run.
                EditorApplication.update += () => { EditorApplication.Exit(0); };
            }
        }

        private static bool IsRunningTestsFromCommandLine()
        {
            var commandLineArgs = Environment.GetCommandLineArgs();
            return commandLineArgs.Any(value => value == "-runTests");
        }
    }
}
~~~

如果 Play Mode 测试运行后 Editor 仍在运行，Player 会尝试使用 [PlayerConnection](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.PlayerConnection.PlayerConnection.html) 报告结果。构建时，PlayerConnection 会包含运行 Editor 所在机器的 IP 地址。

要实现自定义的结果报告方式，请让 Player 中的某个程序集包含 [TestRunCallback](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestRunner.TestRunCallbackAttribute.html)。在 RunFinished 中，可以通过调用 result.ToXml(true) 从 [NUnit](http://www.nunit.org/) 测试结果中获取完整的 XML 测试报告。然后可以保存结果、将其保存到设备，或按需发送到另一台机器。

## 其他资源

- [[00-在Player中运行Play Mode测试]]


---

## 文档导航

- 上一页：[[00-在Player中运行Play Mode测试]]
- 目录：[[00-在Player中运行Play Mode测试]]
- 下一页：[[00-Unity Test Framework学习材料]]
