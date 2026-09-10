# Unity UGUI 2.6 中文文档

本目录整理自 Unity 官方 UGUI 2.6 文档，包含基础 UI、布局、Canvas、可视组件、交互组件、动画集成、富文本和常用 HOWTO。文档中的菜单名、组件名、Inspector 字段名、API 和代码标识符保留英文，解释部分翻译为中文，便于与 Unity 编辑器和官方 API 对照。

## 文档目录

- [[UIAutoLayout-中文文档]]：布局元素、布局控制器、Layout Group、布局计算顺序和布局重建。
- [[UICanvas-中文文档]]：Canvas 绘制顺序、三种渲染模式、额外着色器通道和顶点颜色空间。
- [[UIBasicLayout-中文文档]]：Rect Tool、Rect Transform、Pivot、Anchors 和 Anchor Presets。
- [[UIVisualComponents-中文文档]]：Text、Image、Raw Image、Mask、Raycast Receiver 和 Effects。
- [[UIInteractionComponents-中文文档]]：Button、Toggle、Toggle Group、Slider、Scrollbar、Dropdown、Input Field 和 Scroll Rect。
- [[UIAnimationIntegration-中文文档]]：使用 Animator 为 UI 状态过渡制作动画。
- [[StyledText-中文文档]]：Unity Rich Text 标签、参数、颜色和 Editor GUI 用法。

## 布局组件

- [[LayoutElement-中文文档]]：覆盖布局元素的最小、首选和可伸缩尺寸。
- [[ContentSizeFitter-中文文档]]：让 Rect Transform 适配内容尺寸。
- [[AspectRatioFitter-中文文档]]：按宽高比调整 UI 元素尺寸。
- [[HorizontalLayoutGroup-中文文档]]：将子元素水平排列。
- [[VerticalLayoutGroup-中文文档]]：将子元素垂直排列。
- [[GridLayoutGroup-中文文档]]：将子元素排列为固定单元格网格。

## HOWTO

- [[WorldSpaceUI-中文文档]]：创建世界空间 UI。
- [[CreateUIFromScript-中文文档]]：通过脚本实例化和定位 UI 元素。
- [[ScreenTransitions-中文文档]]：使用 Animator 和状态机创建屏幕过渡。
- [[UIShaderGraph-中文文档]]：使用 Shader Graph 创建自定义 UI 效果。
- [[InfiniteScrollList-中文文档]]：使用 ScrollRect 和 UI 单元复用实现大数据量滚动列表。

## 结构与工程规范

- [[UGUIArchitecture-中文文档]]：Window、Widget、基础控件的职责划分、Prefab 层级、组件清单和命名规范。
- [[SceneTransformTools-中文文档]]：Unity Scene 视图中 Center、Pivot、Local 和 Global 的区别。

## 资源说明

页面引用的官方图片已统一保存到 [images](images) 目录，并将 UGUI 文档中的图片链接统一为 `images/文件名`。布局示例中的 `.gif` 文件保留原格式，以便在 Obsidian 中查看锚点变化动画。原有的 `图片` 目录保留不删除，以避免影响其他历史笔记。

## 来源

原始文档版本：`com.unity.ugui@2.6`。  
官方文档入口：[Unity UI 自动布局](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/UIAutoLayout.html)
