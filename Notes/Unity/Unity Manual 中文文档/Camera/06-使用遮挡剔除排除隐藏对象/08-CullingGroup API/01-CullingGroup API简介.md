# CullingGroup API 简介

> 原文：[Introduction to the CullingGroup API](https://docs.unity3d.com/6000.7/Documentation/Manual/CullingGroupAPI.html)

`CullingGroup` 提供了将自定义系统接入 Unity culling 和 LOD pipeline 的方式。用途包括：

- 模拟人群，只为当前实际可见的角色保留完整 GameObject。
- 构建由 `Graphics.DrawProcedural` 驱动的 GPU 粒子系统，同时跳过墙后粒子系统的渲染。
- 跟踪哪些出生点被 Camera 隐藏，从而在玩家看不到的位置生成敌人，避免敌人突然出现。
- 角色靠近时使用高质量动画和 AI 计算，远处切换为更低质量、开销更低的行为。
- 在 Scene 中放置 10,000 个标记点，并高效检测玩家何时进入任意标记点 1 米范围内。

该 API 要求你提供 bounding sphere 数组，然后计算这些 sphere 相对于指定 Camera 的可见性，以及可以视为 LOD 级别编号的 distance band 值。

## CullingGroup API 最佳实践

使用 CullingGroup 时，请考虑以下设计方面。

### 使用可见性

出于性能原因，CullingGroup 计算可见性的所有体积都由 bounding sphere 定义，实际就是球心位置和半径。不支持其他 bounding shape。因此，需要定义一个完全包围目标对象的 sphere。如果需要更紧密的包围，可以使用多个 sphere 覆盖对象的不同部分，并根据所有 sphere 的可见性状态做出决定。

为了评估可见性，CullingGroup 需要知道应从哪个 Camera 计算可见性。目前，一个 CullingGroup 只支持一个 Camera。如果需要评估多个 Camera 的可见性，应为每个 Camera 使用一个 CullingGroup，然后合并结果。

CullingGroup 只会根据 Frustum Culling 和静态 Occlusion Culling 计算可见性，不会将动态对象作为潜在遮挡物考虑在内。

### 使用距离

CullingGroup 可以计算参考点（例如 Camera 或玩家的位置）与每个 sphere 最近点之间的距离。它不会直接提供距离值，而是使用你提供的一组阈值将距离量化为离散的 **distance band** 整数结果。可以将这些 distance band 理解为“近距离”“中距离”“远距离”等。

当对象从一个 band 移动到另一个 band 时，CullingGroup 会提供回调，让你有机会将对象的行为切换为 CPU 开销更低的行为。

超过最后一个 distance band 的 sphere 会被视为不可见，因此可以轻松构建完全停用远处对象的剔除实现。如果不希望出现这种行为，只需将最后一个阈值设置为无限远。

每个 CullingGroup 只支持一个 reference point。

### 性能和设计

CullingGroup 不支持修改 Scene 后立即请求 bounding sphere 的新可见性状态。出于性能原因，CullingGroup 只会在 Camera 整体执行 culling 时计算新的可见性信息；此时可以通过 callback 或 CullingGroup Query API 获取信息。实际上，这意味着应以异步方式使用 CullingGroup。

CullingGroup 会引用你提供的 bounding sphere 数组，而不是复制数组。因此，应保留传递给 `SetBoundingSpheres` 的数组引用，并且可以修改数组内容，而不需要再次调用 `SetBoundingSpheres`。如果多个 CullingGroup 要对同一组 sphere 计算可见性和距离（例如多个 Camera），让它们共享同一个 bounding sphere 数组实例会更高效。

---

## 文档导航
- 上一页：[[00-CullingGroup API]]
- 目录：[[00-CullingGroup API]]
- 下一页：[[02-创建Culling Group]]
