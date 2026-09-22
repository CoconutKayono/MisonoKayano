---
title: "Voronoi Noise"
author: Jasper Flick
source: "https://catlikecoding.com/unity/tutorials/pseudorandom-noise/voronoi-noise/"
license: "CC BY-NC-SA 4.0"
tags:
  - Unity
  - 噪声
  - 翻译
---

> 原作者：Jasper Flick / Catlike Coding  ·  [原文](https://catlikecoding.com/unity/tutorials/pseudorandom-noise/voronoi-noise/)  ·  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

# Voronoi Noise

沃利和切比雪夫

- 将单元点放置在晶格网格内。
- 找出到最近点的距离。
- 还要找到到第二个最近点的距离。
- 支持不同的功能和距离度量。

这是有关 [ 伪随机噪声](https://catlikecoding.com/unity/tutorials/pseudorandom-noise/) 系列教程的第六篇。它介绍了各种 Voronoi 噪声。

本教程使用Unity 2020.3.12f1制作。

![[images/voronoi-noise/tutorial-image.jpg]]

*显示 3D Voronoi Worley F2 − F1 噪声的球体。*

## 到最近点的距离

除了值噪声和梯度噪声之外，还有第三种常见的噪声类型。它基于用任意点填充空间并查找到最近点的距离。生成的图案看起来像 Voronoi 图（充满凸多边形单元的空间），因此被称为 Voronoi 或单元噪声。这种类型的噪声是由 Steven Worley 首先提出的，因此也称为 Worley 噪声。

### Voronoi 噪声类型

为了支持 Voronoi 噪声，我们将在单独的 *Noise.Voronoi* 资产中创建一个新的部分 `Noise` 类，其中包含 `INoise` 的 1D、2D 和 3D 实现。尽管从技术上讲它不是晶格噪声，但我们将使用晶格网格来生成任意点，因此使所有实现都使用通用 `ILattice` 来获取所有维度的晶格跨度。除此之外，它们最初都会返回零。

```csharp
using Unity.Mathematics;

using static Unity.Mathematics.math;

public static partial class Noise {

	public struct Voronoi1D<L> : INoise where L : struct, ILattice {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			LatticeSpan4 x = default(L).GetLatticeSpan4(positions.c0, frequency);

			return 0f;
		}
	}

	public struct Voronoi2D<L> : INoise where L : struct, ILattice {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			var l = default(L);
			LatticeSpan4
				x = l.GetLatticeSpan4(positions.c0, frequency),
				z = l.GetLatticeSpan4(positions.c2, frequency);

			return 0f;
		}
	}

	public struct Voronoi3D<L> : INoise where L : struct, ILattice {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			var l = default(L);
			LatticeSpan4
				x = l.GetLatticeSpan4(positions.c0, frequency),
				y = l.GetLatticeSpan4(positions.c1, frequency),
				z = l.GetLatticeSpan4(positions.c2, frequency);

			return 0f;
		}
	}
}
```

为了支持可视化噪声，请将所有 Voronoi 版本的常规版本和平铺版本添加到 `NoiseVisualization` 中的噪声作业数组中。

```csharp
	static ScheduleDelegate[,] noiseJobs = {
		{ … },
		{ … },
		{ … },
		{ … },
		{
			Job<Voronoi1D<LatticeNormal>>.ScheduleParallel,
			Job<Voronoi1D<LatticeTiling>>.ScheduleParallel,
			Job<Voronoi2D<LatticeNormal>>.ScheduleParallel,
			Job<Voronoi2D<LatticeTiling>>.ScheduleParallel,
			Job<Voronoi3D<LatticeNormal>>.ScheduleParallel,
			Job<Voronoi3D<LatticeTiling>>.ScheduleParallel
		}
	};
```

并在 `NoiseType` 枚举中包含一个条目。

```csharp
	public enum NoiseType { Perlin€, PerlinTurbulence, Value€, ValueTurbulence, Voronoi }
```

### 一维距离

我们将从最简单的情况开始，即一维 Voronoi 噪声。与其他一维噪声类型一样，它不是很有用，但它最容易理解，因此是一个很好的起点。

沃罗诺伊噪声的想法是空间以某种方式充满了任意数量的点。噪声函数等于到任意位置最近点的距离。从技术上讲，要检查的点的数量是无限的，但我们只需要知道最近的一个。为了能够计算噪声，我们将把自己限制为每个跨度的单个任意点。

每个跨度覆盖一个空间单位。我们可以使用该范围的哈希值中的 `Floats01A` 在其中的某个位置放置一个点。从样本位置到该点的距离等于它们在跨度内的偏移的绝对差。跨度内的样本偏移量等于 `g0`，因此从 `Floats01A` 中减去它，并将其传递给 `abs` 方法。

```csharp
	public struct Voronoi1D : INoise where L : struct, ILattice {
		
		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			LatticeSpan4 x = default(L).GetLatticeSpan4(positions.c0, frequency);

			SmallXXHash4 h = hash.Eat(x.p0);
			return abs(h.Floats01A - x.g0);
		}
	}
```

![[images/voronoi-noise/distance-to-nearest-point/1d-distances-inside-span.png]]

*跨度内的距离； 1个八度；频率 4.*

结果是一系列楔形或线性斜坡，每个跨度一个，基于每个跨度内 Voronoi 点所在的位置。每个斜坡或楔形的最小值始终为零，这表示 Voronoi 点的位置。最大可能距离为 1，只有当 Voronoi 点位于跨度的边缘时才能达到该距离。因此，与湍流噪声变体一样，噪声的幅度范围为 0-1。

### 合并相邻跨度

噪声目前是不连续的，因为我们只考虑每个跨度内的单个点。但通常相邻跨度的 Voronoi 点比当前跨度内的点更靠近样本位置。因此，为了获得正确的距离，我们还必须计算到相邻跨度中的 Voronoi 点的距离并选择最小值。

为了获得正确的矢量化最小值，我们必须调用 `select` 方法。为了方便起见，直接在 *Noise.Voronoi* 内部引入静态矢量化 `UpdateVoronoiMinima` 方法。它将当前最小值和一组新距离作为输入并返回更新的最小值。

```csharp
	static float4 UpdateVoronoiMinima (float4 minima, float4 distances) {
		return select(minima, distances, distances < minima);
	}
```

现在更改 `Voronoi1D.GetNoise4`，使其循环遍历偏移量为 -1、0 和 1 的三个跨度，计算到每个跨度中的点的距离，并每次更新最小值。循环之前的初始最小值必须无效才能正常工作。由于到最近点的理论最大距离为 1，所以任何更大的初始值都可以。让我们使用2。

```csharp
		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			LatticeSpan4 x = default(L).GetLatticeSpan4(positions.c0, frequency);

			float4 minima = 2f;
			for (int u = -1; u <= 1; u++) {
				SmallXXHash4 h = hash.Eat(x.p0 + u);
				minima = UpdateVoronoiMinima(minima, abs(h.Floats01A + u - x.g0));
			}
			return minima;
		}
```

![[images/voronoi-noise/distance-to-nearest-point/1d-voronoi.png]]

*跨度最小值。*

现在我们有了正确的一维 Voronoi 噪声。

### 我们是否总是必须评估所有三个跨度？

有时可以避免评估一个甚至两个相邻的跨度。如果到相关跨度最近边缘的距离超过当前距离，则该跨度永远不会包含更近的点，因此可以跳过它。然而，这必须根据每个样本来确定，因此不适用于矢量化。只有当所有四个样本位置都满足标准时，才可以跳过跨度。因此，我们必须添加代码来检查这一点，并添加逻辑来有条件地评估跨度，这比简单循环要复杂得多，而且速度也慢。因此，我们依靠简单的强力矢量化来使其快速并始终获得相同的性能，而不是试图在某些时候避免工作。

### 平铺

在我们的计算中必须包括相邻跨度的结果是平铺不再起作用，因为相邻跨度可以延伸到平铺区域之外。

![[images/voronoi-noise/distance-to-nearest-point/tiling-incorrect.png]]

*瓷砖铺贴不正确；频率2；域规模 4.*

为了解决这个问题，我们还必须对偏移跨度应用平铺。因为我们要么对已经平铺的晶格坐标减 1，要么加 1，所以我们只需要检查两个边缘情况。我们将通过添加到 `ILattice` 接口的新 `ValidateSingleStep` 方法签名来完成这两项操作。它以已经偏移的点和频率作为参数，并返回经过验证的点。请注意，此方法的假设是输入点已经正确平铺，然后添加了 -1、0 或 1。

```csharp
	public interface ILattice {
		LatticeSpan4 GetLatticeSpan4 (float4 coordinates, int frequency);

		int4 ValidateSingleStep (int4 points, int frequency);
	}
```

如果我们不平铺，那么此方法的实现只会返回相同的点。

```csharp
	public struct LatticeNormal : ILattice {

		…

		public int4 ValidateSingleStep (int4 points, int frequency) => points;
	}
```

如果使用平铺，则有两种可能的情况需要调整。首先，如果偏移点等于频率，那么它现在就太远了，必须循环回零。

```csharp
	public struct LatticeTiling : ILattice {

		…

		public int4 ValidateSingleStep (int4 points, int frequency) =>
			select(points, 0, points == frequency);
	}
```

其次，如果偏移点等于-1，它必须循​​环到最大侧，变得等于频率负1。

```csharp
		public int4 ValidateSingleStep (int4 points, int frequency) =>
			select(select(points, 0, points == frequency), frequency - 1, points == -1);
```

现在，我们可以通过将偏移格点传递给 `ValidateSingleStep`，然后将其馈送到循环内的哈希来正确地制作 `Voronoi1D.GetNoise4` 平铺。

```csharp
		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			var l = default(L);
			LatticeSpan4 x = l.GetLatticeSpan4(positions.c0, frequency);

			float4 minima = 2f;
			for (int u = -1; u <= 1; u++) {
				SmallXXHash4 h = hash.Eat(l.ValidateSingleStep(x.p0 + u, frequency));
				minima = UpdateVoronoiMinima(minima, abs(h.Floats01A + u - x.g0));
			}
			return minima;
		}
```

![[images/voronoi-noise/distance-to-nearest-point/tiling-correct.png]]

*正确铺贴。*

### 2D 距离

为了找到二维中的最短距离，我们需要应用毕达哥拉斯定理。让我们在 *Noise.Voronoi* 中放置一个方便的静态 `GetDistance` 方法，以对两个矢量化 X 和 Y 相对坐标偏移执行此操作。

```csharp
	static float4 GetDistance (float4 x, float4 y) => sqrt(x * x + y * y);
```

### 我们不能推迟平方根计算吗？

是的，我们将在本教程后面使用该优化。

我们通过复制 1D 噪声循环并将其放入 `Voronoi2D.GetNoise4` 中来开始创建 2D Voronoi 噪声。

```csharp
	public struct Voronoi2D<L> : INoise where L : struct, ILattice {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			var l = default(L);
			LatticeSpan4
				x = l.GetLatticeSpan4(positions.c0, frequency),
				z = l.GetLatticeSpan4(positions.c2, frequency);

			float4 minima = 2f;
			for (int u = -1; u <= 1; u++) {
				SmallXXHash4 h = hash.Eat(l.ValidateSingleStep(x.p0 + u, frequency));
				minima = UpdateVoronoiMinima(minima, abs(h.Floats01A + u - x.g0));
			}
			return minima;
		}
	}
```

为了合并 Z 维度，我们还必须循环遍历它，每个 X 偏移一次，因此我们最终得到一个嵌套循环，评估总共九个格子方块。将偏移 Z 晶格点输入哈希并通过应用 X 偏移和 Z 偏移来查找距离。

```csharp
			float4 minima = 2f;
			for (int u = -1; u <= 1; u++) {
				SmallXXHash4 hx = hash.Eat(l.ValidateSingleStep(x.p0 + u, frequency));
				float4 xOffset = u - x.g0;
				for (int v = -1; v <= 1; v++) {
					SmallXXHash4 h = hx.Eat(l.ValidateSingleStep(z.p0 + v, frequency));
					float4 zOffset = v - z.g0;
					minima = UpdateVoronoiMinima(minima, GetDistance(
						h.Floats01A + xOffset, h.Floats01D + zOffset
					));
				}
			}
			return minima;
```

![[images/voronoi-noise/distance-to-nearest-point/2d-voronoi.png]]

![[images/voronoi-noise/distance-to-nearest-point/2d-voronoi-2-octaves.png]]

*一个和两个八度 2D Voronoi 噪声。*

2D Voronoi 噪声看起来像 Voronoi 图，每个单元都包含一个圆形梯度，从单元点处的零增加到单元边缘处的最大值。边缘始终与至少两个像元点等距。

噪声的最大值等于任何样本点距单元点的最大距离。在最极端的情况下，这是位于格子正方形角上的样本点，最近的单元格点位于该样本点周围的四个单元格的对角对角处。因此噪声的最大幅度为√2。

![[images/voronoi-noise/distance-to-nearest-point/maximum-distance-visualization.png]]

*最大距离可视化；大圆圈表示最大距离为 1。*

尽管 √2 是理论上的最大值，但遇到这种情况的情况极为罕见。大多数距离最终都小于 1，但超过 1 的情况相当常见。我们可以通过返回最小值 1 的阈值来可视化这一点。

```csharp
			return select(0f, 1f, minima > 1f);
```

![[images/voronoi-noise/distance-to-nearest-point/2d-f32-normal.png]]

![[images/voronoi-noise/distance-to-nearest-point/2d-f32-exceeding-1.png]]

*频率32，可视化正常且超过1。*

### 每个方格有两个点

允许距离超过 1 的问题在于，这意味着最近的像元点可能最终位于偏移量大于 1 的像元中。我们目前没有考虑到这一点，这意味着我们在噪声中存在潜在的不连续性，其中相邻的格子方块对于最近的点不一致。

![[images/voronoi-noise/distance-to-nearest-point/potential-nearest-point.png]]

*暗方块中最近细胞点的潜在位置；红色为角点；蓝色表示边缘中点。*

因此，保证无伪影噪声的唯一方法是评估最多 21 个单元，但这是不切实际的。然而，只有当距离超过 1 时才需要这样做，这种情况并不常见。但我们不希望噪声超过1，它的范围应该是0-1。因此，实际的解决方案是限制噪声，使其永远不会超过 1。

![[images/voronoi-noise/distance-to-nearest-point/potential-nearest-point-clamped.png]]

*最近像元点的潜在位置，最大距离为 1。*

将幅度限制为 1 的缺点是我们的噪声将包含小区域，在这些区域中它会变得平坦均匀 1。虽然我们无法完全消除这些区域，但我们可以通过将每个格子正方形的单元点数量从 1 增加到 2 来使它们变得极其罕见。我们可以通过每个格子正方形更新最小值两次而不是一次来做到这一点，利用我们可以从哈希中提取四个值的事实。

```csharp
			for (int u = -1; u <= 1; u++) {
				SmallXXHash4 hx = hash.Eat(l.ValidateSingleStep(x.p0 + u, frequency));
				float4 xOffset = u - x.g0;
				for (int v = -1; v <= 1; v++) {
					SmallXXHash4 h = hx.Eat(l.ValidateSingleStep(z.p0 + v, frequency));
					float4 zOffset = v - z.g0;
					minima = UpdateVoronoiMinima(minima, GetDistance(
						h.Floats01A + xOffset, h.Floats01B + zOffset
					));
					minima = UpdateVoronoiMinima(minima, GetDistance(
						h.Floats01C + xOffset, h.Floats01D + zOffset
					));
				}
			}
			return minima;
```

![[images/voronoi-noise/distance-to-nearest-point/2d-two-points.png]]

![[images/voronoi-noise/distance-to-nearest-point/2d-two-points-2-octaves.png]]

*每方格两点；一个和两个八度。*

这使得噪声更加紧凑并且实际上消除了平坦区域。最后一步是保证最终结果永远不会超过 1，以防我们遇到平坦区域。

```csharp
			return min(minima, 1f);
```

### 3D 距离

将 1D 噪声扩展到 2D 噪声的相同方法可用于创建 3D 噪声。首先介绍 `GetDistance` 方法的 3D 变体。

```csharp
	static float4 GetDistance (float4 x, float4 y, float4 z) =>
		sqrt(x * x + y * y + z * z);
```

### 毕达哥拉斯定理适用于三维吗？

是的。要看到这一点，首先将距离计算减少到单个维度：“d_1=|x|=sqrt(x^2)”。

如果我们从一维变为二维，则可以通过添加第二维形成三角形来找到二维距离：`d_2=sqrt(d_1^2+y^2)=sqrt(sqrt(x^2)^2+y^2)=sqrt(x^2+y^2)`。

从二维到三维会在其顶部添加第三个维度，在二维斜边顶部形成一个三角形：`d_3=sqrt(d_2^2+z^2)=sqrt(sqrt(x^2+y^2)^2+z^2)=sqrt(x^2+y^2+z^2)`。

对于更高维度也是如此。一般来说，`d_n=sqrt(c_1^2+...+c_n^2)=sqrt(sum_(i=1)^nc_i^2)`。

然后用三重循环填充 `Voronoi3D.GetNoise4`，最初每个晶格立方体更新一次最小值，即 27 次。

```csharp
	public struct Voronoi3D<L> : INoise where L : struct, ILattice {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			var l = default(L);
			LatticeSpan4
				x = l.GetLatticeSpan4(positions.c0, frequency),
				y = l.GetLatticeSpan4(positions.c1, frequency),
				z = l.GetLatticeSpan4(positions.c2, frequency);

			float4 minima = 2f;
			for (int u = -1; u <= 1; u++) {
				SmallXXHash4 hx = hash.Eat(l.ValidateSingleStep(x.p0 + u, frequency));
				float4 xOffset = u - x.g0;
				for (int v = -1; v <= 1; v++) {
					SmallXXHash4 hy = hx.Eat(l.ValidateSingleStep(y.p0 + v, frequency));
					float4 yOffset = v - y.g0;
					for (int w = -1; w <= 1; w++) {
						SmallXXHash4 h =
							hy.Eat(l.ValidateSingleStep(z.p0 + w, frequency));
						float4 zOffset = w - z.g0;
						minima = UpdateVoronoiMinima(minima, GetDistance(
							h.Floats01A + xOffset,
							h.Floats01B + yOffset,
							h.Floats01C + zOffset
						));
					}
				}
			}
			return min(minima, 1f);
		}
	}
```

![[images/voronoi-noise/distance-to-nearest-point/3d-f32-normal.png]]

![[images/voronoi-noise/distance-to-nearest-point/3d-f32-exceeding-1.png]]

*频率 32 平面上的 3D 噪声，正常且超过 1。*

这得到了 3D Voronoi 噪声，它与 2D 版本具有相同的问题，但理论最大幅度为 √3。我们将再次通过在每个晶格立方体上使用两个点来大幅降低最小值超过 1 的可能性。然而，因为我们需要三个值来生成 3D 单元格点，所以我们总共需要从哈希中提取六个值。所以目前可用的A、B、C、D值是不够的。

### 每个哈希有六个值

我们可以向 `SmallXXHash4` 添加更显式的方法来支持从中提取六个值，但这会使类变得混乱。因此，我们将为其提供通用的值提取方法。第一个是 `GetBits` 方法，该方法返回可配置的位数，并按可配置的步数进行移位。通过首先右移所需的量然后屏蔽结果以将其限制为所需的位数来找到结果。通过将计数左移 1，然后减 1 即可找到掩码。

```csharp
	public uint4 GetBits (int count, int shift) =>
		((uint4)this >> shift) & (uint)((1 << count) - 1);
```

### 位掩码的生成是如何进行的？

将 1 左移“s”步相当于“2^s”。例如，将 `1b` 移动三倍将得到 `1000b`，即“2^3=8”。减去 1 将其减少到 7，即 `111b`，当用作位掩码时，会消除除三个最低有效位之外的所有内容。

还添加随附的 `GetBitsAsFloats01` 方法，该方法通过强制转换和适当的缩放将位转换为 0-1 值。

```csharp
	public float4 GetBitsAsFloats01 (int count, int shift) =>
		(float4)GetBits(count, shift) * (1f / ((1 << count) - 1));
```

### 每个格子立方体有两个点

现在我们可以从 `Voronoi3D.GetNoise4` 中的哈希中提取六个值。 32 除以 6 向下舍入等于 5，因此我们将每个坐标使用 5 位，留下 2 位未使用。这意味着每个坐标只有“2^5=32”可能值，而不是“2^8=256”，但这仍然足以产生可接受的噪声。

```csharp
						SmallXXHash4 h =
							hv.Eat(l.ValidateSingleStep(z.p0 + w, frequency));
						float4 wOffset = w - z.g0;
						minima = UpdateVoronoiMinima(minima, GetDistance(
							h.GetBitsAsFloats01(5, 0) + xOffset,
							h.GetBitsAsFloats01(5, 5) + yOffset,
							h.GetBitsAsFloats01(5, 10) + zOffset
						));
						minima = UpdateVoronoiMinima(minima, GetDistance(
							h.GetBitsAsFloats01(5, 15) + xOffset,
							h.GetBitsAsFloats01(5, 20) + yOffset,
							h.GetBitsAsFloats01(5, 25) + zOffset
						));
```

![[images/voronoi-noise/distance-to-nearest-point/3d-sphere-1o-positive.png]]

![[images/voronoi-noise/distance-to-nearest-point/3d-sphere-2o-positive.png]]

![[images/voronoi-noise/distance-to-nearest-point/3d-sphere-1o-negative.png]]

![[images/voronoi-noise/distance-to-nearest-point/3d-sphere-2o-negative.png]]

*一倍频和二倍频 6 3D Voronoi 噪声；正位移和负位移。*

请注意，当 3D Voronoi 噪声投影到轴对齐的平面上时，它看起来与 2D Voronoi 噪声有很大不同。 3D 版本中的单元点很可能并不完全位于平面上，因此大多数可见单元内的梯度不会达到零。

![[images/voronoi-noise/distance-to-nearest-point/3d-voronoi.png]]

![[images/voronoi-noise/distance-to-nearest-point/3d-voronoi-2-octaves.png]]

*一个和两个八度 3D Voronoi 噪声。*

## 到第二个最近点的距离

我们不需要限制自己只考虑到最近像元点的距离。还有第二最近的点、第三最近的点，依此类推。使用这些距离会产生不同的图案。当然，到更远的点的距离更长，因此平均噪声值会更高，并且夹紧平坦区域会更常见。因此，我们将仅包括第二最近的距离。

### 追踪两个最小值

为了找到第二最近的距离，我们还需要知道最近的距离，因此我们必须跟踪每个样本点的两个最小值，而不是一个。调整 `UpdateVoronoiMinima`，使其接受并返回 `float4x2` 最小值。它的第一个向量包含最近的距离，第二个向量包含第二最近的距离。这需要我们重写该方法的代码，最初返回最小值不变。

```csharp
	static float4x2 UpdateVoronoiMinima (float4x2 minima, float4 distances) {
		return minima;
	}
```

第一步是像以前一样更新真实最小值，现在包含在 `c0` 中。为了方便起见，将新最小值的距离检查存储在布尔向量变量中，因为我们必须对每个最小值向量检查两次。

```csharp
	static float4x2 UpdateVoronoiMinima (float4x2 minima, float4 distances) {
		bool4 newMinimum = distances < minima.c0;
		minima.c0 = select(minima.c0, distances, newMinimum);
		return minima;
	}
```

如果有新的最小值，则旧的最小值将成为次要最小值。因此 `c1` 必须在 `c0` 之前更新。

```csharp
		bool4 newMinimum = distances < minima.c0;
		minima.c1 = select(minima.c1, minima.c0, newMinimum);
		minima.c0 = select(minima.c0, distances, newMinimum);
```

除此之外，新距离也可能不提供新的主要最小值，但确实提供新的次要最小值，因此也要检查这一点。

```csharp
		minima.c1 = select(
			select(minima.c1, distances, distances < minima.c1),
			minima.c0,
			newMinimum
		);
```

我们必须调整 `Voronoi1D.GetNoise4`，使其使用新的双最小值类型。为了保持噪声相同，使用 `c0` 作为最终结果。这将产生与之前相同的代码，因为未使用的次要最小值将被 *Burst* 优化掉。

```csharp
			float4x2 minima = 2f;
			for (int u = -1; u <= 1; u++) {
				SmallXXHash4 h = hash.Eat(l.ValidateSingleStep(x.p0 + u, frequency));
				minima = UpdateVoronoiMinima(minima, abs(h.Floats01A + u - x.g0));
			}
			return minima.c0;
```

对 `Voronoi2D` 和 `Voronoi3D` 执行相同的操作。

```csharp
			float4x2 minima = 2f;
			…
			return min(minima.c0, 1f);
						
					
```

### 沃罗诺伊函数

我们用于 Voronoi 噪声的具体结果通常称为其函数。显示到最近像元点的距离的函数称为 F1。到第二个最近点的距离称为 F2，依此类推。为了支持这些函数的轻松应用，我们将引入带有单个 `Evaluate` 方法的 `IVoronoiFunction` 接口，该方法采用双最小值向量并生成单向量结果。将其放入新的 *Noise.Voronoi.Function* 部分 `Noise` 类资产中。

```csharp
using Unity.Mathematics;

public static partial class Noise {

	public interface IVoronoiFunction {
		float4 Evaluate (float4x2 minima);
	}
}
```

然后添加实现该接口的 `F1` 和 `F2` 结构体，只需返回 `c0` 或 `c1` 即可。

```csharp
	public struct F1 : IVoronoiFunction {

		public float4 Evaluate (float4x2 distances) => distances.c0;
	}

	public struct F2 : IVoronoiFunction {

		public float4 Evaluate (float4x2 distances) => distances.c1;
	}
```

下一步是让 Voronoi 结构使用这些函数。将 `IVoronoiFunction` 的通用类型参数添加到 `Voronoi1D` 并使用它来评估最小值。

```csharp
	public struct Voronoi1D<L, F> : INoise
		where L : struct, ILattice where F : struct, IVoronoiFunction {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			…
			return default(F).Evaluate(minima);
		}
	}
```

对 `Voronoi2D` 执行相同的操作，并在评估最终结果之前限制最小值向量。

```csharp
	public struct Voronoi2D<L, F> : INoise
		where L : struct, ILattice where F : struct, IVoronoiFunction {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			…
			minima.c0 = min(minima.c0, 1f);
			minima.c1 = min(minima.c1, 1f);
			return default(F).Evaluate(minima);
		}
	}
```

以同样的方式调整`Voronoi3D`。然后调整 `NoiseVisualization` 中的作业数组，使其包含 F1 和 F2 的 Voronoi 版本。

```csharp
		{
			Job<Voronoi1D<LatticeNormal, F1>>.ScheduleParallel,
			Job<Voronoi1D<LatticeTiling, F1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeNormal, F1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeTiling, F1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeNormal, F1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeTiling, F1>>.ScheduleParallel
		},
		{
			Job<Voronoi1D<LatticeNormal, F2>>.ScheduleParallel,
			Job<Voronoi1D<LatticeTiling, F2>>.ScheduleParallel,
			Job<Voronoi2D<LatticeNormal, F2>>.ScheduleParallel,
			Job<Voronoi2D<LatticeTiling, F2>>.ScheduleParallel,
			Job<Voronoi3D<LatticeNormal, F2>>.ScheduleParallel,
			Job<Voronoi3D<LatticeTiling, F2>>.ScheduleParallel
		}
```

最后，将 `NoiseType` 的单个 Voronoi 元素替换为两个元素，即 F1 和 F2。

```csharp
	public enum NoiseType {
		Perlin€, PerlinTurbulence, Value€, ValueTurbulence, VoronoiF1, VoronoiF2
	}
```

![[images/voronoi-noise/distance-to-nearest-point/1d-voronoi.png]]

![[images/voronoi-noise/distance-to-second-nearest-point/1d-f2.png]]

*一维沃罗诺伊 F1 和 F2。*

![[images/voronoi-noise/distance-to-nearest-point/2d-two-points.png]]

![[images/voronoi-noise/distance-to-second-nearest-point/2d-f2.png]]

*2D Voronoi F1 和 F2。*

![[images/voronoi-noise/distance-to-nearest-point/3d-sphere-1o-positive.png]]

![[images/voronoi-noise/distance-to-second-nearest-point/3d-f2.png]]

*3D Voronoi F1 和 F2。*

F2 的结果显示与 F1 相同的 Voronoi 单元，但梯度方向相反。此外，单元被划分为具有不同方向的梯度，因为单元的不同区域具有不同的最近单元邻居。

### F2 减 F1

我们不必限制自己只使用 F1 或 F2，我们还可以使用以某种方式组合它们的函数。最有趣的变体是 F2 − F1。在 *Noise.Voronoi.Function* 中为其创建一个 `IVoronoiFunction`。

```csharp
	public struct F2MinusF1 : IVoronoiFunction {

		public float4 Evaluate (float4x2 distances) => distances.c1 - distances.c0;
	}
```

将其添加到`NoiseVisualization`中的作业数组中。

```csharp
		{
			…
			Job<Voronoi3D<LatticeTiling, F2>>.ScheduleParallel
		},
		{
			Job<Voronoi1D<LatticeNormal, F2MinusF1>>.ScheduleParallel,
			Job<Voronoi1D<LatticeTiling, F2MinusF1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeNormal, F2MinusF1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeTiling, F2MinusF1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeNormal, F2MinusF1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeTiling, F2MinusF1>>.ScheduleParallel
		}
```

并将其包含在 *NoiseType* 中。

```csharp
	public enum NoiseType {
		Perlin€, PerlinTurbulence, Value€, ValueTurbulence,
		VoronoiF1, VoronoiF2, VoronoiF2MinusF1
	}
```

![[images/voronoi-noise/distance-to-second-nearest-point/1d-f2-f1.png]]

![[images/voronoi-noise/distance-to-second-nearest-point/2d-f2-f1.png]]

![[images/voronoi-noise/distance-to-second-nearest-point/3d-f2-f1.png]]

*1D、2D 和 3D Voronoi F2 − F1。*

F2 - F1 产生强烈分段的图案，看起来有点像有角的鹅卵石。发生这种情况是因为 F1 和 F2 沿单元边缘相等，而单元内部 F2 始终超过 F1。因此，结果保证在 0-1 范围内。

请注意，此函数不会产生完美的轮廓。单元内梯度的强度取决于其点距离单元边缘的距离。

### 是否有可能创建完全均匀的细胞轮廓？

是的，但它需要对距离进行二次搜索，并且不能使用变体 Voronoi 函数来求解。这适用于 2D 噪声，但不适用于 3D 噪声，因为细胞面最终可能与样本表面显着对齐，从而产生主要由轮廓组成的区域。

## 距离度量

除了改变 Voronoi 噪声的函数之外，还可以以不同的方式确定距离，因为标准欧几里得距离不是唯一的选择。

### Voronoi 距离接口

为了支持多个距离指标，我们将在新的 *Noise.Voronoi.Distance* 部分 `Noise` 类资产中引入 `IVoronoiDistance` 接口。为其提供三种 `GetDistance` 方法，分别用于 1D、2D 和 3D。

```csharp
using Unity.Mathematics;

using static Unity.Mathematics.math;

public static partial class Noise {

	public interface IVoronoiDistance {
		float4 GetDistance (float4 x);

		float4 GetDistance (float4 x, float4 y);

		float4 GetDistance (float4 x, float4 y, float4 z);
	}
}
```

除此之外，还包括最小向量的三种最终确定方法，每个维度一种。这些将在最终最小值上调用，并且是最终钳位和其他调整所属的位置。

```csharp
	public interface IVoronoiDistance {
		…

		float4x2 Finalize1D (float4x2 minima);

		float4x2 Finalize2D (float4x2 minima);

		float4x2 Finalize3D (float4x2 minima);
	}
```

调整 `Voronoi1D`，使其依赖于通用 `IVoronoiDistance` 类型参数。使用它来获取每个跨度的距离并在评估之前确定最小值。

```csharp
	public struct Voronoi1D<L, D, F> : INoise
		where L : struct, ILattice
		where D : struct, IVoronoiDistance
		where F : struct, IVoronoiFunction {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			var l = default(L);
			var d = default(D);
			LatticeSpan4 x = l.GetLatticeSpan4(positions.c0, frequency);

			float4x2 minima = 2f;
			for (int u = -1; u <= 1; u++) {
				SmallXXHash4 h = hash.Eat(l.ValidateSingleStep(x.p0 + u, frequency));
				minima =
					UpdateVoronoiMinima(minima, d.GetDistance(h.Floats01A + u - x.g0));
			}
			return default(F).Evaluate(d.Finalize1D(minima));
		}
	}
```

对 `Voronoi2D` 也执行此操作，同时从其 `GetNoise4` 方法中删除钳位代码。

```csharp
	public struct Voronoi2D<L, D, F> : INoise
		where L : struct, ILattice
		where D : struct, IVoronoiDistance
		where F : struct, IVoronoiFunction {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			var l = default(L);
			var d = default(D);
			…
					minima = UpdateVoronoiMinima(minima, d.GetDistance(
						h.Floats01A + xOffset, h.Floats01B + zOffset
					));
					minima = UpdateVoronoiMinima(minima, d.GetDistance(
						h.Floats01C + xOffset, h.Floats01D + zOffset
					));
			…
			//minima.c0 = min(minima.c0, 1f);
			//minima.c1 = min(minima.c1, 1f);
			return default(F).Evaluate(d.Finalize2D(minima));
		}
	}
```

对 `Voronoi3D` 执行相同操作。确保每个噪声版本调用适当的 `Finalize` 方法。

```csharp
	public struct Voronoi3D<L, D, F> : INoise
		where L : struct, ILattice
		where D : struct, IVoronoiDistance
		where F : struct, IVoronoiFunction {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			var l = default(L);
			var d = default(D);
			…
						minima = UpdateVoronoiMinima(minima, d.GetDistance(
							…
						));
						minima = UpdateVoronoiMinima(minima, d.GetDistance(
							…
						));
			…
			//minima.c0 = min(minima.c0, 1f);
			//minima.c1 = min(minima.c1, 1f);
			return default(F).Evaluate(d.Finalize3D(minima));
		}
	}
```

这些更改后不再需要静态 `GetDistance` 方法，因此将其删除。

```csharp
	//static float4 GetDistance (float4 x, float4 y) => sqrt(x * x + y * y);

	//static float4 GetDistance (float4 x, float4 y, float4 z) =>
	//	sqrt(x * x + y * y + z * z);
```

### Voronoi 沃利噪声

为了使 Voronoi 噪声再次发挥作用，我们必须引入一个在 *Noise.Voronoi.Distance* 中实现 `IVoronoiDistance` 的结构类型，使用我们迄今为止使用的相同的欧几里得距离度量和钳位。因为这是默认的 Voronoi 噪声实现，并且是由 Steven Worley 引入的，所以我们将其命名为 `Worley`。

由于 2D 和 3D 最终确定相同，`Finalize3D` 可以转发到 `Finalize2D`，避免重复代码。

```csharp
	public struct Worley : IVoronoiDistance {

		public float4 GetDistance (float4 x) => abs(x);

		public float4 GetDistance (float4 x, float4 y) => sqrt(x * x + y * y);

		public float4 GetDistance (float4 x, float4 y, float4 z) =>
			sqrt(x * x + y * y + z * z);

		public float4x2 Finalize1D (float4x2 minima) => minima;

		public float4x2 Finalize2D (float4x2 minima) {
			minima.c0 = min(minima.c0, 1f);
			minima.c1 = min(minima.c1, 1f);
			return minima;
		}

		public float4x2 Finalize3D (float4x2 minima) => Finalize2D(minima);
	}
```

此时我们还介绍一个优化。因为如果“a<=b”，那么“a^2<=b^2”——只要“a”和“b”不为负——我们就可以延迟计算平方根，直到最终确定。这意味着我们只需计算一次平方根，而不是每次迭代。

```csharp
		public float4 GetDistance (float4 x, float4 y) => x * x + y * y;

		public float4 GetDistance (float4 x, float4 y, float4 z) => x * x + y * y + z * z;

		public float4x2 Finalize2D (float4x2 minima) {
			minima.c0 = sqrt(min(minima.c0, 1f));
			minima.c1 = sqrt(min(minima.c1, 1f));
			return minima;
		}
```

在 `NoiseVisualization` 的作业数组中提供新的泛型类型参数。

```csharp
		{
			Job<Voronoi1D<LatticeNormal, Worley, F1>>.ScheduleParallel,
			Job<Voronoi1D<LatticeTiling, Worley, F1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeNormal, Worley, F1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeTiling, Worley, F1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeNormal, Worley, F1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeTiling, Worley, F1>>.ScheduleParallel
		},
```

并调整 Voronoi 标签以表明它们代表 Worley 变体。

```csharp
	public enum NoiseType {
		Perlin€, PerlinTurbulence, Value€, ValueTurbulence,
		VoronoiWorleyF1, VoronoiWorleyF2, VoronoiWorleyF2MinusF1
	}
```

### 沃罗诺伊切比雪夫噪声

我们将使用棋盘距离作为替代度量。它描述了一个国王需要多少步才能到达棋盘上的目的地。对于国王来说，对角线移动与轴对齐移动相同。一般来说，这意味着该距离等于任何一维的最大距离。这种类型的距离通常以 Pafnuty Chebyshev 命名，因此我们将其命名为 `Chebyshev`。

由于其本质，最大可能距离在所有维度上都是相同的，因此我们不需要限制最小值。

```csharp
	public struct Chebyshev : IVoronoiDistance {

		public float4 GetDistance (float4 x) => abs(x);

		public float4 GetDistance (float4 x, float4 y) => max(abs(x), abs(y));

		public float4 GetDistance (float4 x, float4 y, float4 z) =>
			max(max(abs(x), abs(y)), abs(z));

		public float4x2 Finalize1D (float4x2 minima) => minima;

		public float4x2 Finalize2D (float4x2 minima) => minima;

		public float4x2 Finalize3D (float4x2 minima) => minima;
	}
```

将切比雪夫版本的 Voronoi 噪声添加到 `NoiseVisualization` 中的作业数组中。

```csharp
		{
			…
			Job<Voronoi3D<LatticeTiling, Worley, F2MinusF1>>.ScheduleParallel
		},
		{
			Job<Voronoi1D<LatticeNormal, Chebyshev, F1>>.ScheduleParallel,
			Job<Voronoi1D<LatticeTiling, Chebyshev, F1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeNormal, Chebyshev, F1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeTiling, Chebyshev, F1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeNormal, Chebyshev, F1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeTiling, Chebyshev, F1>>.ScheduleParallel
		},
		{
			Job<Voronoi1D<LatticeNormal, Chebyshev, F2>>.ScheduleParallel,
			…
		},
		{
			Job<Voronoi1D<LatticeNormal, Chebyshev, F2MinusF1>>.ScheduleParallel,
			…
		}
```

在继续之前，请注意一维沃利噪声和切比雪夫噪声是相同的。因此，我们可以用沃利等效项替换一维切比雪夫噪声的条目。这样做的优点是 Unity 不必生成 1D Chebyshev 作业。

```csharp
		{
			Job<Voronoi1D<LatticeNormal, Worley, F1>>.ScheduleParallel,
			Job<Voronoi1D<LatticeTiling, Worley, F1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeNormal, Chebyshev, F1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeTiling, Chebyshev, F1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeNormal, Chebyshev, F1>>.ScheduleParallel,
			Job<Voronoi3D<LatticeTiling, Chebyshev, F1>>.ScheduleParallel
		},
		{
			Job<Voronoi1D<LatticeNormal, Worley, F2>>.ScheduleParallel,
			Job<Voronoi1D<LatticeTiling, Worley, F2>>.ScheduleParallel,
			Job<Voronoi2D<LatticeNormal, Chebyshev, F2>>.ScheduleParallel,
			…
		},
		{
			Job<Voronoi1D<LatticeNormal, Worley, F2MinusF1>>.ScheduleParallel,
			Job<Voronoi1D<LatticeTiling, Worley, F2MinusF1>>.ScheduleParallel,
			Job<Voronoi2D<LatticeNormal, Chebyshev, F2MinusF1>>.ScheduleParallel,
			…
		}
```

最后，还将切比雪夫变体添加到 `NoiseType` 中。

```csharp
	public enum NoiseType {
		Perlin€, PerlinTurbulence, Value€, ValueTurbulence,
		VoronoiWorleyF1, VoronoiWorleyF2, VoronoiWorleyF2MinusF1,
		VoronoiChebyshevF1, VoronoiChebyshevF2, VoronoiChebyshevF2MinusF1
	}
```

![[images/voronoi-noise/distance-metrics/chebyshev-2d-f1.png]]

![[images/voronoi-noise/distance-metrics/chebyshev-2d-f2.png]]

![[images/voronoi-noise/distance-metrics/chebyshev-2d-f2-f1.png]]

![[images/voronoi-noise/distance-metrics/chebyshev-3d-f1.png]]

![[images/voronoi-noise/distance-metrics/chebyshev-3d-f2.png]]

![[images/voronoi-noise/distance-metrics/chebyshev-3d-f2-f1.png]]

*平面上的 2D 和 3D 切比雪夫噪声； F1、F2 和 F2 - F1。*

![[images/voronoi-noise/distance-metrics/chebyshev-sphere-f1.png]]

![[images/voronoi-noise/distance-metrics/chebyshev-sphere-f2.png]]

![[images/voronoi-noise/distance-metrics/chebyshev-sphere-f2-f1.png]]

*球体上的 3D 切比雪夫噪声； F1、F2 和 F2 - F1。*

切比雪夫沃罗诺伊噪声的单元具有对角线或轴对齐的边缘，并且它们的内部梯度形成方形图案。与沃利噪声更有机的外观相比，这使其具有人造的外观。此外，轴对齐的平面采样 3D 噪声会产生颜色均匀的方形区域，无论最近的点在三维中发生偏移。

### 其他指标

您还可以使用其他距离度量。我将提到三个，但我不会将它们包含在本教程中。

最简单的变体是欧氏距离平方，通过省略最小值的平方根而创建。这会产生与沃利噪声类似的模式，但平均振幅较小，细胞内部较弱。这种变体的优点是计算成本更低。

![[images/voronoi-noise/distance-metrics/worley-squared-2d.png]]

![[images/voronoi-noise/distance-metrics/worley-squared-3d.png]]

*2D 和 3D 沃利平方。*

另一种常见的变体是曼哈顿距离，它不允许对角线测量。它对应于棋盘上车的移动。因此，距离是所有维度上的绝对距离之和。它的 2D 版本看起来有点像切比雪夫旋转 45°。曼哈顿的缺点是最大 2D 距离为 2，最大 3D 距离为 3，这意味着有很多区域被限制为 1，特别是对于 F2。

![[images/voronoi-noise/distance-metrics/manhattan-2d.png]]

![[images/voronoi-noise/distance-metrics/manhattan-3d.png]]

*2D 和 3D 曼哈顿。*

最后，除了产生距离之外，还可以可视化单元格散列。这与我们的哈希可视化类似，但基于 Voronoi 单元而不是晶格网格。这需要调整我们的噪声实现，以便为每个单元点生成一个标识符值并跟踪最近的一个。必须从散列中提取单元标识符，从用于偏移该点的值中提取位。例如，对于 2D 噪声，将每个坐标偏移的位数减少到 6，因此剩余的位数可用于两个 4 位标识符。对于 3D 噪声，每个偏移必须减少到四位。请注意，当真正的最近单元位于我们评估的单步偏移区域之外时，这些标识符在极少数情况下可能会产生不连续伪影。

![[images/voronoi-noise/distance-metrics/cell-hash-2d.png]]

![[images/voronoi-noise/distance-metrics/cell-hash-f2-f1-2d.png]]

*2D 单元格散列，并乘以 F2 − F1。*

下一个教程是 [Simplex Noise](https://catlikecoding.com/unity/tutorials/pseudorandom-noise/simplex-noise/)。

执照

存储库

PDF

---

## 署名与许可

- 原作者：Jasper Flick（Catlike Coding）
- 原文：[Voronoi 噪声](https://catlikecoding.com/unity/tutorials/pseudorandom-noise/voronoi-noise/)
- 网站许可说明：[https://catlikecoding.com/license/](https://catlikecoding.com/license/)
- 本文为英文教程的完整中文翻译与 Markdown 整理，代码片段保持原样，图示已下载并本地嵌入。
- 教程正文及配图按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可分享；本译文沿用相同许可。
- 教程中的代码与项目素材按原作者声明采用 MIT-0。
