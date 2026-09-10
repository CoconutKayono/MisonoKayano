# 将相机输出渲染到 Render Texture

> 原文：[Render a camera’s output to a Render Texture in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-to-a-render-texture.html)

在 Universal Render Pipeline（URP）中，Camera 可以渲染到屏幕或 [Render Texture](https://docs.unity3d.com/6000.7/Documentation/Manual/class-RenderTexture.html)。渲染到屏幕是默认设置，也是最常见的使用方式；渲染到 Render Texture 可以创建游戏内 CCTV monitor 等效果。

如果有 Camera 正在渲染到 Render Texture，必须有第二台 Camera 将该 Render Texture 渲染到屏幕。在 URP 中，所有渲染到 Render Texture 的 Camera 都会在所有渲染到屏幕的 Camera 之前执行 Render Loop，从而确保 Render Texture 已准备好用于屏幕渲染。有关 URP 中 Camera rendering order 的更多信息，请参阅[[../04-相机渲染顺序|渲染顺序和 overdraw]]。

## 渲染到显示在屏幕上的 Render Texture

1. 在项目中创建 Render Texture Asset。选择 **Assets > Create > Rendering > Render Texture**。
2. 在 Scene 中创建 Quad GameObject。
3. 在 Project 中创建 Material。
4. 在 Inspector 中，将 Render Texture 拖到 Material 的 **Base Map** 字段。
5. 在 Scene view 中，将 Material 拖到 Quad 上。
6. 在 Scene 中创建 Camera。
7. 选择 Base Camera，在 Inspector 中将 Render Texture 拖到 **Output Texture** 属性。
8. 在 Scene 中创建另一台 Camera。
9. 将 Quad 放置在新 Base Camera 的视野中。

现在，第一台 Camera 会将其视图渲染到 Render Texture；第二台 Camera 会将包含 Render Texture 的 Scene 渲染到屏幕。

也可以在脚本中设置 Camera 的输出 target，方法是设置 Camera 的 `targetTexture` 属性：

```csharp
myCamera.targetTexture = myRenderTexture;
```

---

## 文档导航

- 上一页：[[05-为不同相机应用不同后处理]]
- 目录：[[00-多台相机]]
- 下一页：[[07-创建Render Request]]
