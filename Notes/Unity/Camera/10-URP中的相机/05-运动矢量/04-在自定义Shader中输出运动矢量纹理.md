# 在自定义 Shader 中输出运动矢量纹理

> 原文：[Output a motion vector texture in a custom shader](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-custom-shader.html)

要让 URP 为 ShaderLab Shader 渲染 **MotionVectors** pass，请确保 active SubShader 包含带有以下 [LightMode tag](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-shaders/urp-shaderlab-pass-tags.html#lightmode) 的 pass：

```hlsl
Tags { "LightMode" = "MotionVectors" }
```

例如：

```hlsl
Shader "Example/MyCustomShaderWithPerObjectMotionVectors"
{
    SubShader
    {
        // ...其他 pass、SubShader tag 和 command。

        Pass
        {
            Tags { "LightMode" = "MotionVectors" }
            ColorMask RG

            HLSLPROGRAM

            // 在此处添加 Shader code。

            ENDHLSL
        }
    }
}
```

有关为 alpha clipping、LOD cross-fade 或 alembic animation 等功能添加 Motion Vector pass 支持的示例，请参阅 URP 预构建 ShaderLab Shader 中 `MotionVectors` pass 的实现，例如 `Unlit.shader` 文件。`MotionVectors` pass 的渲染应与非 motion-vector pass 匹配，并反映该 pass 执行的任何自定义变形和/或顶点动画。

如果 custom Shader 只用于具有 Transform motion 或 skinned animation 的对象，且不使用 alpha clipping、LOD cross-fade、alembic animation、自定义变形或顶点动画，那么 URP 提供的 motion vector fallback Shader 可能已经足够。要添加预构建 fallback Shader，请将以下 ShaderLab command 添加到 SubShader block：

```hlsl
Shader "Example/MyCustomShaderWithPerObjectMotionVectorFallback"
{
    SubShader
    {
        // ...其他 pass、SubShader tag 和 command。

        UsePass "Hidden/Universal Render Pipeline/ObjectMotionVectorFallback/MOTIONVECTORS"
    }
}
```

> [!NOTE]
> 在早于 Unity 2023.2 的版本中，对于没有带有 `MotionVectors` LightMode tag 的 pass 的所有 SubShader block，URP 会自动使用 fallback pass。从 Unity 2023.2 开始，该 fallback 逻辑被禁用，原因如下：
>
> - fallback 逻辑只是最初为 URP 自有 Material 准备的实现细节。
> - URP Material 现在使用特定于 Material 类型的 motion vector pass，以支持 alpha clip、LOD cross-fade 或 alembic animation 等功能，使 fallback 过时。
> - fallback 逻辑会为不适用的内容造成非预期 visual artefacts，例如不应绘制任何对象运动矢量的 decal。

---

## 文档导航

- 上一页：[[03-运动矢量Render Pass]]
- 目录：[[00-运动矢量]]
- 下一页：[[05-在Shader中采样运动矢量]]
