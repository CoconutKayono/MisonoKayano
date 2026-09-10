# MeshRenderer 运动矢量设置参考

> 原文：[Motion Vectors settings reference for URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-reference.html)

要指定 GameObject 如何对 motion vector buffer 产生影响，请使用 **Motion Vectors** 属性：**Mesh Renderer > Additional Settings > Motion Vectors**。此属性可以对特定对象禁用 motion vector rendering，或用零填充该对象 Renderer 的可见 fragment 对应的 motion vector texture。

下表介绍 **Motion Vectors** 属性可用的选项：

| Motion Vectors 选项 | 说明 |
| --- | --- |
| **Camera Motion Only** | 渲染 Camera motion vectors 时，Unity 将对象视为在世界中静止。Unity 不会为该 MeshRenderer 绘制 per-object motion vector pass。如果 motion vector rendering 成为 GPU bottleneck，可以将该选项用于移动缓慢对象的优化。 |
| **Per Object Motion** | Unity 为该对象渲染 per-object **Motion Vectors** pass。 |
| **Force No Motion** | Unity 每帧为该对象渲染 per-object **Motion Vectors** pass，但设置特殊 Shader uniform variable，通知 pass 跳过计算并写入零值。仍然需要 per-object pass，以覆盖 full-screen pass 产生的非零 Camera motion vectors。可以使用此选项避免 3D HUD、third person character、race car 上由 Camera motion blur 产生的 artefacts，或避免对象上与错误 motion vectors 相关的其他 artefacts。 |

---

## 文档导航

- 上一页：[[06-运动矢量故障排查]]
- 目录：[[00-运动矢量]]
- 下一页：[[08-从Camera输出运动矢量纹理]]
