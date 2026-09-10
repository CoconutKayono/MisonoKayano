# Canvas

> 来源：[Unity UGUI 2.6 — Canvas](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/UICanvas.html)  
> 官方源文件：[uGUI/Documentation~/UICanvas.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/UICanvas.md)  
> 整理日期：2026-09-05

Canvas 是所有 UI 元素应当放置的区域。Canvas 是带 Canvas 组件的 GameObject，所有 UI 元素都必须是某个 Canvas 的子对象。

通过菜单 **GameObject > UI（Canvas）> Image** 创建新的 UI 元素时，如果场景中还没有 Canvas，Unity 会自动创建一个 Canvas，并将新元素创建为它的子对象。Canvas 区域会在 Scene View 中显示为一个矩形，因此即使不一直打开 Game View，也可以方便地定位 UI 元素。

Canvas 使用 EventSystem 对象来协助消息系统工作。

## 元素的绘制顺序

Canvas 中的 UI 元素会按照它们在 Hierarchy 中出现的顺序绘制：第一个子元素先绘制，第二个子元素随后绘制，依此类推。如果两个 UI 元素重叠，后绘制的元素会显示在先绘制的元素上方。

要改变元素的前后关系，可以在 Hierarchy 中拖动并重新排序。也可以通过 Transform 组件的以下方法用脚本控制顺序：

- `SetAsFirstSibling`
- `SetAsLastSibling`
- `SetSiblingIndex`

## 渲染模式

Canvas 的 **Render Mode** 设置决定它是在屏幕空间还是世界空间中渲染。

### Screen Space - Overlay（屏幕空间 - 覆盖）

该模式将 UI 元素渲染在屏幕上，并覆盖在场景之上。屏幕尺寸或分辨率发生变化时，Canvas 会自动调整大小以匹配屏幕。

![屏幕空间覆盖模式中的 UI](GUI_Canvas_Screenspace_Overlay.png)

### Screen Space - Camera（屏幕空间 - 摄像机）

该模式与 Screen Space - Overlay 类似，但 Canvas 会放置在指定 Camera 前方的给定距离处。UI 元素由这台摄像机渲染，因此摄像机设置会影响 UI 的外观。

如果 Camera 设置为 **Perspective**，UI 元素会以透视方式渲染，透视畸变程度可以由 Camera 的 **Field of View** 控制。屏幕尺寸、分辨率或摄像机视锥发生变化时，Canvas 也会自动调整大小以匹配。

![屏幕空间摄像机模式中的 UI](GUI_Canvas_Screenspace_Camera.png)

### World Space（世界空间）

在该模式中，Canvas 的行为与场景中的普通对象相同。可以通过 Rect Transform 手动设置 Canvas 的大小，UI 元素会根据它们在 3D 空间中的位置显示在其他对象前方或后方。

这种模式适合 UI 本身就是世界一部分的场景，也称为“叙事内界面”（diegetic interface）。

![世界空间 Canvas](GUI_Canvas_Worldspace.png)

## Additional Shader Channels（额外着色器通道）

Canvas 为渲染生成网格几何体时，始终会包含 `Position`、`Color` 和 `UV0` 顶点属性。在 **Screen Space - Camera** 和 **World Space** 渲染模式下，默认还会包含 `Normal` 和 `Tangent`，用于支持光照。

**Additional Shader Channels** 属性用于在默认属性之外加入额外顶点属性。当 UI 着色器需要采样额外 UV 集，或覆盖模式 Canvas 需要每顶点法线和切线数据时，这一属性很有用。

| 通道 | 说明 |
| --- | --- |
| None | 不添加额外属性，只包含默认属性。 |
| TexCoord1 | 为每个顶点添加第二组 UV，即 UV1。 |
| TexCoord2 | 为每个顶点添加第三组 UV，即 UV2。 |
| TexCoord3 | 为每个顶点添加第四组 UV，即 UV3。 |
| Normal | 添加每顶点法线（Vector3），UI 几何体使用光照效果时需要。 |
| Tangent | 添加每顶点切线（Vector4），使用法线贴图着色器时需要。 |

Screen Space - Overlay Canvas 不受标准场景光照影响，因此在典型场景中 `Normal` 和 `Tangent` 不会产生可见效果。不过，TextMeshPro 等专用着色器仍然可以使用这些数据。

## Reflection Probes（反射探针）

在 Canvas 上启用 **Use Reflection Probes** 时，无论 Additional Shader Channels 设置如何，`Normal` 通道都会自动包含在网格中。

## Vertex Color Always in Gamma Color Space

在 Linear 颜色空间项目中，Unity 通常会在网格生成期间将 UI 顶点颜色从 Gamma 转换为 Linear，然后再传给着色器。这个转换可能损失细节，尤其是较暗的颜色，因为 Gamma 编码在暗部提供了更高的精度。

启用 **Vertex Color Always in Gamma Color Space** 后，顶点颜色会以 Gamma 空间写入网格，UI 着色器再使用浮点运算执行 Gamma 到 Linear 的转换，从而在整个流程中保留更多精度。这能改善 Linear 工作流中暗色调和细微渐变的准确性。

该精度提升只在项目颜色空间设置为 **Linear** 时有意义，路径为 **Project Settings > Player**。在 Gamma 颜色空间项目中，该设置没有效果。

## Custom UI Shader（自定义 UI 着色器）

内置 UI 着色器已经包含此功能所需的 Gamma 到 Linear 转换。如果使用自定义 UI 着色器，则必须在启用该设置时手动处理转换，否则顶点颜色可能显示得过亮。

