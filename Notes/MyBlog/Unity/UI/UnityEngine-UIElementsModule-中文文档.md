# UnityEngine.UIElementsModule（脚本 API 参考）

## 描述（Description）

UIElements 模块实现了 UIElements 保留模式（retained mode）UI 框架。

> 说明：本文档为 UIElements 模块的 API 索引。条目名称保留英文原名，描述已翻译为中文；技术术语（VisualElement、UXML、USS、Panel 等）按惯例保留英文。

## 类（Classes）

| 类 | 描述 |
| --- | --- |
| AbstractBaseField | 字段控件的非泛型抽象基类。 |
| AbstractGenericMenu | 菜单功能的基类。 |
| AbstractProgressBar | ProgressBar 的抽象基类。 |
| AlignmentUtils | 包含用于对齐视觉元素（visual element）的工具方法的静态类。 |
| AttachToPanelEvent | 元素被添加到作为面板（panel）后代的元素上之后发送的事件。 |
| BackgroundPropertyHelper | 用于在背景属性与 ScaleMode 之间转换的辅助类。 |
| BaseBoolField | BaseBoolField 是一个可点击、表示布尔值的元素。 |
| BaseCompositeField<T0,T1,T2> | 复合字段（composite field）的基类。 |
| BaseField<T0> | 控件的抽象基类。BaseField 是 TextField、IntegerField 等字段元素的基类。若要自动让 BaseField 元素与 Inspector 窗口中的其他字段对齐，请使用 `.unity-base-field__aligned` USS 类。该样式类专为 Inspector 元素（如 PropertyField，默认带有该类）设计。不过，如果你手动向 PropertyField 添加子 BaseField 元素，则必须手动添加该样式类。存在该样式类时，字段会自动计算标签宽度，以与 Inspector 窗口中的其他字段对齐。如果存在 IMGUI 字段，UI Toolkit 字段也会与它们对齐，以保持一致性和兼容性。 |
| BaseFieldMouseDragger | 字段鼠标拖拽器（mouse dragger）的基类。 |
| BaseListView | 列表视图（list view）的基类；列表视图是一个纵向可滚动区域，与项目列表相关联并显示它们。 |
| BaseListViewController | 集合列表视图控制器基类。此类视图控制器负责处理任何 BaseListView 继承者虚拟化的数据。 |
| BaseMask64Field | 允许用户从一个选项列表中选择一个或多个选项的控件。 |
| BaseMaskField<T0> | 实现编辑位掩码（bit mask）值共享功能的基类。更多信息请参阅 UXML 元素 MaskField。 |
| BasePopupField<T0,T1> | 所有弹窗字段（popup field）元素的基类。TValue 与 TChoice 可以不同（参见 MaskField），也可以相同（参见 PopupField）。 |
| BaseSlider<T0> | Slider 字段的基类。 |
| BaseTreeView | 树视图（tree view）的基类；树视图是一个纵向可滚动区域，以树形结构组织并显示项目列表。 |
| BaseTreeViewController | 集合树视图控制器基类。此类视图控制器负责处理任何 BaseTreeView 继承者虚拟化的数据。 |
| BaseVerticalCollectionView | 在滚动视图中显示虚拟化垂直内容控件的基类。 |
| BindableElement | 可以绑定到属性的元素。更多信息请参阅 UXML 元素 BindableElement。 |
| Binding | 定义绑定的基类。 |
| BlurEvent | 元素失去焦点后立即发送的事件。该事件向下传递（trickle down），不会冒泡（bubble up）。 |
| BoundsField | Bounds 编辑字段。更多信息请参阅 UXML 元素 BoundsField。 |
| BoundsIntField | BoundsInt 字段。更多信息请参阅 UXML 元素 BoundsIntField。 |
| Box | 与 IMGUI Box 样式匹配的样式化视觉元素。更多信息请参阅 UXML 元素 Box。 |
| Button | 表示可交互的 UI 按钮元素。 |
| CallbackEventHandler | 能够拥有回调来处理事件的类的接口。 |
| ChangeEvent<T0> | 当字段中的值发生变化时发送事件。 |
| Clickable | 跟踪元素上的指针事件并在元素被点击时回调的操纵器（manipulator）。 |
| ClickEvent | 当点击鼠标左键时发送此事件。 |
| CollectionViewController | 集合视图控制器基类。视图控制器负责处理任何 BaseVerticalCollectionView 继承者虚拟化的数据。 |
| Column | 表示多列视图（如多列列表视图或多列树视图）中的一列。提供用于定义用户如何与多列视图中的列交互、该列的数据及其单元格数据如何表示的属性。 |
| Columns | 表示列的集合。 |
| CommandEventBase<T0> | 命令事件的基类。 |
| ContextClickEvent | 点击鼠标右键时发送的事件。 |
| ContextualMenuManager | 使用此类显示上下文菜单（contextual menu）。 |
| ContextualMenuManipulator | 当用户点击鼠标右键或按下键盘上的菜单键时，显示上下文菜单的操纵器。 |
| ContextualMenuPopulateEvent | 当上下文菜单需要菜单项时发送的事件。该事件向下传递并向上冒泡。 |
| ConverterGroup | 保存用于绑定上的本地转换注册表信息的类型。 |
| ConverterGroups | 提供一组注册和使用转换组的静态方法，并注册一组全局转换器。ConverterGroup。DataBinding。 |
| CustomBinding | 通用绑定扩展性的基类。 |
| CustomStyleResolvedEvent | 在 VisualElement 的自定义样式属性解析完成后发送的事件。 |
| DataBinding | 实现数据源属性与 VisualElement 属性之间数据同步的绑定类型。 |
| DefaultMultiColumnTreeViewController<T0> | MultiColumnTreeViewController 的默认实现。 |
| DefaultTreeViewController<T0> | TreeViewController 的默认实现。 |
| DetachFromPanelEvent | 当元素从父级分离之前发送的事件，前提是父级是面板的后代。 |
| DoubleField | 创建用于输入 double 的文本字段。 |
| DragAndDropData | 拖放（drag-and-drop）操作期间存储的数据，使信息能够在整个过程中传递。 |
| DragAndDropEventBase<T0> | 拖放事件的基类。 |
| DragEnterEvent | 使用 DragEnterEvent 类管理拖拽进入元素或其一个后代时发生的事件。DragEnterEvent 不向下传递，也不向上冒泡。 |
| DragExitedEvent | 拖放过程结束时发送给被拖拽元素的事件。 |
| DragLeaveEvent | 使用 DragLeaveEvent 类管理拖拽离开元素或其一个后代时发送的事件。DragLeaveEvent 不向下传递，也不向上冒泡。 |
| DragPerformEvent | 当另一个元素被拖拽并放置到该元素上时，发送给该元素的事件。 |
| DragUpdatedEvent | 当被拖拽的元素进入可能的放置目标（drop target）时发送的事件。 |
| DropdownField | 允许用户从选项列表中选择一项的控件。更多信息请参阅 UXML 元素 DropdownField。 |
| DropdownMenu | 表示一个下拉菜单，类似于大多数操作系统（OS）和 Unity 编辑器中常见的菜单。 |
| DropdownMenuAction | 表示一个菜单动作项。 |
| DropdownMenuEventInfo | 提供导致下拉菜单显示的事件的信息。 |
| DropdownMenuItem | 表示下拉菜单中的一个项。 |
| DropdownMenuSeparator | 提供分隔符菜单项。 |
| DynamicAtlasSettings | 包含动态图集（dynamic atlas）系统使用的设置。 |
| Easing | 与 ValueAnimation 一起使用的缓动曲线（easing curve）集合。 |
| EnumField | 创建用于在枚举值之间切换的下拉框。更多信息请参阅 UXML 元素 EnumField。 |
| EventArg | 所有 EventArg<T0> 实例的基类。 |
| EventArg<T0> | 类型为 TArg 的事件回调参数的可复用标识符。 |
| EventBase | 所有 UIElements 事件的基类。该类实现 IDisposable，以确保必要时从池中正确释放事件以及任何非托管资源。 |
| EventBase<T0> | 事件的泛型基类，实现事件池（event pooling）以及自动注册到事件类型系统。 |
| EventCallback | 允许创建 EventCallbackDefinition 与 EventCallbackDefinition<T0> 实例的静态类。 |
| EventDispatcher | 将事件分派（dispatch）到 IPanel。 |
| EventInterestAttribute | 用于 CallbackEventHandler.HandleEventBubbleUp 和 CallbackEventHandler.HandleEventTrickleDown 覆盖的可选特性。使用该特性可以指定方法覆盖使用的所有事件类型。这样，事件分发器可以在内部将这些方法识别为性能优化的有效候选者时，安全地跳过其不需要的事件。 |
| ExecuteCommandEvent | 当面板中的元素应执行命令时，由编辑器发送此事件。 |
| FieldMouseDragger<T0> | 在视觉元素上提供拖拽以改变值字段。 |
| FilterFunctionDefinition | 表示保存过滤器参数与效果的过滤器函数定义。 |
| FloatField | 创建用于输入 float 的文本字段。更多信息请参阅 UXML 元素 FloatField。 |
| Focusable | 可以获取焦点的对象的基类。 |
| FocusChangeDirection | 定义焦点环（focus ring）中焦点移动方向的基类。 |
| FocusController | 负责管理 Panel 内焦点的类。 |
| FocusEvent | 元素获得焦点后立即发送的事件。该事件向下传递，不会冒泡。 |
| FocusEventBase<T0> | 焦点相关事件的基类。 |
| FocusInEvent | 元素获得焦点之前立即发送的事件。该事件向下传递并向上冒泡。 |
| FocusOutEvent | 元素失去焦点之前立即发送的事件。该事件向下传递并向上冒泡。 |
| Foldout | Foldout 控件是用户界面中可折叠的部分。切换时，它会展开或折叠，从而隐藏或显示其包含的元素。 |
| GenericDropdownMenu | GenericDropdownMenu 允许你显示带默认文本选项或任意 VisualElement 的上下文菜单。 |
| GeometryChangedEvent | 布局计算之后，当元素的位置或尺寸发生变化时发送此事件。 |
| GroupBox | 这是一组 UIElements.IGroupBoxOption 的封闭容器。该容器内的所有组选项会相互作用，允许单选，使用 UIElements.DefaultGroupManager。默认选项是 RadioButton，但用户可以提供其他实现。如果在层级中找不到 UIElements.IGroupBox，默认容器将是面板。 |
| GUIDField | 创建用于编辑 GUID 的字段。 |
| Hash128Field | 创建用于编辑 Hash128 的字段。更多信息请参阅 UXML 元素 Hash128Field。 |
| HelpBox | 创建向用户显示消息的帮助框。更多信息请参阅 UXML 元素 HelpBox。 |
| IBindingExtensions | 提供额外 IBindable 功能的扩展方法。 |
| Image | 表示源纹理的 VisualElement。 |
| IMGUIContainer | 在编辑器中绘制 IMGUI 内容的元素。更多信息请参阅 UXML 元素 IMGUIContainer。 |
| IMGUIEvent | 用于发送没有对应 UIElements 事件的 IMGUI 事件的类。 |
| ImmediateModeElement | 可以实现自定义立即模式（immediate mode）渲染的 VisualElement。 |
| INotifyValueChangedExtensions | 一组对实现 INotifyValueChanged<T0> 的对象有用的扩展方法。 |
| InputEvent | 当 TextField 中的文本发生变化时发送事件。 |
| IntegerField | 创建用于输入整数的文本字段。更多信息请参阅 UXML 元素 LongField。 |
| KeyboardEventBase<T0> | 键盘事件的基类。 |
| KeyboardNavigationManipulator | 提供默认实现，将特定输入设备事件转换为通常可以用键盘完成的高级导航操作。 |
| KeyDownEvent | 按下按键时发送此事件。 |
| KeyUpEvent | 释放按下的按键时发送此事件。 |
| Label | 提供显示文本的元素。更多信息请参阅 UXML 元素 Label。 |
| ListView | ListView 是一个纵向可滚动区域，与项目列表相关联并显示它们。 |
| ListViewController | 列表视图控制器。此类视图控制器负责处理任何 ListView 继承者虚拟化的数据。 |
| LongField | 创建用于输入长整数的文本字段。更多信息请参阅 UXML 元素 LongField。 |
| Manipulator | 所有 Manipulator 实现的基类。 |
| Mask64Field | Mask64Field 是允许用户从 64 位掩码选项列表中选择一个或多个选项的控件。 |
| MaskField | MaskField 是允许用户从选项列表中选择一个或多个选项的控件。更多信息请参阅 UXML 元素 MaskField。 |
| MeshGenerationContext | 提供在 VisualElement.generateVisualContent 回调期间生成视觉元素视觉内容的方法。 |
| MeshWriteData | 表示分配用于绘制 VisualElement 内容的顶点和索引数据。 |
| MinMaxSlider | 包含范围表示的最小/最大滑块。更多信息请参阅 UXML 元素 MinMaxSlider。 |
| MouseCaptureController | 管理鼠标事件捕获的类。 |
| MouseCaptureEvent | 处理器开始捕获鼠标后发送的事件。 |
| MouseCaptureEventBase<T0> | 捕获鼠标的处理器发生变化时发送的事件。 |
| MouseCaptureOutEvent | 处理器停止捕获鼠标之前发送的事件。 |
| MouseDownEvent | 按下鼠标按钮时发送此事件。 |
| MouseEnterEvent | 鼠标指针进入元素或其一个后代元素时发送的事件。该事件向下传递，但不会冒泡。 |
| MouseEnterWindowEvent | 鼠标指针进入窗口时发送的事件。该事件向上冒泡，但不会向下传递。 |
| MouseEventBase<T0> | 鼠标事件的基类。 |
| MouseLeaveEvent | 鼠标指针退出元素及其所有后代元素时发送的事件。该事件向下传递，但不会冒泡。 |
| MouseLeaveWindowEvent | 鼠标指针退出窗口时发送的事件。该事件向上冒泡，但不会向下传递。 |
| MouseManipulator | MouseManipulator 有一组激活过滤器（activation filter）。 |
| MouseMoveEvent | 鼠标移动时发送此事件。 |
| MouseOutEvent | 鼠标指针退出元素时发送的事件。该事件向下传递并向上冒泡。 |
| MouseOverEvent | 鼠标指针进入元素时发送的事件。该事件向下传递并向上冒泡。 |
| MouseUpEvent | 释放鼠标按钮时发送此事件。 |
| MultiColumnController | 多列视图的默认控制器。负责添加 MultiColumnCollectionHeader 并响应各种回调。 |
| MultiColumnListView | 支持多列的列表视图。更多信息请参阅 MultiColumnListView。 |
| MultiColumnListViewController | 多列列表视图控制器。此类视图控制器负责处理任何 MultiColumnListView 继承者虚拟化的数据。 |
| MultiColumnTreeView | 支持多列的树视图。更多信息请参阅 MultiColumnTreeView。 |
| MultiColumnTreeViewController | 多列树视图控制器。此类视图控制器负责处理任何 MultiColumnTreeView 继承者虚拟化的数据。 |
| NavigationCancelEvent | 用户按下取消按钮时发送的事件。 |
| NavigationEventBase<T0> | 导航事件抽象基类。默认情况下，导航事件向下传递并向上冒泡。禁用的元素不会收到这些事件。 |
| NavigationMoveEvent | 通常在用户按下方向键（D-pad）、移动摇杆或按下箭头键时发送的事件。 |
| NavigationSubmitEvent | 用户按下提交按钮时发送的事件。 |
| Painter2D | 用于绘制 2D 矢量图形的对象。 |
| PanelChangedEventBase<T0> | 通知面板变化的事件的抽象基类。 |
| PanelExtensions | 为 Panel 工具提供扩展方法。 |
| PanelInputConfiguration | 配置运行时输入如何路由到 Panel。如果没有激活的输入配置组件，则使用默认配置。 |
| PanelRenderer | 定义将 VisualElement 连接到 GameObject 的组件。 |
| PanelSettings | 定义在运行时实例化面板的 Panel Settings 资源。该面板使 Unity 能够在 Game 视图中显示基于 UXML 文件的 UI。 |
| PanelTextSettings | 表示特定 UI 面板的文本渲染设置。PanelSettings.textSettings。 |
| PointerCancelEvent | 指针交互被取消时发送此事件。 |
| PointerCaptureEvent | 指针被 VisualElement 捕获时发送的事件。 |
| PointerCaptureEventBase<T0> | 指针捕获事件和鼠标捕获事件的基类。 |
| PointerCaptureHelper | 用于捕获和释放指针的静态类。 |
| PointerCaptureOutEvent | VisualElement 释放指针时发送的事件。 |
| PointerDownEvent | 指针在视觉元素内按下时发送。 |
| PointerDownLinkTagEvent | 指针在链接标签（Link tag）上按下时发送此事件。 |
| PointerEnterEvent | 指针进入 VisualElement 或其一个后代时发送此事件。该事件不向下传递，也不向上冒泡。 |
| PointerEventBase<T0> | 所有指针相关事件的基类。 |
| PointerId | 保存指针 ID 值的静态类。 |
| PointerLeaveEvent | 指针退出元素及其所有后代时发送此事件。该事件不向下传递，也不向上冒泡。 |
| PointerManipulator | PointerManipulator 有一组激活过滤器。 |
| PointerMoveEvent | 指针状态发生变化时发送此事件。 |
| PointerMoveLinkTagEvent | 指针在链接标签上状态发生变化时发送此事件。 |
| PointerOutEvent | 指针退出元素时发送此事件。该事件向下传递并向上冒泡。 |
| PointerOutLinkTagEvent | 指针退出链接标签时发送此事件。 |
| PointerOverEvent | 指针进入元素时发送此事件。该事件向下传递并向上冒泡。 |
| PointerOverLinkTagEvent | 指针进入链接标签时发送此事件。 |
| PointerType | 保存指针类型值的静态类。 |
| PointerUpEvent | 指针的最后一个按下的按钮被释放时发送此事件。 |
| PointerUpLinkTagEvent | 指针的最后一个按下的按钮在链接标签上被释放时发送此事件。 |
| PopupField<T0> | 通用弹窗选择字段。 |
| PopupWindow | 样式化的视觉文本元素。该元素没有任何功能。它只是一个带边框和标题的容器，而不是窗口或弹窗。更多信息请参阅 UXML 元素 PopupWindow。 |
| ProgressBar | 显示下界与上界值之间进度的控件。更多信息请参阅 UXML 元素 ProgressBar。 |
| RadioButton | 允许用户在 RadioButtonGroup 内选择单个选项的控件。更多信息请参阅 UXML 元素 RadioButton。 |
| RadioButtonGroup | 允许在逻辑上为一组的 RadioButton 元素中进行单选。选择其中一个会取消选择其他。更多信息请参阅 UXML 元素 RadioButtonGroup。 |
| RectField | Rect 字段。更多信息请参阅 UXML 元素 RectField。 |
| RectIntField | RectInt 字段。更多信息请参阅 UXML 元素 RectIntField。 |
| RegisterUxmlCacheAttribute | 允许 UXML 注册表更高效地检索 UXML 描述数据的特性。 |
| RepeatButton | 按下期间重复执行动作的按钮。更多信息请参阅 UXML 元素 RepeatButton。 |
| RuntimePanelUtils | 提供简单的世界、屏幕和面板坐标转换的静态方法集合。 |
| Scroller | 垂直或水平滚动条。更多信息请参阅 UXML 元素 Scroller。 |
| ScrollView | 在可滚动框架内显示其内容。更多信息请参阅 ScrollView 用户手册页面。 |
| Slider | 包含浮点值的滑块。 |
| SliderInt | 包含整数离散值的滑块。更多信息请参阅 UXML 元素 SliderInt。 |
| SortColumnDescription | 表示按哪个列排序以及以何种顺序排序的描述。 |
| SortColumnDescriptions | 表示多 SortColumnDescription 视图中的 SortColumnDescriptions 集合。 |
| StyleSheet | 样式表应用于视觉元素，以控制用户界面的布局和视觉外观。 |
| Tab | 创建用于在不同页面（screens）上组织内容的标签页。 |
| TabView | 创建一个分组一个或多个 Tab 元素的标签视图。 |
| TemplateContainer | 表示 UXML 文件的根 VisualElement。 |
| TextElement | 如果要声明显示文本的自定义 VisualElement，请将其用作超类。例如，Button 或 Label 以它作为基类。更多信息请参阅 UXML 元素 TextElement。 |
| TextField | TextField 接受并显示文本输入。更多信息请参阅 UXML 元素 TextField。 |
| TextInputBaseField<T0> | 所有基于文本的字段使用的抽象基类。 |
| TextValueField<T0> | 文本字段的基类。 |
| ThemeStyleSheet | 表示由其他样式表组装而成的样式表。 |
| Toggle | Toggle 是可点击、表示布尔值的元素。 |
| ToggleButtonGroup | 允许在逻辑上为一组的 Button 元素中进行单选或多选的控件。 |
| ToggleButtonGroupStatePropertiesAttribute | 定义序列化的 ToggleButtonGroupState 在 Inspector 中如何初始化。 |
| TooltipEvent | 发送事件以查找第一个显示工具提示（tooltip）的 VisualElement。 |
| TransitionCancelEvent | 过渡被取消时发送的事件。 |
| TransitionEndEvent | 过渡完成时发送的事件。如果在完成之前移除过渡，则不会触发该事件。 |
| TransitionEventBase<T0> | 过渡事件抽象基类。 |
| TransitionRunEvent | 创建过渡（即添加到正在运行的过渡集合中）时发送的事件。 |
| TransitionStartEvent | 过渡的延迟阶段结束时发送的事件。 |
| TreeView | TreeView 是一个纵向可滚动区域，以树形结构组织并显示项目列表。 |
| TreeViewController | 树视图控制器。此类视图控制器负责处理任何 TreeView 继承者虚拟化的数据。 |
| TreeViewExpansionChangedArgs | 树视图项目展开事件的数据结构。 |
| TwoPaneSplitView | 包含两个可调整大小窗格的 SplitView。一个窗格固定大小，另一个窗格设置了 flex-grow 样式为 1 以占据所有剩余空间。窗格之间的边框可拖动以调整两个窗格的大小。支持水平与垂直两种模式。要运行需要恰好两个子元素。 |
| UIAnimationClip | 用于为 VisualElement 层级设置动画的资源。 |
| UIDocument | 定义将 VisualElements 连接到 GameObjects 的组件。 |
| UIRenderer | 应添加到 UIDocument 组件旁边的渲染器组件，以允许世界空间渲染。当 PanelSettings 资源配置为世界空间时，UIDocument 会自动添加此组件。 |
| UnsignedIntegerField | 创建用于输入无符号整数的文本字段。更多信息请参阅 UXML 元素 UnsignedIntegerField。 |
| UnsignedLongField | 创建用于输入无符号长整数的文本字段。更多信息请参阅 UXML 元素 UnsignedLongField。 |
| UQuery | UQuery 是一组扩展方法，允许你在复杂层级中选择单个或一组 visualElement。更多信息请参阅 UQuery 手册页面。 |
| UQueryExtensions | UQuery 是一组扩展方法，允许你在复杂层级中选择单个或一组 visualElement。更多信息请参阅“使用 UQuery 查找视觉元素”。 |
| UxmlAttributeAttribute | 声明字段或属性与 UXML 特性关联。便捷重载，是 Query<T>.Build().First() 的简写。 |
| UxmlChildElementDescription | 描述元素允许的子元素。 |
| UxmlCreateInstanceMethodAttribute | 声明用于代替默认构造函数创建实例的方法。 |
| UxmlDescriptionCache | 包含关于 UXML 特性描述的预处理信息，以避免依赖反射（reflection）。 |
| UxmlElementAttribute | 声明自定义控件。 |
| UxmlEnumeration | 将特性的值限制为从值列表中选择。 |
| UxmlIgnoreAttribute | 用于已序列化但不来自 UXML 数据的字段，例如 UIElements.UxmlSerializedData._uxmlAssetId。 |
| UxmlObjectAttribute | 声明一个类可以从 UXML 实例化并包含 UXML 特性。UxmlSerializedData 包含一个生成的 UxmlSerializedData.CreateInstance 方法，该方法使用默认构造函数。你可以使用 UxmlCreateInstanceMethodAttribute 替换默认行为并提供自己的创建方法。 |
| UxmlObjectReferenceAttribute | 声明字段或属性与嵌套的 UXML 对象关联。 |
| UxmlSerializedData | 在自定义控件中使用 UxmlElementAttribute 时，生成声明元素的实例。 |
| UxmlSerializedDataUtility | 当自定义控件使用 UxmlElementAttribute 时，由代码生成器使用。 |
| UxmlTypeReferenceAttribute | 应用于具有 UxmlAttributeAttribute 特性的 Type 字段或属性时，提供预期类型的信息。 |
| UxmlTypeRestriction | 限制特性值的基类。 |
| UxmlValueBounds | 将特性的值限制在指定范围内。 |
| UxmlValueMatches | 将特性的值限制为匹配正则表达式。 |
| ValidateCommandEvent | 当编辑器确定面板中的元素是否会处理命令时发送此事件。 |
| ValueAnimation<T0> | 过渡动画的实现对象。 |
| Vector2Field | Vector2 字段。更多信息请参阅 UXML 元素 Vector2Field。 |
| Vector2IntField | Vector2Int 字段。更多信息请参阅 UXML 元素 Vector2IntField。 |
| Vector3Field | Vector3 字段。更多信息请参阅 UXML 元素 Vector3Field。 |
| Vector3IntField | Vector3Int 字段。更多信息请参阅 UXML 元素 Vector3IntField。 |
| Vector4Field | Vector4 字段。更多信息请参阅 UXML 元素 Vector4Field。 |
| VectorImage | 表示矢量图像的资源。 |
| VisualElement | 属于 UIElements 视觉树（visual tree）一部分的对象的基类。 |
| VisualElementAssetReferenceTable | 将创作 ID 路径映射到 VisualElement 的引用表。 |
| VisualElementCaptureExtensions | 使用这些扩展方法将 VisualElement 的渲染视觉内容捕获到 RenderTexture 中。 |
| VisualElementExtensions | 对 VisualElement 有用的一组扩展方法。 |
| VisualElementFocusChangeDirection | 定义 VisualElementFocusRing 的焦点更改方向。 |
| VisualElementFocusRing | 线性焦点环的实现。元素按其 focusIndex 排序。 |
| VisualElementReference | 表示 PanelRenderer 中对 VisualElement 的引用。 |
| VisualElementReference<T0> | 表示 PanelRenderer 中对 VisualElement 的强类型引用。 |
| VisualTreeAsset | 该类的实例保存由 UXML 文件创建的 VisualElementAsset 树。文件中的每个节点对应一个 VisualElementAsset。你可以克隆 VisualTreeAsset 来创建 VisualElement 树。注意：不能在运行时从原始 UXML 生成 VisualTreeAsset。 |
| WheelEvent | 鼠标滚轮移动时发送此事件。 |

