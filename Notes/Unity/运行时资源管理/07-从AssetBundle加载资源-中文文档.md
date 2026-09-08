# 从 AssetBundle 加载资源（Loading assets from AssetBundles）

> 来源：[Unity 6000.7 官方手册 · Loading assets from AssetBundles](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Native.html)

要从 AssetBundle 加载资源，你必须先加载 AssetBundle 本身，然后从其中加载资源。

## 加载 AssetBundle

你可以使用以下 API 加载 AssetBundle：

- [AssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.html) 类上的静态 Load 方法，例如 [AssetBundle.LoadFromFile](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.LoadFromFile.html)。该类根据 AssetBundle 的位置以及你是同步还是异步加载，提供了一系列加载方法。
- 对 AssetBundle 的 [UnityWebRequest](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request.html) 支持，例如 [UnityWebRequestAssetBundle.GetAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestAssetBundle.GetAssetBundle.html)。

有关这些类可用的全部 AssetBundle 加载方法及使用示例，请参阅这些类的 API 参考。

## 加载资源

AssetBundle 加载完成后，你可以使用 AssetBundle 类从中加载单个资源，如下所示。

使用 `LoadAsset` 同步加载单个资源，例如预制件的根 GameObject：

```csharp
GameObject gameObject = loadedAssetBundle.LoadAsset<GameObject>(assetName);
```

使用 `LoadAllAssets` 加载所有资源：

```csharp
Unity.Object[] objectArray = loadedAssetBundle.LoadAllAssets();
```

这将返回一个包含每个资源所有根 Object 的数组。

前面片段中的方法返回要加载的对象类型或对象数组。这些方法的异步版本会改为返回一个 [AssetBundleRequest](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleRequest.html)。你必须等待此操作完成后再访问资源。

异步加载单个资源：

```csharp
AssetBundleRequest request = loadedAssetBundleObject.LoadAssetAsync<GameObject>(assetName);
yield return request; // or await request;
var loadedAsset = request.asset;
```

异步加载所有资源：

```csharp
AssetBundleRequest request = loadedAssetBundle.LoadAllAssetsAsync();
yield return request; // or await request;
var loadedAssets = request.allAssets;
```

有关更多信息和完整代码示例，请参阅 [AssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.html) API 参考。

## 加载 AssetBundle 清单

你可以将 AssetBundle 清单加载到 [AssetBundleManifest](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.html) 类的实例中，以获取已构建 AssetBundle 的依赖数据、哈希数据和变体数据等信息。

这在管理 AssetBundle 之间的依赖时尤其有用。清单对象使动态查找和加载依赖成为可能，因此你不必在代码中硬编码所有 AssetBundle 名称及其关系。

有关更多信息和代码示例，请参阅[处理 AssetBundle 之间的依赖](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Dependencies.html)。

## 管理已加载的 AssetBundle

[Addressables](http://docs.unity3d.com/Packages/com.unity.addressables@latest) 包简化了管理 AssetBundle、依赖和资源的过程。对于手动管理，理解正确的 AssetBundle 加载和卸载至关重要，以免出现内存重复或对象缺失。

### 推荐的卸载策略

[AssetBundle.Unload](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.Unload.html) 函数会从内存中移除 AssetBundle 头部及相关结构，其布尔参数决定是否同时卸载已加载的对象。

使用 `AssetBundle.Unload(true)` 防止对象重复。例如：

- **定义卸载点**：在特定时间点卸载临时 AssetBundle，例如在关卡切换或加载界面期间。
- **引用计数**：跟踪对象的使用情况，并仅在所有组成对象都不再使用时卸载 AssetBundle。示例实现请参阅[示例卸载策略：引用计数](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Dependencies.html#reference-counting)。

如果必须使用 `Unload(false)`，则只能通过以下方式之一卸载不需要的对象：

- **消除引用**：移除对对象的所有引用，然后调用 [Resources.UnloadUnusedAssets](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Resources.UnloadUnusedAssets.html)。
- **非叠加场景加载**：非叠加地加载新场景以销毁当前场景对象，这会自动调用 `Resources.UnloadUnusedAssets`。

有关 AssetBundle 加载期间内存使用的详细信息，以及整个 AssetBundle 可能被加载到 RAM 中的特定场景，请参阅[优化 AssetBundle 内存使用](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-optimizing.html)。

## 分发 AssetBundle

你可以通过以下方式分发 AssetBundle：

- 将文件放在 [StreamingAssets](https://docs.unity3d.com/6000.7/Documentation/Manual/StreamingAssets.html) 文件夹中，并随 Player 构建一起分发。
- 将文件托管在 Web 服务上，例如 [Unity 的 Cloud Content Delivery](https://docs.unity.com/ugs/manual/ccd/manual/UnityCCD)，并使用 [UnityWebRequestAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/UnityWebRequestAssetBundle.html) 下载它们。
- 编写自定义的下载和安装代码。这种方法需要更多的开发工作，但可以让你在加载文件之前，使用 Unity API 控制压缩、缓存、补丁和[验证](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Integrity.html)等环节。

## 其他资源

- [构建 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Building.html)
- [管理已加载的 AssetBundle（Unity Learn 教程）](https://learn.unity.com/tutorial/assets-resources-and-assetbundles#Managing_Loaded_Assets)
