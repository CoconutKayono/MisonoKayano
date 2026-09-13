# 变换顺序：为什么 TRS 是先缩放再旋转最后平移？

## 1. 先看向量在哪边

采用列向量写法，把点 p 放在右边：

$$
p'=TRSp=T\bigl(R(Sp)\bigr)
$$

因此实际作用顺序是：**先 S 缩放，再 R 旋转，最后 T 平移。** 最靠近 p 的 S 先作用，就像嵌套函数先算里面。

T、R、S 分别来自 Translation、Rotation、Scale。这里 p 用齐次坐标表示，二维点写成 $(x,y,1)^T$，三维点写成 $(x,y,z,1)^T$，这样平移也能纳入矩阵乘法。

> 记忆：先找点，再从离点最近的矩阵开始读。

若教材使用行向量 $p'=pSRT$，同样的步骤会写成相反的矩阵排列；此时相应矩阵也要按行向量约定表示，不能只把同一个矩阵挪到另一边。行主序 / 列主序的内存存储方式又是另一件事，不能单凭它判断作用顺序。

## 2. 为什么不能随便交换？

只看一维坐标也能明白。令原坐标 $x=1$，缩放是乘 2，平移是加 3：

- 先缩放再平移：$1\times2+3=5$。
- 先平移再缩放：$(1+3)\times2=8$。

第二种顺序连平移带来的距离也放大了，所以结果不同。矩阵乘法通常不满足交换律：$TS\ne ST$。

可以改变括号来预先合并矩阵，但不能因此交换次序。$T(RS)=(TR)S$ 与 $TRS=SRT$ 是完全不同的说法。

## 3. Unity 中怎么对应？

Unity 的 `Matrix4x4.TRS(position, rotation, scale)` 构造位置、旋转、缩放矩阵。按列向量理解，其作用为 $T(R(Sp))$，即先缩放，再旋转，最后平移。[Unity 官方：Matrix4x4.TRS](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Matrix4x4.TRS.html)

```csharp
Matrix4x4 m = Matrix4x4.TRS(position, rotation, scale);
Vector3 transformedPoint = m.MultiplyPoint3x4(originalPoint);
```

这是常用的物体变换组合，**不是所有变换都必须遵守的唯一顺序**。你想得到不同效果，就可能选择不同顺序。例如希望物体围绕自身原点旋转后放到指定位置，通常先旋转再平移；先平移再绕坐标原点旋转，会连物体的位置一起转动。

有父物体时，还要继续应用父物体的变换：

$$
p_{world}=M_{parent\to world}\,M_{local\to parent}\,p_{local}
$$

Inspector 中先改 Position 还是先改 Scale，不等于改变最终 TRS 矩阵的组合顺序。按帧调用移动或旋转 API 则要另外看 API 的局部 / 世界空间语义。

## 4. “旋转的顺序”是另一个问题

如果问的是 Unity 欧拉角内部绕 X、Y、Z 的顺序，官方约定为 **Z → X → Y 的外禀旋转**，即绕固定轴依次转。它描述的是 R 内部如何组成，与外层的 S → R → T 不同。[Unity 官方：Euler angles](https://docs.unity3d.com/6000.0/Documentation/Manual/QuaternionAndEulerRotationsInUnity.html)

当前先记住 $p'=TRSp$ 的读取方法；欧拉角内部顺序等遇到具体旋转问题时再展开。

相关笔记：[[FAQ索引]] · [[Unity是左手坐标系还是右手坐标系]] · [[mul、dot、cross：矩阵乘法与点乘叉积的区别]]
