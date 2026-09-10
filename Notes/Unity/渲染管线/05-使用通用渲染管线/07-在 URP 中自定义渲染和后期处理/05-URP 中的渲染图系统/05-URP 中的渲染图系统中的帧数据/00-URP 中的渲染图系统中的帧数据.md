# URP 中的渲染图系统中的帧数据

> 原文：[Frame data in the render graph system in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-frame-data.html)


获取通用渲染管线 (URP) 为当前帧或先前帧创建的纹理，例如颜色纹理或深度纹理。

| **页面** | **描述** |
| --- | --- |
| [[01-从 URP 中的当前帧获取数据]] | 获取 URP 为当前帧创建的纹理。 |
| [[02-在 URP 中获取先前帧的数据]] | 要获取摄像机渲染的先前帧，请使用 `UniversalCameraData.historyManager` API。 |
| [[03-将纹理添加到摄像机历史记录]] | 要将您自己的纹理添加到摄像机历史记录中，请创建一个摄像机历史记录类型来存储帧之间的纹理。 |
| [使用帧缓冲区提取功能获取当前帧缓冲区](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-framebuffer-fetch.html) | 要加快渲染速度，请使用帧缓冲区获取来读取 Unity 到目前为止已渲染的帧。 |
| [[04-URP 的帧数据纹理参考]] | 探索可从当前帧或先前帧获取的纹理。 |

---


## 目录

| 页面 | 说明 |
| --- | --- |
| [[01-从 URP 中的当前帧获取数据]] | Get data from the current frame in URP |
| [[02-在 URP 中获取先前帧的数据]] | Get data from previous frames in URP |
| [[03-将纹理添加到摄像机历史记录]] | Add textures to the camera history |
| [[04-URP 的帧数据纹理参考]] | Frame data textures reference for URP |

## 文档导航

- 上一页：[[../04-URP 中的 Render Graph 系统中的纹理/03-在 URP 中的渲染通道之间传输纹理/03-将纹理导入 URP 中的渲染图系统]]
- 目录：
- 下一页：[[01-从 URP 中的当前帧获取数据]]
