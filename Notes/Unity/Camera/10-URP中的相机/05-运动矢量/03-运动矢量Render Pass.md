# URP 中的运动矢量 Render Pass

> 原文：[Motion vectors render pass in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-render-pass.html)

本页介绍 `MotionVectors` Render Pass 如何渲染 motion vector texture。

## 在帧循环中的位置

URP 在 `BeforeRenderingPostProcessing` 事件中渲染 motion vector。在此事件之前，motion vector texture 可能尚未设置，也可能仍然包含上一帧的 motion vector 数据。

因此，请求 motion vector texture 的后处理效果或自定义 Pass 应在正确的渲染事件之后读取它。过早读取可能得到未设置的纹理，或误用上一帧的数据。

## MotionVectors Pass 的结构

URP 分两个步骤渲染 motion vector texture：

1. URP 在 `MotionVectors` 全屏 Pass 中渲染 Camera motion vector。该 Pass 使用 depth texture，以及当前帧和上一帧的 Camera 矩阵，计算 Camera motion vector。
2. URP 为每个支持 motion vector 的 Renderer 与 Material 组合，绘制每对象的 motion vector Shader Pass。

第一步的计算量对每台 Camera 固定，不需要 Renderer 或 Material 提供特殊的 motion vector 支持。第二步只处理能够提供对象运动信息的 Renderer 和 Material；其计算量会随场景中相关对象的数量和复杂程度增加。

Camera motion vector 描述 Camera 自身的运动，而每对象 Pass 负责补充对象在 world space 中的运动。最终的 motion vector texture 将这些结果用于后处理、Temporal Anti-Aliasing 和其他需要帧间运动数据的功能。

---

## 文档导航

- 上一页：[[02-Shader中的内置运动矢量支持]]
- 目录：[[00-运动矢量]]
- 下一页：[[04-在自定义Shader中输出运动矢量纹理]]
