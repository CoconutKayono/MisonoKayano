# 将 URP 安装到现有项目中

> 原文：[Install and configure URP for an existing Built-In Render Pipeline project](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/InstallURPIntoAProject.html)


如果已经使用内置渲染管线启动了一个项目，则可以安装 URP 并将该项目配置为使用 URP。执行此操作时，您必须自行配置 URP。您可能需要手动转换或重新创建项目中的某些部分（例如光照着色器或后期处理效果），以确保它们与 URP 兼容。

您可以通过 [Package Manager 系统](https://docs.unity3d.com/Packages/com.unity.package-manager-ui@latest/index.html)将最新版本的通用渲染管线 (URP) 下载并安装到现有项目中。如果您尚未创建项目，请参考[[01-使用 URP 创建新项目]]。

## 准备工作

URP 提供了自身的[集成后期处理解决方案](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/integration-with-post-processing.html)。如果您的项目中安装了 Post Processing v2 包，则需要在将 URP 安装到项目中之前删除 Post Processing v2 包。安装 URP 后，您可以重新创建所需的后期处理效果。

URP 目前不支持自定义后期处理效果。如果您的项目使用自定义后期处理效果，目前无法在 URP 中重新创建这些效果。即将发布的 URP 版本将支持自定义后期处理效果。

使用 URP 创建的项目与高清渲染管线 (HDRP) 或内置渲染管线不兼容。在开始开发之前，必须决定在项目中使用哪个渲染管线。有关选择渲染管线的信息，请参阅 [[00-选择渲染管线]]。

## 安装 URP

1. 在 Unity 中，打开您的项目。
2. 在顶部菜单栏中，选择**窗口 (Window)** > **资源包管理器 (Package Manager)**，以打开**资源包管理器**窗口。
3. 在**资源包 (Package)** 菜单中，选择 **Unity 注册表 (Unity Registry)**。这显示了当前运行的 Unity 版本的可用资源包列表。
4. 在显示的包列表中，选择 **Universal RP**。
5. 在资源包管理器窗口的右下角，点击**安装 (Install)** 按钮。这将直接将 URP 安装到您的项目中。

## 配置 URP

在开始使用 URP 之前，您需要对其进行配置。创建一个可编程渲染管线资源，并调整项目的图形设置。

### 创建通用渲染管线资源

[[01-URP 通用渲染管线资源参考]] (URP Asset) 包含项目的全局渲染和质量设置，并用于创建渲染管线实例。渲染管线实例包含中间资源和渲染管线实现。

要创建通用渲染管线资源，请按照以下步骤操作：

1. 在 Editor 中，打开 Project 窗口。
2. 在项目窗口中右键单击，选择**创建 (Create)** > **渲染 (Rendering)** > **URP 资源（带有通用渲染器）(URP Asset (with Universal Renderer))**。或者，导航到顶部的菜单栏，然后选择 **资源 (Assets)** > **创建 (Create)** > **渲染 (Rendering)** > **URP 资源（带有通用渲染器）(URP Asset (with Universal Renderer))**。

您可以保留默认名称，或为新的通用渲染管线资源输入一个新名称。

### 设置 URP 为活动渲染管线

要设置 URP 为活动渲染管线：

1. 在项目中找到您刚刚创建的渲染管线资源。
**提示**：要查找项目中的所有通用渲染管线资源，可以在项目窗口的搜索框中输入以下查询：`t:universalrenderpipelineasset`。
2. 选择**编辑 (Edit)** > **项目设置 (Project Settings)** > **图形 (Graphics)**。
3. 在 **Scriptable Render Pipeline Settings** 字段中，选择您创建的 URP 资源。选择后，图形设置将立即更新为 URP 的配置。

**（可选）**：

为不同的质量级别设置覆盖 URP 资源：

1. 选择**编辑 (Edit)** > **项目设置 (Project Settings)** > **质量 (Quality)**。
2. 选择一个质量级别。在 **Render Pipeline Asset** 字段中，为该质量级别指定一个渲染管线资源。

## 升级着色器

如果您的项目使用预构建的[标准着色器](https://docs.unity3d.com/Manual/shader-StandardShader.html)或为内置渲染管线制作的自定义 Unity 着色器，则必须将它们转换为与 URP 兼容的 Unity 着色器。有关此主题的更多信息，请参阅[[08-使用渲染管线转换器将着色器转换为 URP]]。

## 从内置渲染管线升级

将项目从内置渲染管线 (BiRP) 升级到通用渲染管线 (URP) 时，会发生许多变化。这些变化涉及广泛，除了上述 URP 的初始安装步骤外，还需要进行额外的操作。以下页面将详细介绍这些变化，并提供进一步的指导：

- [[08-使用渲染管线转换器将着色器转换为 URP]]
- [[06-使用渲染管线转换器转换资源]]
- [[04-升级自定义着色器以实现 URP 兼容性]]
- [[09-查找 URP 中内置渲染管线质量设置]]
- [[05-将质量设置从内置渲染管线转换到 URP。]]

---

## 文档导航

- 上一页：[[01-从内置渲染管线迁移到 URP 的工作流]]
- 目录：[[00-从内置渲染管线升级到 URP]]
- 下一页：[[03-将内置渲染管线的资源和质量级别转换为 URP]]
