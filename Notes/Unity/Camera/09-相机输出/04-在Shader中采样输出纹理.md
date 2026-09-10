# 在 Shader 中采样输出纹理

> 原文：[Sample output textures in a shader](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraOutput-shader.html)

> [!IMPORTANT]
> Built-In Render Pipeline 已弃用，并将在未来版本中变为 obsolete。在整个 Unity 6.7 LTS 生命周期内，它仍受支持，包括 bug 修复和维护。有关迁移信息，请参阅[从 Built-In Render Pipeline 迁移到 URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrading-from-birp.html)和[Render Pipeline 功能比较](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines-feature-comparison.html)。

Depth texture 可以作为 global Shader property 在 Shader 中采样。声明一个名为 `_CameraDepthTexture` 的 sampler，即可采样 Camera 的主 depth texture。

`_CameraDepthTexture` 始终指向 Camera 的 primary depth texture。相反，可以使用 `_LastCameraDepthTexture` 指向最近由任意 Camera 渲染的 depth texture。例如，如果使用 secondary Camera 在脚本中渲染 half-resolution depth texture，并希望将其提供给 post-process Shader，这会很有用。

在 Built-In Render Pipeline 中，启用后 motion vectors texture 会作为 global Shader property 提供。在 Shader 中声明名为 `_CameraMotionVectorsTexture` 的 sampler，即可采样当前正在渲染的 Camera 的 texture。

从该 texture 采样时，编码像素返回的 motion 范围为 `-1..1`，表示从上一帧到当前帧的 UV offset。

## 其他资源

- [在 URP 的 Shader 中采样运动矢量](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-sample.html)

---

## 文档导航

- 上一页：[[03-从相机输出运动矢量纹理]]
- 目录：[[00-相机输出]]
- 下一页：[[05-排查相机输出问题]]