## 结构体（Structs）

| 结构体 | 描述 |
| --- | --- |
| Angle | 表示角度值。 |
| AnimationIterationCount | 表示动画重复的次数，由 animation-iteration-count 样式属性使用。计数可以是有限的迭代次数或 AnimationIterationCount.Infinite。 |
| AuthoringIdPath | 表示用于标识 VisualElement 的创作 ID 路径的结构体。 |
| Background | 描述 VisualElement 的背景。 |
| BackgroundGradient | 可用作 Background 的颜色渐变，对应 CSS 的 linear-gradient() / radial-gradient() 函数。 |
| BackgroundGradientStop | BackgroundGradient 中的单个颜色停止点（color stop）。 |
| BackgroundPosition | VisualElement background-position 样式属性 IStyle.backgroundPositionX 和 IStyle.backgroundPositionY 的脚本接口。 |
| BackgroundRepeat | VisualElement background-repeat 样式属性 IStyle.backgroundRepeat 的脚本接口。 |
| BackgroundSize | VisualElement background-size 样式属性 IStyle.backgroundSize 的脚本接口。 |
| BindablePropertyChangedEventArgs | 提供关于已更改属性的信息。 |
| BindingActivationContext | 包含在注册和注销期间传递给绑定实例的信息。 |
| BindingContext | 包含解析绑定所需信息的上下文对象。 |
| BindingId | 定义绑定属性，作为绑定系统的标识符。 |
| BindingInfo | 提供关于绑定的信息。 |
| BindingResult | 提供关于绑定更新的信息。 |
| CanStartDragArgs | 关于即将开始的拖放操作的信息。参见 BaseVerticalCollectionView.canStartDrag。 |
| CreationContext | 该结构体保存 UXML 模板实例化期间使用的信息。 |
| Cursor | VisualElement cursor 样式属性 IStyle.cursor 的脚本接口。 |
| CustomStyleProperty<T0> | 为元素定义自定义样式属性，通过 CustomStyleResolvedEvent 检索。 |
| DataSourceContext | 包含绑定的数据源和数据源路径的信息。 |
| DataSourceContextChanged | 包含解析的数据源上下文发生变化时传递给绑定实例的信息。 |
| DrawData | 属于当前元素的已生成网格之一的可变视图。 |
| DrawDataEnumerable | 对 MeshModificationContext 的绘制内容的可迭代视图。 |
| DrawDataEnumerator | 对 MeshModificationContext 的绘制内容的枚举器。 |
| EasingFunction | 确定过渡如何计算中间值。 |
| EventCallbackDefinition | 可以注册到 VisualElement 上以响应任何事件类型的对象。 |
| EventCallbackDefinition<T0> | 可以注册到指定类型的元素上以响应任何事件类型的对象。 |
| EventCallbackGroup | 可以注册到任何类型的元素上以快速注册多个事件回调的对象。 |
| EventCallbackGroup<T0> | 可以注册到特定类型的元素上以快速注册多个事件回调的对象。 |
| EventDispatcherGate | 门（Gate）控制分发器何时处理事件。 |
| FillGradient | 描述用于在 Painter2D 中渲染填充形状的填充渐变。start、end、center、focus 和 radius 属性是相对于绘制器坐标系的像素坐标。 |
| FilterFunction | 表示保存过滤器定义和参数的过滤器函数。 |
| FilterParameter | 表示 FilterFunctionDefinition 的过滤器参数。 |
| FilterParameterDeclaration | FilterFunctionDefinition 的过滤器参数声明。 |
| FilterPassContext | 过滤器的上下文。 |
| FontDefinition | 描述 VisualElement 的字体。 |
| HandleDragAndDropArgs | 进行中的拖放操作的信息。参见 BaseVerticalCollectionView.dragAndDropUpdate 和 BaseVerticalCollectionView.handleDrop。 |
| Length | 表示距离值。 |
| ManipulatorActivationFilter | 定义操纵器响应特定事件的条件。 |
| MaterialDefinition | 描述 VisualElement 的材质。 |
| MeshGenerationNode | 包含 VisualElement 绘制序列的一部分。你可以在作业（job）中使用它添加嵌套绘制调用。 |
| MeshModificationContext | 每次调用时传递给 MeshModificationCallback 的上下文。 |
| ParameterBinding | 表示参数索引与后处理材质属性之间的绑定。 |
| PostProcessingMargins | FilterFunction 所需的后处理边距。 |
| PostProcessingPass | 表示可以应用到视觉元素的后处理效果。用作 FilterFunctionDefinition 的一部分。 |
| Ratio | 表示比率，用于 Aspect Ratio 样式属性。 |
| Rotate | 提供围绕 TransformOrigin 旋转的视觉元素的旋转信息。正值表示顺时针旋转。 |
| Scale | 表示作为元素变换应用的缩放。应用缩放时不动点是 TransformOrigin。 |
| SetupDragAndDropArgs | 关于刚刚开始的拖放操作的信息。你可以用它为拖拽的其余部分存储通用数据。参见 BaseVerticalCollectionView.setupDragAndDrop。 |
| StartDragArgs | 提供初始化新拖放操作的入口点。 |
| StyleBackground | 可以是 Background 或 StyleKeyword 的样式值。 |
| StyleBackgroundPosition | 可以是 BackgroundPosition 或 StyleKeyword 的样式值。 |
| StyleBackgroundRepeat | 可以是 BackgroundRepeat 或 StyleKeyword 的样式值。 |
| StyleBackgroundSize | 可以是 BackgroundSize 或 StyleKeyword 的样式值。 |
| StyleColor | 可以是 Color 或 StyleKeyword 的样式值。 |
| StyleCursor | 可以是 Cursor 或 StyleKeyword 的样式值。 |
| StyleEnum<T0> | 可以是枚举或 StyleKeyword 的样式值。 |
| StyleFloat | 可以是 float 或 StyleKeyword 的样式值。 |
| StyleFont | 可以是 Font 或 StyleKeyword 的样式值。 |
| StyleFontDefinition | 可以是 FontDefinition 或 StyleKeyword 的样式值。 |
| StyleInt | 可以是整数或 StyleKeyword 的样式值。 |
| StyleLength | 可以是 Length 或 StyleKeyword 的样式值。 |
| StyleList<T0> | 可以是列表或 StyleKeyword 的样式值。 |
| StyleMaterialDefinition | 可以是 Material 或 StyleKeyword 的样式值。 |
| StylePropertyName | 定义样式属性的名称。 |
| StylePropertyNameCollection | StylePropertyName 的集合。 |
| StyleRatio | 表示比率值，表示两个无单位值之间的比例。 |
| StyleRotate | 可以是 Rotate 或 StyleKeyword 的样式值。 |
| StyleScale | 可以是 Scale 或 StyleKeyword 的样式值。 |
| StyleTextAutoSize | 可以是 TextAutoSize 或 StyleKeyword 的样式值。 |
| StyleTextShadow | 可以是 TextShadow 或 StyleKeyword 的样式值。 |
| StyleTransformOrigin | 可以是 TransformOrigin 或 StyleKeyword 的样式值。 |
| StyleTranslate | 可以是 Translate 或 StyleKeyword 的样式值。 |
| StyleUIAnimationClip | 可以是 UIAnimationClip 或 StyleKeyword 的样式值。 |
| StyleValues | 用于一次为多个样式值设置动画的容器对象。 |
| TempMeshAllocator | 用于在作业中分配 UI Toolkit 临时网格。 |
| TextAutoSize | 控制自动字体大小调整的设置。 |
| TextShadow | VisualElement text-shadow 样式属性 IStyle.textShadow 的脚本接口。 |
| TimerState | 包含 IVisualElementScheduler 事件的计时信息。 |
| TimeValue | 表示时间值。 |
| ToggleButtonGroupState | 跟踪 ToggleButtonGroup 内按钮状态的结构。 |
| TransformOrigin | 表示应用变换（Scale、Translate 和 Rotate）的原点。 |
| Translate | 表示对象的平移。X 和 Y 的百分比值相对于应用样式值的视觉元素的宽度和高度。 |
| TreeViewItemData<T0> | 使用默认实现提供给 TreeView 的项目结构。更多用法信息，请参阅 TreeView 与“创建列表和树视图”。 |
| UIMesh | 传递给 MeshGenerationContext.DrawMesh 的顶点、索引和可选附加片段的捆绑包。 |
| UniqueStyleString | 常见字符串的基于整数的唯一表示，用于各种样式算法中更快的比较和更小的内存占用。 |
| UQueryBuilder<T0> | 构建一组在根视觉元素上运行的选择规则的实用对象。 |
| UQueryState<T0> | 包含所有选择规则的查询对象。该对象可以保存并在之后重新运行，无需重新分配内存。 |
| UxmlAttributeNames | 保存 UXML 特性的描述数据。 |
| Vertex | 表示用于绘制 VisualElement 内容的几何体顶点。 |
| VisualElementStyleSheetSet | 该结构体操作附加到所有者 VisualElement 的 StyleSheet 对象集合。 |

