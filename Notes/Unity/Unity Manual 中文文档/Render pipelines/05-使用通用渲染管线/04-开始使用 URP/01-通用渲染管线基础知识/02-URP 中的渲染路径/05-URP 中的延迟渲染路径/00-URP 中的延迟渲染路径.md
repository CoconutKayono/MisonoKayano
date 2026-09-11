# URP 中的延迟渲染路径

> 原文：[Deferred and Deferred+ rendering paths in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/deferred-rendering-path-landing.html)


![使用延迟渲染路径渲染的场景](deferred-intro-image.png)

使用延迟渲染路径渲染的场景

使用延迟渲染路径的资源，该路径对影响不透明游戏对象的光源数量没有限制。

| **页面** | **描述** |
| --- | --- |
| [[04-延迟渲染路径简介]] | 了解延迟渲染路径的工作原理及其局限性。 |
| [[01-URP 中延迟渲染路径中的渲染通道]] | 了解延迟渲染路径中的渲染通道事件顺序。 |
| [[02-URP 中延迟渲染路径中的 G 缓冲区布局]] | 理解 Unity 如何将材质特性存储在延迟渲染路径中的几何缓冲区（G 缓冲区）中。 |
| [[03-在 URP 的延迟渲染路径中启用 Accurate G-buffer normals]] | 配置 Unity 在将法线存储在 G 缓冲区时如何对法线进行编码。 |
| [[05-在 URP 中使着色器与延迟渲染路径兼容]] | 使用着色器中的 `LightMode` 标签可以使着色器与延迟渲染路径兼容。 |

---


## 目录

| 页面 | 说明 |
| --- | --- |
| [[01-URP 中延迟渲染路径中的渲染通道]] | Render passes in the Deferred and Deferred+ rendering paths in URP |
| [[02-URP 中延迟渲染路径中的 G 缓冲区布局]] | G-buffer layout in the Deferred and Deferred+ rendering paths in URP |
| [[03-在 URP 的延迟渲染路径中启用 Accurate G-buffer normals]] | Enable accurate G-buffer normals in the Deferred and Deferred+ rendering path in URP |
| [[04-延迟渲染路径简介]] | Blend terrain accurately in the Deferred and Deferred+ rendering paths in URP |
| [[05-在 URP 中使着色器与延迟渲染路径兼容]] | Make a shader compatible with the Deferred or Deferred+ rendering paths in URP |

## 文档导航

- 上一页：[[04-URP 中的前向渲染路径]]
- 目录：
- 下一页：[[01-URP 中延迟渲染路径中的渲染通道]]
