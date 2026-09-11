# 将 HDRP 光照转换为 URP

> 原文：[Convert lighting from HDRP to URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-hdrp-lighting-to-urp.html)

将 High Definition Render Pipeline（HDRP）项目中的光照设置转换为与 Universal Render Pipeline（URP）兼容。

迁移后，场景光照会与原 HDRP 项目不同。URP 不支持所有 HDRP 功能，例如 physical light units、exposure 和 dynamic area lights，并且使用不同于 HDRP 的光照方程，因此需要调整光照设置。支持情况请参阅 [[02-渲染管线功能比较参考]]。有关 URP 光照，请参阅 [Lighting in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting-landing.html) 和 [URP 中的自定义光照简介](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting/custom-lighting-introduction.html)。

> [!TIP]
> 建议在原 HDRP 项目中打开场景，以便将 URP 场景与原始外观进行比较。

对于每个场景，执行以下操作调整 URP 光照：

1. 在 URP 项目中打开 [Light 组件](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/light-component.html)。
2. 在 **Emission > Intensity** 中将当前值调低，例如设为 1；对场景中的每个光源重复此操作。
3. 打开 [Reflection Probe 组件](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/reflection-probes-introduction.html)。URP 不支持 Reflection Proxies 或 Planar Reflection Probes，可能需要调整 Reflection Probe 的位置以获得相似外观。
4. 将 **Type** 改为 **Baked** 或 **Realtime**，并按需调整 **Runtime Settings > Intensity**；对每个 Reflection Probe 重复。
5. 可选：在 URP 资源中选择 **Lighting > Reflection Probes > Box Projection**，启用 Sphere 和 Box 投影。
6. 可选：在 URP 资源中选择 **Lighting > Reflection Probes > Probe Blending**，启用 Reflection Probe 平滑混合。
7. [重新生成烘焙光照](https://docs.unity3d.com/6000.7/Documentation/Manual/Lightmapping-bake.html)。烘焙 Reflection Probe 后，项目中的 Emissive 材质可能导致光照问题；请降低 Emissive 材质的 **Intensity** 值。
8. 继续调整光源和 Reflection Probe 的值，使其匹配原场景外观。

URP 不支持自动曝光。要在场景中应用曝光，必须手动将其创建为后期处理效果，并调整到与原场景匹配。请参阅 [URP 中的后期处理和全屏效果](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing-and-full-screen-effects-urp.html)。

## 其他资源

- [[01-从 HDRP 迁移到 URP 的工作流]]
- [Lighting in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting-landing.html)
- [URP 中的自定义光照简介](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/lighting/custom-lighting-introduction.html)
- [URP 中的后期处理和全屏效果](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing-and-full-screen-effects-urp.html)
- [[00-使用通用渲染管线]]

---

## 文档导航

- 上一页：[[04-将 HDRP 的 Visual Effect Graph 转换为 URP]]
- 目录：[[00-安装和升级 URP]]
- 下一页：[[06-URP 中的 HDRP 质量设置参考]]
