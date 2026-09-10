# URP 的帧数据纹理参考

> 原文：[Frame data textures reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-frame-data-reference.html)


您可以从帧数据获取以下纹理。

## 颜色数据

| **属性** | **纹理** | **写入纹理的 URP 着色器通道** |
| --- | --- | --- |
| `activeColorTexture` | 摄像机当前针对的目标颜色纹理。 | 任何通道，具体取决于您的设置 &#124; `afterPostProcessColor` &#124; URP 后期处理通道后的主要颜色纹理。 &#124; `UberPost` |
| `backBufferColor` | 屏幕后备缓冲区的颜色纹理。如果使用[后期处理](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/integration-with-post-processing.html)，则除非您启用了 [HDR 调试视图](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing/hdr-output-debug-views-urp.html)，否则 URP 会在渲染结束时写入此纹理。有关更多信息，请参阅 `debugScreenTexture`。 | 任何通道，具体取决于您的设置 |
| `cameraColor` | 摄像机的主要颜色纹理。如果启用[[../../../06-在通用渲染管线中添加抗锯齿]]，则可以在此纹理中存储多个样本。 | 任何通道，具体取决于您的设置 |
| `cameraOpaqueTexture` | 如果在 [[../../../08-通用渲染管线参考/01-URP 通用渲染管线资源参考]] 中启用了 **Opaque Texture**，则场景中具有不透明对象的纹理。 | `CopyColor` |
| `debugScreenTexture` | 如果启用 [HDR Debug Views](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing/hdr-output-debug-views-urp.html)，URP 会将[后期处理](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/integration-with-post-processing.html)的输出写入此纹理而不是 `backBufferColor`。 | `uberPost` 和 `finalPost` |

## 深度数据

| **属性** | **纹理** | **写入纹理的 URP 着色器通道** |-|-|-| | `activeDepthTexture` | GPU 当前渲染到的深度缓冲区。这是 `backBufferDepth` 或 `cameraDepth`。| 任何通道，具体取决于您的设置 | | `backBufferDepth` | 屏幕后备缓冲区的深度缓冲区。如果您的目标是 `backBufferDepth`，则当 URP 将 `cameraDepth` blit 到帧末尾附近的后备缓冲区时，所做的任何更改都将被覆盖。| 任何通道，具体取决于您的设置 | | `cameraDepth` | 摄像机当前渲染到的渲染纹理的深度缓冲区。避免以 `cameraDepth` 为目标，因为 URP 会将此缓冲区用于它自己的大部分渲染。| 任何通道，具体取决于您的设置 | | `cameraDepthTexture` | 如果在[[../../../08-通用渲染管线参考/02-URP 的通用渲染器资源参考]]中启用了 **Depth Priming Mode** 或在活动的 [[../../../08-通用渲染管线参考/01-URP 通用渲染管线资源参考]] 中启用了 **Depth Texture**，则为深度缓冲区的深度纹理副本。如果使用[[../../../04-开始使用 URP/01-通用渲染管线基础知识/02-URP 中的渲染路径/05-URP 中的延迟渲染路径/00-URP 中的延迟渲染路径]]，则 `cameraDepthTexture` 是一种颜色格式而不是深度格式。| `CopyDepth` 或 `DepthPrepass` | | `cameraNormalsTexture` | 场景法线纹理。包含具有 `DepthNormals` 通道的着色器的对象的场景深度。| `DepthNormals` 预通道 |

## 阴影数据

| **属性** | **纹理** | **写入纹理的 URP 着色器通道** |
| --- | --- | --- |
| `additionalShadowsTexture` | 附加阴影贴图。 | `ShadowCaster` |
| `mainShadowsTexture` | 主要阴影贴图。 | `ShadowCaster` |

## 贴花数据

| **属性** | **纹理** | **写入纹理的 URP 着色器通道** |-|-|-| | `dBuffer` | 贴花纹理。有关贴花纹理的更多信息，请参阅 [D 缓冲区](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-feature-decal-reference.html#dbuffer)。| `Decals` | | `dBufferDepth` | 贴花深度纹理。请参阅 [D 缓冲区](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-feature-decal-reference.html#dbuffer)。 | `Decals` |

## 运动矢量图

| **属性** | **纹理** | **写入纹理的 URP 着色器通道** |-|-| | **属性** | **纹理** | **写入纹理的 URP 着色器通道** | | `motionVectorColor` | 运动矢量颜色纹理。请参阅[运动矢量](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors.html)。| `Camera Motion Vectors` 和 `MotionVectors` | | `motionVectorDepth` | 运动矢量深度纹理。请参阅[运动矢量](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors.html)。| `Camera Motion Vectors` 和 `MotionVectors` |

## 其他数据

| **属性** | **纹理** | **写入纹理的 URP 着色器通道** |-|-|-| | `gBuffer` | G 缓冲区纹理。请参阅 [[../../../04-开始使用 URP/01-通用渲染管线基础知识/02-URP 中的渲染路径/05-URP 中的延迟渲染路径/02-URP 中延迟渲染路径中的 G 缓冲区布局]]。| `GBuffer` | | `internalColorLut` | 内部查找纹理 (LUT) 纹理。| `InternalLut` | | `overlayUITexture` | 覆盖__ UI__（即用户界面，User Interface）让用户能够与您的应用程序进行交互。Unity 目前支持三种 UI 系统。[更多信息](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/UI-system-compare.html)
| `overlayUITexture` | 覆盖 UI 纹理。有关 UI 术语，请参阅 [Glossary](https://docs.unity3d.com/6000.7/Documentation/Manual/Glossary.html#UI)。 | `DrawScreenSpaceUI` |
| `renderingLayersTexture` | 渲染层纹理。请参阅[渲染层](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/rendering-layers.html)。 | `DrawOpaques` 或 `DepthNormals` 预通道，具体取决于您的设置。 |
| `ssaoTexture` | 屏幕空间环境光遮挡（SSAO）纹理。请参阅[环境光遮挡](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing-ssao.html)。 | `SSAO` |

## 其他资源

- [[00-URP 中的渲染图系统中的帧数据]]

---

## 文档导航

- 上一页：[[03-将纹理添加到摄像机历史记录]]
- 目录：[[00-URP 中的渲染图系统中的帧数据]]
- 下一页：[[../06-在 URP 中的渲染图形系统中绘制对象]]
