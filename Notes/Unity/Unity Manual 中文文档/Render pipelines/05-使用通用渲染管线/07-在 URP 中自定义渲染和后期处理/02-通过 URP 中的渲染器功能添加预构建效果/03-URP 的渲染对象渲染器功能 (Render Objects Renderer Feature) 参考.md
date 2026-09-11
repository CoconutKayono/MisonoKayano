# URP 的渲染对象渲染器功能 (Render Objects Renderer Feature) 参考

> 原文：[Render Objects Renderer Feature reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/renderer-feature-render-objects.html)

渲染对象渲染器功能 (Render Objects Renderer Feature) 用于在 URP 帧渲染循环中的特定位置绘制对象。可以在此功能中查看和编辑相关设置。

要使用渲染对象渲染器功能，请参阅[[02-通过 URP 中的渲染对象渲染器功能 (Render Objects Renderer Feature) 创建自定义渲染效果的示例]]。

## 属性

渲染对象渲染器功能 (Render Objects Renderer Feature) 包含以下属性。

| 属性 | 描述 |
| --- | --- |
| **名称（Name）** | 定义功能的名称。 |
| **事件（Event）** | 设置 Unity 执行此渲染器功能时在 URP 队列中的注入点。 |

### 过滤器（Filters）

| 属性 | 描述 |
| --- | --- |
| **队列（Queue）** | 仅渲染选定队列中的对象：**Opaque** 仅渲染不透明队列，**Transparent** 仅渲染透明队列。 |
| **层遮罩（Layer Mask）** | 仅渲染选定层中的对象。 |
| **LightMode 标签（LightMode tags）** | 按 `LightMode` 标签过滤着色器通道，只渲染标签匹配的着色器通道。 |

## 覆盖（Overrides）

| 属性 | 描述 |
| --- | --- |
| **覆盖模式（Override Mode）** | 设置材质覆盖模式：**None** 不覆盖材质或着色器；**Material** 覆盖材质及其所有属性；**Shader** 仅覆盖着色器并保留当前材质属性。 |
| **材质（Material）** | 使用此材质替换对象原有材质，并覆盖所有材质属性。仅在覆盖模式为 **Material** 时可用。 |
| **着色器（Shader）** | 使用此着色器替换对象材质中的着色器，同时保留材质属性供覆盖着色器访问。此模式性能较低且与 SRP Batcher 不兼容；仅在覆盖模式为 **Shader** 时可用。 |
| **通道索引（Pass Index）** | 设置覆盖材质或着色器使用的通道索引。 |
| **深度（Depth）** | 覆盖深度缓冲区设置。 |
| **写入深度（Write Depth）** | 渲染对象时将深度值写入深度缓冲区；仅在启用 **Depth** 时可用。 |
| **深度测试（Depth Test）** | 指定决定对象像素何时通过深度测试的比较函数：**Disabled**、**Never**、**Less**、**Equal**、**Less Equal**、**Greater**、**Not Equal**、**Greater Equal** 或 **Always**；仅在启用 **Depth** 时可用。 |
| **设置为输入附件（Set As Input Attachment）** | 从片上内存以只读输入附件读取深度，而不是采样深度纹理，从而减少基于图块 GPU 的内存带宽。启用后 Unity 会覆盖 **Write Depth** 和 **Depth Test**，并忽略任何 Stencil 覆盖；仅在启用 **Depth** 时可用。有关在着色器中读取深度值的信息，请参阅[从 GPU 内存获取 URP 中的当前深度缓冲区](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/read-depth-input-attachment.html)。 |
| **模板（Stencil）** | 处理并覆盖模板缓冲区值。有关 Unity 如何使用模板缓冲区的信息，请参阅 [ShaderLab：Stencil](https://docs.unity3d.com/Manual/SL-Stencil.html)。 |
| **Value** | 设置与模板缓冲区值比较的引用值。如果 **Pass** 为 **Replace**，Unity 会将此值写入缓冲区；仅在启用 **Stencil** 时可用。 |
| **Compare Function** | 将 **Value** 与每个像素的模板缓冲区值比较。可选 **Disabled**、**Never**、**Less**、**Equal**、**Less Equal**、**Greater**、**Not Equal**、**Greater Equal** 和 **Always**；仅在启用 **Stencil** 时可用。 |
| **Pass** | 模板测试通过时对模板缓冲区执行的操作：**Keep**、**Zero**、**Replace**、**Increment Saturate**、**Decrement Saturate**、**Invert**、**Increment Wrap** 或 **Decrement Wrap**；仅在启用 **Stencil** 时可用。 |
| **Fail** | 模板测试失败时对模板缓冲区执行的操作；可选值与 **Pass** 相同，仅在启用 **Stencil** 时可用。 |
| **Z Fail** | 模板测试通过但深度测试失败时对模板缓冲区执行的操作；可选值与 **Pass** 相同，仅在启用 **Stencil** 时可用。 |
| **摄像机（Camera）** | 覆盖摄像机矩阵并使用透视投影。 |
| **视野（Field Of View）** | 定义渲染对象时垂直轴方向的视野（以度为单位）。Unity 使用此值，而不是摄像机上指定的值；仅在启用 **Camera** 时可用。 |
| **位置偏移（Position Offset）** | 按此偏移量从原摄像机位置移动对象；仅在启用 **Camera** 时可用。 |
| **恢复（Restore）** | 执行此渲染器功能中的渲染通道后重置摄像机矩阵；仅在启用 **Camera** 时可用。 |

---

## 文档导航

- 上一页：[[02-通过 URP 中的渲染对象渲染器功能 (Render Objects Renderer Feature) 创建自定义渲染效果的示例]]
- 目录：[[00-通过 URP 中的渲染器功能添加预构建效果]]
- 下一页：[[03-URP 中的自定义渲染通道工作流程]]
