# URP 中的 Forward+ 渲染路径的故障排除

> 原文：[Troubleshooting the Forward+ rendering path in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/forward-plus-rendering-path-limitations.html)


## 减少构建时间

由于项目中使用了多种用例、目标平台、渲染器和功能，某些 URP 配置可能导致着色器变体数量变多。这可能导致编译时间变长。

着色器编译时间变长会影响播放器构建时间和场景在编辑器中渲染的时间。

每个摄像机的可见光源限制值会影响每个**光照**和**复杂光照**着色器变体的编译时间。在桌面平台上的 Forward+ 渲染路径中，该限制为 256。

本部分介绍如何通过更改默认的每个摄像机最大可见光源数量来减少着色器编译时间。

### 更改最大可见光源数量

**注意：**本说明描述了 URP 设计限制的解决方法。此限制将在 Unity 未来的版本中得到解决。

[[06-使用 URP 配置包配置设置]]包含用于定义最大可见光源数量的设置。以下说明描述了如何更改此类设置。

**注意：**如果升级项目的 Unity 版本，请重复此过程。

1. 在项目文件夹中，将 **URP Config Package** 文件夹从 `/Library/PackageCache/com.unity.render-pipelines.universal-config` 复制到 `/Packages/com.unity.render-pipelines.universal-config`。
2. 打开文件 `/com.unity.render-pipelines.universal-config/Runtime/ShaderConfig.cs.hlsl`。 该文件包含多个以 `MAX_VISIBLE_LIGHT_COUNT` 开头并以目标平台名称结尾的定义。将括号中的值更改为适合项目的最大每摄像机视锥体光源计数，例如 `MAX_VISIBLE_LIGHT_COUNT_DESKTOP (32)`。 对于 **Forward+** 渲染路径，该值包括主光源。对于**前向**渲染路径，该值不包括主光源。
3. 打开文件 `/com.unity.render-pipelines.universal-config/Runtime/ShaderConfig.cs`。 该文件包含多个以 `k_MaxVisibleLightCount` 开头并以平台名称结尾的定义。更改该值，使其与 `ShaderConfig.cs.hlsl` 文件中设置的值（例如 `k_MaxVisibleLightCountDesktop = 32;`）相匹配。
4. 保存编辑的文件并重新启动 Unity 编辑器。Unity 会自动配置项目和着色器，以使用新配置。

现在每个着色器变体的编译时间减少，因此播放器构建时间应该会减少。

---

## 文档导航

- 上一页：[[05-在 URP 中使着色器与延迟渲染路径兼容]]
- 目录：[[00-URP 中的渲染路径]]
- 下一页：[[00-安装和升级 URP]]
