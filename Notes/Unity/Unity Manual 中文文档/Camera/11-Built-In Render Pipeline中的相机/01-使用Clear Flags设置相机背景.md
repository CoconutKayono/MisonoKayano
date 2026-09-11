# 使用 Clear Flags 设置相机背景

> 原文：[Set the camera background with Clear Flags in the Built-In Render Pipeline](https://docs.unity3d.com/6000.7/Documentation/Manual/camera-background-birp.html)

> [!IMPORTANT]
> Built-In Render Pipeline 已弃用，并将在未来版本中变为 obsolete。在整个 Unity 6.7 LTS 生命周期内，它仍受支持，包括 bug 修复和维护。有关迁移信息，请参阅[从 Built-In Render Pipeline 迁移到 URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrading-from-birp.html)和[Render Pipeline 功能比较](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines-feature-comparison.html)。

每台 Camera 在渲染视图时都会保存 color 和 depth 信息。未绘制的屏幕区域为空，默认显示 skybox。使用多台 Camera 时，每台 Camera 都会在 buffer 中保存自己的 color 和 depth 信息；随着每台 Camera 渲染，buffer 中会积累更多数据。

Camera 渲染视图时，可以设置 **Clear Flags** 清除 buffer 信息的不同部分。可以选择以下四个选项之一。

## Skybox

这是默认设置。屏幕的空白区域显示当前 Camera 的 skybox。如果当前 Camera 没有设置 skybox，则使用 Lighting 窗口中选择的 skybox（菜单：**Window > Rendering > Lighting**），最后回退到 **Background Color**。也可以向 Camera 添加 Skybox Component。

## Solid Color

屏幕的空白区域显示当前 Camera 的 **Background Color**。

## Depth Only

如果希望绘制玩家的武器，同时避免武器被环境裁剪，可以让一台 Camera 的 **Depth** 为 `0`，用于绘制环境；让另一台 Camera 的 **Depth** 为 `1`，只绘制武器。将武器 Camera 的 **Clear Flags** 设置为 **Depth Only**。

这样会保留环境在屏幕上的图像，但丢弃每个对象在 3D 空间中的位置信息。绘制枪支时，不透明部分会完全覆盖已有内容，无论枪支与墙壁的距离远近。

![清除前置 Camera 的 depth buffer 后最后绘制枪支](Camera-ClearFlags.jpg)

## Don’t Clear

此模式既不清除 color buffer，也不清除 depth buffer。结果是每一帧都会绘制在下一帧之上，产生类似 smear 的效果。该模式通常不用于游戏，更可能与 custom Shader 配合使用。

请注意，在某些 GPU（主要是移动 GPU）上，不清除屏幕可能导致下一帧的内容未定义。在某些系统上，屏幕可能包含上一帧图像、纯黑屏幕或随机颜色像素。

---

## 文档导航

- 上一页：[[00-Built-In Render Pipeline中的相机]]
- 目录：[[00-Built-In Render Pipeline中的相机]]
- 下一页：[[02-Camera Inspector窗口参考]]
