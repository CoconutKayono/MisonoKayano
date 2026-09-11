# 从 HDRP 迁移到 URP 的工作流

> 原文：[HDRP to URP migration workflow](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/migrating-from-hdrp-workflow.html)

按照此工作流，将使用 High Definition Render Pipeline（HDRP）的现有项目迁移为使用 Universal Render Pipeline（URP）。此工作流帮助你设置 HDRP 项目，并转换其中与 URP 兼容的部分。

要从 HDRP 迁移到 URP，请完成以下任务：

1. [[02-设置 HDRP 项目以使用 URP]]。
2. 转换与 URP 兼容的资源。
3. 调整 URP 中的场景设置。

## 开始之前

许多 HDRP 功能在 URP 中不受支持，或实现方式不同，因此需要手动转换或重新创建。例如，光线追踪和高级光照模型在 URP 中需要自定义解决方案。HDRP 到 URP 的迁移需要大量时间；包含许多自定义 Shader 和材质，或具有复杂光照、后期处理设置的大型定制项目需要更多时间。

有关渲染管线支持的功能及差异，请参阅 [[02-渲染管线功能比较参考]] 和 [[01-选择渲染管线]]。

## 设置 HDRP 项目以使用 URP

迁移前，建议先复制现有项目，然后安装并配置 URP。请参阅 [[02-设置 HDRP 项目以使用 URP]]。

## 转换与 URP 兼容的资源

设置项目以使用 URP 后，不受支持的 Shader 可能使资源显示为亮粉色。你需要手动转换 Shader、材质和 Visual Effect Graph 节点。

### 将 HDRP Shader 转换为 URP

HDRP 和 URP Shader 的材质类型、功能和输入不同；转换方式取决于 Shader 是默认、Shader Graph、自定义还是第三方 Shader。请参阅 [[03-将 HDRP Shader 转换为 URP 兼容版本]]。

### 将 HDRP Visual Effect Graph 转换为 URP

Visual Effect Graph 中的大多数节点会自动转换。请参阅 [[04-将 HDRP 的 Visual Effect Graph 转换为 URP]]。

## 调整 URP 中的场景设置

迁移后场景外观会与原 HDRP 项目不同。

### 光照

迁移后场景光照会更亮。请参阅 [[05-将 HDRP 光照转换为 URP]]。

### 后期处理

Volume 中的大多数 HDRP 后期处理重载都有对应的 URP 实现。要应用相同效果，必须在 URP 中以类似设置重新创建每个 Volume，也可以创建工具转换它们。支持情况请参阅 [[02-渲染管线功能比较参考]]。

## 其他资源

- [[02-设置 HDRP 项目以使用 URP]]
- [[01-选择渲染管线]]
- [[02-渲染管线功能比较参考]]
- [[00-使用通用渲染管线]]
- [HDRP 软件包文档](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@latest)

---

## 文档导航

- 上一页：[[00-从 HDRP 迁移到 URP]]
- 目录：[[00-安装和升级 URP]]
- 下一页：[[02-设置 HDRP 项目以使用 URP]]
