# 将资源构建为 AssetBundle（Build assets into AssetBundles）

> 来源：[Unity 6000.7 官方手册 · Build assets into AssetBundles](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Building.html)

要将资源构建为 AssetBundle，你必须先将资源分配到 AssetBundle——可以在 Unity 编辑器中完成，也可以通过脚本完成。然后你可以创建并使用脚本构建 AssetBundle。关于组织 AssetBundle 的最佳方法，请参阅[为 AssetBundle 准备资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html)。

> **注意**：本工作流介绍的是使用内置的 `BuildPipeline.BuildAssetBundles` API 创建 AssetBundle。更友好的替代方案是使用 [Addressables](http://docs.unity3d.com/Packages/com.unity.addressables@latest) 包。

## AssetBundle 构建脚本

要构建 AssetBundle，你必须创建一个构建脚本，并将其放在 Assets 文件夹中名为 `Editor` 的文件夹里。

以下脚本是 AssetBundle 构建脚本的示例。它在 Assets 菜单底部添加了一个名为 **Build AssetBundles** 的菜单项。当你选择 **Build AssetBundles** 时，会调用 `BuildAllAssetBundles` 方法。构建过程中会显示进度条，构建会获取所有标记了 AssetBundle 名称的资源，并用它们在 `assetBundleDirectory` 定义的路径填充 AssetBundle。

```csharp
using UnityEditor;
using System.IO;

public class CreateAssetBundles
{
    [MenuItem("Assets/Build AssetBundles")]
    static void BuildAllAssetBundles()
    {
        // Ensure the AssetBundles directory exists, and if it doesn't, create it.
        string assetBundleDirectory = "Assets/AssetBundles";
        if (!Directory.Exists(assetBundleDirectory))
            Directory.CreateDirectory(assetBundleDirectory);

        // Build all AssetBundles and place them in the specified directory.
        BuildPipeline.BuildAssetBundles(assetBundleDirectory,
                                        BuildAssetBundleOptions.None,
                                        BuildTarget.StandaloneWindows);
    }
}
```

该脚本有以下参数：

- **assetBundleDirectory**：在当前 Unity 项目内输出 AssetBundle 的目录。该文件夹不必位于 Assets 文件夹中。在代码示例中，如果文件夹不存在，会在需要时按需创建。
- **BuildAssetBundleOptions.None**：构建选项参数的默认值。你可以使用该参数指定一个或多个标志以启用各种可选行为。例如，该参数控制压缩算法的选择。有关可用选项的完整列表，请参阅 `BuildAssetBundleOptions` API 文档。
- **BuildTarget.StandaloneWindows**：定义 AssetBundle 的目标平台。另外，你可以调用 `EditorUserBuildSettings.activeBuildTarget`，它返回 Build Profiles 窗口中当前设置为活动的平台配置文件。

## 构建 AssetBundle 子集

当你不为 `BuildPipeline.BuildAssetBundles` 方法指定特定的 AssetBundle 名称时，它会构建项目中定义的所有 AssetBundle。如果你只想构建 AssetBundle 子集，可以向 `AssetDatabase` 查询已定义的 AssetBundle，然后将过滤后的列表传递给构建管线。

以下脚本演示了如何检索所有 AssetBundle 名称及其分配的资源，以便在构建前过滤或修改列表：

```csharp
using UnityEditor;
using System.IO;
using UnityEngine;
using System.Collections.Generic;

public class BuildSubsetAssetBundles
{
    [MenuItem("Assets/Build Selected AssetBundles")]
    static void BuildSpecificAssetBundles()
    {
        string assetBundleDirectory = "Assets/AssetBundles";
        if (!Directory.Exists(assetBundleDirectory))
        {
            Directory.CreateDirectory(assetBundleDirectory);
        }

        List<AssetBundleBuild> builds = new List<AssetBundleBuild>();
        string[] allAssetBundleNames = AssetDatabase.GetAllAssetBundleNames();

        // Example: Only build AssetBundles that start with "environment"
        foreach (string bundleName in allAssetBundleNames)
        {
            if (bundleName.StartsWith("environment"))
            {
                AssetBundleBuild build = new AssetBundleBuild
                {
                    assetBundleName = bundleName,
                    assetNames = AssetDatabase.GetAssetPathsFromAssetBundle(bundleName)
                };
                builds.Add(build);
            }
        }

        if (builds.Count > 0)
        {
            BuildPipeline.BuildAssetBundles(assetBundleDirectory,
                                            builds.ToArray(),
                                            BuildAssetBundleOptions.None,
                                            BuildTarget.StandaloneWindows);
            Debug.Log($"Built {builds.Count} specific AssetBundles.");
        }
        else
        {
            Debug.Log("No AssetBundles matching criteria found to build.");
        }
    }

    [MenuItem("Assets/Log All AssetBundle Assignments")]
    static void LogAllAssetBundleAssignments()
    {
        string[] allAssetBundleNames = AssetDatabase.GetAllAssetBundleNames();
        Debug.Log($"Total AssetBundles Defined: {allAssetBundleNames.Length}");
        foreach (string bundleName in allAssetBundleNames)
        {
            string[] assetPaths = AssetDatabase.GetAssetPathsFromAssetBundle(bundleName);
            Debug.Log($"AssetBundle: {bundleName} (Assets: {assetPaths.Length})");
            foreach (string path in assetPaths)
            {
                Debug.Log($"  - {path}");
            }
        }
    }
}
```

这种方法让你的脚本能够尊重现有的 Inspector 分配，同时让你对构建哪些 AssetBundle 拥有精细的控制。

## 将 AssetBundle 包含在 Player 构建中

本示例演示了一个高级 AssetBundle 构建脚本，它构建 AssetBundle 并将其包含在 Player 构建中。它引入了几个概念：

- **使用活动构建配置文件**：脚本根据活动构建配置文件设置场景列表、标志和设置。使用此脚本之前，请在 Build Profiles 窗口中创建构建配置文件来配置构建。
- **动态输出路径**：脚本根据配置文件名称和时间戳为输出路径命名，类似于基础构建服务器的做法。
- **AssetBundle 构建**：脚本先执行 AssetBundle 构建，再执行 Player 构建。
- **类型保留**：脚本将 AssetBundle 构建的类型信息作为 Player 构建的输入，这样托管代码剥离（managed code stripping）不会移除 AssetBundle 中使用的类型。
- **构建回调**：脚本使用 `BuildPlayerProcessor` 构建回调将 AssetBundle 注入 Player 构建的 StreamingAssets 文件夹。

```csharp
using UnityEngine;
using System.IO;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEditor.Build.Profile;

// Example BuildScript that supports building the current build profile.
//
//
// It builds AssetBundles and includes them in the player build.
// Each time it runs it builds into a new directory derived from the
// current build profile and timestamp.
public class BuildScript
{
    public const string kBuildRootPath = "Build"; // All builds are inside this top level project folder
    public const string kAssetBundleDirectory = "AssetBundles";
    public const string kPlayerDirectory = "Player";
    public const string kAppName = "MyGame";
    public const string kTextureSourceDirectory = "Assets/Textures";
    public const string kTextureSearchPattern = "*.png";

    // Global variable so that RegisterContentForPlayer can find the correct AssetBundles to include in the player build
    public static string gCurrentBuildRootPath = null;

    [MenuItem("Build/Build Active Profile")]
    public static void BuildPlayerAndBundles()
    {
        var profile = BuildProfile.GetActiveBuildProfile();
        if (profile == null)
            throw new BuildFailedException("No active build profile is set." +
                "Use the Build Profiles window or the `-activeBuildProfile` cli argument");

        // Use a timestamp so that each build goes to a unique output folder
        var timeStamp = System.DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss");
        gCurrentBuildRootPath = $"{kBuildRootPath}/{profile.name}/{timeStamp}";

        // Build AssetBundles so that they can be shipped inside the player
        var assetBundleBuildPath = BuildAssetBundles(gCurrentBuildRootPath);

        // To preserve types used by the AssetBundles
        var assetBundleManifestPath = assetBundleBuildPath + "/AssetBundles.manifest";

        // Build the player
        var playerBuildOptions = new BuildPlayerWithProfileOptions()
        {
            buildProfile = profile,
            locationPathName = CreatePlayerOutputPath(gCurrentBuildRootPath),
            assetBundleManifestPath = assetBundleManifestPath,

            // These options can be adjusted as needed.
            // Note: the development and compression flags come from the build profile
            options = BuildOptions.CleanBuildCache | BuildOptions.StrictMode
        };

        // Convenient for manual testing
        if (!Application.isBatchMode)
            playerBuildOptions.options |= BuildOptions.AutoRunPlayer;

        var report = BuildPipeline.BuildPlayer(playerBuildOptions);

        gCurrentBuildRootPath = null;

        if (report.summary.result != BuildResult.Succeeded)
            throw new BuildFailedException("Player build failed, see Editor log for details");

        Debug.Log($"Completed build to {playerBuildOptions.locationPathName}");
    }

    private static string BuildAssetBundles(string buildRootDirectory)
    {
        var assetBundlePath = buildRootDirectory + "/" + kAssetBundleDirectory;

        if (!Directory.Exists(assetBundlePath))
            Directory.CreateDirectory(assetBundlePath);

        // For simplicity in this example, define a single AssetBundle,
        // containing all the textures found inside a hard-coded directory in the project
        string[] texturePaths = Directory.GetFiles(kTextureSourceDirectory, kTextureSearchPattern, SearchOption.AllDirectories);

        var assetBundleContents = new AssetBundleBuild()
        {
            assetBundleName = "textures.bundle",
            assetNames = texturePaths
        };

        // The target platform will be automatically set based on the active build profile
        var assetBundleBuildOptions = new BuildAssetBundlesParameters()
        {
            outputPath = assetBundlePath,
            bundleDefinitions = new AssetBundleBuild[] { assetBundleContents }
        };

        AssetBundleManifest manifest = BuildPipeline.BuildAssetBundles(assetBundleBuildOptions);

        if (manifest == null)
            throw new BuildFailedException("AssetBundle build failed, see Editor log for details");

        return assetBundlePath;
    }

    private static string CreatePlayerOutputPath(string buildRootDirectory)
    {
        var playerOutputFolder = $"{buildRootDirectory}/{kPlayerDirectory}";

        if (!Directory.Exists(playerOutputFolder))
            Directory.CreateDirectory(playerOutputFolder);

        var playerPath = $"{playerOutputFolder}/{kAppName}";

        // This property will match the target in the active build profile
        var target = EditorUserBuildSettings.activeBuildTarget;

        // See "Build path requirements for target platforms" in the Unity Manual
        if ((target == BuildTarget.StandaloneWindows64) ||
            (target == BuildTarget.StandaloneWindows))
            playerPath += ".exe";
        else if (target == BuildTarget.StandaloneOSX)
            playerPath += ".app";
        else if (target == BuildTarget.StandaloneLinux64)
            playerPath += ".x86_64";
        else if (target == BuildTarget.Android)
            playerPath += ".aab";

        return playerPath;
    }
}

// Put the AssetBundle build directory into the StreamingAssets folder of the player output.
// This approach keeps built content separate from the source project, avoiding clutter in "Assets/StreamingAssets".
public class RegisterContentForPlayer : BuildPlayerProcessor
{
    public override void PrepareForBuild(BuildPlayerContext buildPlayerContext)
    {
        var currentBuildPath = BuildScript.gCurrentBuildRootPath;

        if (string.IsNullOrEmpty(currentBuildPath))
            // Do not do anything if we are not in a build initiated by BuildScript
            return;

        buildPlayerContext.AddAdditionalPathToStreamingAssets(currentBuildPath + "/" + BuildScript.kAssetBundleDirectory);
    }

    public override int callbackOrder => 1;
}
```

要在 Unity 编辑器中使用此脚本：

1. 在 Build Profiles 窗口中选择构建配置文件。
2. 从菜单中选择 **Build > Build Active Profile**。

你也可以从命令行调用此脚本。在 Windows 上，命令如下：

```
.\Unity.exe -batchmode -projectPath "C:\UnityProjects\CLIBuildExample" -activeBuildProfile "Assets\Settings\Build Profiles\MyWindowsProfile.asset" -executeMethod BuildScript.BuildPlayerAndBundles -logFile C:\logs\buildlog.txt -quit
```

macOS 上的等效命令如下：

```
Unity -batchmode -projectPath "~/UnityProjects/CLIBuildExample" -activeBuildProfile "Assets/Settings/Build Profiles/MyWeb - Desktop - Development.asset" -executeMethod BuildScript.BuildPlayerAndBundles -logFile "~/logs/buildlog.txt" -quit
```

> **注意**：请调整这些命令行中的路径，以匹配你的设备配置和 Unity 项目的路径。有关命令行参数的更多信息，请参阅「从命令行构建 Player」。

## 执行干净构建

创建正式（official）AssetBundle 版本时，请执行干净构建，以确保 Unity 在构建过程中重建所有内容。要执行干净构建，请将 `BuildAssetBundleOptions.ForceRebuildAssetBundle` 标志作为选项传递给 `BuildPipeline.BuildAssetBundles`。

在某些项目中，你可以删除 `Library/ShaderCache` 目录以强制完全重新编译着色器，或回收过时着色器数据占用的磁盘空间。但是，删除 ShaderCache 文件夹会增加 Unity 创建另一次构建所需的时间。

有关干净构建的更多信息，请参阅「创建干净构建」。

## 更改目标平台

`BuildPipeline.BuildAssetBundles` API 允许你指定部署 AssetBundle 的目标平台和子目标平台。

如果指定的目标平台与 Build Profiles 中配置的平台不同，Unity 必须重新编译编辑器脚本，并重新导入具有平台特定表示的资源（例如纹理）。构建完成后，Unity 会恢复原始的目标平台设置。

这个过程会显著增加构建时间。此外，包含 `BuildPipeline.BuildAssetBundles` 调用的脚本会继续以当前目标平台编译后的形式执行，而不是以指定的构建目标平台执行。如果构建脚本或回调脚本依赖平台特定代码或程序集，这可能会导致问题。

为避免此问题，请确保构建期间执行的任何代码都动态检查目标平台（例如使用 `if` 语句），而不是依赖平台特定的条件编译（例如 `#ifdef` 语句）。最佳实践是始终先将目标设置为所需平台，然后启动构建 AssetBundle 的脚本，以避免来自你无法控制的代码（例如包内的构建回调）造成任何问题。

对于命令行构建，请使用 `--buildTarget` 或 `-activeBuildProfile` 命令行参数，使目标平台与你的构建需求保持一致。更多信息，请参阅「从命令行创建构建」。

## 增量重建资源

每个 AssetBundle 都有一个哈希，Unity 用它来确定是否需要重建。Unity 按以下方式决定如何增量重建 AssetBundle：

- 如果存在该 AssetBundle 上次构建生成的 `.manifest` 文件，Unity 会比较两次构建的 `IncrementalBuildHash` 哈希。
- 如果 AssetBundle 哈希匹配，则 Unity 计算并比较它们的类型树哈希（type tree hashes）。Unity 使用 `TypeTreeHash` 作为次要哈希，检测 AssetBundle 中使用的任何对象是否具有更新的序列化格式。你可以通过指定 `BuildAssetBundleOptions.IgnoreTypeTreeChanges` 标志来忽略此检查。
- 如果 AssetBundle 哈希和类型树哈希都不匹配，Unity 将重建该 AssetBundle，除非你指定了 `BuildAssetBundleOptions.ForceRebuildAssetBundle`——该标志会每次强制重建 AssetBundle。
- Unity 会将新计算的哈希值序列化到新 AssetBundle 的 `.manifest` 文件中。

AssetBundle 的 `IncrementalBuildHash` 会考虑目标平台、包含的资源、依赖、构建选项，以及网格剥离（mesh stripping）和光照配置等平台特定设置。但是，此哈希不会考虑每一种可能影响构建的因素，如果增量构建系统未能检测到所有更改，可能会导致崩溃或意外失败。请在内部开发时使用增量构建，但在创建发布构建时执行干净构建。

> **警告**：`TypeTreeHash` 与 AssetBundle 的主输入哈希（`IncrementalBuildHash`）不同。`TypeTreeHash` 的变化可以在 AssetBundle 输入哈希值不变的情况下强制进行增量构建，因此 AssetBundle 输入哈希并不是跟踪文件版本的理想值。更可靠的做法是使用基于内容计算的哈希或其他版本编号方案。更多信息，请参阅[缓存版本哈希](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-caching.html#cache-version-hash)。

## 其他资源

- [从 AssetBundle 加载资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Native.html)
- [AssetBundle 压缩格式](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-compression-format.html)
- [为 AssetBundle 准备资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html)
