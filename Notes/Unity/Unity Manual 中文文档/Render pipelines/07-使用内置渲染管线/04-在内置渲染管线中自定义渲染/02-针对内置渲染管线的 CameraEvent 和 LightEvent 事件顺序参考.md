# 针对内置渲染管线的 CameraEvent 和 LightEvent 事件顺序参考

> 原文：[CameraEvent and LightEvent events order reference for the Built-In Render Pipeline](https://docs.unity3d.com/6000.7/Documentation/Manual/GraphicsCommandBuffers-order.html)

> [!IMPORTANT]
> 内置渲染管线已弃用，并将在未来版本中废止。在整个 Unity 6.7 LTS 生命周期内，Unity 仍会支持它，包括错误修复和维护。有关迁移的信息，请参阅[从内置渲染管线迁移到通用渲染管线](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrading-from-birp.html)和[渲染管线功能比较](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines-feature-comparison.html)。

## CameraEvent

CameraEvent 的执行顺序取决于项目使用的[渲染路径](https://docs.unity3d.com/6000.7/Documentation/Manual/RenderingPaths.html)。

### 延迟渲染路径

- [`BeforeGBuffer`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeGBuffer.html)：Unity 渲染不透明几何体。
- [`AfterGBuffer`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterGBuffer.html)：Unity 解析深度。
- [`BeforeReflections`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeReflections.html)：Unity 渲染默认反射和 Reflection Probe 反射。
- [`AfterReflections`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterReflections.html)：Unity 将反射复制到 G-buffer 的 Emissive 通道。
- [`BeforeLighting`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeLighting.html)：Unity 渲染阴影。请参阅下面的 LightEvent 执行顺序。
- [`AfterLighting`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterLighting.html)
- [`BeforeFinalPass`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeFinalPass.html)：Unity 处理最终通道。
- [`AfterFinalPass`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterFinalPass.html)
- [`BeforeForwardOpaque`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeForwardOpaque.html)（仅当存在无法使用延迟渲染的不透明几何体时调用）：Unity 渲染无法通过延迟渲染的方式渲染的不透明几何体。
- [`AfterForwardOpaque`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterForwardOpaque.html)（仅当存在无法使用延迟渲染的不透明几何体时调用）
- [`BeforeSkybox`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeSkybox.html)：Unity 渲染天空盒。
- [`AfterSkybox`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterSkybox.html)：Unity 渲染光环。
- [`BeforeImageEffectsOpaque`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeImageEffectsOpaque.html)：Unity 应用仅针对不透明对象的后期处理效果。
- [`AfterImageEffectsOpaque`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterImageEffectsOpaque.html)
- [`BeforeForwardAlpha`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeForwardAlpha.html)：Unity 渲染透明几何体，以及渲染模式为 **Screen Space - Camera** 的 UI Canvas。
- [`AfterForwardAlpha`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterForwardAlpha.html)
- [`BeforeHaloAndLensFlares`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeHaloAndLensFlares.html)：Unity 渲染 Lens Flare。
- [`AfterHaloAndLensFlares`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterHaloAndLensFlares.html)
- [`BeforeImageEffects`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeImageEffects.html)：Unity 应用后期处理效果。
- [`AfterImageEffects`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterImageEffects.html)
- [`AfterEverything`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterEverything.html)：Unity 渲染渲染模式不是 **Screen Space - Camera** 的 UI Canvas。

### 前向渲染路径

- [`BeforeDepthTexture`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeDepthTexture.html)：Unity 为不透明几何体渲染深度。
- [`AfterDepthTexture`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterDepthTexture.html)
- [`BeforeDepthNormalsTexture`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeDepthNormalsTexture.html)：Unity 为不透明几何体渲染深度法线。
- [`AfterDepthNormalsTexture`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterDepthNormalsTexture.html)：Unity 渲染阴影。请参阅下面的 LightEvent 执行顺序。
- [`BeforeForwardOpaque`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeForwardOpaque.html)：Unity 渲染不透明几何体。
- [`AfterForwardOpaque`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterForwardOpaque.html)
- [`BeforeSkybox`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeSkybox.html)：Unity 渲染天空盒。
- [`AfterSkybox`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterSkybox.html)：Unity 渲染光环。
- [`BeforeImageEffectsOpaque`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeImageEffectsOpaque.html)：Unity 应用仅针对不透明对象的后期处理效果。
- [`AfterImageEffectsOpaque`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterImageEffectsOpaque.html)
- [`BeforeForwardAlpha`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeForwardAlpha.html)：Unity 渲染透明几何体，以及渲染模式为 **Screen Space - Camera** 的 UI Canvas。
- [`AfterForwardAlpha`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterForwardAlpha.html)
- [`BeforeHaloAndLensFlares`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeHaloAndLensFlares.html)：Unity 渲染 Lens Flare。
- [`AfterHaloAndLensFlares`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterHaloAndLensFlares.html)
- [`BeforeImageEffects`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.BeforeImageEffects.html)：Unity 应用后期处理效果。
- [`AfterImageEffects`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterImageEffects.html)
- [`AfterEverything`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.CameraEvent.AfterEverything.html)：Unity 渲染渲染模式不是 **Screen Space - Camera** 的 UI Canvas。

## LightEvent 执行顺序

在上面的“渲染阴影”阶段，对于每个投射阴影的光源，Unity 会执行以下步骤：

- [`BeforeShadowMap`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.LightEvent.BeforeShadowMap.html)
- [`BeforeShadowMapPass`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.LightEvent.BeforeShadowMapPass.html)：Unity 渲染当前 Pass 的所有投射阴影者。
- [`AfterShadowMapPass`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.LightEvent.AfterShadowMapPass.html)：Unity 对每个 Pass 重复前面三个步骤。
- [`AfterShadowMap`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.LightEvent.AfterShadowMap.html)
- [`BeforeScreenSpaceMask`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.LightEvent.BeforeScreenSpaceMask.html)：Unity 将阴影贴图收集到屏幕空间缓冲区，并执行过滤。
- [`AfterScreenSpaceMask`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.LightEvent.AfterScreenSpaceMask.html)

---

## 文档导航

- 上一页：[[01-内置渲染管线中 CommandBuffer 的基础知识]]
- 目录：[[00-在内置渲染管线中自定义渲染]]
- 下一页：无
