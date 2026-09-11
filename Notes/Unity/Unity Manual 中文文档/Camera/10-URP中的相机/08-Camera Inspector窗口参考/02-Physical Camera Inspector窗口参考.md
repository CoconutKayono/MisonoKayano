# Physical Camera Inspector 窗口参考

> 原文：[Physical Camera Inspector window reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras/physical-camera-reference.html)

Physical Camera 属性让 URP Camera 模拟真实相机。这些属性对应真实相机的功能，并以相同方式工作。有关如何使用这些属性创建所需 Camera effect 的信息，请参阅[[00-使用物理相机模拟真实相机|使用物理相机模拟真实相机]]。

> [!NOTE]
> 使用 Physical Camera 时，Unity 使用以下属性计算 Field of View：**Sensor Size**、**Focal Length** 和 **Shift**。

Physical Camera 属性分为以下部分：**Camera Body**、**Lens** 和 **Aperture Shape**。

## Camera Body

| 属性 | 说明 |
| --- | --- |
| **Sensor Type** | 指定 Camera 要模拟的真实相机格式。选择格式后，Unity 会自动将 **Sensor Size > X** 和 **Y** 设置为正确值。URP 提供以下预设：`8mm`（X `4.8`，Y `3.5`）、`Super 8mm`（X `5.79`，Y `4.01`）、`16mm`（X `10.26`，Y `7.49`）、`Super 16mm`（X `12.522`，Y `7.417`）、`35mm 2-perf`（X `21.95`，Y `9.35`）、`35mm Academy`（X `21.946`，Y `16.002`）、`Super–35`（X `24.89`，Y `18.66`）、`35mm TV Projection`（X `20.726`，Y `15.545`）、`35mm Full Aperture`（X `24.892`，Y `18.669`）、`35mm 1.85 Projection`（X `20.955`，Y `11.328`）、`35mm Anamorphic`（X `21.946`，Y `18.593`）、`65mm ALEXA`（X `54.12`，Y `25.59`）、`70mm`（X `52.476`，Y `23.012`）、`70mm IMAX`（X `70.41`，Y `52.63`）、`Custom`（手动设置 X 和 Y）。如果手动更改 Sensor Size，Unity 会自动将该属性设置为 `Custom`。 |
| **Sensor Size** | 设置 Camera sensor 的大小，单位为毫米。选择 Sensor Type 时 Unity 会自动设置 X 和 Y 值，也可以输入自定义值。**X** 是 sensor 的水平尺寸；**Y** 是 sensor 的垂直尺寸。 |
| **ISO** | Camera sensor 的感光度。 |
| **Shutter Speed** | Camera sensor 捕获光线的时间。**Unit** 可选择 `Second` 或 `1/Second`。 |
| **Gate Fit** | 更改 resolution gate（Game view 的大小/aspect ratio）相对于 film gate（Physical Camera sensor 的大小/aspect ratio）的尺寸。可选 **Vertical**、**Horizontal**、**Fill**、**Overscan** 和 **None**，具体含义参阅 [Gate Fit 简介](01-Gate%20Fit%20简介.md)。 |

## Lens

| 属性 | 说明 |
| --- | --- |
| **Focal Length** | Camera sensor 与 lens 之间的距离，单位为毫米。值越小，Field of View 越宽，反之亦然。更改该值时，Unity 会自动更新 Field of View。 |
| **Shift** | 将 lens 从中心水平或垂直移动。值是 sensor size 的倍数，例如沿 X 轴移动 `0.5` 会将 sensor 偏移其水平尺寸的一半。可以使用 lens shift 修正 Camera 与 subject 成角度时产生的 distortion（例如平行线汇聚），沿任一轴移动 lens 会使 Camera frustum 变为 oblique。**X** 是 lens 相对于 sensor 的水平偏移；**Y** 是垂直偏移。 |
| **Aperture** | lens 的 f-stop（f-number）。值越低，lens aperture 越宽。 |
| **Focus Distance** | 启用 Depth of Field 时，对象显示清晰的距离。使用 Physical Camera 属性和 Depth of Field post-processing 时，Lens 属性会直接影响 Depth of Field effect，需要同时调整两者以创建所需效果。 |

## Aperture Shape

| 属性 | 说明 |
| --- | --- |
| **Blade Count** | lens aperture 的 blade 数量。值越高，aperture 形状越圆。 |
| **Curvature** | lens aperture blade 的曲率。 |
| **Barrel Clipping** | lens 的自遮挡。值越高，cat’s eye effect 越明显。 |
| **Anamorphism** | Camera sensor 的垂直拉伸量，使 sensor 变高或变矮。值越高，sensor 拉伸越明显，可模拟 anamorphic 外观。 |

---

## 文档导航

- 上一页：[[01-Camera Inspector窗口参考]]
- 目录：[[00-Camera Inspector窗口参考]]
- 下一页：[[00-Built-In Render Pipeline中的相机]]
