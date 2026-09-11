# URP Shader 对运动矢量的内置支持

> 原文：[Built-in shader support for motion vectors in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-shader-support.html)

本页介绍不同类型的 Shader 支持哪些运动类型，以及 URP 如何使用这些运动类型计算 motion vector。

URP 只支持不透明 Material 的 motion vector，包括 Alpha Clipping 材质。URP 不支持透明 Material 的 motion vector。

## URP ShaderLab Shader

URP 的 `Lit`、`Unlit`、`Simple Lit`、`Complex Lit` 和 `Baked Lit` Shader 支持以下类型的每对象运动矢量：

- 刚性 Transform 运动。
- 骨骼动画。
- Blend Shape 动画。
- Alembic 动画。

要为特定 Material 启用 Alembic motion vector，请在 Material Inspector 的 `Advanced` 区域中启用 `Alembic Motion Vectors` 复选框。

只应将启用了 Alembic Motion Vectors 的 Material 用于由 `PlayableDirector` Component 播放并渲染的 Alembic 顶点动画缓存。如果在普通绘制调用和 MeshRenderer 中使用此类 Material，Material 无法读取正确的 motion vector 属性流，从而生成错误的 motion vector。

## URP Lit 和 Unlit Shader Graph Target

URP Shader Graph 的 Lit 和 Unlit Target 支持 URP ShaderLab Shader 部分介绍的全部运动矢量功能。此外，它们还提供 `Additional Motion Vectors` 设置，其中包含以下选项：

### Time-Based

为 Shader Graph 顶点动画自动生成 motion vector。Unity 使用当前帧和上一帧的 `Time` Node 值，分别运行两次顶点位置 Subgraph。

此模式只适用于以下顶点动画：

- 以 `Time` Node 为基础进行过程化计算。
- 只使用不会跨帧变化的用户定义参数，例如常量、属性、Buffer 和 Texture。

### Custom

选择此选项会添加一个额外的 `Motion Vector` 顶点输出。该输出允许为每个顶点指定自定义的 object motion vector：表示顶点上一帧位置到当前位置的 3D local object space 偏移。

如果知道上一帧顶点位置的计算方式，就可以为顶点动画编写自定义 motion vector。Unity 会在将 motion vector 投影为最终的二维屏幕空间向量之前，将自定义 motion vector 与 Transform 运动、骨骼动画和 Alembic 动画产生的运动相加。

### None

这是默认值。Shader 不修改顶点输出，或者不对顶点形变进行动画时，应使用此选项。

`Time-Based` 和 `Custom` 会为 Material 启用 `MotionVectors` Pass。对于这两种模式，即使对象的 Transform 在相邻帧之间保持静止，Unity 也会每帧渲染 object motion vector pass；但如果 `MotionVectorGenerationMode` 属性设置为 `Camera`，则不会这样做。

---

## 文档导航

- 上一页：[[01-运动矢量简介]]
- 目录：[[00-运动矢量]]
- 下一页：[[03-运动矢量Render Pass]]
