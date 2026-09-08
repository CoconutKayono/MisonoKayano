# AssetBundle 类

继承关系：`object` → `Object` → `AssetBundle`

命名空间：`UnityEngine`

程序集：`Unity.AssetBundleModule.dll`

## 描述

用于访问 AssetBundle 文件内容的 API。

静态方法提供了一组 API，用于加载和管理 AssetBundle。

这个类还提供了一组实例方法（非静态方法）和属性，用来操作某个**已经加载好的 AssetBundle**——比如查看它包含哪些资源，或者把其中的某个资源（Asset）加载出来。

调用 `BuildPipeline.BuildAssetBundles` 或使用 Addressables 包即可创建 AssetBundle。构建过程会生成一个或多个 AssetBundle 文件，每个文件都包含一个本类的序列化实例。

## AssetBundle 中的场景（Scenes inside AssetBundles）

- 一个 AssetBundle 只能包含场景或资源，**不能两者混装**。
- `AssetBundle.LoadAsset` 和其他 Load 方法**不支持**从 AssetBundle 加载场景。
- 可以使用 `SceneManager` 从 AssetBundle 加载场景。在 Player 中运行或在编辑器的 Play 模式下，先加载包含场景的 AssetBundle，然后使用场景路径或名称调用 `SceneManager.LoadScene` 或 `SceneManager.LoadSceneAsync`。
- 编辑器处于 Edit 模式时，不支持从 AssetBundle 加载场景。使用 `EditorSceneManager.OpenScene` 打开已加载 AssetBundle 内的场景会失败，并记录一条"场景文件未找到"的错误。

其他资源：[Intro to AssetBundles（AssetBundle 简介）](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundlesIntro.html)、[UnityWebRequestAssetBundle.GetAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestAssetBundle.GetAssetBundle.html)、[BuildPipeline.BuildAssetBundles](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildPipeline.BuildAssetBundles.html)

## 示例

### 示例 1：通过网络加载 AssetBundle 并实例化资源

```csharp
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class SampleBehaviour : MonoBehaviour
{
    IEnumerator Start()
    {
        var uwr = UnityWebRequestAssetBundle.GetAssetBundle("https://myserver/myBundle.unity3d");
        yield return uwr.SendWebRequest();

        // Get an asset from the bundle and instantiate it.
        AssetBundle bundle = DownloadHandlerAssetBundle.GetContent(uwr);
        var loadAsset = bundle.LoadAssetAsync<GameObject>("Assets/Players/MainPlayer.prefab");
        yield return loadAsset;

        Instantiate(loadAsset.asset);

        bundle.Unload(true);
    }
}
```

### 示例 2：把场景打进 AssetBundle，并构建包含该 AssetBundle 的 Player

