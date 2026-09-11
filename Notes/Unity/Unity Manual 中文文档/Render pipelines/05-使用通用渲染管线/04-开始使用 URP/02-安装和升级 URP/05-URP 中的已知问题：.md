# URP 中的已知问题：

> 原文：[Known issues in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/known-issues.html)


本页包含您在使用 URP 时可能遇到的已知问题的信息。

## 使用 Forward+ 渲染路径时构建时间过长

由于项目中使用了多种用例、目标平台、渲染器和功能，某些 URP 配置可能导致着色器变体数量变多。这可能导致编译时间过长。

着色器编译时间过长会影响播放器构建时间以及场景在编辑器中渲染的时间。

逐摄像机的可见光限制值会影响所有**光照**和**复杂光照**着色器变体的编译时间。在桌面平台的 Forward+渲染路径中，该限制值为 256。

请参阅以下页面以了解如何通过减少可见光源的最大数量来缩短 Forward+ 渲染路径的构建时间：

- [[06-URP 中的 Forward+ 渲染路径的故障排除]]

## 导入 URP 包示例时，Unity 未在质量 (Quality) > 渲染管线资产 (Render Pipeline Asset) 中设置必要的 URP 资产

导入 URP 包示例时，Unity 未在**质量 (Quality)** > **渲染管线资产 (Render Pipeline Asset)** 中设置必要的 URP 资产，且某些示例渲染效果不起作用。

要解决此问题，请执行以下操作：

打开**项目设置 (Project Settings)** > **质量 (Quality)** > **渲染管线资产 (Render Pipeline Asset)**，选择 `SamplesPipelineAsset`。

![打开项目设置 (Project Settings) > 质量 (Quality) > 渲染管线资产 (Render Pipeline Asset)，选择 SamplesPipelineAsset](urp-12-package-samples.png)

打开项目设置 (Project Settings) > 质量 (Quality) > 渲染管线资产 (Render Pipeline Asset)，选择 SamplesPipelineAsset

## 将 URP 渲染器资产重命名为与任一渲染器功能重名的名称会导致错误行为

如果 URP 渲染器资产分配了任何渲染器功能，将渲染器资产重命名为与任一渲染器功能重名的名称就会导致错误行为：URP 渲染器和渲染器功能会互换位置。

以下情景展示了错误是如何发生的：

- 假设项目中的 URP 渲染器名为 `UniversalRenderer`。
- 该渲染器被分配了一个名为 `NewRenderObjects` 的渲染器功能。

![分配了渲染器功能的 UniversalRenderer。](urp-10-renaming-renderer.png)

分配了渲染器功能的 UniversalRenderer。
- 将 `UniversalRenderer` 重命名为 `NewRenderObjects` 会导致错误行为：
渲染器与渲染器功能交换了位置且行为错误。

为避免此问题，请勿让 URP 渲染器资产与渲染器功能资产使用相同的名称。

如需查找有关此问题的更新，请参阅 [Unity 问题跟踪器](https://issuetracker.unity3d.com/issues/parent-and-child-nested-scriptable-object-assets-switch-places-when-parent-scriptable-object-asset-is-renamed)。

## 升级 URP 包时出现关于 _AdditionalLights 属性的警告

在某些情况下，将 URP 包升级到新版本时，可能会出现以下警告：

```
Property (_AdditionalLights) exceeds previous array size (256 vs 16). Cap to previous size.
```

此警告不会导致项目出现问题，重启编辑器后警告就会消失。


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
Property (_AdditionalLights<...>) exceeds previous array size (256 vs 16). Cap to previous size.
```

---

## 文档导航

- 上一页：[[18-从轻量级渲染管线升级到通用渲染管线]]
- 目录：[[00-安装和升级 URP]]
- 下一页：[[03-配置 URP 以获得更好的性能]]
