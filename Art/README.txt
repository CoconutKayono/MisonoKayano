Dark Fairy Tale – Unity UGUI 独立素材

共 26 张独立 PNG（RGBA）。来源：第一张透明背景素材图；第二张说明图不作为直接裁切源。
按钮、标题、交互提示与道具提示面板的原始文字通过局部图像修复去除，可能保留轻微痕迹。提示面板的图标和装饰线仍保留。HP/MP 框由原图去除彩色槽及标签，Track 为根据原图明度重建的深色空槽。

Unity: Texture Type = Sprite (2D and UI); Sprite Mode = Single; Alpha Is Transparency = true; Mip Maps = off; Compression = None（初次检查时）。
血条蓝条：Frame、Track、Fill_Aligned 为相同 583x100 画布，可使用相同 RectTransform 尺寸与锚点叠放。顺序：Track -> Fill_Aligned -> Frame -> TMP Text。
如果使用 Image Type=Filled，Horizontal / Left，建议改用紧裁 Fill.png，按槽内实际尺寸定位；不要直接对带大量透明边距的 Fill_Aligned 使用 Filled，否则百分比表现不准确。
对于其他面板，按实际边饰设置 9-Slice；未制作或验证 Unity .meta 与 Border 参数。装饰边框不宜任意拉伸。所有素材为单独 PNG，没有合并图。
