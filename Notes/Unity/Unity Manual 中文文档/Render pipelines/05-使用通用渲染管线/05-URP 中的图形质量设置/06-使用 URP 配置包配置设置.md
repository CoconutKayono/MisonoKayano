# 使用 URP 配置包配置设置

> 原文：[Configure settings with the URP Config package](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/URP-Config-Package.html)

可以使用通用渲染管线（URP）配置包控制 URP 的部分设置。此包是 URP 的依赖项，因此 Unity 会自动将包文件添加到包缓存中；但在使用该包之前，必须先将这些文件复制到项目中。

目前，URP 配置包只能更改一项设置：使用 Forward+ 渲染路径时，URP 渲染的最大可见光源数量。有关如何更改此数量的更多信息，请参阅 [[06-URP 中的 Forward+ 渲染路径的故障排除]]。

## 将 URP 配置包源代码嵌入项目

要准备好可供修改的 URP 配置包源代码，请执行以下步骤：

1. 在项目根目录下，进入 `Library/PackageCache`。
2. 将以下文件夹复制到项目根目录下的 `Packages` 文件夹中：

    ```xml
    com.unity.render-pipelines.universal-config
    ```

现在可以在项目中修改 URP 配置包了。

> **注意**：将包源代码复制到 `Packages` 文件夹后，该包的代码就嵌入到项目中，不再属于 Unity 安装的一部分。以后升级 Unity 版本时，Unity 不会自动更新嵌入的包源代码，需要手动将更改应用到源代码中。有关嵌入包的更多信息，请参阅[嵌入的依赖项](https://docs.unity3d.com/6000.7/Documentation/Manual/upm-embed.html)。

## 使用 URP 配置包配置 URP

可以编辑 `ShaderConfig.cs` 文件来配置 URP 项目的属性。如果编辑了此文件，还必须更新对应的 `ShaderConfig.cs.hlsl` 头文件，使它与 `ShaderConfig.cs` 中设置的定义保持一致。

有两种方式可以更新 `ShaderConfig.cs.hlsl` 文件：

- 手动编辑 `ShaderConfig.cs.hlsl`，使其与 `ShaderConfig.cs` 保持一致。这种方式更快，但更容易因为操作失误而引入错误。
- 使用编辑器根据 `ShaderConfig.cs` 生成 `ShaderConfig.cs.hlsl`。这种方式可能比手动编辑耗时更长，但可以确保两个文件同步。

要使用编辑器生成 `ShaderConfig.cs.hlsl` 文件，请执行以下步骤：

1. 在 **Project** 窗口中转到 **Packages** > **Universal RP Config** > **Runtime**，打开 **ShaderConfig.cs**。
2. 编辑需要更改的属性值，然后保存并关闭文件。
3. 在编辑器中选择 **Edit** > **Rendering** > **Generate Shader Includes**。
4. Unity 会自动配置项目和着色器，使它们使用新的配置。

### 更新 URP 配置包

使用 Package Manager 更新 URP 包时，Package Manager 会将最新版本的 URP 配置包下载到 `/Library/PackageCache/` 文件夹中，但不会自动更新 `Packages` 文件夹内的 URP 配置包文件。需要手动更新 `Packages` 文件夹中的 URP 配置包副本，并重新应用自己的修改。步骤如下：

1. 为 `Packages` 文件夹中的 `com.unity.render-pipelines.universal-config` 文件夹创建副本，以便稍后重新应用修改时参考。
2. 删除 `Packages` 文件夹中的 `com.unity.render-pipelines.universal-config` 文件夹。
3. 按照  中的步骤，再次将 `com.unity.render-pipelines.universal-config` 文件夹从 `/Library/PackageCache/` 复制到 `Packages` 文件夹。
4. 将自己的修改手动重新应用到更新后的 URP 配置包副本中。

---

## 文档导航

- 上一页：[[05-在运行时更改 URP 资源设置]]
- 目录：[[00-URP 中的图形质量设置]]
- 下一页：[[06-在通用渲染管线中添加抗锯齿]]