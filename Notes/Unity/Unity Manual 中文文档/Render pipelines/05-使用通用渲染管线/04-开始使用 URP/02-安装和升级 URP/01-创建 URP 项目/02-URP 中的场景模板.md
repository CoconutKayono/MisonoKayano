# URP 中的场景模板

> 原文：[Scene templates in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/scene-templates.html)

您可以使用[场景模板](https://docs.unity3d.com/6000.7/Documentation/Manual/scene-templates.html)快速创建包含预配置 URP 特定设置和后期处理效果的场景。有关如何从场景模板创建新场景的信息，请参阅[从新场景对话框创建新场景](https://docs.unity3d.com/6000.7/Documentation/Manual/scenes-working-with.html#creating-a-new-scene-from-the-new-scene-dialog)。

![显示场景模板的新场景对话框。](scene-templates.png)

显示场景模板的新场景对话框。

以下场景模板可用于 URP：

- **基本 (URP)**：包含 [Camera](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/camera-component-reference.html) 和 [Light](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/light-component.html) 的场景。这相当于 Unity 默认场景的 URP 版本。
- **标准 (URP)**：包含 Camera、Light 和带有各种后期处理效果的全局 [Volume](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Volumes.html) 的场景。**注意**：如果使用标准 (URP) 场景模板创建场景，Unity 会创建新的 [Volume Profile](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/Volume-Profile.html) 来存储后期处理效果。

---

## 文档导航

- 上一页：[[01-使用 URP 创建新项目]]
- 目录：[[00-创建 URP 项目]]
- 下一页：[[03-在 URP 中导入包示例]]
