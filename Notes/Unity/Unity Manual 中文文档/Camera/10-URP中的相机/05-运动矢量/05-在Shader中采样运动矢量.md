# 在 Shader 中采样运动矢量

> 原文：[Sample motion vectors in a shader](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-sample.html)

任何 `ScriptableRenderPass` 实现都可以请求 motion vector texture 作为输入。要实现这一点，请在 custom Renderer Feature 的 `AddRenderPasses` callback 中，调用 [`ScriptableRenderPass.ConfigureInput`](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.2/api/UnityEngine.Rendering.Universal.ScriptableRenderPass.html#UnityEngine_Rendering_Universal_ScriptableRenderPass_ConfigureInput_UnityEngine_Rendering_Universal_ScriptableRenderPassInput_) 方法，并添加 `ScriptableRenderPassInput.Motion` flag。如果该帧没有其他 effect 使用 motion vectors，设置此 input flag 会强制 URP Renderer 将 motion vector render pass 注入该帧。

要在 Shader pass 中采样 motion vector texture，请在 `HLSLPROGRAM` 部分声明 Shader resource：

```hlsl
TEXTURE2D_X(_MotionVectorTexture);
SAMPLER(sampler_MotionVectorTexture);
```

要执行采样，请使用以下 macro：

```hlsl
SAMPLE_TEXTURE2D_X(_MotionVectorTexture, sampler_MotionVectorTexture, uv);
```

`_X` postfix 确保面向 XR platform 时，texture 能够被正确声明和采样。

---

## 文档导航

- 上一页：[[04-在自定义Shader中输出运动矢量纹理]]
- 目录：[[00-运动矢量]]
- 下一页：[[06-运动矢量故障排查]]
