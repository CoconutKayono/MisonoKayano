# URP 中的 Render Graph 系统中的纹理

> 原文：[Textures in the Render Graph system in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/working-with-textures.html)


如何在通用渲染管线 (URP) 中的自定义渲染通道中访问和使用纹理。

| 页面 | 描述 |
| --- | --- |
| [[02-在 URP 中的渲染图形系统中创建纹理]] | 在 Render Graph 系统渲染通道中创建纹理。 |
| [[03-在 URP 中的渲染通道之间传输纹理/03-将纹理导入 URP 中的渲染图系统]] | 要在 Render Graph 系统渲染通道中创建或使用渲染纹理，请使用 `RTHandle` API。 |
| [[01-在 URP 中的渲染通道中使用纹理]] | 要允许渲染通道读取或写入纹理，请使用 Render Graph 系统 API 将纹理设置为输入或输出。 |
| [[03-在 URP 中的渲染通道之间传输纹理/00-在 URP 中的渲染通道之间传输纹理]] | 将纹理设置为全局纹理，或将纹理添加到帧数据。 |
| [[../../04-在 URP 中执行 Blit 的最佳实践]] | 了解在 URP 中执行__ blit__“位块传输 (Bit Block Transfer)”的简写。blit 操作是将数据块从内存中的一个位置传输到另一个位置的过程。 <br><br>执行 Blit 操作的不同方法，以及编写自定义渲染通道时应遵循的最佳实践。有关 Blit 术语，请参阅 [Glossary](https://docs.unity3d.com/6000.7/Documentation/Manual/Glossary.html#blit)。 &#124; |

## 其他资源

- [[../05-URP 中的渲染图系统中的帧数据/01-从 URP 中的当前帧获取数据]]

---


## 目录

| 页面 | 说明 |
| --- | --- |
| [[01-在 URP 中的渲染通道中使用纹理]] | Read or write to a texture in a render pass in URP |
| [[02-在 URP 中的渲染图形系统中创建纹理]] | Create a temporary texture for a single frame in URP |
| [[03-在 URP 中的渲染通道之间传输纹理/00-在 URP 中的渲染通道之间传输纹理]] | Use a texture in multiple render passes in URP |

## 文档导航

- 上一页：[[../03-在 URP 中使用渲染图系统执行 Blit]]
- 目录：
- 下一页：[[01-在 URP 中的渲染通道中使用纹理]]
