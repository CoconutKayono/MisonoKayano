# 处理 AssetBundle 之间的依赖（Handling dependencies between AssetBundles）

> 来源：[Unity 6000.7 官方手册 · Handling dependencies between AssetBundles](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Dependencies.html)

当 AssetBundle 中的对象引用另一个 AssetBundle 中的对象时，该 AssetBundle 就依赖于其他 AssetBundle。如果被引用的对象没有分配到任何 AssetBundle，Unity 会在构建时将其嵌入依赖它的 AssetBundle 中。如果多个 AssetBundle 引用同一个未分配的对象，每个 AssetBundle 都会包含自己的副本，从而增加内存占用。

要加载有依赖的 AssetBundle，请确保在访问依赖它的 AssetBundle 之前，依赖已被加载到内存中。例如，如果 Bundle 1 包含一个引用 Bundle 2 中纹理的材质，请先将 Bundle 2 加载到内存中，再访问 Bundle 1 中的材质。Unity 不会自动解析依赖。要在运行时管理依赖，你可以使用 `AssetBundleManifest`。更多信息，请参阅[从 AssetBundle 加载资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Native.html)。

## Unity 如何跟踪引用

Unity 通过以下方式跟踪 AssetBundle 之间的引用：

- **清单级依赖**：AssetBundle 之间的依赖位于构建文件夹的根 `.manifest` 文件中，可通过 [AssetBundleManifest.GetAllDependencies](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.GetAllDependencies.html) 访问。
- **底层 SerializedFile 引用**：AssetBundle 之间的直接对象引用会作为外部引用出现在 SerializedFile 文本转储中。这些底层引用不记录 AssetBundle 的名称，只记录 AssetBundle 内部序列化文件的名称。它们只在对应的 AssetBundle 已经加载时才能工作。例如：
  - bundle0 中的 Material 引用 bundle1 中的 Shader。
  - bundle0 内部的 SerializedFile 在其头部有一个外部引用表。该表有一个条目指向 bundle1 的 SerializedFile 路径。
  - Material 对象的 `m_Shader.m_FileID` 记录外部引用表中与 bundle1 内部 SerializedFile 对应的索引。
- **AssetBundle 对象**：AssetBundle 对象在其 `m_Container` 和 `m_PreloadTable` 中整合依赖信息。当请求加载某个资源时，`m_PreloadTable` 确保所有必要的对象（包括来自其他 AssetBundle 的对象）都被识别出来用于加载。对于包含大量资源和依赖的 AssetBundle，这可能涉及非常庞大的数据结构。

## AssetBundle 中的脚本类型表示

Unity 中的 `MonoScript` 对象代表一个特定的 MonoBehaviour 派生类，这也涵盖从 ScriptableObject 派生的类。`MonoScript` 对象以字符串记录程序集、命名空间和类，这些字符串唯一标识类型。

当 Unity 序列化 MonoBehaviour 对象时，它会记录 MonoScript 类的 GUID 和 LFID，然后直接记录类的名称。

