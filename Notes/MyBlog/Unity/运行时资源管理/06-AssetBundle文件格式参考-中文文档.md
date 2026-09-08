# AssetBundle 文件格式参考（AssetBundle file format reference）

> 来源：[Unity 6000.7 官方手册 · AssetBundle file format reference](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-file-format.html)

当你使用 `BuildPipeline.BuildAssetBundles` 构建 AssetBundle 时，Unity 会向指定的输出目录写入以下文件：

- AssetBundle 文件。
- 每个 AssetBundle 文件对应的 `.manifest` 文件。
- 一个清单包（manifest bundle）。

> **注意**：如果你使用 Addressables 包构建 AssetBundle，它只会生成 AssetBundle 文件，不会生成 `.manifest` 文件或清单包。

## Unity 存档文件格式

Unity 存档文件格式（Unity archive file format）是一种通用打包格式，可以存储任何类型的文件，类似于 `.zip` 文件。存档文件会被挂载到 Unity 的虚拟文件系统（VFS）中，从而可以在不同平台上以统一的方式访问。

Unity 将存档格式用于 AssetBundle——存档文件作为 AssetBundle 构建过程的最后阶段创建，并在加载 AssetBundle 时挂载到 Unity 虚拟文件系统中。该存档格式也用于以 LZ4 压缩构建的 Player，这种情况下存档会在 Player 运行时自动挂载。

通常你不需要在底层与存档交互。不过，Unity 提供了 `ArchiveFileInterface` API，需要时可以直接用底层 API 管理存档文件。

## AssetBundle 文件

AssetBundle 文件是一个存档文件，包含多个在运行时加载资源的文件。下图展示了一个 AssetBundle 文件布局示例：

> 典型 AssetBundle 文件的内部结构，以一系列容器表示。

它包含一系列嵌套容器，最外层是与 AssetBundle 同名的存档文件系统（archive file system）实例。

在本示例中，ArchiveFileSystem 存档文件包含两个文件：

- 主 AssetBundle 文件，采用 Unity 的序列化文件格式。该文件包含 AssetBundle 对象，以及 AssetBundle 中所有资源包含的对象。
- 一个或多个存储在带 `.resource` 扩展名的文件中的音频剪辑。

Unity 组织 AssetBundle 内部内容的方式称为构建布局（build layout）。构建布局取决于 AssetBundle 包含的是资源还是场景：

- **资源型 AssetBundle**：在 Unity 存档文件内，将所有资源中的对象包含在一个序列化文件中。它还包含这些资源引用的所有对象，除非另一个 AssetBundle 暴露了被引用的资源。同一个被引用对象可能会在多个 AssetBundle 中重复出现。
- **场景型 AssetBundle**：布局与 Player 构建类似。每个场景都有一个包含该场景对象的序列化文件，文件名类似于 `PlayerBuild-SceneFileName`。这对应 Player 构建中的 `level0` 文件。Unity 将场景文件引用的资源存储在 `sharedasset` 文件中，例如 `PlayerBuild-SceneFileName.sharedasset`，除非另一个 AssetBundle 暴露了被引用的资源。由于 `sharedasset` 的计算只覆盖同一 AssetBundle 中的场景，如果将场景存储在单独的 AssetBundle 中，而不是全部放在单个 AssetBundle 中，Unity 可能会产生大量重复对象。不过，将场景放在单独的 AssetBundle 中也有性能和分发方面的优势。

存档内序列化文件的命名约定如下：

- 资源型 AssetBundle 将序列化文件命名为 `CAB-`，后跟 AssetBundle 名称的 MD4 哈希。例如 `CAB-cc6c60ef8808e0fc6663136604321554`。
- 使用 `BuildPipeline.BuildAssetBundles` 创建的场景型 AssetBundle，使用以 `PlayerBuild-` 开头、后跟场景文件名（不含路径和扩展名）的名称。例如 `Assets/Scene1.unity` 变成 `PlayerBuild-Scene1`。由于此约定，请为每个场景文件指定唯一的文件名以避免冲突。
- Addressables 创建的场景型 AssetBundle，将每个场景的序列化文件命名为 `CAB-`，后跟场景项目相对路径的 MD4 哈希。配套的 `sharedasset` 文件使用相同的文件名，后跟 `.sharedasset` 扩展名。

与 Player 构建一样，AssetBundle 中的每个序列化文件都可以配有一个 `.resS` 文件和一个 `.resource` 文件来存储大型二进制数据。所有音频或视频都存储在 `.resource` 文件中，纹理和网格以 `.resS` 格式存储。这些文件的命名沿用其对应的序列化文件，例如 `CAB-cc6c60ef8808e0fc6663136604321554.resource` 或 `PlayerBuild-Scene1.sharedasset.resS`。

## 检查 AssetBundle 文件内容

Unity 编辑器安装中包含 WebExtract 和 Binary2Text 可执行文件，你可以用它们提取 AssetBundle 内嵌套的文件，并将二进制 SerializedFile 的内容转储为文本格式。其输出类似于 Unity 使用的 YAML 格式。

有关这些工具的更多信息，请参阅[分析 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-analyze.html)。

## 清单文件（Manifest files）

对于生成的每个 AssetBundle，Unity 都会生成一个关联的清单文件。清单文件具有 `.manifest` 扩展名，你可以使用任何文本编辑器打开它。

