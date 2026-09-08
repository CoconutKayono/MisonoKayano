# AssetBundle 平台注意事项（AssetBundle platform considerations）

> 来源：[Unity 6000.7 官方手册 · AssetBundle platform considerations](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-platforms.html)

AssetBundle 是平台相关的，这意味着在运行时你只能加载为目标平台构建的 AssetBundle。这是因为 AssetBundle 包含平台特定的资源格式，如果在其他平台加载会导致意外行为。此限制可防止将错误内容意外交付到错误的平台。

## Android 平台细节

要分发 Android 平台的 AssetBundle 内容，你有以下选项：

- 将 AssetBundle 构建到 [StreamingAssets](https://docs.unity3d.com/6000.7/Documentation/Manual/StreamingAssets.html) [文件夹](https://docs.unity3d.com/6000.7/Documentation/Manual/StreamingAssets.html)中。
- 将 AssetBundle 打包到自定义资源包（asset packs）中。
- 通过 CDN 部署 AssetBundle。

你选择的选项取决于项目的需求。

### 将 AssetBundle 构建到 StreamingAssets 文件夹

放在 [StreamingAssets](https://docs.unity3d.com/6000.7/Documentation/Manual/StreamingAssets.html) [文件夹](https://docs.unity3d.com/6000.7/Documentation/Manual/StreamingAssets.html)中的 AssetBundle 会自动打包为应用 APK 或 OBB 文件的一部分。

你不能使用标准文件路径 API 直接从 APK 或 OBB 文件加载这些文件。相反，你必须使用带 `file:///` URL 方案的 [UnityWebRequestAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestAssetBundle.html) API 加载它们。例如：

```csharp
var assetBundlePath = "file://" + Application.streamingAssetsPath + "/" + assetbundleToLoad;
var loadOp = UnityWebRequestAssetBundle.GetAssetBundle(assetBundlePath);
yield return loadOp.SendWebRequest();
var assetBundle = DownloadHandlerAssetBundle.GetContent(loadOp);
```

避免对 StreamingAssets 文件夹中的 AssetBundle 使用 LZMA 压缩，因为将 LZMA 文件解压到临时内存文件的效率很低。请使用 LZ4 压缩或保持未压缩。更多信息，请参阅 [AssetBundle 压缩格式](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-compression-format.html)。

### 将 AssetBundle 打包到自定义资源包

你可以将 AssetBundle 放入 Android 的资源包（asset pack）格式，并交付到 Google Play Store。更多信息，请参阅 [Unity 中的资源包](https://docs.unity3d.com/6000.7/Documentation/Manual/android-asset-packs-in-unity.html)。

### 通过 CDN 部署 AssetBundle

你可以将 AssetBundle 托管在 Web 服务器上，并使用 [UnityWebRequestAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestAssetBundle.html) 按需下载。

你可以使用 Unity 的 [Cloud Content Delivery（CCD）](https://docs.unity.com/ugs/manual/ccd/manual/UnityCCD) 服务来简化部署，尤其是与 Addressables 集成时。这种方法适合具有大量动态内容的应用。下载的 AssetBundle 通常保存到应用缓存目录或 `Application.persistentDataPath`。

## 主机平台下载与 CRC

通常，主机的 AssetBundle 不是通过游戏内代码直接从 Web 下载的。相反，它们通常通过平台自身的 DLC（可下载内容）机制交付。这些 DLC 由平台系统安全地购买、下载并存储在本地，独立于游戏的直接控制。安装后，游戏可以检测并加载这些新文件。

在主机平台上加载 AssetBundle 时，不要执行 CRC。主机的 CPU 通常较弱，对新打开的 AssetBundle 校验 CRC 可能需要相当长的时间。即使在存储较快的平台上，CPU 密集型的 CRC 检查也可能显著拖慢加载。

## 其他资源

- [下载 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Integrity.html)
- [AssetBundle 压缩格式](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-compression-format.html)
- [Web 平台上的 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/webgl-assetbundles.html)
