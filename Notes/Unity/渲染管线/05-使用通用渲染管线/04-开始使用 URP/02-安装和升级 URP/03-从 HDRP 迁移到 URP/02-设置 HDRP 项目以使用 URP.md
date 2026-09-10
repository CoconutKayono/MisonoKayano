# 设置 HDRP 项目以使用 URP

> 原文：[Set up your HDRP project to use URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/hdrp-project-setup.html)

要将现有 High Definition Render Pipeline（HDRP）项目改用 Universal Render Pipeline（URP），必须先安装并配置 URP。

有关渲染管线，请参阅 [[../../../../03-选择渲染管线/01-选择渲染管线]] 和 [[../../../../03-选择渲染管线/02-渲染管线功能比较参考]]。如果没有现有 HDRP 项目，请参阅 [[../01-创建 URP 项目/01-使用 URP 创建新项目]]。

要设置项目，请执行以下操作：

1. 可选：复制 HDRP 项目。
2. 安装 URP。
3. 配置 URP。

## 复制 HDRP 项目

1. 复制现有 HDRP 项目。
2. 重命名副本，明确表示它是要迁移到 URP 的项目。

迁移过程中保持两个独立项目都处于打开状态。

> [!TIP]
> 可以使用分支管理项目。

## 安装 URP

1. 在 Unity 中打开要迁移到 URP 的项目。
2. 从主菜单选择 **Window > Package Management > Package Manager**，打开 Package Manager 窗口。
3. 转到 **Sources > Unity Registry**。这里会显示当前 Unity 版本可用的软件包。
4. 从列表中选择 **Universal Render Pipeline**。
5. 选择 **Install**，Unity 会直接将 URP 安装到项目中。

迁移期间保持 URP 和 HDRP 软件包都安装在项目中。

## 配置 URP

在开始使用 URP 前，需要将其配置为在项目中工作。在新的 URP 项目中执行以下操作：

1. 创建 URP 资源。
2. 配置 URP 资源。
3. 将 URP 设为活动渲染管线。

### 创建 URP 资源

为项目中的每个 HDRP 资源创建一个 URP 资源和 Universal Renderer 资源。请参阅 [创建 Universal Render Pipeline 资源](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/universalrp-asset.html)。

### 配置 URP 资源

配置每个 URP 资源和 Universal Renderer 资源中的设置，使其对应 HDRP 资源中的设置。有关 URP 设置，请参阅 [URP 资源参考](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/universalrp-asset.html) 和 [Universal Renderer 资源参考](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/universal-renderer-asset.html)。HDRP 的许多设置在 URP 中并不相同或不受支持；对应关系请参阅 [[06-URP 中的 HDRP 质量设置参考]]。

### 将 URP 设为活动渲染管线

1. 找到要使用的 URP 资源。要查找项目中的所有 URP 资源，可在搜索框使用查询 `t:universalrenderpipelineasset`。
2. 转到 **Edit > Project Settings > Graphics**。
3. 在 **Set Default Render Pipeline Asset** 部分，将 **Default Render Pipeline** 设置为该 URP 资源。选择后，可用的 Graphics 设置会立即改变。

也可以为每个质量级别设置不同的 URP 资源：

1. 选择 **Edit > Project Settings > Quality**。
2. 选择一个质量级别。
3. 在 **Render Pipeline Asset** 字段中选择 URP 资源。

## 其他资源

- [[01-从 HDRP 迁移到 URP 的工作流]]
- [[../../../../03-选择渲染管线/01-选择渲染管线]]
- [[../../../../03-选择渲染管线/02-渲染管线功能比较参考]]
- [[../../../00-使用通用渲染管线]]
- [[06-URP 中的 HDRP 质量设置参考]]

---

## 文档导航

- 上一页：[[01-从 HDRP 迁移到 URP 的工作流]]
- 目录：[[../00-安装和升级 URP]]
- 下一页：[[03-将 HDRP Shader 转换为 URP 兼容版本]]