```csharp
 //This example shows how to build a scene into an AssetBundle, and then build a Player with that AssetBundle included.
 //When the Player starts it loads the scene and then unloads after a few seconds.
 //
 //To try this example:
 // - Save it into a file, for example "Assets/AssetBundleSceneLoader.cs".  The source file name needs to match the name of the MonoBehaviour.
 // - From the Editor Menu select "Example" / "Scene in AssetBundle Example".
 //
 //It is also possible to try it in Play mode in the Editor:
 // - Run the menu at least once to create the scenes and AssetBundle
 // - Open "Assets/Scenes/StartingScene.unity"
 // - Enter Play mode

using System.IO;
using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

#if UNITY_EDITOR
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
#endif

public class Constants
{
    // Scene in the project that is intended for an AssetBundle
    public static readonly string SceneForAssetBundle = "Assets/Scenes/SceneForBundle.unity";

    // Scene for the Player build that contains the "AssetBundleSceneLoader" MonoBehaviour
    public static readonly string StartingSceneForPlayer = "Assets/Scenes/StartingScene.unity";

    // Note: AssetBundles are always created lower case
    public static readonly string AssetBundleFileName = "scenebundle";

    // Path for AssetBundle (relative to the StreamingAsset location)
    public static readonly string AssetBundlePath = "/AssetBundles";

    // Output directory for the player build (Relative to project and not inside Assets)
    public static readonly string PlayerBuildPath = "PlayerBuild";

    // Name of the player executable inside PlayerBuildPath
    public static readonly string PlayerExecutable = "PlayerBuild";
}

#if UNITY_EDITOR
 // Note: Typically this would be in its own source file, in an Editor-only assembly.
public class BuildBundleWithScene
{
    [MenuItem("Example/Scene in AssetBundle Example")]
    public static void BuildAssetBundle()
    {
        // Location inside StreamingAssets so the AssetBundle content is included in the Player
        string AssetBundleBuildPath = Application.streamingAssetsPath + Constants.AssetBundlePath;

        // Create the content expected by this example
        CreateStartingScene();
        CreateSceneForAssetBundle();

        var buildTargetPlatform = EditorUserBuildSettings.activeBuildTarget;

        if (!Directory.Exists(AssetBundleBuildPath))
            Directory.CreateDirectory(AssetBundleBuildPath);

        // Define an AssetBundle containing the Scene
        var bundleContents = new AssetBundleBuild[]
        {
            new AssetBundleBuild()
            {
                assetBundleName = Constants.AssetBundleFileName,
                assetNames = new string[]
                {
                    Constants.SceneForAssetBundle
                }
            }
        };

        var buildAssetBundlesParameters = new BuildAssetBundlesParameters()
        {
            targetPlatform = buildTargetPlatform,
            bundleDefinitions = bundleContents,
            outputPath = AssetBundleBuildPath
        };
        BuildPipeline.BuildAssetBundles(buildAssetBundlesParameters);

        var buildReport = BuildReport.GetLatestReport();
        if (buildReport.summary.result != BuildResult.Succeeded)
        {
            Debug.Log("AssetBundle Build failed.");
            return;
        }

        // Perform a Player build.  It will include the content of the
        // StreamingAssets folder.
        if (!Directory.Exists(Constants.PlayerBuildPath))
            Directory.CreateDirectory(Constants.PlayerBuildPath);

        var buildOutput = Constants.PlayerBuildPath + "/" + Constants.PlayerExecutable;
        if (buildTargetPlatform == BuildTarget.StandaloneWindows64)
            buildOutput += ".exe";

        var buildPlayerParameters = new BuildPlayerOptions()
        {
            scenes = new string[] { Constants.StartingSceneForPlayer },
            target = buildTargetPlatform,
            locationPathName = buildOutput,
            options = BuildOptions.Development | BuildOptions.AutoRunPlayer,
            assetBundleManifestPath = AssetBundleBuildPath + "/AssetBundles.manifest"
        };

        if (buildTargetPlatform == BuildTarget.StandaloneWindows64)
            buildPlayerParameters.locationPathName += ".exe";

        var playerBuildReport = BuildPipeline.BuildPlayer(buildPlayerParameters);
        if (playerBuildReport.summary.result != BuildResult.Succeeded)
        {
            Debug.Log($"Player Build failed. {playerBuildReport.SummarizeErrors()}");
            return;
        }
    }

    static void CreateStartingScene()
    {
        var startingScene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        var go = new GameObject();
        go.AddComponent<AssetBundleSceneLoader>();
        GameObject.CreatePrimitive(PrimitiveType.Sphere);
        EditorSceneManager.SaveScene(startingScene, Constants.StartingSceneForPlayer);
    }

    static void CreateSceneForAssetBundle()
    {
        var scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        GameObject.CreatePrimitive(PrimitiveType.Cube);
        EditorSceneManager.SaveScene(scene, Constants.SceneForAssetBundle);
    }
}
#endif

 // MonoBehaviour that is included in the starting scene.
public class AssetBundleSceneLoader : MonoBehaviour
{
    AssetBundle sceneBundle = null;
    bool sceneLoaded = false;

    // Triggered when the scene containing this MonoBehaviour is loaded
    void Start()
    {
        StartCoroutine(LoadAssetBundleAndScene());
        StartCoroutine(CleanupAfterDelay());
    }

    IEnumerator LoadAssetBundleAndScene()
    {
        // Determine the path to the AssetBundle.
        // Application.streamingAssetsPath is used so that this works in both the Player and Play mode in the Editor.
        string AssetBundleBuildPath = Application.streamingAssetsPath + Constants.AssetBundlePath;
        var bundlePath = AssetBundleBuildPath + "/" + Constants.AssetBundleFileName;

        var op = AssetBundle.LoadFromFileAsync(bundlePath);
        yield return op;

        sceneBundle = op.assetBundle;
        if (sceneBundle == null)
        {
            Debug.LogError("Failed to load AssetBundle: " + Constants.AssetBundleFileName);
        }
        else
        {
            var sceneLoadOp = SceneManager.LoadSceneAsync(Constants.SceneForAssetBundle, LoadSceneMode.Additive);

            if (sceneLoadOp == null)
                Debug.Log($"Failed to load {Constants.SceneForAssetBundle}");
            else
            {
                yield return sceneLoadOp;
                Scene sceneLookup = SceneManager.GetSceneByPath(Constants.SceneForAssetBundle);

                //Will report "Finished loading SceneForBundle (index -1)."
                Debug.Log($"Finished loading {sceneLookup.name} (index {sceneLookup.buildIndex}).");
                sceneLoaded = true;
            }
        }
    }

    IEnumerator CleanupAfterDelay()
    {
        yield return new WaitForSeconds(3.0f);

        if (sceneLoaded)
            yield return SceneManager.UnloadSceneAsync(Constants.SceneForAssetBundle);
        sceneLoaded = false;

        if (sceneBundle != null)
            yield return sceneBundle.UnloadAsync(true);
        sceneBundle = null;

        Debug.Log("Finished unloading Content");
    }
}
```

