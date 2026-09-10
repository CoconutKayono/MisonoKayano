# 创建 Culling Group

> 原文：[Create a Culling Group](https://docs.unity3d.com/6000.7/Documentation/Manual/CullingGroupAPI-getstarted.html)

没有用于操作 CullingGroup 的 Component 或可视化工具；它们只能通过脚本访问。

可以使用 `new` 运算符构造 CullingGroup：

```csharp
CullingGroup group = new CullingGroup();
```

要让 CullingGroup 执行可见性和/或距离计算，需要指定它使用的 Camera：

```csharp
group.targetCamera = Camera.main;
```

创建并填充 `BoundingSphere` 结构体数组，为 sphere 设置位置和半径，然后将数组以及数组中实际使用的 sphere 数量传递给 `SetBoundingSpheres`。sphere 数量不必等于数组长度。Unity 建议创建一个足以容纳运行时最大 sphere 数量的数组，即使初始实际使用的 sphere 数量很少。使用较大的数组，可以在运行时添加或移除 sphere，而不必执行开销较高的数组大小调整操作。

```csharp
BoundingSphere[] spheres = new BoundingSphere[1000];
spheres[0] = new BoundingSphere(Vector3.zero, 1f);
group.SetBoundingSpheres(spheres);
group.SetBoundingSphereCount(1);
```

此时，CullingGroup 会开始逐帧计算这一个 sphere 的可见性。

要清理 CullingGroup 并释放其使用的全部内存，请通过标准 .NET `IDisposable` 机制释放它：

```csharp
group.Dispose();
group = null;
```

---

## 文档导航

- 上一页：[[01-CullingGroup API简介]]
- 目录：[[00-CullingGroup API]]
- 下一页：[[03-获取剔除结果]]
