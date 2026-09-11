# Burst Modding 支持

> 原文：[Burst modding support](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/modding-support.html)

可以加载额外的 Burst 编译库，从而创建使用 Burst 编译代码的 Mod。

Burst 只提供加载额外库的方法，不提供创建 Mod 的工具。你需要使用 Unity Editor 编译这些额外的库。

本节给出一种使用 Burst 制作 Mod 的示例方案，仅作为概念验证。

## 支持的使用方式

此功能只能在 Play 模式（或 Standalone Player）中使用。

请尽早加载这些库，并确保在第一次使用 Burst 编译的 C# 方法之前完成加载。当退出 Editor 的 Play 模式或退出 Standalone Player 时，Unity 会卸载 `BurstRuntime.LoadAdditionalLibraries` 加载的所有 Burst 库。

## Mod 系统示例

> **注意**：此示例范围有限。要理解此示例，需要了解[程序集和程序集定义](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-files.html)。

下面的示例声明一个 Mod 必须遵守的接口：

```csharp
using UnityEngine;

public interface PluginModule
{
    void Startup(GameObject gameObject);
    void Update(GameObject gameObject);
}
```

可以使用此接口创建符合这些规范的新类，并将其与应用程序分开发布。只传入一个 `GameObject` 可以限制插件能够影响的状态。

### Mod 管理器

下面是一个 Mod 管理器示例：

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using UnityEngine;
using Unity.Burst;

public class PluginManager : MonoBehaviour
{
    public bool modsEnabled;
    public GameObject objectForPlugins;

    List<PluginModule> plugins;

    void Start()
    {
        plugins = new List<PluginModule>();

        // 如果禁用了 Mod，则提前退出——这样可以禁用 Mod、进入 Play Mode、退出 Play Mode，
        // 并确保托管程序集已被卸载（假定发生了 DomainReload）。
        if (!modsEnabled)
            return;

        var folder = Path.GetFullPath(Path.Combine(Application.dataPath, "..", "Mods"));
        if (Directory.Exists(folder))
        {
            var mods = Directory.GetDirectories(folder);

            foreach (var mod in mods)
            {
                var modName = Path.GetFileName(mod);
                var monoAssembly = Path.Combine(mod, $"{modName}_managed.dll");

                if (File.Exists(monoAssembly))
                {
                    var managedPlugin = Assembly.LoadFile(monoAssembly);

                    var pluginModule = managedPlugin.GetType("MyPluginModule");

                    var plugin = Activator.CreateInstance(pluginModule) as PluginModule;

                    plugins.Add(plugin);
                }

                var burstedAssembly = Path.Combine(mod, $"{modName}_win_x86_64.dll");      // Burst dll（假定为 Windows 64 位）
                if (File.Exists(burstedAssembly))
                {
                    BurstRuntime.LoadAdditionalLibrary(burstedAssembly);
                }
            }
        }

        foreach (var plugin in plugins)
        {
            plugin.Startup(objectForPlugins);
        }
    }

    // 每帧调用一次 Update
    void Update()
    {
        foreach (var plugin in plugins)
        {
            plugin.Update(objectForPlugins);
        }
    }
}
```

此代码会扫描 `Mods` 文件夹，并尝试加载其中每个子文件夹内的托管 DLL 和 Burst 编译 DLL。它会将这些 DLL 添加到内部列表中，然后遍历列表并调用相应的接口函数。

文件名是任意的；请参阅[简单的 Create Mod 菜单按钮](#简单的-Create-Mod-菜单按钮)，其中包含生成这些文件的代码。

由于此代码会将托管程序集加载到当前域中，因此需要域重载才能在覆盖程序集之前将其卸载。Unity 会在退出 Play 模式时自动卸载 Burst DLL。因此，示例中包含一个用于禁用 Mod 系统的布尔值，以便在 Editor 中测试。

### 使用 Burst 的 Mod

为此创建一个单独的 Unity 项目，用它来生成 Mod。

下面的脚本附加到包含名为 **Main UI Label** 的文本组件的 UI Canvas，并在使用 Mod 时更改文本。文本可能是 **Plugin Updated : Bursted** 或 **Plugin Updated : Not Bursted**。默认情况下会看到 **Plugin Updated : Bursted**；但如果注释掉 `PluginManager` 中加载 Burst 库的代码行，Burst 编译的代码就不会加载，消息会相应变为 **Plugin Updated : Not Bursted**。

```csharp
using Unity.Burst;
using Unity.Collections;
using Unity.Jobs;
using UnityEngine;
using UnityEngine.UI;

