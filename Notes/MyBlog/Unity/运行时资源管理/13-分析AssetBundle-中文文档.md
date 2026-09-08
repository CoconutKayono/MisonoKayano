# 分析 AssetBundle（Analyzing AssetBundles）

> 来源：[Unity 6000.7 官方手册 · Analyzing AssetBundles](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-analyze.html)

Unity 提供了多种工具来检查 AssetBundle 的内部结构和内容，以帮助故障排除。

## WebExtract 和 binary2text

WebExtract 和 binary2text 是随每个 Unity 编辑器安装一起提供的底层命令行工具。

- **WebExtract**：提取 AssetBundle 中嵌入的文件，类似于解压存档。它会在 AssetBundle 所在目录中创建一个以 AssetBundle 命名的文件夹，其中包含其内部文件。
- **binary2text**：将二进制 SerializedFile（Unity 的核心数据格式）转换为人类可读的文本格式，类似于 Unity 的 YAML 格式。

你也可以使用 [UnityDataTools](https://github.com/Unity-Technologies/UnityDataTools)，它是 WebExtract 和 binary2text 工具的替代方案。

更多信息，请参阅[分析已构建的资源](https://docs.unity3d.com/6000.7/Documentation/Manual/assets-analyze-built-assets.html)。

## BuildReport

BuildReport 文件（位于项目目录中的 `Library/LastBuild.buildreport`）是一个 Unity SerializedFile，记录了每个 AssetBundle 的内容。此 SerializedFile 包含关于构建的详细信息，包括构建步骤的耗时以及 AssetBundle 内容的细粒度视图。你可以通过以下方式查看此文件：

- **Build Report Inspector**：使用 [Build Report Inspector](https://github.com/Unity-Technologies/BuildReportInspector) 包在编辑器内查看 BuildReport 内容。
- **编程访问**：使用 [BuildReport](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Build.Reporting.BuildReport.html) 访问 BuildReport 文件中的数据。
- **文本格式**：启用 **Preferences > Diagnostics > BuildReportingEditor > SerializeBuildReportAsText**，直接将 BuildReport 输出为 YAML 文本。

## 其他资源

- [UnityDataTools 仓库](https://github.com/Unity-Technologies/UnityDataTools)
- [优化 AssetBundle 内存使用](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-optimizing.html)
- [AssetBundle 文件格式参考](https://docs.unity3d.com/6000.7/Documentation/Manual/assetbundles-file-format.html)
- [将资源构建为 AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundles-Building.html)
- [BuildReport API 文档](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Build.Reporting.BuildReport.html)
- [AssetBundleManifest API 文档](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.html)
