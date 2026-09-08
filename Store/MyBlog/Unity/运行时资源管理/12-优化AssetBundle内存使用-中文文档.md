# 优化 AssetBundle 内存使用（Optimizing AssetBundle memory usage）

> 来源：[Unity 6000.7 官方手册 · Optimizing AssetBundle memory usage](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-optimizing.html)

加载 AssetBundle 会消耗内存，具体取决于压缩格式和访问模式。

加载 AssetBundle 时，Unity 会为 AssetBundle 包含的资源以及其内部数据分配内存。已加载 AssetBundle 的主要内部数据类型包括：

- **加载缓存（Loading cache）**：存储 AssetBundle 文件最近访问的页面。使用 [AssetBundle.memoryBudgetKB](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle-memoryBudgetKB.html) 控制其大小。
- **[TypeTrees（类型树）](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-optimizing.html#typetrees)**：定义对象的序列化布局。
- **[目录（Table of contents）](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-optimizing.html#table-of-contents)**：列出 AssetBundle 中的资源。
- **[预加载表（Preload table）](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-optimizing.html#preload-table)**：列出每个资源的依赖。

## TypeTrees（类型树）

TypeTree 是 Unity 的内部数据结构，描述序列化二进制对象内的数据结构。从序列化系统的角度来看，它充当 Unity 对象的架构（schema）。

AssetBundle 中的每个序列化文件都包含该文件中每个对象类型的 TypeTree。你可以使用 TypeTree 信息反序列化那些类型定义自序列化以来可能已更改的文件（例如添加、删除或修改字段时）。

当 Unity 加载 AssetBundle 时，它会加载所有 TypeTree，并在 AssetBundle 的生命周期内将其保留在内存中。TypeTree 的内存开销取决于从 AssetBundle 加载的唯一对象类型的数量及其复杂度。每个 AssetBundle 都包含其对象的完整 TypeTree 集合。Unity 会在多个 AssetBundle 之间共享相同的 TypeTree，以减少加载多个 AssetBundle 时的内存占用。

### 减少 TypeTree 内存

你可以通过以下方式减少 AssetBundle TypeTree 的内存需求：

- **禁用 TypeTree**：这会从 AssetBundle 中排除 TypeTree 信息，使 AssetBundle 更小。但是，没有 TypeTree 信息时，如果用较新版本的 Unity 加载旧 AssetBundle，或在项目中更改脚本，可能会出现序列化错误或未定义行为。
- 使用简单的数据类型来降低 TypeTree 复杂度。

要测试 TypeTree 对 AssetBundle 大小的影响，可以分别在不禁用 TypeTree 和禁用 TypeTree 的情况下构建，并比较它们的大小。使用 [BuildAssetBundleOptions.DisableWriteTypeTree](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildAssetBundleOptions.DisableWriteTypeTree.html) 禁用 AssetBundle 中的 TypeTree。

> **注意**：某些平台需要 TypeTree，会忽略 `DisableWriteTypeTree` 设置。此外，并非所有平台都支持 TypeTree。

如果禁用或剥离 TypeTree，请考虑以下事项：

- **兼容性**：只有当你始终将 AssetBundle 与 Player 构建一起重建以确保类型兼容时，剥离 TypeTree 才是安全的。这常见于随 StreamingAssets 文件夹分发的 AssetBundle。
- **编辑器加载**：如果在 Play 模式下尝试加载没有 TypeTree 的 AssetBundle，会记录错误。这是因为编辑器和 Player 的类型不同。例如，MonoBehaviour 在编辑器中会有额外字段。
- **调试**：Unity 提供的用于在没有 TypeTree 的情况下分析兼容性的工具有限。AssetBundle 清单中的 `TypeTreeHash` 可以提供帮助，`binary2text` 工具（带 `-typeinfo` 标志）可以暴露原始 TypeTree 细节用于比较。

## 目录（Table of contents）

目录是 AssetBundle 中的一张映射表，你可以用它按名称查找每个显式包含的资源。目录数据的大小会随着 AssetBundle 中显式包含的资源数量以及用于映射它们的字符串名称长度而增加。[addressableNames](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleBuild-addressableNames.html) 属性表示字符串名称，如果未定义，则使用资源路径代替。

要尽量减少用于保存目录数据的内存，请减少某一时刻加载的 AssetBundle 数量。

[GetAllAssetNames](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.GetAllAssetNames.html) 和 [GetAllScenePaths](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.GetAllScenePaths.html) 方法会暴露目录映射。

## 预加载表（Preload table）

预加载表列出了资源依赖的所有对象。当你从 AssetBundle 加载资源时，Unity 会使用此表自动加载所有必要的依赖。

每个资源都有自己的预加载表。例如，预制件的预加载表包含预制件上所有组件的条目、被引用的材质和纹理，以及预制件使用的任何其他资源。

每个预加载条目使用 64 位内存，可以引用其他 AssetBundle 中的对象。

当资源引用另一个资源，而后者又引用其他资源时，预加载表可能会变得很大，因为资源共享依赖时会包含重复条目。如果两个资源都引用第三个资源，那么两个资源的预加载表都会包含加载第三个资源的条目。

预加载表可能包含资源共享依赖时产生的重复条目。当一个资源引用另一个资源，而后者又引用其他资源时，Unity 会将此信息存储在每个资源的预加载表中。这会影响内存使用。

你可以通过以下方式减轻大型预加载表的影响：

- **仅使用 AssetBundle 的项目**：将任何包含大量对象且被频繁引用的资源显式添加到 AssetBundle 中，以便共享该资源的预加载信息。
- **使用 Addressables 或 Scriptable Build Pipeline 的项目**：避免显式包含的资源直接或间接引用大型对象层级。

## 临时内存 AssetBundle

Unity 能高效管理内存，但在以下场景会创建临时的内存 AssetBundle：

- 通过 `AssetBundle.LoadFromFile`、`LoadFromMemory` 或 `LoadFromStream` API 加载的 LZMA 压缩 AssetBundle。
- 不使用缓存且在没有版本或哈希参数的情况下下载的 AssetBundle。
- 在没有 AssetBundle 缓存的平台（如 Web）上通过 `UnityWebRequestAssetBundle` 下载的 AssetBundle。

临时文件在读取完成并调用 `AssetBundle.Unload` 之前一直存在。这些内存副本会显著增加 RAM 占用和加载时间。

## 缓存注意事项

- **LZ4（默认）**：当 `Caching.compressionEnabled` 为 true（默认）时，下载的 AssetBundle 会被重新压缩为 LZ4 并存储在缓存中。这种转换通常会提高加载性能。
- **未压缩**：当 `Caching.compressionEnabled` 为 false 时，临时 AssetBundle 以未压缩形式存储；如果原始 AssetBundle 是压缩的，可能会增加 RAM 占用。

## CRC 检查与性能

[CRC 检查](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Integrity.html)对 LZ4 文件可能影响加载时间，因为需要解压整个文件。这会占用最少的内存，因为 Unity 会单独解压每个块，而不是一次性解压整个文件。

对 LZMA 文件的 CRC 检查不会带来额外开销，因为完整解压是固有的。更多信息，请参阅[下载 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Integrity.html)。

建议仅在下载时执行一次 CRC 检查，而不是在每次加载 AssetBundle 时都检查，尤其是在 CPU 较弱的平台上。

## 详细内存使用

除了临时内存 AssetBundle，其他结构也会消耗内存：

- **LZ4 和未压缩的 AssetBundle**：当基于 LZ4 的 AssetBundle 打开时，块会按需解压。一个小型缓存（`ArchiveStorageReader.m_CachedBlocks`）有助于管理顺序读取。对于未压缩的 AssetBundle，可能仍会使用此缓存。
- **PersistentManager 的 SerializedFile 缓存**：PersistentManager 使用共享缓存（`PooledFileCacherManager`）存储从 AssetBundle 中 SerializedFile 读取的数据页。其默认大小为 1MB。
- **存档和 AssetBundle 元数据**：已挂载 Unity 存档和 AssetBundle 的附加数据结构会消耗少量内存，例如包含目录的 AssetBundle 对象和 `PreloadData` 对象。
- **PersistentManager.Remapper**：跟踪实例 ID 与源文件之间的关系。对于包含非常大预制件（对象层级）的 AssetBundle，它可能占用可观的内存，因为一旦分配就永远不会缩小。场景中的对象不在此处跟踪。
- **实例化对象**：从 AssetBundle 加载资源和场景后，实例化的 Unity 对象本身会消耗内存。

## Unity 何时将整个 AssetBundle 加载到内存中

以下信息总结了使用可用 API 加载不同格式 AssetBundle 时内存文件和格式转换的使用情况。这会直接影响运行时内存消耗。

### 基于文件的加载 API

**AssetBundle.LoadFromFile、LoadFromFileAsync**

| 压缩格式 | 行为 |
| --- | --- |
| LZMA 压缩 | 转换为 LZ4 并打开内存文件。 |
| LZ4 压缩、未压缩 | 直接从文件读取内容。 |

**AssetBundle.LoadFromMemory、LoadFromMemoryAsync**

| 压缩格式 | 行为 |
| --- | --- |
| LZMA 压缩、未压缩 | 转换为 LZ4 并打开内存文件。 |
| LZ4 压缩 | 直接从内存读取内容。 |

**AssetBundle.LoadFromStream、LoadFromStreamAsync**

| 压缩格式 | 行为 |
| --- | --- |
| LZMA 压缩 | 转换为 LZ4 并打开内存文件。 |
| LZ4 压缩、未压缩 | 直接从文件流读取内容。 |

### 基于 Web 的加载 API

**UnityWebRequestAssetBundle.GetAssetBundle（空缓存，Caching.compressionEnabled = true）**

| 压缩格式 | 行为 |
| --- | --- |
| LZMA 压缩 | 下载并流式写入缓存文件（将 LZMA 转换为 LZ4），然后从缓存加载。 |
| LZ4 压缩 | 下载并流式写入缓存文件（不转换），然后从缓存加载。 |
| 未压缩 | 下载并流式写入缓存文件（转换为 LZ4），然后从缓存加载。 |

**UnityWebRequestAssetBundle.GetAssetBundle（已缓存，Caching.compressionEnabled = true）**

| 压缩格式 | 行为 |
| --- | --- |
| 所有压缩格式 | 直接从缓存的 LZ4 文件读取内容。 |

**UnityWebRequestAssetBundle.GetAssetBundle（无缓存）**

| 压缩格式 | 行为 |
| --- | --- |
| LZMA 压缩 | 下载、转换为 LZ4 并打开内存文件。 |
| LZ4 压缩、未压缩 | 下载并流式写入基于内存的临时文件（不转换）。 |

> **注意**：转换并打开内存文件涉及：打开源文件、检查其格式、将其转换为 LZ4（如果 `Caching.compressionEnabled` 为 false 则转换为未压缩）作为内存存档文件、打开此内存文件，最后在卸载且没有更多读取器时删除它。此过程可能造成内存和加载时间的低效使用。

## 减少包含大量资源的 AssetBundle 的运行时内存使用

加载资源时，Unity 支持按完整项目相对路径、文件名或不带扩展名的文件名加载。后两种选项通过构建额外的字符串表实现。在包含大量可加载资源的 AssetBundle 中，这些额外的字符串表可能占用可观的内存。

为减少这种开销，最佳实践是始终使用资源的精确键（项目相对路径或 Addressables 名称）加载资源，并在构建时禁用额外的匹配功能：

- [BuildAssetBundleOptions.DisableLoadAssetByFileName](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildAssetBundleOptions.DisableLoadAssetByFileName.html)
- [BuildAssetBundleOptions.DisableLoadAssetByFileNameWithExtension](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildAssetBundleOptions.DisableLoadAssetByFileNameWithExtension.html)

有关更多信息，请参阅 [AssetBundle.LoadAssetAsync](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.LoadAssetAsync.html) 中 `name` 参数的文档。

## 其他资源

- [处理 AssetBundle 之间的依赖](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Dependencies.html)
- [从 AssetBundle 加载资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Native.html)
- [分析 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-analyze.html)
