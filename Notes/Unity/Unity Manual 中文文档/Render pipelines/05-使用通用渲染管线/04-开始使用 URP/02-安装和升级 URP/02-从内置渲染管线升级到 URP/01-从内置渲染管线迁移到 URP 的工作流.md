# 从内置渲染管线迁移到 URP 的工作流

> 原文：[Migrate from the Built-In Render Pipeline to URP workflow](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/migrating-from-birp-workflow.html)


Follow this workflow to migrate an existing project that uses the Built-In Render Pipeline to use the Universal Render Pipeline (URP).

As the Built-In Render Pipeline is deprecated, you can migrate your project to use URP instead. This workflow helps you set up your project to use URP and explains how to convert parts of your project automatically and manually to be compatible with URP.

要从内置渲染管线迁移到 URP，请完成以下任务：

1. 安装 URP 包。
2. 将 URP 设置为活动渲染管线。
3. 自动转换预构建资源和质量级别。
4. 手动转换或重新创建项目中与 URP 不兼容的部分。

## Prerequisites

You must have an existing project that uses the Built-In Render Pipeline. If you don’t have an existing project, refer to [[01-使用 URP 创建新项目]] instead.

## 安装 URP 包

要在项目中安装 URP，请使用 Package Manager 查找并安装 Universal Render Pipeline 包。

有关更多信息，请参阅[[02-将 URP 安装到现有项目中]]。

## 将 URP 设置为活动渲染管线

要配置 URP 以便在项目中工作，请将默认渲染管线资源设置为 URP 资源。

有关更多信息，请参阅[[02-将 URP 安装到现有项目中]]。

## 自动转换预构建资源和质量级别

将项目配置为使用 URP 后，使用[[06-使用渲染管线转换器转换资源]]或命令行，自动将只读材质引用、预构建着色器和质量级别转换为与 URP 兼容的资源。也可以自动转换项目中的动画剪辑或 Post-Processing Stack v2 资源。

有关更多信息，请参阅[[03-将内置渲染管线的资源和质量级别转换为 URP]]。

## 手动转换项目中的部分内容

将项目从内置渲染管线迁移到 URP 时，并非所有功能都相同或受支持。您需要手动转换或重新创建项目中的这些部分，使其与 URP 兼容。

有关更多信息，请参阅[[02-渲染管线功能比较参考]]。

### Custom shaders

如果项目使用自定义着色器，则必须手动重写这些着色器，使其与 URP 兼容。渲染管线转换器不支持转换自定义着色器。

要手动重写自定义着色器，请参阅[[04-升级自定义着色器以实现 URP 兼容性]]。

### Quality levels

In URP, your quality levels might provide a different level of performance to your Built-In Render Pipeline project.

要手动更新 URP 项目中的质量级别，请参阅[[05-将质量设置从内置渲染管线转换到 URP。]]。

**Note**: In URP, some settings that the Built-In Render Pipeline listed in the Project Settings **Quality** section have moved or changed, or no longer exist. To find the new location of these settings, refer to [[09-查找 URP 中内置渲染管线质量设置]].

### Lighting

将必要的设置和材质转换为 URP 后，URP 场景中的光照外观可能仍与原项目不一致。

要更改 URP 中的光源衰减函数，使其外观接近内置渲染管线中的衰减，请参阅 [在 URP 中更改光源衰减函数](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting/custom-lighting-change-light-falloff.html)。

### Rendering

要了解 URP 中的渲染方式，请参阅[[01-通用渲染管线中的渲染]]和[[00-在 URP 中自定义渲染和后期处理]]。

## Additional resources

- [[06-使用渲染管线转换器转换资源]]
- [[02-将 URP 安装到现有项目中]]
- [[03-将内置渲染管线的资源和质量级别转换为 URP]]

---

## 文档导航

- 上一页：[[00-从内置渲染管线升级到 URP]]
- 目录：[[00-从内置渲染管线升级到 URP]]
- 下一页：[[02-将 URP 安装到现有项目中]]
