# 将 HDRP Shader 转换为 URP 兼容版本

> 原文：[Convert shaders from HDRP to URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-hdrp-shaders-to-urp.html)

将 High Definition Render Pipeline（HDRP）Shader 转换为 Universal Render Pipeline（URP）兼容版本的方式取决于 Shader 的设置。

HDRP 和 URP 默认 Shader 的材质类型、功能和输入不同。转换 HDRP Shader 和材质可能需要：

- 将 Shader 重新分配为 URP 等效 Shader。
- 重新映射材质属性。
- 接受缺失的功能，或实现替代方案。
- 重新制作纹理。
- 创建新 Shader。

> [!TIP]
> 对于大型项目，尤其可以使用脚本自动化此过程。

有关支持的 Shader，请参阅 [[../../../../03-选择渲染管线/02-渲染管线功能比较参考]]。

## 默认 Shader

大多数 [默认 HDRP Shader](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/shader-materials-reference.html) 与 [默认 URP Shader](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shaders-in-universalrp.html) 并不对应，必须在 URP 中手动重新创建 HDRP Shader。有关编写 URP 自定义 Shader，请参阅 [在 URP 中编写自定义 Shader 的示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-landing.html)。

| HDRP Shader | URP Shader |
| --- | --- |
| **HDRP/Lit** | **Universal Render Pipeline/Lit**；如果有 **Coat Mask** 纹理，使用 **Universal Render Pipeline/Complex Lit**。 |
| **HDRP/LitTessellation** | **Universal Render Pipeline/Lit**；如果有 **Coat Mask** 纹理，使用 **Universal Render Pipeline/Complex Lit**。URP 不支持 Tessellation；可改用 [Parallax Occlusion Mapping 节点](https://docs.unity3d.com/Packages/com.unity.shadergraph@17.5/manual/Parallax-Occlusion-Mapping-Node.html)。 |
| **HDRP/Terrain Lit** | **Universal Render Pipeline/Terrain/Lit** |
| **HDRP/Unlit** | **Universal Render Pipeline/Unlit**。URP 不支持所有属性。 |

## 将 Lit Shader 从 HDRP 转换为 URP

### Surface types

**Surface Type** 属性在 HDRP 与 URP 之间不对应，因此转换为 URP/Lit 会破坏这些设置。必须将材质改回正确的表面类型和混合模式。

### 材质类型

HDRP 中的 **Material Type** 对应关系如下：

- **Standard** 对应 URP **Workflow Mode** 的 **Metallic**。
- **Specular** 对应 URP **Workflow Mode** 的 **Specular**。

其他 Material Type 没有对应的 URP 设置。对于不是 Standard 或 Specular 的材质，请在自定义 Shader 或 Shader Graph 中重新创建。

### 法线贴图和缩放

HDRP Shader 使用 `_NormalMap` 和 `_NormalScale`；URP 使用 `_BumpMap` 和 `_BumpScale`。必须重新映射这些属性。URP/Lit 和 URP/ComplexLit 没有 **Bent Normal Map** 的对应项。

### Mask map

在 HDRP/Lit 中，Mask Map 的通道为 R：Metallic、G：AO、B：Detail Mask、A：Smoothness。在 URP/Lit 中这些是分开的纹理，并按通道映射，因此建议使用 Mask 纹理设置这些贴图。

### 细节输入

HDRP/Lit Detail Map 不对应 URP/Lit 的细节输入。HDRP 的 Detail Map 是包含多种材质细节信息的打包纹理；URP 使用分开的 Mask、Base Map 和 Normal Map 纹理。要在 URP 中重新创建它，可以：

- 创建自定义 Shader 或 Shader Graph。
- 根据 HDRP Mask Map 和 Detail Map 创建新的 Mask、Base Map 和 Normal Map 纹理。

## 将 Unlit Shader 从 HDRP 转换为 URP

### Surface types

**Surface type** 属性在 HDRP 与 URP 之间不对应，因此转换为 URP/Unlit 会破坏这些设置。必须将材质改回正确的表面类型和混合模式。

### 颜色和颜色贴图

HDRP 使用 `_UnlitColor` 和 `_UnlitColorMap`；URP 使用 `_BaseColor` 和 `_BaseMap`。必须重新映射这些属性。

### Emission 输入

URP/Unlit 没有 Emission 的对应项。若要重新创建 Emission，可以尝试使用 `_BaseColor` 和 `_BaseMap`，或使用自定义 Shader 或 Shader Graph 实现相同效果。

## Shader Graph Shader

要转换使用 Shader Graph 创建的 Shader，请将 Graph Target 更新为 URP，并更新其 fragment 和 vertex context。可能会缺少功能，且 URP 不支持 HDRP fragment 和 vertex context 中的某些输出节点。若 HDRP 节点没有 URP 对应项，可以创建自定义 Shader 方案、使用 Scriptable Renderer Feature 实现高级效果，或设计相似的替代方案。

## 第三方 Shader

如果使用第三方 Shader，请联系第三方以了解其跨平台支持情况。

## 自定义 Shader

在 HDRP 中创建的自定义 Shader 必须重写为 URP 兼容版本；复杂 Shader 可能需要大量时间。请参阅 [在 URP 中编写自定义 Shader 的示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-landing.html) 和 [URP 中的 Shader 方法](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shader-methods.html)。

> [!TIP]
> 为避免迁移期间破坏原 HDRP Shader，可创建带有正确 URP 标签的重复 SubShader：`{ "RenderType" = "Opaque" "RenderPipeline" = "UniversalPipeline" }`。

如果 Shader 写入 G-buffer，请使用 `PackGBuffersBRDFData` 方法正确打包数据。URP 与 HDRP 的 G-buffer 布局不同；手动打包或使用 HDRP 打包函数会导致光照不正确。

如果 Shader 在多个 pass 后访问渲染管线的 camera texture，请在 URP 中使用 **Opaque Texture** 重新创建，它直接存储在 opaque pass 之后。如果效果需要在渲染管线的其他位置访问 camera texture，请创建 Scriptable Renderer Feature。

### 自定义 Lit Shader

将自定义 Lit Shader 转换为 URP 兼容版本需要：

- 更新 ShaderLab 标签以使用 URP。
- 使用 **LightMode Pass** 标签，告诉 URP 在不同阶段使用哪个 pass。
- 对于使用 `UniversalForward` 和 `UniversalForwardOnly` 的 Shader，调用 `UniversalFragmentPBR`，使 Shader 获得正确光照。
- 使用 URP 光照函数；请参阅 [URP 中的自定义光照简介](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting/custom-lighting-introduction.html)。

### 自定义 Unlit Shader

将 ShaderLab 标签更新为使用 URP。

## 其他资源

- [[01-从 HDRP 迁移到 URP 的工作流]]
- [[../../../../03-选择渲染管线/02-渲染管线功能比较参考]]

---

## 文档导航

- 上一页：[[02-设置 HDRP 项目以使用 URP]]
- 目录：[[../00-安装和升级 URP]]
- 下一页：[[04-将 HDRP 的 Visual Effect Graph 转换为 URP]]