它包含以下内容：

- 增量构建计算和内容验证所需的哈希。更多信息，请参阅 `BuildPipeline.GetHashForAssetBundle`。
- 循环冗余校验（CRC）。你可以通过 `BuildPipeline.GetCRCForAssetBundle` 获取此信息。
- AssetBundle 中的场景或资源列表。
- 此 AssetBundle 依赖的所有 AssetBundle 列表（以绝对路径表示）。
- 用于类型剥离（type stripping）的类型使用信息。这包括 Unity 对象、MonoBehaviour 和 ScriptableObject 派生类，以及 SerializeReference 类型的使用情况。更多信息，请参阅 `BuildPlayerOptions.assetBundleManifestPath`。

以下是 AssetBundle 清单文件内容的示例：

```yaml
ManifestFileVersion: 0
UnityVersion: 6000.2.0a6
CRC: 4208470199
Compression: None
Hashes:
  AssetFileHash:
    serializedVersion: 2
    Hash: 81197c4674c1f389b3568a0aa1b41119
  TypeTreeHash:
    serializedVersion: 2
    Hash: 3c2131fb3360d17991621f547033218e
  IncrementalBuildHash:
    serializedVersion: 2
    Hash: 489e266cfc1b361a94c3efc39afecb54
HashAppended: 0
ClassTypes:
- Class: 1
  Script: {instanceID: 0}
- Class: 4
  Script: {instanceID: 0}
SerializeReferenceClassIdentifiers: []
Assets:
- Assets/Scenes/Scene2.unity
- Assets/Scenes/SampleScene.unity
Dependencies:
- C:/MyBuild/audio.bundle
- C:/MyBuild/sprites.bundle
```

Unity 使用 `.manifest` 文件进行增量构建管线。执行构建时，Unity 会检查现有的 AssetBundle 和 `.manifest` 文件，确定 AssetBundle 是否需要重建或可以复用。如果删除 `.manifest` 文件，Unity 总是从头重建 AssetBundle。

加载 AssetBundle 并不需要清单文件，因此你无需分发它们。如果使用了 `BuildAssetBundleOptions.AppendHashToAssetBundleName`，哈希会追加到 AssetBundle 文件名上，但该哈希不会包含在 `.manifest` 文件名中。

## 根清单文件（Root manifest file）

除了每个 AssetBundle 的 `.manifest` 文件之外，Unity 还会生成一个根 `.manifest`，以构建文件夹本身的名称命名（例如 `MyBuildFolder.manifest`）。此文件列出生成的 AssetBundle 及其依赖，路径相对于构建目录。它还包含清单 AssetBundle（manifest AssetBundle）的 CRC。这个根清单对于 Player 构建期间的代码剥离至关重要，因为你可以将它的路径传递给 `BuildPipeline.BuildPlayer`，防止 AssetBundle 所需的脚本类型和 Unity 模块被剥离。

以下是根清单文件的示例：

```yaml
ManifestFileVersion: 0
CRC: 2309754985
AssetBundleManifest:
  AssetBundleInfos:
    Info_0:
      Name: bundle_prefab
      Dependencies:
        Dependency_0: bundle_sobject
    Info_1:
      Name: bundle_sobject
      Dependencies: {}
```

## 清单包（Manifest bundles）

Unity 还会生成一个清单包（manifest bundle），它是一个以所在目录命名的 AssetBundle 文件。它包含 `AssetBundleManifest` 对象，Unity 用它在运行时确定要加载哪些包依赖。

构建会额外生成两个文件。

第一个是一个小型的 AssetBundle，以它所在的目录（AssetBundle 构建到的位置）命名。该文件称为清单包（Manifest Bundle），包含 `AssetBundleManifest` 对象，可用于在运行时确定要加载哪些包依赖。有关如何使用该包的说明，请参阅[从 AssetBundle 加载资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Native.html)。

清单包也有自己的 `.manifest` 文件。以下是清单包的清单文件示例：

```yaml
ManifestFileVersion: 0
AssetBundleManifest:
  AssetBundleInfos:
    Info_0:
      Name: scene1assetbundle
      Dependencies: {}
```

清单包的 `.manifest` 文件记录了 AssetBundle 之间如何关联以及它们的依赖关系。这些信息与清单包内 `AssetBundleManifest` 对象记录的信息类似。

清单文件对于防止代码剥离你在 AssetBundle 中使用的未使用类型非常重要。如果你在项目中启用了代码剥离，请设置 `BuildPlayerOptions.assetBundleManifestPath`，在执行 Player 构建时传入此清单的路径。

## 构建报告（Build Report）

AssetBundle 构建还会生成一个 BuildReport 文件，这是一个 Unity SerializedFile，写入项目目录中的 `Library/LastBuild.buildreport`。此文件可用于查看构建步骤耗时的摘要以及 AssetBundle 内容的详细视图。你可以使用 BuildReport API 从 BuildReport 文件读取信息。

你也可以使用 Build Report Inspector 查看 BuildReport 文件的内容。

## 其他资源

- [从 AssetBundle 加载资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Native.html)
- [处理 AssetBundle 之间的依赖](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Dependencies.html)
- [AssetBundleManifest API 文档](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.html)