public class MyPluginModule : PluginModule
{
    Text textComponent;

    public void Startup(GameObject gameObject)
    {
        var childTextComponents = gameObject.GetComponentsInChildren<Text>();
        textComponent = null;
        foreach (var child in childTextComponents)
        {
            if (child.name == "Main UI Label")
            {
                textComponent = child;
            }
        }

        if (textComponent==null)
        {
            Debug.LogError("something went wrong and i couldn't find the UI component i wanted to modify");
        }
    }

    public void Update(GameObject gameObject)
    {
        if (textComponent != null)
        {
            var t = new CheckBurstedJob { flag = new NativeArray<int>(1, Allocator.TempJob, NativeArrayOptions.UninitializedMemory) };

            t.Run();

            if (t.flag[0] == 0)
                textComponent.text = "Plugin Updated : Not Bursted";
            else
                textComponent.text = "Plugin Updated : Bursted";

            t.flag.Dispose();
        }
    }

    [BurstCompile]
    struct CheckBurstedJob : IJob
    {
        public NativeArray<int> flag;

        [BurstDiscard]
        void CheckBurst()
        {
            flag[0] = 0;
        }

        public void Execute()
        {
            flag[0] = 1;
            CheckBurst();
        }
    }

}
```

将前面的脚本与程序集定义文件放在同一个文件夹中，并将程序集命名为 `TestMod_Managed`，这样下一个脚本就能找到托管部分。

### 简单的 Create Mod 菜单按钮

下面的脚本添加一个菜单按钮。使用该菜单按钮时，它会构建一个 Standalone Player，然后将 C# 托管 DLL 和 `lib_burst_generated.dll` 复制到所选的 `Mod` 文件夹中。本示例假定使用 Windows。

```csharp
using UnityEditor;
using System.IO;
using UnityEngine;

public class ScriptBatch
{
    [MenuItem("Modding/Build X64 Mod (Example)")]
    public static void BuildGame()
    {
        string modName = "TestMod";

        string projectFolder = Path.Combine(Application.dataPath, "..");
        string buildFolder = Path.Combine(projectFolder, "PluginTemp");

        // 获取文件名。
        string path = EditorUtility.SaveFolderPanel("Choose Final Mod Location", "", "");

        FileUtil.DeleteFileOrDirectory(buildFolder);
        Directory.CreateDirectory(buildFolder);

        // 构建 Player。
        var report = BuildPipeline.BuildPlayer(new[] { "Assets/Scenes/SampleScene.unity" }, Path.Combine(buildFolder, $"{modName}.exe"), BuildTarget.StandaloneWindows64, BuildOptions.Development);

        if (report.summary.result == UnityEditor.Build.Reporting.BuildResult.Succeeded)
        {
            // 复制 Managed 库
            var managedDest = Path.Combine(path, $"{modName}_Managed.dll");
            var managedSrc = Path.Combine(buildFolder, $"{modName}_Data/Managed/{modName}_Managed.dll");
            FileUtil.DeleteFileOrDirectory(managedDest);
            if (!File.Exists(managedDest))  // Managed 端未卸载
                FileUtil.CopyFileOrDirectory(managedSrc, managedDest);
            else
                Debug.LogWarning($"Couldn't update managed dll, {managedDest} is it currently in use?");

            // 复制 Burst 库
            var burstedDest = Path.Combine(path, $"{modName}_win_x86_64.dll");
            var burstedSrc = Path.Combine(buildFolder, $"{modName}_Data/Plugins/x86_64/lib_burst_generated.dll");
            FileUtil.DeleteFileOrDirectory(burstedDest);
            if (!File.Exists(burstedDest))
                FileUtil.CopyFileOrDirectory(burstedSrc, burstedDest);
            else
                Debug.LogWarning($"Couldn't update bursted dll, {burstedDest} is it currently in use?");
        }
    }
}
```

## 其他资源

- [导入并配置插件](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-in-inspector.html)


---

## 文档导航

- 上一页：[[14-浮点精度和确定性]]
- 目录：[[00-Burst编译]]
- 下一页：[[00-条件编译]]
