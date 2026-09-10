# 修改 URP 源代码

> 原文：[Modify URP source code](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customize/modify-urp-source-code.html)


对于高级自定义，仅扩展或重写 URP 中定义的 API 可能还不够。您可能需要修改 URP 源代码，以更改某些方法的实现。

要准备 URP 源代码以便修改，请执行以下操作：

1. 在项目根文件夹中，打开 `Library/PackageCache`。
2. 将以下文件夹复制到项目根目录下的 `Packages` 文件夹：`com.unity.render-pipelines.universal` 和 `com.unity.render-pipelines.universal-config`。

现在 Unity 会使用项目 `Packages` 文件夹中的 URP 源代码，您可以修改这些代码。

**注意：** 将包源代码复制到 `Packages` 文件夹后，该包代码会嵌入项目，不再属于 Unity 安装的一部分。如果之后升级 Unity 版本，Unity 不会自动更新嵌入的包源代码。您需要手动将更改应用到源代码。有关嵌入式包的更多信息，请参阅[嵌入式依赖项](https://docs.unity3d.com/6000.7/Documentation/Manual/upm-embed.html)。

## 记录对嵌入式包的更改

为了便于升级到未来的 Unity 版本，请记录您对嵌入式 URP 包代码所做的所有更改。

## 其他资源

- [URP 中的自定义光照](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting/custom-lighting-landing.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
com.unity.render-pipelines.universal
com.unity.render-pipelines.universal-config
```

---

## 文档导航

- 上一页：[[06-在 URP 中将可编程渲染通道添加到帧渲染循环/04-URP 的注入点参考]]
- 目录：[[00-在 URP 中自定义渲染和后期处理]]
- 下一页：[[../08-通用渲染管线参考/00-通用渲染管线参考]]
