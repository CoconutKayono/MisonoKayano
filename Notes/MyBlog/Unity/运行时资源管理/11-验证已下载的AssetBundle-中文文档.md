# 验证已下载的 AssetBundle（Verifying downloaded AssetBundles）

> 来源：[Unity 6000.7 官方手册 · Verifying downloaded AssetBundles](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Integrity.html)

你可以随应用分发 AssetBundle，也可以设置远程服务器来下载 AssetBundle。

下载 AssetBundle 时，必须采取预防措施，防止数据损坏和恶意攻击。下载的 AssetBundle 中的数据损坏是用户设备上崩溃的常见原因。虽然 AssetBundle 不能包含可执行代码，但被篡改的序列化数据可能会利用应用代码或 Unity 运行时的漏洞。验证层（validation layer）有助于防止随机崩溃或异常行为。

## 使用安全协议下载

使用 [UnityWebRequestAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestAssetBundle.html) 从远程 Web 服务器下载 AssetBundle。除非是同一台机器上的本地 Web 服务器，否则 URL 始终使用 HTTPS。HTTP 不安全，容易受到中间人攻击。

## 循环冗余校验（CRC）

要检查 AssetBundle 是否损坏，你可以使用循环冗余校验（CRC）对照 Unity 在 AssetBundle 构建过程中生成的 32 位校验和。该校验和存储在 `.manifest` 文件中，可通过 [BuildPipeline.GetCRCForAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildPipeline.GetCRCForAssetBundle.html) 获取。通过 `UnityWebRequestAssetBundle.GetAssetBundle` 下载 AssetBundle 时，请提供预期的 CRC 值，防止无效 AssetBundle 被[缓存](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-caching.html)。

如果你在 Unity 缓存之外直接处理 AssetBundle 下载，请在使用检索到的内容之前执行完整性检查。AssetBundle 加载 API 中的可选参数允许你传入 CRC 值进行验证。如果计算出的 CRC 不匹配，AssetBundle 将无法加载。对于 LZ4 压缩的 AssetBundle，此检查消耗大量资源，因为它需要将完整内容解压到 RAM 中。LZMA 压缩的 AssetBundle 在加载时本身就需要完整解压，因此 CRC 检查不会增加显著开销。为避免加载时反复检查，请在 AssetBundle 检索并保存到设备时验证一次。更多信息，请参阅 [AssetBundle 压缩格式](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-compression-format.html)。

验证 AssetBundle 时需要注意以下几点：

- 不要使用 md5 等常见哈希算法来验证使用 [LZMA 压缩](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-compression-format.html#lzma-compression)的 AssetBundle。Unity 可能会在不改变内容的情况下重新压缩 AssetBundle，这会改变文件哈希，尽管内容有效。Unity 根据未压缩内容计算 CRC 值，压缩内容后这些值保持一致。
- `.manifest` 文件中的 `IncrementalBuildHash` 不是完整文件内容的哈希。它用作版本标识符，不适合用于检测文件损坏。
- `.manifest` 文件中的 `AssetFileHash`（可通过 [BuildPipeline.GetHashForAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildPipeline.GetHashForAssetBundle.html) 获取）才是内容真正的哈希。

## 用户生成的内容（UGC）

对于分发给其他玩家的用户生成内容（UGC），请过滤提交内容以防止不当或恶意内容。不要允许用户直接上传二进制 AssetBundle 文件。相反，要求他们上传源资源，并由你自己构建 AssetBundle 文件。此过程可以实现人工和自动过滤，并在需要时允许你为更新的 Unity 版本重建 AssetBundle。

## 修补 AssetBundle

创建新的 AssetBundle 构建时，你可以用新增或更改的 AssetBundle 更新现有安装，并删除任何不再被引用的 AssetBundle。对现有 AssetBundle 的更新称为补丁（patch）。Unity 通过 [AssetBundle 缓存](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-caching.html)支持基本的补丁功能，你可以使用 [UnityWebRequestAssetBundle.GetAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/UnityWebRequestAssetBundle.GetAssetBundle.html) 替换 AssetBundle 的现有版本。但是，Unity 不支持差分补丁（differential patching）——即选择性地更新现有文件的内容以匹配新文件。如果你想创建差分补丁，必须用自己的逻辑扩展或替换 AssetBundle 缓存。

使用带不同版本或哈希参数的 `UnityWebRequestAssetBundle.GetAssetBundle` 会触发下载更新的 AssetBundle。

主要的挑战是确定哪些 AssetBundle 需要替换。补丁系统必须管理两个列表：

- **本地 AssetBundle**：当前已下载的 AssetBundle 及其版本信息。
- **服务器 AssetBundle**：服务器上可用的 AssetBundle 及其版本信息。

补丁系统会比较这些列表，重新下载缺失的或版本信息已更新的 AssetBundle。

Unity 默认不支持差分补丁。即使使用内置缓存系统，`UnityWebRequestAssetBundle.GetAssetBundle` 也会下载整个文件。如果需要差分补丁，请实现自定义下载器。Unity 会确定性地排序 AssetBundle 数据，因此重建后的 AssetBundle 的补丁文件可以小得多。未压缩的 AssetBundle 或使用 LZ4 压缩的 AssetBundle 比 LZMA 压缩的 AssetBundle 更适合补丁。

对于自定义系统，请使用 JSON 格式的 AssetBundle 文件列表，并使用 [.NET 加密 API](https://learn.microsoft.com/en-us/dotnet/standard/security/cryptography-model) 计算文件哈希。这些哈希可以作为版本标识符；如果构建系统支持，你也可以使用传统的版本号。

## 其他资源

- [UnityWebRequestAssetBundle API 文档](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestAssetBundle.html)
- [Caching API 文档](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Caching.html)
- [从 AssetBundle 加载资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Native.html)
