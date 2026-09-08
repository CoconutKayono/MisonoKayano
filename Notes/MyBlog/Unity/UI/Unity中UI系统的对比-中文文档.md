# Unity 中 UI 系统的对比

本页面提供 [UI Toolkit](https://docs.unity3d.com/6000.7/Documentation/Manual/UIElements.html)、[uGUI（Unity UI）](https://docs.unity3d.com/Packages/com.unity.ugui@latest) 和 [IMGUI](https://docs.unity3d.com/6000.7/Documentation/Manual/ui-imgui.html) 的高级功能对比，并介绍它们各自的 UI 设计方法。

## 一般考虑因素

下表列出了运行时和编辑器的推荐 UI 系统及替代系统：

| Unity 6.6 | 推荐系统 | 替代系统 |
| --- | --- | --- |
| [运行时](https://docs.unity3d.com/6000.7/Documentation/Manual/UI-system-compare.html#runtime) | uGUI（Unity UI） | UI Toolkit |
| [编辑器](https://docs.unity3d.com/6000.7/Documentation/Manual/UI-system-compare.html#editor) | UI Toolkit | IMGUI |

## 角色和技能集

团队的技能集以及对不同技术的熟练程度也是一个重要的考虑因素。

下表列出了针对不同角色的推荐系统：

| 角色 | UI Toolkit | uGUI（Unity UI） | IMGUI | 技能集 |
| --- | --- | --- | --- | --- |
| 程序员 | ✅ | ✅ | ✅ | 程序员可以使用任何游戏开发工具或 API。 |
| 技术美术师 | 部分支持 | ✅ | ❌ | 熟悉 Unity 基于 GameObject 的工具和工作流程的技术美术师，很可能可以熟练使用 GameObject、组件和场景（Scene）视图。他们可能不习惯 UI Toolkit 类似 Web 的方法或 IMGUI 纯 C# 的方法。 |
| UI 设计师 | ✅ | 部分支持 | ❌ | 熟悉 UI 创建工具的设计师，很可能可以熟练使用 UI Toolkit 基于文档的方法，并使用 [UI Builder](https://docs.unity3d.com/6000.7/Documentation/Manual/UIBuilder.html) 直观地编辑 UI。如果他们不熟悉基于 GameObject 的工作流程，可能需要程序员或关卡设计师的帮助。 |

## 创新和开发

UI Toolkit 正处于积极开发阶段，会频繁发布新功能。uGUI 和 IMGUI 是成熟且经过生产验证的 UI 系统，更新频率较低。

如果你需要 UI Toolkit 中尚未提供的功能，或者需要支持或复用较旧的 UI 内容，uGUI 和 IMGUI 可能是更好的选择。

## 运行时

如果你创建的是能够在多种屏幕分辨率下运行的屏幕覆盖（screen overlay）UI，UI Toolkit 可以作为 uGUI（Unity UI）的替代方案。在以下情况下可考虑使用 UI Toolkit：

- 制作包含大量用户界面的项目
- 需要美术师和设计师熟悉且易上手的创作工作流程
- 寻求无纹理 UI 渲染能力
- 在 3D 世界中定位和照亮的 UI
- 使用自定义着色器和材质的高级视觉效果

以下情况下 uGUI 是推荐解决方案：

- 易于从 MonoBehaviour 引用

### 用例

下表总结了主要运行时用例中常用的系统：

| Unity 6.6 | 常用系统 |
| --- | --- |
| 密集型 UI 项目中的多分辨率菜单和 HUD | UI Toolkit |
| 世界空间 UI 和 VR | UI Toolkit |
| 需要自定义着色器和材质的 UI | UI Toolkit |
| 需要关键帧动画的 UI | uGUI |

### 详细信息

下表对比了各 UI 系统对详细运行时功能的支持情况：

| Unity 6.6 | UI Toolkit | uGUI |
| --- | --- | --- |
| 所见即所得（WYSIWYG）创作 | ✅ | ✅ |
| 嵌套可复用组件 | ✅ | ✅ |
| 布局和样式调试器 | ✅ | ✅ |
| 场景内创作 | ❌ | ✅ |
| [富文本标签](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-rich-text-tags.html) | ✅ | ✅ |
| 可缩放文本 | ✅ | ✅ |
| [字体回退](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-fallback-font.html) | ✅ | ✅ |
| 自适应布局 | ✅ | ✅ |
| [输入系统](https://docs.unity3d.com/6000.7/Documentation/Manual/com.unity.inputsystem.html)支持 | ✅ | ✅ |
| 序列化事件 | ❌ | ✅ |
| 与[渲染管线](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines.html)兼容 | ✅ | ✅ |
| 屏幕空间（2D）渲染 | ✅ | ✅ |
| [世界空间（3D）渲染](https://docs.unity3d.com/6000.7/Documentation/Manual/ui-systems/world-space-ui.html) | ✅ | ✅ |
| [自定义材质和着色器](https://docs.unity3d.com/6000.7/Documentation/Manual/ui-systems/ui-shader-graph.html) | ✅ | ✅ |
| [精灵](https://docs.unity3d.com/6000.7/Documentation/Manual/sprite/sprite-landing.html) / [精灵图集](https://docs.unity3d.com/6000.7/Documentation/Manual/sprite/atlas/atlas-landing.html)支持* | ✅ | ✅ |
| 矩形裁剪 | ✅ | ✅ |
| 遮罩裁剪 | ✅ | ✅ |
| 嵌套遮罩 | ✅ | ✅ |
| 与动画剪辑和 Timeline 集成 | ❌ | ✅ |
| [数据绑定系统](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-runtime-binding.html) | ✅ | ❌ |
| [UI 过渡动画](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-Transitions.html) | ✅ | ❌ |
| 无纹理元素 | ✅ | ❌ |
| 高级灵活布局 | ✅ | ❌ |
| 全局样式管理 | ✅ | ❌ |
| 动态纹理图集 | ✅ | ❌ |
| UI 抗锯齿 | ✅ | ❌ |
| [从右到左语言](https://docs.unity3d.com/6000.7/Documentation/Manual/ui-systems/language-direction.html)和 emoji | ✅ | ❌ |
| [SVG 支持](https://docs.unity3d.com/6000.7/Documentation/Manual/ui-systems/work-with-vector-graphics.html) | ✅ | ❌ |

*精灵图集：**图形：一种将多张精灵纹理紧密打包到单个纹理（称为图集）中的工具。[更多信息](https://docs.unity3d.com/6000.7/Documentation/Manual/sprite/atlas/v2/v2-landing)。2D：由多个较小纹理组成的纹理，也称为纹理图集、图像精灵、精灵表或打包纹理。[更多信息](https://docs.unity3d.com/6000.7/Documentation/Manual/sprite/atlas/atlas-landing.html)。另见[术语表](https://docs.unity3d.com/6000.7/Documentation/Manual/Glossary.html#SpriteAtlas)。**

## 编辑器

如果创建复杂的编辑器工具，建议使用 UI Toolkit。推荐理由如下：

- 更好的可复用性和解耦性
- 用于创作 UI 的可视化工具
- 在代码维护和性能方面有更好的可扩展性

在以下情况下，IMGUI 可以作为 UI Toolkit 的替代方案：

- 不受限制地访问编辑器的可扩展功能
- 用于快速在屏幕上渲染 UI 的轻量级 API

### 用例

下表列出了主要编辑器用例的推荐系统：

| Unity 6.6 | 推荐系统 |
| --- | --- |
| 复杂的编辑器工具 | UI Toolkit |
| 属性绘制器 | UI Toolkit |
| 与设计师协作 | UI Toolkit |

### 详细信息

下表列出了详细编辑器功能的推荐系统：

| Unity 6.6 | UI Toolkit | IMGUI |
| --- | --- | --- |
| 所见即所得（WYSIWYG）创作 | ✅ | ❌ |
| 嵌套可复用组件 | ✅ | ❌ |
| 全局样式管理 | ✅ | ✅ |
| 布局和样式调试器 | ✅ | ❌ |
| 富文本标签 | ✅ | ✅ |
| 可缩放文本 | ✅ | ❌ |
| 字体回退 | ✅ | ✅ |
| 自适应布局 | ✅ | ✅ |
| 默认检视面板 | ✅ | ✅ |
| 检视面板：编辑自定义对象类型 | ✅ | ✅ |
| 检视面板：编辑自定义属性类型 | ✅ | ✅ |
| 检视面板：混合值（多对象编辑）支持 | ✅ | ✅ |
| [数组和列表视图控件](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-uxml-element-ListView.html) | ✅ | ✅ |
| [数据绑定：序列化属性](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-Binding.html) | ✅ | ✅ |
| 高级灵活布局 | ✅ | ❌ |
| [从右到左语言](https://docs.unity3d.com/6000.7/Documentation/Manual/ui-systems/language-direction.html)和 emoji | ✅ | ❌ |
| [SVG 支持](https://docs.unity3d.com/6000.7/Documentation/Manual/ui-systems/work-with-vector-graphics.html) | ✅ | ❌ |

## 其他资源

- [UI Toolkit](https://docs.unity3d.com/6000.7/Documentation/Manual/UIElements.html)
- [uGUI（Unity UI）](https://docs.unity3d.com/Packages/com.unity.ugui@latest)
- [IMGUI（即时模式 GUI）](https://docs.unity3d.com/6000.7/Documentation/Manual/ui-imgui.html)
- [从 uGUI 迁移到 UI Toolkit](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-Transitioning-From-UGUI.html)
- [从 IMGUI 迁移到 UI Toolkit](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-IMGUI-migration.html)

---

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