## 枚举（Enumerations）

| 枚举 | 描述 |
| --- | --- |
| AddressMode | 指定 UV 坐标超出 [0, 1] 范围时如何采样渐变。 |
| Align | 定义沿轴的对齐行为。 |
| AlternatingRowBackground | 为集合视图行显示交替背景颜色的选项。 |
| AngleUnit | 用于表示 Angle 值的度量单位。 |
| AnimationDirection | 确定 USS 动画是向前播放、向后播放，还是在各迭代之间交替方向。 |
| AnimationPlayState | 确定 USS 动画正在运行还是已暂停。 |
| ArcDirection | 定义圆弧时要使用的方向（参见 Painter2D.Arc）。 |
| BackgroundGradientShape | 径向渐变的形状。 |
| BackgroundGradientSize | 径向渐变的大小规则，对应 CSS radial-gradient 的 extent 关键字。 |
| BackgroundPositionKeyword | 定义背景的位置。 |
| BackgroundSizeType | 定义背景的大小。 |
| BindingLogLevel | 更改数据绑定更新期间出现的警告日志级别的选项。 |
| BindingMode | 控制绑定更新方式的绑定模式。 |
| BindingSourceSelectionMode | 在集合视图中使用数据绑定时更改数据源分配的选项。 |
| BindingStatus | 报告绑定更新结果的状态。 |
| BindingUpdateTrigger | 告诉绑定何时更新的选项。 |
| CallbackOptions | 可用于 CallbackEventHandler.RegisterCallback 的额外属性。 |
| CollectionVirtualizationMethod | 更改集合视图用于显示其内容的虚拟化方法的选项。 |
| ColumnSortingMode | 定义 MultiColumnListView 或 MultiColumnTreeView 的排序模式。 |
| ContextType | 描述 VisualElement 层级正在运行的上下文。 |
| DeltaSpeed | 给定输入设备增量的值变化速度。 |
| DisplayStyle | 定义元素在布局中的显示方式。 |
| DragAndDropPosition | 放置操作发生的位置。 |
| DragVisualMode | 拖放操作的状态。 |
| DrawPhase | 将绘制分类到元素渲染中属于的视觉阶段。 |
| DropdownMenuSizeMode | 用于计算下拉菜单宽度的模式。 |
| DynamicAtlasFilters | 启用或禁用动态图集过滤器的选项。 |
| EasingMode | 表示描述数值变化速率的数学函数。 |
| EditorTextRenderingMode | 定义编辑器默认如何渲染文本。 |
| EventInterestOptions | 当受影响方法以一般、非特定类型的方式处理事件时，用作 EventInterestAttribute 参数的选项。 |
| ExtraVertexChannels | UI Toolkit 面板可以选用供自定义着色器使用的可选每顶点通道。 |
| FillRule | 使用 Painter2D.Fill 填充形状时使用的填充规则。 |
| FilterFunctionType | FilterFunction 的过滤器函数类型。 |
| FilterParameterType | 过滤器参数的类型。 |
| FlexDirection | 定义弹性（flex）布局的主轴。 |
| GradientType | 指定颜色插值使用的渐变类型。 |
| HelpBoxMessageType | 用户消息类型。 |
| Justify | 定义主轴上的对齐方式，即额外空间如何分配。 |
| KeyboardNavigationOperation | 表示用户试图通过特定输入机制完成的操作。 |
| LanguageDirection | 指示元素文本的方向性。该值级联（cascade）到子元素。 |
| LengthUnit | 描述如何解释 Length 值。 |
| LibraryVisibility | 控制 UxmlElement 在 UI Builder Library 项目选项卡中的可见性。 |
| LineCap | 路径起点和终点的线帽类型（参见 Painter2D.lineCap）。 |
| LineJoin | 连接两个子路径的连接类型（参见 Painter2D.lineJoin）。 |
| ListViewReorderMode | 更改 ListView 中项目拖放模式的选项。 |
| MouseButton | 枚举鼠标按钮以识别特定的鼠标按钮交互。 |
| Overflow | 定义内容溢出元素边界时会发生什么。 |
| OverflowClipBox | VisualElement 内容被裁剪的框。 |
| PanelRenderMode | 确定面板的渲染方式。 |
| PanelScaleMode | 指定屏幕尺寸变化时面板中的元素如何缩放的选项。参见 PanelSettings.scaleMode。 |
| PanelScreenMatchMode | 当前屏幕分辨率的宽高比与参考分辨率不匹配时，指定如何缩放面板区域的选项。参见 PanelSettings.screenMatchMode。 |
| PenButton | 描述 PenButton。基于 W3 约定：https://www.w3.org/TR/pointerevents2/#the-buttons-property |
| PickingMode | 描述拾取（picking）行为。参见 VisualElement.pickingMode。 |
| Pivot | 用于指定 UIDocument 原点的枚举值。 |
| PivotReferenceSize | 用于指定计算 Pivot 位置所用大小的枚举值。 |
| Position | 定义布局引擎如何解释位置值。 |
| PropagationPhase | 事件的传播阶段。 |
| RenderType | DrawData 表示的几何体类型。 |
| Repeat | 定义背景的重复方式。 |
| ScrollerVisibility | 控制 ScrollView 中滚动条可见性的选项。 |
| ScrollViewMode | 影响 ScrollView 内容布局以及滚动条外观的配置。ScrollView.mode。 |
| SelectionType | 控制一次可以选择多少项。 |
| SliceType | 切片类型决定图像中心是缩放还是平铺。 |
| SliderDirection | Slider 和 SliderInt 的方向。 |
| SortDirection | 排序方向。 |
| StyleKeyword | 可用于任何样式值类型的关键字。 |
| TextAutoSizeMode | 定义文本元素如何自适应其字体大小。 |
| TextOverflow | 指定文本元素如何处理隐藏的溢出内容。 |
| TextOverflowPosition | 指定当 textOverflow 设置为 TextOverflow.Ellipsis 时，元素用省略号替换文本的哪个部分。 |
| TextureOptions | 描述纹理在绘制命令上下文中必须如何使用的标志。 |
| TextureSlotCount | UI Toolkit 可以同时绑定到着色器以减少绘制调用的纹理数量。 |
| TimeUnit | 描述如何解释 TimeValue。 |
| TransformOriginOffset | 指定 TransformOrigin 的对齐关键字。 |
| TrickleDown | 使用此枚举指定事件处理程序在哪个传播阶段执行。 |
| TwoPaneSplitViewOrientation | 确定两个可调整大小窗格的方向。 |
| UsageHints | 提供一组描述 VisualElement 预期使用模式的选项。这些选项为优化提供指导。你可以在一个元素上设置多个使用提示。例如，如果位置和颜色都会变化，可以同时设置 UsageHints.DynamicTransform 和 UsageHints.DynamicColor。注意：请在编辑时或 VisualElement 添加到面板之前设置使用提示。对于过渡（transition），当过渡开始时，系统可能会自动添加缺失的相关使用提示，以避免每帧重新生成几何体。然而，这会造成一帧的性能开销，因为 VisualElement 及其后代的渲染数据会被重新生成。 |
| VersionChangeType | 用于表示 VisualElement 中的某些变化的值。 |
| Visibility | 指定 VisualElement 是否可见的样式值。 |
| VisualElementClearOptions | 指示清除 VisualElement 子元素的选项。更多信息请参阅 VisualElement.Clear。 |
| WhiteSpace | 控制如何处理元素文本中的空白和换行，类似于 CSS 的 white-space 属性。与 CSS 属性不同，只有尾随空白会被折叠，文本中的空白会被保留。参见 white-space。 |
| WorldSpaceSizeMode | 描述世界空间 UIDocument 如何调整大小的枚举。 |
| Wrap | 默认情况下，所有项目都会尝试排成一行。你可以更改此属性，允许项目在需要时换行。 |