## 静态属性

| 属性 | 说明 |
| --- | --- |
| `memoryBudgetKB` | 控制共享 AssetBundle 加载缓存的大小。默认值为 1MB。 |

## 属性

| 属性 | 说明 |
| --- | --- |
| `isStreamedSceneAssetBundle` | 如果 AssetBundle 包含 Unity 场景文件，则返回 true。 |

## 公共方法

| 方法 | 说明 |
| --- | --- |
| `Contains` | 检查 AssetBundle 是否包含特定对象。 |
| `GetAllAssetNames` | 返回 AssetBundle 中的所有资源名称。 |
| `GetAllScenePaths` | 返回 AssetBundle 中所有场景的名称。 |
| `LoadAllAssets` | 同步加载 AssetBundle 中包含的所有资源。 |
| `LoadAllAssetsAsync` | 异步加载 AssetBundle 中包含的所有资源。 |
| `LoadAsset` | 从 AssetBundle 同步加载一个资源。 |
| `LoadAssetAsync` | 从 AssetBundle 异步加载一个资源。 |
| `LoadAssetWithSubAssets` | 从 AssetBundle 同步加载资源及其子资源。 |
| `LoadAssetWithSubAssetsAsync` | 从 AssetBundle 异步加载资源及其子资源。 |
| `Unload` | 卸载 AssetBundle，释放其数据。 |
| `UnloadAsync` | 卸载 AssetBundle 中的资源。 |

## 静态方法

| 方法 | 说明 |
| --- | --- |
| `GetAllLoadedAssetBundles` | 枚举当前所有已加载的 AssetBundle。 |
| `LoadFromFile` | 从磁盘上的文件同步加载 AssetBundle。 |
| `LoadFromFileAsync` | 从磁盘上的文件异步加载 AssetBundle。 |
| `LoadFromMemory` | 从内存缓冲区同步加载 AssetBundle。 |
| `LoadFromMemoryAsync` | 从内存缓冲区异步加载 AssetBundle。 |
| `LoadFromStream` | 从托管 Stream 同步加载 AssetBundle。 |
| `LoadFromStreamAsync` | 从托管 Stream 异步加载 AssetBundle。 |
| `RecompressAssetBundleAsync` | 将已下载或已存储的 AssetBundle 从一种 BuildCompression 异步重压缩为另一种。 |
| `UnloadAllAssetBundles` | 卸载当前所有已加载的 AssetBundle。 |

## 继承的成员（来自 Object）

### 属性

| 属性 | 说明 |
| --- | --- |
| `hideFlags` | 控制对象是否被隐藏、随场景保存以及是否可由用户编辑。 |
| `name` | 对象的名称。 |

### 公共方法

| 方法 | 说明 |
| --- | --- |
| `GetEntityId` | 获取对象的 EntityId。 |
| `GetHashCode` | 返回对象的哈希码。 |
| `ToString` | 返回对象的名称。 |

### 静态方法

| 方法 | 说明 |
| --- | --- |
| `Destroy` | 移除一个 GameObject、组件或资源。 |
| `DestroyImmediate` | 立即销毁指定对象。请谨慎使用，且仅在编辑器模式下使用。 |
| `DontDestroyOnLoad` | 加载新场景时不要销毁目标对象。 |
| `FindAnyObjectByType` | 查找当前已加载的任意活动对象（类型 T）。 |
| `FindObjectsByType` | 查找所有已加载的指定类型（Type）对象列表。 |
| `Instantiate` | 克隆对象 original，并返回克隆体。 |
| `InstantiateAsync` | 捕获与另一个 GameObject 相关的原对象（original）快照，并取得所生成对象的 AsyncInstantiateOperation 实例。 |

### 运算符

| 运算符 | 说明 |
| --- | --- |
| `bool` | 判断对象是否存在。 |
| `operator !=` | 判断两个对象引用是否指向不同的对象。 |
| `operator ==` | 判断两个对象引用是否指向同一个对象。 |

---

相关文档：[[00-AssetBundleModule]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
