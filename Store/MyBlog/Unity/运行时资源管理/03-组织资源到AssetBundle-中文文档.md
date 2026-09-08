# 将资源组织到 AssetBundle（Organizing assets into AssetBundles）

> 来源：[Unity 6000.7 官方手册 · Organizing assets into AssetBundles](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html)

创建 AssetBundle 时，有一些[限制](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html#assetbundle-limitations)和值得注意的组织策略。

关于可以放入 AssetBundle 的资源种类以及如何设置它们，存在一些限制。下表列出了 AssetBundle 的限制：

| 限制 | 说明 |
| --- | --- |
| 文件类型 | 不能将场景和资源组合到同一个 AssetBundle 中。场景必须存储在单独的 AssetBundle 中，与包含资源的 AssetBundle 分开。不能在 AssetBundle 中包含脚本资源。不能包含 StreamingAssets 文件夹中的文件。不能将资源或场景分配到多个 AssetBundle。 |
| 命名 | AssetBundle 的名称必须与输出文件夹不同。 |
| 平台支持 | AssetBundle 只能在你为其构建的特定平台上加载。无论 [Build Profile](https://docs.unity3d.com/6000.7/Documentation/Manual/build-profiles.html) 中定义了什么平台，编辑器都可以加载任何 AssetBundle，但如果某些资源使用了编辑器所运行操作系统不支持的平台特定格式，它们可能无法正确加载。 |

## AssetBundle 命名约定

在构建过程中，Unity 会自动将所有 AssetBundle 名称转为小写。例如，名为 `Foo` 的 AssetBundle 会生成名为 `foo` 的文件。为避免任何冲突或问题，请使用小写名称命名 AssetBundle。

AssetBundle 没有既定或约定的文件扩展名。在定义 AssetBundle 名称时，你可以提供自定义扩展名，Unity 会予以保留。但这可能与 AssetBundle 变体功能冲突，因为变体功能要求以相同的根文件名配合不同的扩展名来区分变体。

你可以使用 [BuildAssetBundleOptions.AppendHashToAssetBundleName](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildAssetBundleOptions.AppendHashToAssetBundleName.html) 标志将 AssetBundle 的内容哈希作为文件名的一部分。这对 Web 托管很有用，可以让同一 AssetBundle 的不同版本共存。

不过，该标志也有缺点：

- 内置的 AssetBundle 缓存不会自动替换旧版本，因此同一 AssetBundle 的多个版本可能会留在缓存中。
- 它会影响主机平台上的文件级补丁系统，因为微小的更改会被视为一个全新的文件，而不是一个小补丁。

## AssetBundle 变体

你可以使用 AssetBundle 变体为不同情况或配置创建多个优化版本，例如不同的图形设置。例如，你可以为低、中、高分辨率纹理创建变体，以支持性能各异的设备或用户选择的图形设置。

使用 AssetBundle 变体时，Unity 允许为每个 AssetBundle 指定一个变体名称。AssetBundle 名称与变体名称的组合可唯一标识每个 AssetBundle 变体。例如，名为 `environment` 的 AssetBundle 可以有 `lowQuality`、`mediumQuality` 和 `highQuality` 变体。

AssetBundle 内的资源文件名必须匹配，但内容可以根据变体的用途而有所不同。

你可以在 Inspector 中使用 AssetBundle 旁边的变体下拉菜单创建变体，也可以使用 [AssetImporter.assetBundleVariant](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetImporter-assetBundleVariant.html)。

## 组织 AssetBundle 的策略

你可以用以下方式组织资源：

- [按功能](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html#organize-assets-by-function)：根据项目的功能部分组织资源。典型类别可能包括用户界面、角色、环境，以及应用中经常使用的其他元素。
- [按类型](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html#organize-assets-by-type)：按类型分组侧重于将同类型的资源捆绑在一起，例如音频轨道或本地化文件。
- [按运行时使用](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html#organize-assets-by-use-at-runtime)：将同时加载和使用的资源分组。这种策略常用于基于关卡的项目。

你可以在项目中混合使用这些策略以获得最佳效率。例如，你可以将不同平台的 UI 元素放入一个 AssetBundle，而将其交互内容按关卡或场景分组。

无论采用何种组织方式，遵循以下通用准则都是最佳实践：

- 将频繁更新的对象与很少更改的对象分到不同的 AssetBundle。
- 为不太可能同时加载的对象集合创建单独的 AssetBundle，例如标准资源和高清资源。你可以使用 [AssetBundle 变体](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html#assetbundle-variants)来组织。
- 将通常一起卸载的对象分组。例如，一个模型、它的纹理和它的动画。
- 如果 AssetBundle 中不足一半的内容会同时加载，请拆分该 AssetBundle。
- 如果内容经常同时加载，请合并较小的 AssetBundle。
- 如果某个 AssetBundle 中的多个对象依赖另一个 AssetBundle 中的单个资源，请考虑将该依赖移动到自己的 AssetBundle。同样，如果多个 AssetBundle 引用同一组资源，请考虑将依赖放入一个共享的 AssetBundle。

## 按功能组织资源

按功能协同工作的方式组织资源在以下情况下很有用：

- 将某个 UI 界面的所有纹理和布局数据捆绑在一起。
- 将某个角色或一组角色的所有模型和动画捆绑在一起。
- 将多个关卡共享的布景部件的纹理和模型捆绑在一起。

这种方法非常适合可下载内容（DLC），因为你可以对项目进行小幅更改，而无需向用户分发大量未更改的资源。但是，使用这种方法时，你必须熟悉每个资源在项目中的使用位置和使用时机。

## 按类型组织资源

你可以将相似类型的资源（例如音频轨道或语言本地化文件）组织到单个 AssetBundle 中，这对于很少更改的 AssetBundle 很有用。

以这种方式分组 AssetBundle，可以减少创建增量构建时需要更改和分发的 AssetBundle 数量。但运行时可能需要下载和加载更多 AssetBundle，才能将相互依赖的对象组装在一起。

## 按运行时使用组织资源

你可以将 Unity 同时加载和使用的资源分组，如果你想基于场景加载 AssetBundle，这很有用。例如，你可以将这种方法用于基于关卡的游戏：每个关卡包含独特资源，而一个 AssetBundle 包含某个场景的所有依赖。

然而，这种方法意味着一个 AssetBundle 中的资源只能在其余资源同时被使用时才能使用，否则会增加加载时间。

> **重要提示**：包含场景的 AssetBundle 会自动包含该场景中引用的所有资源，除非这些资源被明确分配到单独的 AssetBundle。如果任何其他场景在其它 AssetBundle 中使用了被引用的资源，这可能会导致资源重复。

## 其他资源

- [使用资源数据库（Asset Database）管理资源](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetDatabase.html)
- [将资源构建为 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Building.html)
- [避免资源重复](https://docs.unity3d.com/6000.7/Documentation/Manual/assets-avoid-duplication.html)
