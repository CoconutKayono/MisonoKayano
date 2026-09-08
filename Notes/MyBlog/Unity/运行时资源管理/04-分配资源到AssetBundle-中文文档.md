# 将资源分配到 AssetBundle（Assign assets to an AssetBundle）

> 来源：[Unity 6000.7 官方手册 · Assign assets to an AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-assign-assets.html)

要将资源构建为 AssetBundle，你必须先将资源分配到 AssetBundle——可以在 Unity 编辑器中进行，也可以通过脚本完成。然后你可以[创建并使用脚本](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Building.html)构建 AssetBundle。关于组织 AssetBundle 的最佳方法，请参阅[将资源组织到 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html)。

> **注意**：本工作流介绍的是使用内置的 [BuildPipeline.BuildAssetBundles](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildPipeline.BuildAssetBundles.html) API 创建 AssetBundle。另一种选择是使用 [Addressables](http://docs.unity3d.com/Packages/com.unity.addressables@latest) 包，它构建在 AssetBundle 之上，并提供在项目中组织资源的 UI。

## 在编辑器中分配资源到 AssetBundle

要在 Unity 编辑器中为给定资源分配 AssetBundle，请执行以下步骤：

1. 在 Project 窗口中选择资源，并在 [Inspector](https://docs.unity3d.com/6000.7/Documentation/Manual/UsingTheInspector.html) 中查看它。
2. 使用 Inspector 窗口底部的 **AssetBundle** 左侧下拉菜单分配或创建 AssetBundle：
   - 要创建新的 AssetBundle，请选择左侧下拉菜单并选择 **New**，或从列表中选择一个现有的 AssetBundle。
   - **提示：** 要使用子文件夹组织 AssetBundle，请使用 `/` 字符。例如，使用 AssetBundle 名称 `environment/forest`，可以在 environment 子文件夹下创建名为 forest 的 AssetBundle。
3. 可选：使用右侧菜单分配或创建 [AssetBundle 变体](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html#assetbundle-variants)：
   - 要创建新的变体，请选择右侧下拉菜单并选择 **New**，或从列表中选择一个现有的变体。

## 将多个资源分配到 AssetBundle

你可以为项目中的文件夹分配 AssetBundle。默认情况下，该文件夹中的所有资源都与文件夹分配到同一个 AssetBundle。不过，单个资源的 AssetBundle 分配优先。要将 AssetBundle 分配给文件夹：

- 在 Project 窗口中，选中其父文件夹中的该文件夹。
- 使用 **AssetBundle** 下拉菜单为文件夹分配新的或现有的 AssetBundle。

你也可以选择多个资源并将它们分配到同一个 AssetBundle。但以这种方式分配资源，会覆盖这些资源现有的任何 AssetBundle 分配。

## 通过脚本分配资源到 AssetBundle

要在代码中分配资源到 AssetBundle，请使用带 [AssetBundleBuild](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleBuild.html) 结构数组的 [BuildPipeline.BuildAssetBundles](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildPipeline.BuildAssetBundles.html) 方法。此方法会覆盖在 Inspector 中进行的任何 AssetBundle 分配。

如果你希望脚本尊重 Inspector 中进行的 AssetBundle 分配，请使用 [AssetDatabase.GetAllAssetBundleNames](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetDatabase.GetAllAssetBundleNames.html) 和 [AssetDatabase.GetAssetPathsFromAssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetDatabase.GetAssetPathsFromAssetBundle.html) 检索必要的信息，并填充 `AssetBundleBuild` 数组。

## 其他资源

- [将资源组织到 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Preparing.html)
- [将资源构建为 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Building.html)
