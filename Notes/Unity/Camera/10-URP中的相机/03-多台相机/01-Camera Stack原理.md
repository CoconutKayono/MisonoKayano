# Camera Stack 原理

> 原文：[Camera stacking in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras/camera-stacking-concepts.html)

在 Universal Render Pipeline（URP）中，可以使用 Camera Stacking 将多台 Camera 的输出分层，创建单个合并输出。Camera Stacking 可以创建 2D UI 中的 3D 模型、车辆驾驶舱等效果。

Camera Stack 由一台 [[../02-相机渲染类型/01-相机渲染类型简介#Base Camera|Base Camera]] 和一台或多台 [[../02-相机渲染类型/01-相机渲染类型简介#Overlay Camera|Overlay Camera]] 组成。Camera Stack 会使用 Stack 中所有 Camera 的合并输出覆盖 Base Camera 的输出。因此，凡是可以对 Base Camera 输出执行的操作，也可以对 Camera Stack 输出执行，例如将 Camera Stack 渲染到 render target 或应用 post-processing effect。

有关更多信息，请参阅[[02-设置Camera Stack|设置 Camera Stack]]。要下载 URP 中 Camera Stacking 的示例，请安装 [Camera Stacking samples](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/package-sample-urp-package-samples.html#camera-stacking)。

## Camera Stacking 与渲染顺序

URP 会在单个 Camera 内执行多项优化，包括减少 overdraw 的渲染顺序优化。但是，使用 Camera Stack 时，需要定义 URP 渲染 Camera 的顺序。必须避免以导致过度 overdraw 的顺序排列 Camera。有关 URP 中 overdraw 的更多信息，请参阅[渲染顺序优化](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras-advanced.html#rendering-order-optimizations)。

## Camera Stacking 与 post-processing

应该只对 Stack 中最后一台 Camera 应用 post-processing，因此：

- URP 只渲染一次 post-processing effect，而不是对每台 Camera 重复渲染。
- 视觉效果保持一致，因为 Stack 中的所有 Camera 都接收相同的 post-processing。

## 限制

Camera Stack 中的 Camera 不能混用不同类型的 Renderer（2D 和 3D）。

## 其他资源

- [[02-设置Camera Stack]]
- [[../08-Camera Inspector窗口参考/01-Camera Inspector窗口参考|Camera Component 参考]]

---

## 文档导航

- 上一页：[[00-多台相机]]
- 目录：[[00-多台相机]]
- 下一页：[[02-设置Camera Stack]]
