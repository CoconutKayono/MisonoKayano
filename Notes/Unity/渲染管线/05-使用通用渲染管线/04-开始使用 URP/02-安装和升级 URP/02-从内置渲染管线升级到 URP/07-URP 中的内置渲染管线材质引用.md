# URP 中的内置渲染管线材质引用

> 原文：[Built-In Render Pipeline material references in URP reference](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-material-refs.html)


使用 [[03-将内置渲染管线的资源和质量级别转换为 URP]] 后，Unity 会将所选只读材质的引用转换为对应的通用渲染管线（URP）材质。

## 材质映射

下表列出了使用 Render Pipeline Converter 时，内置渲染管线材质会转换成的 URP 材质。

| **内置渲染管线材质** | **通用渲染管线材质** |
| --- | --- |
| Default-Diffuse | Lit |
| Default-Material | Lit |
| Default-ParticleSystem | Particles Unlit |
| Default-Particle | Particles Unlit |
| Default-Terrain-Diffuse | Terrain Lit |
| Default-Terrain-Specular | Terrain Lit |
| Default-Terrain-Standard | Terrain Lit |
| Sprites-Default | Sprite-Lit Default |
| Sprites-Mask | Sprite-Lit Default |
| SpatialMappingOcclusion | SpatialMapping Occlusion |
| SpatialMappingWireframe | SpatialMapping Wireframe |

## 其他资源

- [[06-使用渲染管线转换器转换资源]]
- [[03-将内置渲染管线的资源和质量级别转换为 URP]]

---

## 文档导航

- 上一页：[[06-使用渲染管线转换器转换资源]]
- 目录：[[00-从内置渲染管线升级到 URP]]
- 下一页：[[08-使用渲染管线转换器将着色器转换为 URP]]
