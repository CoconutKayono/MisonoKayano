# AssetBundle 简介（Introduction to AssetBundles）

> 来源：[Unity 6000.7 官方手册 · Introduction to AssetBundles](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundlesIntro.html)

AssetBundle 是一种存档（archive）文件，你可以用它把资源分组打包，用于制作可下载内容（DLC），或减小应用最初的安装体积。你也可以使用 AssetBundle 加载针对特定平台优化的资源，或在运行时降低内存占用。

AssetBundle 可以包含平台相关的非代码资源，例如模型、纹理、预制件、音频剪辑，甚至整个场景，Unity 会在运行时加载这些内容。AssetBundle 是平台相关的，因为 Unity 会根据你在[创建构建](https://docs.unity3d.com/6000.7/Documentation/Manual/building-introduction.html)时设置的 [BuildTarget](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildTarget.html) 将资源数据构建成相应的格式。例如，为 iOS 构建的 AssetBundle 不兼容 Android。

你还可以使用 LZMA 或 LZ4 [压缩 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-compression-format.html)，以便高效分发存档文件。

要构建和定义 AssetBundle，你可以使用高层级的 [Addressables](http://docs.unity3d.com/Packages/com.unity.addressables@latest) 包，它提供了一种从 Unity 编辑器定义和构建 AssetBundle 的方式。如果你更偏好底层 API 控制，可以使用 [BuildPipeline.BuildAssetBundles](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildPipeline.BuildAssetBundles.html)、[AssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.html) 和 [UnityWebRequestAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestAssetBundle.html) 等原生 API。

## 使用 AssetBundle 的理由

使用 AssetBundle 有助于内容分发和优化应用性能。以下是使用 AssetBundle 系统的好处：

- **动态内容交付**：你可以使用 AssetBundle 按需加载资源，这对于带有可下载内容（DLC）、章节式更新或运营服务（live service）模式的游戏尤其有用。它还有助于高效管理内存，确保只有应用所需的资源被加载进内存。
- **减小构建体积**：将资源移入 AssetBundle 可以减小应用的初始构建体积，这对于手游或体积限制严格的平台尤为重要。
- **平台兼容性**：你可以针对不同平台创建 AssetBundle，减少在应用构建中附带平台特定资源的必要。

如果你想优化资源加载——例如只流式加载角色附近的内容、只加载相关的本地化内容，或在后台加载资源——AssetBundle 很有用。不过，AssetBundle 系统提供的是底层资源管理，你或许应考虑使用 [Addressables](http://docs.unity3d.com/Packages/com.unity.addressables@latest) 包，它提供了更高级的项目内 AssetBundle 管理方式。

如果你正在做原型，或项目特别小，可以考虑使用 [Resources 系统](https://docs.unity3d.com/6000.7/Documentation/Manual/LoadingResourcesatRuntime.html)。

## 限制

AssetBundle 系统有以下限制：

- 你只能在脚本中使用 AssetBundle，没有用于构建 AssetBundle 的编辑器界面。
- AssetBundle API 不跟踪资源依赖。例如，你想从 AssetBundle 加载一个预制件时，需要在加载预制件之前手动加载该 AssetBundle 及其依赖的所有 AssetBundle。安全地卸载 AssetBundle 通常需要编写引用计数系统。更多信息，请参阅[处理 AssetBundle 之间的依赖](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Dependencies.html)。
- 你需要手动分配和释放内存，因此如果卸载了其他代码仍在依赖的 AssetBundle 中的资源，可能会造成内存泄漏或内容缺失。
- AssetBundle API 不感知 AssetBundle 是托管在本地还是远程，因此你需要跟踪项目中所有 AssetBundle 的位置。

## AssetBundle 的结构

AssetBundle 是一种容器文件格式，类似于 zip 文件。它以二进制格式的头部（header）包含以下文件类型：

- **序列化文件（Serialized files）**：包含序列化的 Unity 对象。这与 Player 构建中使用的二进制文件格式相同。输出取决于 AssetBundle 包含的内容：
  - 仅包含资源：Unity 创建一个序列化文件。
  - 仅包含场景：每个场景创建两个序列化文件。一个文件包含场景层级（scene hierarchy）中的对象，另一个包含所有被引用的对象。
- **资源文件（Resource files）**：为某些资源（如纹理和音频）单独存储的二进制数据块。这种分离使 Unity 可以使用多线程代码高效地从磁盘加载资源。

AssetBundle 文件始终包含一个序列化的 [AssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.html) 对象，它就像 AssetBundle 内容的目录。你可以在代码中使用 AssetBundle 实例从特定 AssetBundle 存档中加载资源。有关内部文件格式的详细介绍，请参阅 [AssetBundle 文件格式参考](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-file-format.html)。

## 场景 AssetBundle

不包含场景的 AssetBundle 是基于资源列表构建的。Unity 支持将场景文件分配到 AssetBundle，但你不能在单个 AssetBundle 中混合场景与其他资源。在 API 中，这类 AssetBundle 称为流式场景 AssetBundle（streaming scene AssetBundle），可通过 [AssetBundle.isStreamedSceneAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle-isStreamedSceneAssetBundle.html) 访问。

将场景构建进 AssetBundle 的过程与 Player 构建类似，并复用了大量相同的代码。

## 不同 Unity 版本之间的 AssetBundle 支持

你用旧版本 Unity 创建的 AssetBundle 通常与更新版本的 Unity 兼容。但如果版本之间存在重大变化，Unity 可能无法加载数据，此时必须使用较新版本的 Unity 重建 AssetBundle。Unity 不支持 AssetBundle 的前向兼容，因此你不能将用较新版本 Unity 构建的 AssetBundle 加载到旧版本 Unity 中。

如果对象的序列化格式发生了变化，AssetBundle 加载代码会使用安全的二进制读取反序列化方法（safe binary read deserialization）读取该对象。此方法使用类型树（type trees）将序列化数据中的字段与当前对象序列化布局进行匹配，这会影响性能。如果 AssetBundle 在构建时未写入类型树（`BuildAssetBundleOptions.DisableWriteTypeTree`），那么新版本 Unity 中的任何序列化更改都会导致加载失败，甚至可能导致崩溃。此外，安全二进制读取速度较慢，你可以通过重建 AssetBundle 以匹配当前 Player 构建来避免这种情况。

> 提示：默认情况下，Unity 会将构建 AssetBundle 所用的编辑器版本信息包含在 AssetBundle 头部。这些信息可能导致 AssetBundle 被不必要地重建。为避免这种情况，请将该编辑器版本从头部中排除。更多信息，请参阅 [BuildAssetBundleOptions.AssetBundleStripUnityVersion](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildAssetBundleOptions.AssetBundleStripUnityVersion.html)。

Unity 根据创建 AssetBundle 时的 Unity 版本和当时存在的 C# 类型对 AssetBundle 进行序列化。Unity 将这些信息存储在类型树结构中，并在从不同版本的 Unity 编辑器加载对象时使用这些信息。有关类型树（TypeTrees）的更多信息，请参阅[优化 AssetBundle 内存使用](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-optimizing.html#typetrees)。

## 脚本支持

AssetBundle 不能包含程序集，因此你不能用它分发新的 C# 类或对现有类的修改。不过，你可以使用 AssetBundle 分发序列化的对象实例，例如 ScriptableObject 资源。

Unity 根据对象的程序集、命名空间和类名进行匹配，然后创建该类的一个实例，并使用序列化的值设置对象的字段。Unity 使用类型树中存储的信息来调整不同 Unity 版本之间的字段映射。

Unity 使用代码中的[条件编译](https://docs.unity3d.com/6000.7/Documentation/Manual/platform-dependent-compilation.html)信息来决定 AssetBundle 中包含哪些字段。如果某个字段的编译是通过 `#if` 指令进行条件编译的，并且关联的符号在构建 AssetBundle 时未被定义，那么 Unity 不会将该字段包含在 AssetBundle 中。

例如，在下面的代码片段中，`always` 字段无条件包含在 AssetBundle 中，而 `experimental` 字段仅当构建时定义了 `EXPERIMENTAL_FEATURE` 符号时才会被包含：

```csharp
public class MyData : ScriptableObject
{
    public int always;
#if EXPERIMENTAL_FEATURE
    public int experimental;
#endif

public int ConditionalDataValue()
{
#if EXPERIMENTAL_FEATURE
    return experimental;
#else  
    return always;
#endif 
}

}
```

## 构建 AssetBundle

你可以使用以下方法构建 AssetBundle：

- **Addressables**：[Addressables](http://docs.unity3d.com/Packages/com.unity.addressables@latest) 包是一种从 Unity 编辑器定义和构建 AssetBundle 的友好方式。它通过高层级 API 简化了 AssetBundle 的创建和管理。
- **原生 API**：`BuildPipeline.BuildAssetBundles`、`AssetBundle` 和 `UnityWebRequestAssetBundle` 是可用于构建 AssetBundle 的原生 API，但它们需要手动管理依赖，并且你必须自己编写构建脚本。

更多信息，请参阅[将资源构建为 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Building.html)。

## 构建多个 AssetBundle

构建或重建 AssetBundle 时，最佳实践是使用一次 [AssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.html) API 调用将所有项目的 AssetBundle 一起构建。AssetBundle 之间可以相互引用和依赖。例如，一个 AssetBundle 中的材质可以引用另一个 AssetBundle 中的纹理。当你一起构建 AssetBundle 时，Unity 会自动管理它们之间的引用和依赖。

## 其他资源

- [Addressables 包](http://docs.unity3d.com/Packages/com.unity.addressables@latest)
- [BuildPipeline.BuildAssetBundles API 文档](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildPipeline.BuildAssetBundles.html)
- [将资源组织到 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html)
