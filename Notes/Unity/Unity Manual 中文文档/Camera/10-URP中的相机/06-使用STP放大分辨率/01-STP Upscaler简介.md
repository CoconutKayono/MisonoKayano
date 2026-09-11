# STP Upscaler 简介

> 原文：[Introduction to Spatial-Temporal Post-processing in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/stp/stp-upscaler.html)

Spatial-Temporal Post-Processing（STP）使用 spatial 和 temporal upsampling 技术生成高质量、抗锯齿的图像。

STP 是一种基于软件的 upscaler。

## 要求

STP 使用 compute shader，因此目标平台必须支持 [Shader Model 5.0](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/d3d11-graphics-reference-sm5)。

STP 不支持 OpenGL ES，即使平台支持 compute shader 也不支持。

STP 需要 temporal anti-aliasing（TAA）pre-processing。如果尚未选择 TAA，STP 会隐式启用它。

## STP 性能

STP 会根据应用运行的平台自动配置，以在性能和质量之间提供最佳平衡。无需为不同平台分别配置 STP。

在 PC 和主机等高性能平台上，STP 使用质量更高的 image filtering 逻辑和额外的 deringing 逻辑，以改善图像放大时的图像质量。这些技术需要额外处理能力，Unity 会在性能影响不明显的高性能设备上使用它们。

在移动设备上，STP 使用性能更高的 image filtering 逻辑，在性能和图像质量之间取得平衡。这会减少 STP 对低性能设备的影响，同时仍然提供高质量图像。

## 其他资源

- [[02-启用STP]]
- [[03-STP Rendering Debugger参考]]

---

## 文档导航

- 上一页：[[00-使用STP放大分辨率]]
- 目录：[[00-使用STP放大分辨率]]
- 下一页：[[02-启用STP]]