构建 AssetBundle 时，Unity 会为构建中包含的每个 MonoBehaviour 派生类包含 `MonoScript` 对象。这些 `MonoScript` 对象可能与 MonoBehaviour 位于同一 SerializedFile 中（本地引用），也可能位于外部序列化文件中。无论哪种情况，MonoScript 都使用与对象之间的其他[直接引用](https://docs.unity3d.com/6000.7/Documentation/Manual/assets-direct-reference.html)完全相同的机制来引用。

以下操作可能导致 `MonoScript` 数据发生变化：

- 将脚本文件移动到另一个[程序集定义文件](https://docs.unity3d.com/6000.7/Documentation/Manual/ScriptCompilationAssemblyDefinitionFiles)下的位置。
- 更改包含该类的程序集定义文件的名称。
- 添加或更改类命名空间。
- 更改类名。

发生这些更改后，请重建项目中的 AssetBundle。

## 避免跨 AssetBundle 的重复信息

默认情况下，Unity 不会优化跨 AssetBundle 的重复数据。例如，如果两个 AssetBundle 各包含一个引用相同未分配材质的预制件，Unity 会将材质副本嵌入两个 AssetBundle。这会增加安装体积和运行时内存占用，并影响合批（batching），因为 Unity 将每份副本视为独立对象。

将共享资源分配到同一个 AssetBundle 可以避免重复。构建期间，Unity 会自动将依赖包含到已分配的 AssetBundle 中，这能显著减小其他 AssetBundle 的体积。例如：

- 将共享材质及其依赖提取到 `modulesmaterials` AssetBundle 中。
- 预制件 AssetBundle 随后只需引用 `modulesmaterials` AssetBundle，从而减小其体积。

更多信息，请参阅[避免资源重复](https://docs.unity3d.com/6000.7/Documentation/Manual/assets-avoid-duplication.html)。

## 运行时加载

当共享资源使用同一个 AssetBundle 时，请先将其加载到内存中，再加载依赖它的 AssetBundle。在下面的示例中，共享材质被正确加载，因为它的 AssetBundle（`materialsAB`）先被加载：

```csharp
using System.IO;
using UnityEngine;

public class InstantiateAssetBundles : MonoBehaviour
{
    void Start()
    {
        // Load the AssetBundles
        AssetBundle materialsAB = AssetBundle.LoadFromFile(Path.Combine(Application.dataPath, Path.Combine("AssetBundles", "modulesmaterials")));
        AssetBundle moduleAB = AssetBundle.LoadFromFile(Path.Combine(Application.dataPath, Path.Combine("AssetBundles", "example-prefab")));

        // Check for errors
        if (materialsAB == null || moduleAB == null)
        {
            Debug.Log("Failed to load AssetBundle!");
            return;
        }
        
        GameObject prefab = moduleAB.LoadAsset<GameObject>("example-prefab");
        // Instantiate the prefab
        Instantiate(prefab);
    }
}
```

## AssetBundle 卸载

卸载 AssetBundle 时，请妥善管理依赖，以防止崩溃或未定义的行为。依赖的 AssetBundle 在其依赖被卸载后，不能继续保持在加载状态。单独重新加载依赖也可能导致问题。加载 AssetBundle 时，它会建立指向依赖 AssetBundle 内对象的数据结构。如果被引用的 AssetBundle 被卸载后重新加载，其对象会被分配新的 InstanceID，并且不会重新连接到依赖它的 AssetBundle，这可能导致崩溃或序列化错误。

为避免这种情况，请跟踪依赖，并且永远不要在另一个 AssetBundle 仍在引用它时卸载该 AssetBundle，除非你也卸载引用它的那个 AssetBundle。实现引用计数系统是管理 AssetBundle 卸载的安全方式。

## 示例卸载策略：引用计数

实现引用计数系统，仅在 AssetBundle 不再被使用时安全地卸载它。

下面的示例跟踪依赖并安全地卸载未使用的 AssetBundle：

```csharp
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class AssetBundleManager
{
    // Path to the directory containing AssetBundles
    private string assetBundlesDirectory;
    // The AssetBundleManifest containing dependency information
    private AssetBundleManifest assetBundleManifest;
    // Reference counts for loaded AssetBundles
    private Dictionary<string, int> assetBundleReferenceCounts = new Dictionary<string, int>();
    // Loaded AssetBundles cache
    private Dictionary<string, AssetBundle> loadedAssetBundles = new Dictionary<string, AssetBundle>();

    // Initializes the AssetBundleManager with the manifest and directory path
    public void Initialize(string manifestBundlePath, string assetBundlesDirectory)
    {
        this.assetBundlesDirectory = assetBundlesDirectory;
        AssetBundle manifestBundle = AssetBundle.LoadFromFile(manifestBundlePath);
        assetBundleManifest = manifestBundle.LoadAsset<AssetBundleManifest>("AssetBundleManifest");
        manifestBundle.Unload(false);
    }

    // Loads an AssetBundle and its dependencies, incrementing reference counts
    public AssetBundle LoadBundle(string bundlePath)
    {
        AssetBundle bundle = LoadAssetBundleIfNotLoaded(bundlePath);
        IncrementReferenceCount(bundle.name);

        string[] dependencyBundleNames = assetBundleManifest.GetAllDependencies(bundle.name);
        foreach (string dependency in dependencyBundleNames)
        {
            string dependencyBundlePath = GetAssetBundlePathFromName(dependency);
            LoadAssetBundleIfNotLoaded(dependencyBundlePath);
            IncrementReferenceCount(dependency);
        }

        return bundle;
    }

    // Loads an AssetBundle if it is not already loaded
    private AssetBundle LoadAssetBundleIfNotLoaded(string bundlePath)
    {
        if (!loadedAssetBundles.TryGetValue(bundlePath, out AssetBundle bundle))
        {
            // For simplicity, this example only shows the case of synchronous loading, but support for
            // LoadFromFileAsync() and the other load methods could also be added with similar code.
            bundle = AssetBundle.LoadFromFile(bundlePath);
            
            if (bundle == null)
            {
                throw new System.Exception($"Failed to load AssetBundle at path {bundlePath}");
            }
            loadedAssetBundles.Add(bundlePath, bundle);
        }

        return bundle;
    }

    // Unloads an AssetBundle and its dependencies if their reference counts reach zero
    public void UnloadBundle(AssetBundle bundle)
    {
        string[] dependencyBundleNames = assetBundleManifest.GetAllDependencies(bundle.name);

        DecrementReferenceCount(bundle.name);
        foreach (string dependency in dependencyBundleNames)
        {
            DecrementReferenceCount(dependency);
        }

        List<string> bundlesToUnload = new List<string>();
        foreach (KeyValuePair<string, AssetBundle> loadedBundleEntry in loadedAssetBundles)
        {
            if (assetBundleReferenceCounts[loadedBundleEntry.Value.name] <= 0)
            {
                bundlesToUnload.Add(loadedBundleEntry.Key);
            }
        }

        foreach (string bundlePath in bundlesToUnload)
        {
            loadedAssetBundles[bundlePath].Unload(true);
            loadedAssetBundles.Remove(bundlePath);
        }
    }

    // Gets the full path of an AssetBundle given its name
    private string GetAssetBundlePathFromName(string name)
    {
        return Path.Combine(assetBundlesDirectory, name);
    }

    // Increments the reference count for a given AssetBundle
    private void IncrementReferenceCount(string bundleName)
    {
        if (assetBundleReferenceCounts.ContainsKey(bundleName))
        {
            assetBundleReferenceCounts[bundleName]++;
        }
        else
        {
            assetBundleReferenceCounts[bundleName] = 1;
        }
    }

    // Decrements the reference count for a given AssetBundle
    private void DecrementReferenceCount(string bundleName)
    {
        if (assetBundleReferenceCounts.ContainsKey(bundleName))
        {
            assetBundleReferenceCounts[bundleName]--;
        }
        else 
        {
            string errorMessage = $"Attempted to decrement reference count for non-existent bundle: {bundleName}";
            throw new KeyNotFoundException(errorMessage);
        }
    }
}
```

> **注意**：对于 [LZ4 压缩和未压缩](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-compression-format.html) 的 AssetBundle，[AssetBundle.LoadFromFile](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.LoadFromFile.html) 只将内容目录加载到内存中，而不加载内容本身。要检查是否发生这种情况，可以使用 [Memory Profiler](https://docs.unity3d.com/Packages/com.unity.memoryprofiler@latest) 包检查内存占用。

## 其他资源

- [AssetBundleManifest](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.html)
- [从 AssetBundle 加载资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Native.html)
