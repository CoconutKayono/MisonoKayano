# Unity 是左手坐标系还是右手坐标系？

> 我在看 GAMES101 第二、第三节课，想把课上的向量知识用到 Unity。

**Unity 场景的世界坐标系采用左手约定：+X 向右，+Y 向上，+Z 向前。** 这是坐标轴的约定，不需要推导。物体的局部轴随物体旋转，不能把局部“前方”永远当成世界 +Z。[Unity 官方：旋转与方向](https://docs.unity3d.com/6000.0/Documentation/Manual/QuaternionAndEulerRotationsInUnity.html)

## 叉积为什么之前讲右手，这里又是左手？

之前的叉积笔记采用右手空间约定。Unity 官方说明 `Vector3.Cross(a,b)` 的空间方向用左手定则判断；不要把两种空间图像混用。[Unity 官方：Vector3.Cross](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Vector3.Cross.html)

一个比手势更容易核对的坐标例子是：

```csharp
Vector3.Cross(Vector3.right, Vector3.up) // (0, 0, 1)，即 forward
Vector3.Cross(Vector3.up, Vector3.right) // (0, 0, -1)，即 back
```

坐标式仍是熟悉的分量相乘相减；当坐标轴在空间中的摆放约定改变时，同一坐标结果对应的空间方向也会改变。**不要因为看到“左手”，就擅自把所有叉积结果取负。**

## 左右手会决定矩阵写左边还是右边吗？

不会。这是两个独立约定：

- 左手 / 右手：坐标轴在空间中如何定向。
- 行向量 / 列向量：公式里向量如何排列、矩阵如何作用。

学习时分别检查，不能从“Unity 是左手系”推出“矩阵必须从左往右作用”。渲染中还会切换世界、观察、裁剪等空间，不要把世界空间的结论不加检查地套到所有阶段。

**记忆：Unity 场景记“右、上、前”；叉积用具体轴测试；矩阵顺序另看向量放哪边。**

相关笔记：[[FAQ索引]] · [[叉积：为什么是向量、为什么用sin、如何记忆]] · [[变换顺序：为什么TRS是先缩放再旋转最后平移]]
