# 将 HDRP 的 Visual Effect Graph 转换为 URP

> 原文：[Convert Visual Effect Graph from HDRP to URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-hdrp-vfx-graph-to-urp.html)

将 High Definition Render Pipeline（HDRP）项目中的 Visual Effect Graph 转换为与 Universal Render Pipeline（URP）兼容。

在 URP 项目中打开 Visual Effect Graph，或将渲染管线从 HDRP 改为 URP 时，大多数节点会自动转换。但是，有几种 Output Particle 节点类型不会自动从 HDRP 转换为 URP。

| HDRP 输出节点 | URP 输出节点 | 说明 |
| --- | --- | --- |
| Output Particle Lit | Output Particle Lit。Shader Graph 和 Unlit 粒子会自动从 HDRP 转换为 URP。 | 确保输出几何体类型匹配，例如 mesh、quad 和 decal。 |
| Output ParticleStrip Lit | Output ParticleStrip Lit。Shader Graph 和 Unlit 粒子条带会自动转换。 | 不适用。 |
| Output Particle Distortion | URP 不支持 Distortion 输出。改在 Output Particle URP Shader Graph 或 Output Particle Strip Shader Graph 中重新创建。 | 可参考 Shader Graph 子图模板：Particle Distortion、Particle Camera Fade 和 Particle Flipbook Blending。 |
| Output Particle HDRP Volumetric Fog | URP 不支持体积雾。要在 URP 中使用体积雾，必须实现自定义或第三方体积雾方案。 | 不适用。 |

转换 HDRP Visual Effect Graph 到 URP 时，如果输出区域使用上述类型之一，Unity 会移除整个输出区域。必须添加新的 URP Output Particle 节点，并重新创建 HDRP 图中的其他节点，例如 Set Size Over Life 和 Orient Camera Facing。

## 其他资源

- [[01-从 HDRP 迁移到 URP 的工作流]]
- [[../../../../03-选择渲染管线/02-渲染管线功能比较参考]]

---

## 文档导航

- 上一页：[[03-将 HDRP Shader 转换为 URP 兼容版本]]
- 目录：[[../00-安装和升级 URP]]
- 下一页：[[05-将 HDRP 光照转换为 URP]]
