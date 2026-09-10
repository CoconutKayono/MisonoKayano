# URP 中的内置渲染管线预制着色器参考

> 原文：[Built-In Render Pipeline prebuilt shaders in URP reference](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrading-your-shaders.html)

使用[[06-使用渲染管线转换器转换资源]]中的**材质着色器转换器 (Material Shader Converter)** 后，Unity 会将选定的预制着色器转换为对应的通用渲染管线 (URP) 着色器。

> **注意**：本页仅介绍将预制着色器转换为 URP。有关如何将自定义着色器转换为 URP 的信息，请参阅[升级自定义着色器以实现 URP 兼容性](04-升级自定义着色器以实现 URP 兼容性.md)。

## 着色器映射

下表显示了使用渲染管线转换器时，内置渲染管线着色器会转换成哪一种 URP 着色器。

| 内置渲染管线着色器 | URP 着色器 |
| --- | --- |
| Standard | Universal Render Pipeline/Lit |
| Standard (Specular Setup) | Universal Render Pipeline/Lit |
| Standard Terrain | Universal Render Pipeline/Terrain/Lit |
| Particles/Standard Surface | Universal Render Pipeline/Particles/Lit |
| Particles/Standard Unlit | Universal Render Pipeline/Particles/Unlit |
| Mobile/Diffuse | Universal Render Pipeline/Simple Lit |
| Mobile/Bumped Specular | Universal Render Pipeline/Simple Lit |
| Mobile/Bumped Specular(1 Directional Light) | Universal Render Pipeline/Simple Lit |
| Mobile/Unlit (Supports Lightmap) | Universal Render Pipeline/Simple Lit |
| Mobile/VertexLit | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Diffuse | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Specular | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Bumped Diffuse | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Bumped Specular | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Self-Illumin/Diffuse | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Self-Illumin/Bumped Diffuse | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Self-Illumin/Specular | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Self-Illumin/Bumped Specular | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Transparent/Diffuse | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Transparent/Specular | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Transparent/Bumped Diffuse | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Transparent/Bumped Specular | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Transparent/Cutout/Diffuse | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Transparent/Cutout/Specular | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Transparent/Cutout/Bumped Diffuse | Universal Render Pipeline/Simple Lit |
| Legacy Shaders/Transparent/Cutout/Bumped Specular | Universal Render Pipeline/Simple Lit |

## 定义着色器的升级路径

要定义着色器的升级路径，请执行以下操作：

- 使用自定义 `MaterialUpgrader` 将旧着色器映射到新着色器。
- 使用 `IMaterialUpgradersProvider` 向系统公开升级器。

```cs
// This class defines the upgrade rule from an old shader to a new shader
public class MaterialUpgraderExample : MaterialUpgrader
{
    // Priority determines order — higher values override lower-priority upgraders
    public int priority => 1000;
    public MaterialUpgraderExample(string oldShaderName, string newShaderName)
    {
        if (oldShaderName == null)
            throw new ArgumentNullException(nameof(oldShaderName));

        // Maps the old shader to the new shader with optional property remapping (null here)
        RenameShader(oldShaderName, newShaderName, null);
    }
}

// This provider makes the upgrader discoverable by the upgrader system.
// It declares support for the Universal Render Pipeline and exposes the custom upgrade rule.
[SupportedOnRenderPipeline(typeof(UniversalRenderPipeline))]
private class ExampleMaterialProvider : IMaterialUpgradersProvider
{

    public IEnumerable<MaterialUpgrader> GetUpgraders()
    {
        // Replace "SomePathToShader" and "MappingShaderPath" with actual shader names/paths
        yield return new MaterialUpgraderExample("SomePathToShader", "MappingShaderPath");

        // Add as many upgraders you need
    }
}
```

## 其他资源

- [[06-使用渲染管线转换器转换资源]]
- [[03-将内置渲染管线的资源和质量级别转换为 URP]]
- [[04-升级自定义着色器以实现 URP 兼容性]]
- [预制着色器渲染管线兼容性参考](https://docs.unity3d.com/6000.7/Documentation/Manual/shader-built-in.html)
- [着色器错误和加载](https://docs.unity3d.com/6000.7/Documentation/Manual/shader-error.html)

---

## 文档导航

- 上一页：[[07-URP 中的内置渲染管线材质引用]]
- 目录：[[00-从内置渲染管线升级到 URP]]
- 下一页：[[09-查找 URP 中内置渲染管线质量设置]]
