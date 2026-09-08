# Aseprite 功能支持（Aseprite Features）

> 来源：[Unity Package 官方文档 · Aseprite Features](https://docs.unity3d.com/Packages/com.unity.2d.aseprite@6.0/manual/AsepriteFeatures)

本页说明 Aseprite Importer 支持哪些 Aseprite 功能、不支持哪些功能。

## 支持的功能

### 文件格式

- `.ase` 与 `.aseprite`
- 颜色模式（支持所有模式）：
  - RGBA
  - 灰度（Grayscale）
  - 索引色（Indexed）

### 图层设置

- **可见/隐藏图层**

  默认不导入隐藏图层。可在导入设置中勾选 **Include hidden layers**（包含隐藏图层）来改变这一行为。

- **图层混合模式**

  使用导入模式 **Merge frames**（合并帧）时支持所有混合模式。

- **图层与单元（Cell）的不透明度**
- **关联单元（Linked Cells）**
- **标签（Tags）**

  仅支持动画方向（Animation Direction）为 **Forward**（正向）。

  重复（repeat）字段的值在导入时只有两种结果：

  - `∞` 会生成循环播放的 Animation Clip。这是 Aseprite 中所有标签的默认值。
  - `1 -> N` 会生成非循环的 Animation Clip。

- [单个帧时长](https://www.aseprite.org/docs/frame-duration/)
- [图层组](https://www.aseprite.org/docs/layer-group/)

  - 导入器会尊重为组选择的可见性模式。如果组被隐藏，默认不会导入其底层图层。
  - 如果导入模式设置为 **Individual layers**（独立图层），会在预制件层级中生成图层组。

### 用户数据（User data）

单元中的用户数据字段可用于向生成的 Animation Clip 注入事件。更多信息请阅读[这里](https://docs.unity3d.com/Packages/com.unity.2d.aseprite@6.0/manual/ImporterFAQ.html#how-to-add-events-to-animation-clips)。

### 其他

- [Tilemap（瓦片地图）](https://www.aseprite.org/docs/tilemap/)

  导入瓦片数据时，请选择 **Import Mode: Tile Set**（导入模式：瓦片集）。这会告诉 Unity 为每个 Aseprite 瓦片生成 [Tile 资源](https://docs.unity3d.com/Manual/Tilemap-TileAsset.html)，并生成一个 [Tile Palette](https://docs.unity3d.com/Manual/Tilemap-Palette.html) 来统一存放它们。

  Aseprite Importer 只支持尺寸相同的瓦片集。如果导入的 Aseprite 文件包含多种不同尺寸的瓦片集，将使用第一个瓦片集来设置 Unity 内的瓦片尺寸。

## 不支持的功能

- [Slices（切片）](https://www.aseprite.org/docs/slices/)

## 修改生成的 Animator Controller

如果 Aseprite 文件包含多个帧，并且导入器中的 [Import Mode](https://docs.unity3d.com/Packages/com.unity.2d.aseprite@6.0/manual/ImporterFeatures#general) 设置为 **Animated Sprite**、且勾选了 **Animation Clip** 复选框，Aseprite Importer 会生成一个 Animator Controller。此 Animator Controller 是只读的，意味着无法更改。要修改 Animator Controller，请参阅[导入器 FAQ](https://docs.unity3d.com/Packages/com.unity.2d.aseprite@6.0/manual/ImporterFAQ#how-to-make-changes-to-an-animator-controller)。
