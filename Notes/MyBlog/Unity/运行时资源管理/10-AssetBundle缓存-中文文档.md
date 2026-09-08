# AssetBundle 缓存（AssetBundle caching）

> 来源：[Unity 6000.7 官方手册 · AssetBundle caching](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-caching.html)

Unity 内置的基于磁盘的缓存系统会存储通过 `UnityWebRequestAssetBundle` 下载的 AssetBundle，从而避免冗余下载。

Unity 会将缓存中的 AssetBundle 转换为 LZ4 以获得最佳性能。如果 `Caching.compressionEnabled` 为 false，AssetBundle 会以未压缩形式存储。使用 [Caching](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Caching.html) 类管理缓存的 AssetBundle，例如清除缓存或检查缓存是否存在。

如果你使用 Web 平台，请参阅 Web 缓存以了解如何处理缓存。

如果你使用 `UnityWebRequestAssetBundle.GetAssetBundle`，只有接受 `Hash128` 或 `uint` 版本参数的重载会使用内置缓存。

当不缓存下载时，Unity 会将 AssetBundle 下载到内存文件中，然后加载它。如果下载的文件是 LZMA 格式，Unity 会将其重新压缩为 LZ4 格式的内存文件，并加载该文件。

## AssetBundle 缓存的位置

本地 AssetBundle 缓存位于根文件夹（例如 `Application.temporaryCachePath`）下，结构如下：

```
RootCacheFolder
- BundleName1 
  - Hash1__data (AssetBundle content)
  - Hash1__info (cache metadata)
- BundleName2
  - Hash2__data
  - Hash2__info
```

下载期间，Unity 会使用临时目录存放传入数据，然后在此结构中建立重新压缩后的 AssetBundle。

默认情况下，下载 URL 的最后一部分用作缓存中的 AssetBundle 名称。要更改名称，你可以在 `CachedAssetBundle.name` 结构中指定，该结构可以传递给某些 `UnityWebRequestAssetBundle.GetAssetBundle` 重载。请注意，缓存基于 AssetBundle 名称，而不是完整 URL。

## 缓存版本哈希

AssetBundle 缓存使用哈希值作为 AssetBundle 的版本。你可以提供 128 位哈希（`Hash128`）或 32 位 `uint` 值来区分版本。这可以是构建生成的哈希、数字版本或自定义值。发布新的 AssetBundle 构建时，务必更新此版本，以便设备下载正确的新版本，而不是使用过时的缓存版本。

> **重要提示**：Unity 在下载和加载期间不会自动对 AssetBundle 执行哈希计算，来验证内容是否与提供的版本哈希一致。版本哈希只是一个标识符。内容验证可以使用循环冗余校验（CRC）。

你也可以使用 `BuildAssetBundleOptions.ForceRebuildAssetBundle` 执行完全重建，并使用 `BuildAssetBundleOptions.AssetBundleStripUnityVersion` 防止哈希在 Unity 版本之间发生变化。

## 清除缓存

Unity 会在桌面系统上自动清除缓存。它在启动时检查缓存，并清除在过去 150 天内未在 `Cache.expirationDelay` 中被访问的 AssetBundle。

移动设备的平台提供商会维护各自的缓存。要在移动平台上显式清除缓存，请使用 `Cache.ClearCache`。

## 其他资源

- [从 AssetBundle 加载资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Native.html)
- [验证已下载的 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Integrity.html)
- [UnityWebRequestAssetBundle API 文档](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestAssetBundle.html)
