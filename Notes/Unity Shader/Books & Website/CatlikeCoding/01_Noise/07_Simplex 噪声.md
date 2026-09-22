---
title: "Simplex Noise"
author: Jasper Flick
source: "https://catlikecoding.com/unity/tutorials/pseudorandom-noise/simplex-noise/"
license: "CC BY-NC-SA 4.0"
tags:
  - Unity
  - 噪声
  - 翻译
---

> 原作者：Jasper Flick / Catlike Coding  ·  [原文](https://catlikecoding.com/unity/tutorials/pseudorandom-noise/simplex-noise/)  ·  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

# Simplex Noise

单纯形和径向核

- 应用径向对称衰减内核。
- 使用单纯形来划分空间。
- 将正方形转变为三角形，将立方体转变为四面体。
- 引入基于圆形和球形的渐变。

这是有关 [ 伪随机噪声](https://catlikecoding.com/unity/tutorials/pseudorandom-noise/) 系列教程的第七篇。它增加了对单纯形噪声算法的矢量化版本的支持。

本教程使用Unity 2020.3.17f1制作。

![[images/simplex-noise/tutorial-image.jpg]]

*显示 3D 单纯形噪声的球体。*

## 单纯形值噪声

Ken Perlin 创建 Perlin 噪声后，他又发明了另一种噪声模式，并将其命名为单纯形噪声。这种类型的噪声使用核求和而不是插值，并且基于单纯形网格而不是超立方网格。

在这种情况下，内核可以被认为是限制模式影响的印记或掩模。通过将以不同位置为中心的多个内核样本相加在一起来生成结果。

单纯形是最简单的多面体——具有平坦侧面的物体——占据所有可用维度的空间。直线段是一维单纯形。三角形是二维单纯形。正方形不是二维单纯形，因为它比三角形多一个角和边，因此不是最简单的形状。直线段也不是二维单纯形，因为无论它在二维空间中的方向如何，它都只有一个维度。最后，四面体是一个 3D 单纯形。

单纯形噪声是一种梯度噪声，但我们也可以创建它的值噪声变体。我们从这些开始，因为它们比梯度变体更简单、更容易分析。

### 单纯形噪声不是有专利吗？

美国专利 6,867,776 B2 仅涵盖 3D 单纯形梯度噪声，不涉及 2D 或 1D 噪声，并且不涉及本教程中的任何值噪声变体。本教程中的实现与专利中描述的并不完全相同，因为它是一种矢量化算法，并且以不同的方式生成梯度。无论如何，父级已于 2022 年 1 月 8 日到期，不再相关。

请注意，该专利涉及 Perlin 有缺陷的初始噪声实现。单纯形噪声应该是该版本的改进。在完成单纯形噪声后，他后来又回到了原来的柏林噪声并对其进行了改进。除了审美选择之外，没有任何令人信服的理由使用单纯形噪声来代替 Perlin 噪声。两者都有各自的优点和缺点。

### 单纯形工作

我们不能依赖现有的晶格结构来生成单纯形噪声，因为它们使用超立方晶格来划分空间，而我们需要单纯形晶格。因此，我们将创建一个名为 *Noise.Simplex* 的新部分 `Noise` 类资源，并在其中声明新的单纯形噪声类型（1D、2D 和 3D）。

尽管我们可以创建平铺单纯形噪声变体，但它们不会很有用，因为平铺将基于单纯形晶格，因此不与超立方体网格对齐。因此，2D 平铺不会匹配正方形区域，3D 平铺不会匹配立方体。一维平铺适合直线段，因此是可能的，但我们将保持一致，并且不支持所有单纯形噪声变体的平铺。因此这些噪声类型只需要一个 `IGradient` 泛型类型参数。我们首先仅使用梯度进行插值后的评估，但现在将零传递给它。

```csharp
using Unity.Mathematics;

using static Unity.Mathematics.math;

public static partial class Noise {

	public struct Simplex1D<G> : INoise where G : struct, IGradient {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			return default(G).EvaluateAfterInterpolation(0f);
		}
	}

	public struct Simplex2D<G> : INoise where G : struct, IGradient {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			return default(G).EvaluateAfterInterpolation(0f);
		}
	}

	public struct Simplex3D<G> : INoise where G : struct, IGradient {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			return default(G).EvaluateAfterInterpolation(0f);
		}
	}
}
```

将单纯形值噪声和单纯形值湍流噪声条目添加到 `NoiseVisualization` 中的枚举中。

```csharp
	public enum NoiseType {
		Perlin€, PerlinTurbulence, Value€, ValueTurbulence,
		SimplexValue, SimplexValueTurbulence,
		VoronoiWorleyF1, VoronoiWorleyF2, VoronoiWorleyF2MinusF1,
		VoronoiChebyshevF1, VoronoiChebyshevF2, VoronoiChebyshevF2MinusF1
	}
```

并将它们插入作业数组的适当位置。不支持平铺变体的最简单方法是对这些元素使用非平铺变体，因此每个变体都会包含两次。

```csharp
		{
			Job<Simplex1D<Value>>.ScheduleParallel,
			Job<Simplex1D<Value>>.ScheduleParallel,
			Job<Simplex2D<Value>>.ScheduleParallel,
			Job<Simplex2D<Value>>.ScheduleParallel,
			Job<Simplex3D<Value>>.ScheduleParallel,
			Job<Simplex3D<Value>>.ScheduleParallel
		},
		{
			Job<Simplex1D<Turbulence<Value>>>.ScheduleParallel,
			Job<Simplex1D<Turbulence<Value>>>.ScheduleParallel,
			Job<Simplex2D<Turbulence<Value>>>.ScheduleParallel,
			Job<Simplex2D<Turbulence<Value>>>.ScheduleParallel,
			Job<Simplex3D<Turbulence<Value>>>.ScheduleParallel,
			Job<Simplex3D<Turbulence<Value>>>.ScheduleParallel
		},
```

### 一维单纯形和核

我们从一维单纯形噪声开始。它使用与常规值噪声相同的线段空间分区，但我们没有 `ILattice` 类型来生成所需的数据。相反，我们直接在 `Simplex1D.GetNoise4` 内找到第一个格点 `x0`，首先将频率应用于位置，然后对 X 坐标进行取整。

```csharp
	public struct Simplex1D<G> : INoise where G : struct, IGradient {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			positions *= frequency;
			int4 x0 = (int4)floor(positions.c0);

			return default(G).EvaluateAfterInterpolation(0f);
		}
	}
```

为了生成噪声值，我们需要一个内核。对于一维噪声，内核需要评估哈希和一维梯度输入。我们向 `Simplex1D` 添加静态 `Kernel` 方法来执行此操作，该方法基于哈希、格点和样本位置，全部矢量化。就像 `Lattice1D` 一样，通过从 X 坐标中减去格点来找到梯度输入。

```csharp
	public struct Simplex1D<G> : INoise where G : struct, IGradient {

		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			…
		}
		
		static float4 Kernel (SmallXXHash4 hash, float4 lx, float4x3 positions) {
			float4 x = positions.c0 - lx;
			return default(G).Evaluate(hash, x);
		}
	}
```

要将内核应用于第一个格点，请在 `GetNoise4` 内部调用它，并向其传递由该点、点本身和位置提供的哈希值。将其结果传递给最终评估。

```csharp
		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			positions *= frequency;
			int4 x0 = (int4)floor(positions.c0);

			return default(G).EvaluateAfterInterpolation(
				Kernel(hash.Eat(x0), x0, positions)
			);
		}
```

为了完成一维噪声，我们还必须包括晶格跨度的第二个点 `x1`，沿着 X 轴更进一步。并且由于单纯形噪声对内核求和，因此将其内核添加到第一个内核，而不是对它们进行插值。

```csharp
		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			positions *= frequency;
			int4 x0 = (int4)floor(positions.c0), x1 = x0 + 1;

			return default(G).EvaluateAfterInterpolation(
				Kernel(hash.Eat(x0), x0, positions) + Kernel(hash.Eat(x1), x1, positions)
			);
		}
```

### 径向对称衰减

此时，我们只需添加值噪声的统一晶格值，并在整个范围内使用这些常数值。为了将其转变为连续模式，我们必须引入从一个格点到下一个格点的平滑过渡。常规晶格噪声通过插值在晶格点之间混合，而单纯形噪声通过限制每个晶格点的影响来实现这一点。这是内核的工作。它定义了一个衰减函数，该函数从晶格点处的 1 开始，在两个方向上到达相邻晶格点时降至零。因此它是一个对称内核，在单一维度上也使其径向对称。

最简单的衰减函数“f”是一减去沿单一维度的绝对距离：“f(x)=1-|x|”。该函数从 1 开始，在相邻格点处降至零。用它来缩放梯度评估。

```csharp
		static float4 Kernel (SmallXXHash4 hash, float4 lx, float4x3 positions) {
			float4 x = positions.c0 - lx;
			float4 f = 1f - abs(x);
			return f * default(G).Evaluate(hash, x);
		}
```

![[images/simplex-noise/simplex-value-noise/1d-linear-falloff.png]]

*一维值单纯形噪声，线性衰减。*

结果是连续的噪声，但它相当于简单的线性插值，因此不平滑。为了使常规值噪声变得平滑，我们需要使用 C2 连续插值。同样，我们需要找到一个C2连续衰减函数，使单纯值噪声达到相同的标准。

让我们从观察“|x|=sqrt(x^2)”开始，因此调整衰减函数的最简单方法是消除平方根。这导致“f(x)=1-x^2”。

```csharp
			float4 f = 1f - x * x;
```

![[images/simplex-noise/simplex-value-noise/1d-squared-falloff.png]]

*平方衰减。*

这种平方衰减引入了曲率，但显然还不是 C2 连续的。这是有道理的，因为一阶导数是“f”(x)=-2x”，二阶导数是“f”(x)=-2”。这些在端点处都不为零，其中“x”等于 1 或 -1。

我们可以进行的另一个观察是，在跨度的中间，噪声的幅度可能会超过 1。发生这种情况是因为在中间点“f(1/2)=1-(1/2)^2=1-1/4=3/4”。这是单个内核的最大值，但我们添加了两个，因此总的最大幅度为“2f(1/2)=3/2=1.5”。

![[images/simplex-noise/simplex-value-noise/falloff-graph-linear-squared.png]]

*线性和方形衰减。*

让我们通过仅使用内核结果的衰减因子来使这一点更加明显，从而始终可视化噪声的最大可能幅度。

```csharp
			return f; // * default(G).Evaluate(hash, x);
```

![[images/simplex-noise/simplex-value-noise/1d-squared-max-amplitude.png]]

*最大幅度。*

我们可以通过平方来修改当前的衰减函数，从而得到“f(x)=(1-x^2)^2”以及导数“f”(x)=4x^3-4x”和“f”(x)=12x^2-4”。该函数是 C1 连续的，但不是 C2 连续的。

![[images/simplex-noise/simplex-value-noise/c1-graph.png]]

*C1 衰减及其衍生物。*

### 一阶导数是如何找到的？

最简单的方法是首先重写函数：“f(x)=(1-x^2)^2=(1-x^2)(1-x^2)”。

然后使用多项式乘法规则`(a+b)(c+d)=ac+ad+bc+bd`：

`f(x)=(1-x^2)(1-x^2)=1-x^2-x^2+x^4=x^4-2x^2+1`。

然后可以通过应用 [Value Noise](https://catlikecoding.com/unity/tutorials/pseudorandom-noise/value-noise/) 教程中提到的单个规则来找到导数。

为了达到 C2 连续性，我们必须将函数的幂提高一级，对其进行立方而不是平方：“f(x)=(1-x^2)^3”以及导数“f”(x)=-6x^5+12x^3-6x”和“f”(x)=-30x^4+36x^2-6”。

![[images/simplex-noise/simplex-value-noise/c2-graph.png]]

*C2 衰减及其衍生物。*

### 那么一阶导数是如何找到的呢？

首先重写`f(x)=(1-x^2)^3=(1-x^2)(x^4-2x^2+1)`。

然后再次应用多项式乘法，在这种情况下是稍微复杂的形式 `(a+b)(c+d+e)=ac+ad+ae+bc+bd+be`：

`f(x)=(1-x^2)(x^4-2x^2+1)=-x^6+3x^4-3x^2+1`。

该函数的二阶导数在格点本身不为零，因为这是内核衰减切换方向的地方。由于内核影响双方，这不是问题，它只需在其边缘达到零即可。

将这个衰减应用到我们的内核中。

```csharp
			float4 f = 1f - x * x;
			f = f * f * f;
			return f;// * default(G).Evaluate(hash, x);
```

![[images/simplex-noise/simplex-value-noise/1d-final-max-amplitude.png]]

*最终最大幅度。*

请注意，与一维常规值噪声不同，一维单纯值噪声的最大幅度不是恒定的。它有点摇摆，在格点处达到 1，并在每个跨度的中间降至最小值 0.84375。

### 你如何找到这个最小值？

在中点`2f(1/2)=2(3/4)^3=2(27/64)=27/32=0.84375`。

最后，通过重新引入梯度评估来完成一维单纯形值噪声。

```csharp
			return f * default(G).Evaluate(hash, x);
```

![[images/simplex-noise/simplex-value-noise/1d-simplex-value-noise.png]]

![[images/simplex-noise/simplex-value-noise/1d-regular-value-noise.png]]

*一维单纯形和常规值噪声。*

与常规值噪声相比，单纯形变体由于其可变的最大幅度而更加不稳定。除此之外，两者都显示出相同的图案，因为它们基于相同的线段晶格。

### 重命名

此时，我们使用 `IGradient.EvaluateAfterInterpolation` 方法来调整格噪声插值后和单纯形噪声核求和后的最终组合噪声值。因此，它目前的名称过于具体。让我们重构并重命名所有相关代码，使其变为 `IGradient.EvaluateCombined`。我仅显示 `IGradient` 接口的更改。

```csharp
	public interface IGradient {
		…
		
		float4 EvaluateCombined (float4 value);
	}
```

### 2D 内核

转向 2D 噪声，径向对称核的衰减函数的工作原理与 1D 相同。我们再次用 1 减去距离的平方并对其进行立方。一般来说，衰减函数是“f(d)=(1-d)^3”，其中“d”是平方距离。对于 1D `d=x^2` 和 2D `d=x^2+z^2`，因为我们将 2D 噪声基于 XZ 平面。因此，对于 2D，衰减函数可以定义为 `f(x,z)=(1-x^2-z^2)^3` 将 `Kernel` 方法添加到 `Simplex2D` 中，并将此衰减作为其结果。

```csharp
	public struct Simplex2D<G> : INoise where G : struct, IGradient {

		…

		static float4 Kernel (
			SmallXXHash4 hash, float4 lx, float4 lz, float4x3 positions
		) {
			float4 x = positions.c0 - lx, z = positions.c2 - lz;
			float4 f = 1f - x * x - z * z;
			f = f * f * f;
			return f;
		}
	}
```

接下来是 `GetNoise4` 的实现，其逻辑与 1D 相同，最初使用与 `Lattice2D` 相同的基于正方形的晶格，但这次对四个内核求和。

```csharp
		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			positions *= frequency;
			int4
				x0 = (int4)floor(positions.c0), x1 = x0 + 1,
				z0 = (int4)floor(positions.c2), z1 = z0 + 1;

			SmallXXHash4 h0 = hash.Eat(x0), h1 = hash.Eat(x1);

			return default(G).EvaluateCombined(
				Kernel(h0.Eat(z0), x0, z0, positions) +
				Kernel(h0.Eat(z1), x0, z1, positions) +
				Kernel(h1.Eat(z0), x1, z0, positions) +
				Kernel(h1.Eat(z1), x1, z1, positions)
			);
		}
```

![[images/simplex-noise/simplex-value-noise/2d-square-falloff-unclamped.png]]

*方形晶格的径向衰减；频率 4.*

结果是一个充满圆形梯度的方形网格，指示噪声的最大幅度。虽然在格点处最大幅度应该为 1，但目前情况并非如此，因为以对角对角为中心的核随着其距离超过 1 而变为负值：`f(1,1)=(1-1-1)^3=-1^3=-1`。我们通过消除负面衰减结果来解决这个问题。

```csharp
		static float4 Kernel (
			SmallXXHash4 hash, float4 lx, float4 lz, float4x3 positions
		) {
			…
			return max(0f, f);
		}
```

![[images/simplex-noise/simplex-value-noise/2d-square-falloff-clamped.png]]

*夹紧的内核。*

通过限制核影响，我们可以看到使用方格时核求和的结果。下一步是切换到三角形格子。

### 径向二维值噪声会是什么样子？

使用带有方格的径向核求和会产生比基于插值的值噪声更弱且更不稳定的结果，类似于一维单纯形和常规值噪声之间的差异，但更明显。

![[images/simplex-noise/simplex-value-noise/2d-radial-value-noise.png]]

![[images/simplex-noise/simplex-value-noise/2d-regular-value-noise.png]]

*径向和插值二维值噪声。*

每个晶格边缘中点的最大幅度与一维噪声相同，即 0.84375。在每个正方形的中心，它下降到“4f(1/2,1/2)=4(1-2(1/2)^2)^3=4(1-2/4)^3=4(1/2)^3=4/8=1/2”。

对于 3D 噪声，每个晶格立方体中心的噪声会降至“8(1-3(1/2)^2)^3=8(1/4)^3=8/64=1/8”。

### 2D 单纯形

二维单纯形是一个三角形。可以使用等边三角形网格来平铺 2D 空间。我们可以从现有的基于正方形的方法开始，并使用两步过程将其转换为三角形晶格。我们取一个正方形并沿 XZ 对角线缩小。这种扭曲操作称为偏斜。结果是一个菱形，当沿 XZ 对角线分割时，菱形变成两个方向相反的三角形。如果我们应用正确的倾斜，最终结果是等边三角形的网格。

![[images/simplex-noise/simplex-value-noise/2d-skew-square-rhombus.png]]

*从正方形倾斜到菱形。*

倾斜是通过沿 XZ 对角线移动所有点来执行的。我们通过对每个点的两个坐标应用相同的调整来做到这一点。为了从正方形转换为菱形，我们必须缩小比例，因此我们必须减去一些偏斜值“s”。因此，对于每个点，我们都必须应用变换“[[x],[z]]->[[x-s],[z-s]]”。

要创建菱形，所有点的“s”不可能都相同，因此它取决于它们的坐标，这意味着它必须是一个函数：“s(x,z)”。我们必须确定它是什么。

让我们考虑一下简并菱形的情况：我们倾斜，因此所有点最终都在一条线上。我们还考虑具有角点“[[0],[0]]”、“[[1],[0]]”、“[[1],[1]]”和“[[0],[1]]”的正方形。

![[images/simplex-noise/simplex-value-noise/2d-skew-degenerate.png]]

*倾斜成简并菱形，这是一条线。*

由此我们可以看出`s(0,0)=0`，因为原点处的点没有移动。 XZ 线上的另一个点也结束于原点，因此“s(1,1)=1”。并且`s(0,1)=s(1,0)=1/2`。因此在这种情况下“s(x,z)=(x+z)/2”。一般来说，我们有“s(x,z)=v(x+z)”，其中常数值“v”决定菱形的形状。我们必须确定“v”使用哪个值，这样我们最终会得到等边三角形。

让我们看一下原始正方形的右下角三角形，其角为 `a=[[0],[0]]`、`b=[[1],[0]]` 和 `c=[[1],[1]]`。

![[images/simplex-noise/simplex-value-noise/2d-skew-triangles.png]]

*同一三角形的直角和等边版本。*

倾斜后“a”仍然相同，但其他两个角点发生了变化。我们有 `b=[[1-v(1+0)],[-v(1+0)]]=[[1-v],[-v]]` 和 `c=[[1-v(1+1)],[1-v(1+1)]]=[[1-2v],[1-2v]]`。

我们还不知道“v”是什么，但我们知道三角形的三条边具有相同的长度，因此我们可以将它们相等。由于“a”位于原点，因此从它到“b”和“c”的距离等于它们定义的向量的长度。因此，这两个向量的长度相等：`||b||=||c||`，因此它们的平方长度也相等：`||b||^2=||c||^2`。

二维向量的平方长度是“x^2+z^2”。因此`||b||^2=(1-v)^2+(-v)^2=2v^2-2v+1`和`||c||^2=2(1-2v)^2=8v^2-8v+2`。现在我们可以解方程并找到“v=(3-sqrt(3))/6”。

### 你如何解方程？

重写 `||b||^2=||c||^2->2v^2-2v+1=8v^2-8v+2->6v^2-6v+1=0`。

应用二次公式：如果 `ax^2+bx+c=0` 则 `x=(-b+-sqrt(b^2-4ac))/(2a)`，因此可能有两个解决方案。在我们的例子中，“a=6”、“b=-6”和“c=1”。

求解“v=(6+-sqrt(12))/12=(6+-2sqrt(3))/12=(3+-sqrt(3))/6”。

`(3+sqrt(3))/6~~0.789` 和 `(3-sqrt(3))/6~~0.211`。两种解决方案都是有效的，但大于 0.5 的倾斜因子将导致网格翻转，穿过简并线，因此我们将使用较小的值。

此时我们知道如何从正方形转换为三角形，但我们已经声明我们正在使用三角形格子，这是我们的起点。为了找到格点，我们必须以另一种方式转换，从三角形到正方形。这需要沿相同的 XZ 对角线移动所有点，但现在沿相反的方向移动，即增加而不是减去倾斜，因此我们有“[[x],[z]]->[[x+v(x+z)],[z+v(x+z)]]”，其中“v”是我们必须找到的不同倾斜值。

让我们考虑点“c”的变换。我们知道它必须以“[[1],[1]]”和“x=z”结束，因此“x+2vx=1”。我们还知道 x=1-2(3-sqrt(3))/6=1-(3-sqrt(3))/3=sqrt(3)/3=1/sqrt(3)`。这导致“1/sqrt(3)+(2v)/sqrt(3)=1”，我们发现“v=(sqrt(3)-1)/2”。

### 您如何找到该偏斜值？

重写 `1/sqrt(3)+(2v)/sqrt(3)=1->1+2v=sqrt(3)->2v=sqrt(3)-1->v=(sqrt(3)-1)/2`。

现在我们有两个倾斜值：`(3-sqrt(3))/6` 用于从正方形转换为三角形，`(sqrt(3)-1)/2` 用于从三角形转换为正方形。为了找到格点，我们必须在 `GetNoise4` 中应用后者，然后使用倾斜坐标来确定格点。

```csharp
			positions *= frequency;
			float4 skew = (positions.c0 + positions.c2) * ((sqrt(3f) - 1f) / 2f);
			float4 sx = positions.c0 + skew, sz = positions.c2 + skew;
			int4
				x0 = (int4)floor(sx), x1 = x0 + 1,
				z0 = (int4)floor(sz), z1 = z0 + 1;
```

![[images/simplex-noise/simplex-value-noise/2d-skewed.png]]

*坐标倾斜；频率 4.*

这会创建正确的晶格，但会弄乱内核，因为它们现在是根据倾斜的坐标计算的。我们必须将方形晶格点恢复为 `Kernel` 中的三角形，以便在原始空间中计算它们。为此，我们使用另一个倾斜值并从晶格坐标中减去倾斜，然后再从原始坐标中减去它们。这相当于在现有减法之后添加偏斜。

```csharp
			float4 unskew = (lx + lz) * ((3f - sqrt(3f)) / 6f);
			float4 x = positions.c0 - lx + unskew, z = positions.c2 - lz + unskew;
			float4 f = 1f - x * x - z * z;
```

这修复了内核形状，但结果是吹出的白色。问题是我们的核心影响力延伸得太远，因为三角形比正方形小。衰减应在与其中心角相对的边缘中点处达到零。我们可以通过将内核的起始强度降低到 0.5 来做到这一点。

```csharp
			float4 f = 0.5f - x * x - z * z;
```

### 为什么从一半强度开始？

等边三角形的高度为“h=(lsqrt(3))/2”，其中“l”是其边长。让我们使用`l=||b||`。

我们已经知道 `||b||^2=2v^2-2v+1` 和 `v=(3-sqrt(3))/6`。

计算“v^2=(9-6sqrt(3)+3)/36=(2-sqrt(3))/6”。

找到`||b||^2=(2-sqrt(3))/3-(3-sqrt(3))/3+1=1-1/3=2/3`和`||b||=sqrt(2/3)=sqrt(2)/sqrt(3)`。

因此`h=(||b||sqrt(3))/2=sqrt(2)/2=sqrt(1/2)`，这意味着衰减必须在平方距离0.5处达到零，这可以通过简单地使用`f(x,z)=1/2-x^2-z^2`来实现。

![[images/simplex-noise/simplex-value-noise/2d-unskewed.png]]

*玉米粒不歪斜，但很弱。*

内核现在具有正确的形状和大小，但它们非常弱，因为在它们的中心“f(0,0)=(1/2)^3=1/8”。这是通过放大衰减来补偿来解决的：“f(x,z)=8(1/2-x^2-z^2)^3”。

```csharp
			f = f * f * f * 8f;
```

![[images/simplex-noise/simplex-value-noise/2d-max-amplitude.png]]

*最大振幅；静止频率4*

在这种情况下，我们可以找到两个不同的振幅最小值：沿边缘的中点处的振幅最小值和每个三角形的中心处的振幅最小值。边缘最小值为“m_e=16/27~~0.593”，中心最小值为“m_c=1000/1944~~0.514”。

### 你如何找到这些最小值？

基于距离的衰减函数为“f(d)=8(1/2-d^2)^3”。我们知道边长`l=sqrt(2/3)=sqrt(2)/sqrt(3)`。

沿边的最小值为“m_e=2f(l/2)=16(1/2-2/12)^3=16/27”。

从角到等边三角形中心（也是其外心）的距离等于外接圆的半径“r=l/sqrt(3)=sqrt(2)/3”。

所以中心最小值是`m_c=3f(r)=24(1/2-2/9)^3=1000/1944`。

尽管我们的晶格和内核现已完成，但由于倾斜，与基于平方的版本相比，单纯形噪声变体似乎具有更高的频率。尽管这本身并不是问题，但它使得比较不同的噪声变体变得更加困难。因此，我们缩小频率，在 `GetNoise4` 的开头除以 √3。

```csharp
			positions *= frequency * (1f / sqrt(3f));
```

![[images/simplex-noise/simplex-value-noise/2d-scaled-frequency.png]]

*频率 4，缩放。*

### 这个比例因子从哪里来？

通过原点的 XZ 轴线对角线是唯一可以精确匹配正方形和三角形的格点的地方。沿该线的方格点之间的距离为√2。为了使三角形格点匹配，我们需要将它们缩放为 √2 除以三角形边长 `l=sqrt(2/3)=sqrt(2)/sqrt(3)`。因此，比例因子是“sqrt(2)/l=sqrt(3)”，这意味着我们必须将频率除以它。

我们通过包含梯度评估来完成二维单纯形值噪声。

```csharp
			return max(0f, f) * default(G).Evaluate(hash, x, z);
```

![[images/simplex-noise/simplex-value-noise/2d-simplex-value-1o.png]]

![[images/simplex-noise/simplex-value-noise/2d-regular-value-noise.png]]

![[images/simplex-noise/simplex-value-noise/2d-simplex-value-3o.png]]

![[images/simplex-noise/simplex-value-noise/2d-regular-value-3o.png]]

*2D 单纯形和正则值噪声；频率8； 1 和 3 个八度。*

与常规值噪声相比，单纯形变体会扭曲噪声模式以适应蜂窝格子的形状。它也较弱。在比较湍流变体时，模式差异最为明显。

![[images/simplex-noise/simplex-value-noise/2d-simplex-value-turbulence.png]]

![[images/simplex-noise/simplex-value-noise/2d-regular-value-turbulence.png]]

*二维单纯形和常规值湍流；频率4和3个八度。*

### 只有三个内核

尽管我们的 2D 单纯形值噪声在视觉上已经完成，但我们目前仍然忽略每个三角形仅需要三个内核。我们可以通过查看当前单独使用的四个内核来验证这一点。

![[images/simplex-noise/simplex-value-noise/2d-kernel-00.png]]

![[images/simplex-noise/simplex-value-noise/2d-kernel-01.png]]

![[images/simplex-noise/simplex-value-noise/2d-kernel-10.png]]

![[images/simplex-noise/simplex-value-noise/2d-kernel-11.png]]

*内核 00、01、10 和 11 相互隔离。*

核 00 和 11（沿着 XZ 对角线的核）对每个三角形都有贡献，而其他核仅影响一半的三角形。所以我们总是可以跳过 01 或 10 内核。让我们首先从 `GetNoise4` 中删除两者。

```csharp
			return default(G).EvaluateCombined(
				Kernel(h0.Eat(z0), x0, z0, positions) +
				//Kernel(h0.Eat(z1), x0, z1, positions) +
				//Kernel(h1.Eat(z0), x1, z0, positions) +
				Kernel(h1.Eat(z1), x1, z1, positions)
			);
```

![[images/simplex-noise/simplex-value-noise/2d-kernels-00-11.png]]

*仅内核 00 和 11。*

需要哪个第三核取决于样本点位于倾斜方格空间中 XZ 对角线的哪一侧。如果我们位于相对 X 坐标大于 Z 坐标的一侧，那么我们需要 10 内核，否则需要 01 内核。

![[images/simplex-noise/simplex-value-noise/2d-kernel-choice.png]]

*选择 01 或 10 内核。*

这是一个矢量化决策，适用于选择适当的 X 和 Z 晶格点。找到格点后，将相对倾斜的 X 是否超过 Z 直接存储在 `bool4` 变量中。

```csharp
			float4 sx = positions.c0 + skew, sz = positions.c2 + skew;
			int4
				x0 = (int4)floor(sx), x1 = x0 + 1,
				z0 = (int4)floor(sz), z1 = z0 + 1;

			bool4 xGz = sx - x0 > sz - z0;

			SmallXXHash4 h0 = hash.Eat(x0), h1 = hash.Eat(x1);
```

如果 X 大于 Z，则选择 `x1` 和 `z0`，否则选择 `x0` 和 `z1`。让我们通过 `xC` 和 `zC` 来跟踪我们的选择。

```csharp
			bool4 xGz = sx - x0 > sz - z0;
			int4 xC = select(x0, x1, xGz), zC = select(z1, z0, xGz);
```

这允许我们将变量第三个内核添加到我们的总和中。

```csharp
			return default(G).EvaluateCombined(
				Kernel(h0.Eat(z0), x0, z0, positions) +
				Kernel(h1.Eat(z1), x1, z1, positions) +
				Kernel(hash.Eat(xC).Eat(zC), xC, zC, positions)
			);
```

虽然这有效，但它需要我们向散列提供一个 X 格点，我们已经为这两个选项完成了这一点。理想情况下，我们可以选择 `h0` 或 `h1`，但我们不能使用现有的 `select` 方法，因为这会导致过早的哈希雪崩。因此，让我们添加一个公共静态 `SmallXXHash4.Select` 方法，该方法无需更改即可选择适当的累加器。

```csharp
	public static SmallXXHash4 Select (SmallXXHash4 a, SmallXXHash4 b, bool4 c) =>
		math.select(a.accumulator, b.accumulator, c);
```

现在我们可以为 `Simplex2D.GetNoise4` 中的第三个内核重用部分馈送的哈希值。

```csharp
			SmallXXHash4
				h0 = hash.Eat(x0), h1 = hash.Eat(x1),
				hC = SmallXXHash4.Select(h0, h1, xGz);

			return default(G).EvaluateCombined(
				Kernel(h0.Eat(z0), x0, z0, positions) +
				Kernel(h1.Eat(z1), x1, z1, positions) +
				Kernel(hC.Eat(zC), xC, zC, positions)
			);
```

### 3D 单纯形

生成 3D 单纯形晶格的工作方式与 2D 相同，但具有额外的维度。因此，我们不是将正方形变成菱形，而是将立方体变成菱形。变换为“[[x],[y],[z]]->[[x-v(x+y+z)],[y-v(x+y+z)],[z-v(x+y+z)]]”，其中“v”未知。

![[images/simplex-noise/simplex-value-noise/3d-skew-cube-rhombohedron.png]]

*从立方体倾斜到菱形。*

我们不是将正方形分割成两个三角形，而是通过按以下方式选择角将立方体分割成六个四面体：从 000 角开始，然后选择三个相邻角之一带有一个 1，然后选择两个相邻角之一带有两个 1，最后选择 111。这可以通过六种独特的方式完成，从而产生填充立方体的六个相同形状的四面体。

![[images/simplex-noise/simplex-value-noise/3d-six-tetrahedra.png]]

*一个立方体中有六个四面体。*

我们首先将 `Simplex2D.Kernel` 方法复制到 `Simplex3D` 并将其调整为适用于三个维度。由于我们尚不知道不倾斜因子，因此我们将其设置为零并使用与 2D 相同的衰减开始和比例。同样，我们最初只显示衰减函数，将梯度评估留到以后进行。

```csharp
	public struct Simplex3D<G> : INoise where G : struct, IGradient {

		…

		static float4 Kernel (
			SmallXXHash4 hash, float4 lx, float4 ly, float4 lz, float4x3 positions
		) {
			float4 unskew = (lx + ly + lz) * 0f;
			float4
				x = positions.c0 - lx + unskew,
				y = positions.c1 - ly + unskew,
				z = positions.c2 - lz + unskew;
			float4 f = 0.5f - x * x - y * y - z * z;
			f = f * f * f * 8f;
			return max(0f, f);
		}
	}
```

`GetNoise`的3D版本采用与2D版本相同的方法。这次我们从原始频率开始，将偏斜因子保留为零，并且仅包括 000 和 111 内核。由于它们位于 XYZ 对角线上，因此它们将成为每个四面体的一部分，而其他两个内核是可变的。

```csharp
		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			positions *= frequency;
			float4 skew = (positions.c0 + positions.c1 + positions.c2) * 0f;
			float4
				sx = positions.c0 + skew,
				sy = positions.c1 + skew,
				sz = positions.c2 + skew;
			int4
				x0 = (int4)floor(sx), x1 = x0 + 1,
				y0 = (int4)floor(sy), y1 = y0 + 1,
				z0 = (int4)floor(sz), z1 = z0 + 1;

			SmallXXHash4
				h0 = hash.Eat(x0), h1 = hash.Eat(x1);

			return default(G).EvaluateCombined(
				Kernel(h0.Eat(y0).Eat(z0), x0, y0, z0, positions) +
				Kernel(h1.Eat(y1).Eat(z1), x1, y1, z1, positions)
			);
		}
```

为了找到倾斜因子“v”，我们将查看具有角“a=[[0],[0],[0]]”、“b=[[1],[0],[0]]”、“c=[[1],[0],[1]]”和“d=[[1],[1],[1]]”的四面体。

就像三角形一样，我们可以通过使倾斜的“b”、“c”和“d”向量的边的平方长度相等来找到“v”。这导致倾斜因子为 frac13;。

```csharp
			float4 skew = (positions.c0 + positions.c1 + positions.c2) * (1f / 3f);
```

以及不偏斜因子 frac16;。

```csharp
		static float4 Kernel (
			SmallXXHash4 hash, float4 lx, float4 ly, float4 lz, float4x3 positions
		) {
			float4 unskew = (lx + ly + lz) * (1f / 6f);
			…
		}
```

![[images/simplex-noise/simplex-value-noise/3d-kernels-000-111.png]]

*3D 内核 000 和 111；频率 4.*

### 如何找到倾斜值和非倾斜值？

首先计算从立方体到菱面体的转换。

`||b||^2=(1-v)^2+2(-v)^2=3v^2-2v+1`。

`||c||^2=2(1-2v)^2+(-2v)^2=12v^2-8v+2`。

`||d||^2=3(1-3v)^2=27v^2-18v+3`。

首先尝试 `||b||^2=||c||^2->9v^2-6v+1=0->v=6/18=1/3`。如果我们使用它，那么`||d||^2=0`，所以这是立方体变平并变成平面的退化情况。这证明我们不能通过倾斜操作创建等边四面体。用等边四面体来平铺3D空间确实是不可能的。

其次，尝试`||b||^2=||d||^2=24v^2-16v+2=0->v=(2+-1)/6`，其中我们选择比简并情况小的那个，所以`v=1/6`。这导致`||b||^2=||d||^2=3/4`和`||c||^2=1`。所以我们有两个不同的平方长度，相差“1/4”。

第三，尝试`||c||^2=||d||^2=15v^2-10v+1=0->v=(5+-sqrt(10))/15`，我们再次选择较小的一个，因此`v=1/3-sqrt(2/5)/3`和`v^2=(7/5)/9-(2sqrt(2/5))/9`以便于计算。

这导致`||c||^2=||d||^2=6/5`和`||b||^2=4/5`，差异为`2/5`。

我们选择边缘差异最小的选项，因此“v=1/6”。

对于另一个方向的倾斜，我们考虑点“d”的变换。使用与三角形相同的逻辑，但在 3D 中，我们知道“x+3vx=1”和“x=1-3/6=1/2”。因此“1/2+(3v)/2=1->v=1/3”。

我们得到的是一个基于六个四面体组的晶格，这些四面体具有相同的形状但不同的方向。每个四面体都有 4 个长度为 √3/4 的边和两条长度为 1 的边。

![[images/simplex-noise/simplex-value-noise/3d-tetrahedron-skewed-unskewed.png]]

*四面体有倾斜的和未倾斜的。*

我们再次缩放频率，以便更容易比较噪声变量。在本例中，比例因子为 0.6。

```csharp
		public float4 GetNoise4 (float4x3 positions, SmallXXHash4 hash, int frequency) {
			positions *= frequency * 0.6f;
			…
		}
```

![[images/simplex-noise/simplex-value-noise/3d-scaled-frequency.png]]

*缩放频率，仍然是 4。*

### 这个比例因子从哪里来？

我们再次沿 XZ 轴线匹配晶格点。我们必须首先找到一个恰好落在该线上的 3D 晶格点（除了原点处的晶格点）。所以我们知道“x=z”并且需要找到一些偏向于零的“y”。

`y-(2x+y)/6=0->(5y)/6=x/3->y=(2x)/5`。这意味着每五步就有一个格点恰好位于 XZ 线上。

让我们选择“x=5”：“[[5-12/6],[2-12/6],[5-12/6]]=[[3],[0],[3]]”，距离原点为“sqrt(2(3^2))=3sqrt(2)”。

对于方形晶格，沿 XZ 线五步后的点是“[[5],[0],[5]]”，距离为“5sqrt(2)”。

因此，为了使晶格频率匹配，我们必须将单纯形距离除以平方距离来找到比例因子“(3sqrt(2))/(5sqrt(2))=3/5=0.6”。

为了使衰减函数正确，当它到达与其中心角相对的四面体面时，它应该达到零。这个距离是 √½，所以我们当前的衰减函数已经是正确的。

### 为什么衰减是一样的？

我们需要找到四面体的高度。它的所有面都是等腰三角形，有两条长度为“l_s=sqrt(3/4)”的短边和一条长度为“l_l=1”的长边。

我们的等腰三角形的高度是 `h=sqrt(4l_s^2-l_l^2)/2=sqrt(2)/2=sqrt(1/2)`。由于四面体的形状，这也是四面体本身的高度。因此，3D 晶格四面体的高度与 2D 晶格三角形的高度相同。

![[images/simplex-noise/simplex-value-noise/3d-tetrahedron-topology.png]]

*四面体拓扑，带有侧视图。*

### 四核

四面体有四个角，因此我们需要再选择两个核。需要哪些内核可以通过与我们在 2D 中找到变量内核类似的方式来确定，但现在是在三维中。我们通过沿着立方体的边缘行走来实现这一点，具体取决于哪个相对坐标最大。如果 X 大于 Y 和 Z，则我们从角 000 转到 100。之后，如果 Y 大于 Z，则转到 110，否则转到 101。每个四面体都有相似的模式。

![[images/simplex-noise/simplex-value-noise/3d-choosing-kernels.png]]

*分两步选择内核；大于号与行走方向相匹配。*

为此，我们只需检查三个比较即可：X 是否大于 Y、X 是否大于 Z 以及 Y 是否大于 Z。

```csharp
			int4
				x0 = (int4)floor(sx), x1 = x0 + 1,
				y0 = (int4)floor(sy), y1 = y0 + 1,
				z0 = (int4)floor(sz), z1 = z0 + 1;

			bool4
				xGy = sx - x0 > sy - y0,
				xGz = sx - x0 > sz - z0,
				yGz = sy - y0 > sz - z0;
```

通过这三个布尔检查，我们可以构建一个真值表，其中包含所有八种可能组合的行。对于每一行，我们还可以写下每个维度的第一个和第二个内核偏移量，零或一。

x>y

x>z

y>z

X

是

Z

时间

时间

时间

1 1

0 1

0 0

时间

时间

F

1 1

0 0

0 1

时间

F

时间

0 1

0 0

1 1

时间

F

F

0 1

0 0

1 1

F

时间

时间

0 1

1 1

0 0

F

时间

F

0 0

0 1

1 1

F

F

时间

0 0

1 1

0 1

F

F

F

0 0

0 1

1 1

因为我们无法在矢量化代码中进行分支，所以我们必须将其转换为每个维度的第一和第二偏移的独立选择标准。我们将使用 `xA` 布尔变量来跟踪第一个 X 偏移量是否为 1，并使用 `xB` 作为第二个 X 偏移量。我们将为 Y 和 Z 使用类似的变量。然后我们将真值表转换为布尔表达式并使用它们来设置变量。请注意，我们必须使用 `&` 运算符进行向量化布尔 AND，而不是通常的 `&&` 运算符。

```csharp
			bool4
				xGy = sx - x0 > sy - y0,
				xGz = sx - x0 > sz - z0,
				yGz = sy - y0 > sz - z0;

			bool4
				xA = xGy & xGz,
				xB = xGy | (xGz & yGz),
				yA = !xGy & yGz,
				yB = !xGy | (xGz & yGz),
				zA = (xGy & !xGz) | (!xGy & !yGz),
				zB = !(xGz & yGz);
```

使用它们来查找变量内核的格点选择。

```csharp
			bool4
				xA = xGy & xGz,
				xB = xGy | (xGz & yGz),
				yA = !xGy & yGz,
				yB = !xGy | (xGz & yGz),
				zA = (xGy & !xGz) | (!xGy & !yGz),
				zB = !(xGz & yGz);

			int4
				xCA = select(x0, x1, xA),
				xCB = select(x0, x1, xB),
				yCA = select(y0, y1, yA),
				yCB = select(y0, y1, yB),
				zCA = select(z0, z1, zA),
				zCB = select(z0, z1, zB);
```

然后将缺少的内核添加到总和中。在这种情况下，我们可以为 X 的两种选择重用馈送内核。

```csharp
			SmallXXHash4
				h0 = hash.Eat(x0), h1 = hash.Eat(x1),
				hA = SmallXXHash4.Select(h0, h1, xA),
				hB = SmallXXHash4.Select(h0, h1, xB);

			return default(G).EvaluateCombined(
				Kernel(h0.Eat(y0).Eat(z0), x0, y0, z0, positions) +
				Kernel(h1.Eat(y1).Eat(z1), x1, y1, z1, positions) +
				Kernel(hA.Eat(yCA).Eat(zCA), xCA, yCA, zCA, positions) +
				Kernel(hB.Eat(yCB).Eat(zCB), xCB, yCB, zCB, positions)
			);
```

![[images/simplex-noise/simplex-value-noise/3d-all-kernels.png]]

![[images/simplex-noise/simplex-value-noise/2d-scaled-frequency.png]]

*所有内核，无移位； 3D 和 2D。*

生成的内核图案看起来与 2D 单纯晶格类似，但由于其 3D 性质且不与 XZ 平面对齐，因此具有一些可变性。在这种情况下，我们可以找到多个不同的振幅最小值：在短边的中点`m_s=125/256~~0.488`，在长边的中点`m_l=1/4=0.25`，在三角形的外心`m_c=1029/4026~~0.256`，以及在四面体的外心`m_t=27/128~~0.211`。

### 你如何找到这些最小值？

基于距离的衰减函数又是“f(d)=8(1/2-d^2)^3”。

短边的最小值为“m_s=2f(l_s/2)=16(1/2-3/16)^3=16(5/16)^3=125/256”。

沿长边的最小值为“m_l=2f(1/2)=16(1/4)^3=1/4”。

角到等腰三角形中心的距离等于外接圆的半径`r=l_s^2/(2h)=(3sqrt(2))/8`。

所以三角形外心最小值是`m_c=3f(r)=24(1/2-9/32)^3=24(7/32)^3=1029/4026`

由等腰三角形构成的四面体的外接球半径为“r=sqrt((2l_s^2+l_l^2)/8)=sqrt(5/16)=sqrt(5)/4”。

所以四面体外心最小值是`m_t=4f(r)=32(1/2-5/16)^3=32(3/16)^3=27/128`。

在较高频率下更容易看到变异性。

![[images/simplex-noise/simplex-value-noise/3d-frequency-16.png]]

*频率16。*

有明显的对角线图案。这是 3D 倾斜的结果，因为 Z 维度上晶格点到样本平面的距离发生变化。该图案取决于 2D 切片的方向。例如，将单一维度中的无旋转与 45° 域旋转进行比较。

![[images/simplex-noise/simplex-value-noise/3d-rotation-x.png]]

![[images/simplex-noise/simplex-value-noise/3d-rotation-y.png]]

![[images/simplex-noise/simplex-value-noise/3d-rotation-z.png]]

*围绕 X、Y 和 Z 进行 45° 域旋转。*

另一个有趣的域旋转是围绕 X 和 Y 旋转 45°，这会对齐切片，以便我们可以沿着 XYZ 线直视。

![[images/simplex-noise/simplex-value-noise/3d-rotation-xy.png]]

*绕 X 和 Y 旋转 45°。*

最后，我们通过插入梯度评估来完成3D单纯形值噪声。

```csharp
			return max(0f, f) * default(G).Evaluate(hash, x, y, z);
```

![[images/simplex-noise/simplex-value-noise/3d-simplex-value.png]]

![[images/simplex-noise/simplex-value-noise/3d-simplex-value-rotated-x.png]]

![[images/simplex-noise/simplex-value-noise/3d-simplex-value-rotated-y.png]]

![[images/simplex-noise/simplex-value-noise/3d-simplex-value-rotated-z.png]]

*3D 单纯形值噪声，无旋转且绕 X、Y 和 Z 旋转 45°。*

![[images/simplex-noise/simplex-value-noise/3d-simplex-value-rotated-xy.png]]

![[images/simplex-noise/simplex-value-noise/3d-value-rotated-xy.png]]

*绕 X 和 Y 旋转 45°，单纯形和常规 3D 值噪声。*

![[images/simplex-noise/simplex-value-noise/3d-simplex-value-turbulence-rotated-xy.png]]

![[images/simplex-noise/simplex-value-noise/3d-value-turbulence-rotated-xy.png]]

*绕 X 和 Y 旋转 45°，单纯形和常规 3D 值湍流。*

![[images/simplex-noise/simplex-value-noise/3d-simplex-value-turbulence.png]]

![[images/simplex-noise/simplex-value-noise/2d-simplex-value-turbulence.png]]

*3D 和 2D 单纯形值湍流。*

![[images/simplex-noise/simplex-value-noise/3d-sphere-simplex-value.png]]

![[images/simplex-noise/simplex-value-noise/3d-sphere-value.png]]

*球体上的 3D 单纯形和常规值噪声。*

## 单纯形梯度噪声

为了生成单纯形梯度噪声，我们需要适当的梯度向量。我们已经有了 `Perlin` 结构类型，但我们基于正方形和八面体形状。我们这样做是因为它适用于方形和立方晶格并且避免了矢量归一化。然而，单纯形晶格不是轴对齐的，因此我们需要使用基于圆和球体的梯度来处理单纯形噪声。

### 基础渐变

正方形和圆形以及八面体和球体之间的唯一区别在于它们的向量是否被归一化。因此，我们不会重复矢量生成代码，而是将其放入嵌套的静态 `Noise.BaseGradients` 类中。我们也对线条渐变执行此操作，并以此开始，引入 `BaseGradients.Line` 方法并在 `Perlin` 中使用它。

```csharp
	public struct Perlin : IGradient {

		public float4 Evaluate (SmallXXHash4 hash, float4 x) =>
			//(1f + hash.Floats01A) * select(-x, x, ((uint4)hash & 1 << 8) == 0);
			BaseGradients.Line(hash, x);

		…
	}

	public static class BaseGradients {

		public static float4 Line (SmallXXHash4 hash, float4 x) =>
			(1f + hash.Floats01A) * select(-x, x, ((uint4)hash & 1 << 8) == 0);
	}
```

然后给出 `BaseGradients` 私有方法，在给定哈希的情况下生成并返回基于正方形或八面体的向量。

```csharp
		static float4x2 SquareVectors (SmallXXHash4 hash) {
			float4x2 v;
			v.c0 = hash.Floats01A * 2f - 1f;
			v.c1 = 0.5f - abs(v.c0);
			v.c0 -= floor(v.c0 + 0.5f);
			return v;
		}
		
		static float4x3 OctahedronVectors (SmallXXHash4 hash) {
			float4x3 g;
			g.c0 = hash.Floats01A * 2f - 1f;
			g.c1 = hash.Floats01D * 2f - 1f;
			g.c2 = 1f - abs(g.c0) - abs(g.c1);
			float4 offset = max(-g.c2, 0f);
			g.c0 += select(-offset, offset, g.c0 < 0f);
			g.c1 += select(-offset, offset, g.c1 < 0f);
			return g;
		}
```

使用这些方法可以实现 `Square`、`Circle`、`Octahedron` 和 `Sphere€` 梯度方法，无需任何缩放。

```csharp
		public static float4 Square (SmallXXHash4 hash, float4 x, float4 y) {
			float4x2 v = SquareVectors(hash);
			return v.c0 * x + v.c1 * y;
		}
	
		public static float4 Circle (SmallXXHash4 hash, float4 x, float4 y) {
			float4x2 v = SquareVectors(hash);
			return (v.c0 * x + v.c1 * y) * rsqrt(v.c0 * v.c0 + v.c1 * v.c1);
		}
	
		public static float4 Octahedron (
			SmallXXHash4 hash, float4 x, float4 y, float4 z
		) {
			float4x3 v = OctahedronVectors(hash);
			return v.c0 * x + v.c1 * y + v.c2 * z;
		}

		public static float4 Sphere€ (SmallXXHash4 hash, float4 x, float4 y, float4 z) {
			float4x3 v = OctahedronVectors(hash);
			return
				(v.c0 * x + v.c1 * y + v.c2 * z) *
				rsqrt(v.c0 * v.c0 + v.c1 * v.c1 + v.c2 * v.c2);
		}
```

然后在 `Perlin` 中使用 `Square` 和 `Octahedron` 方法，并在那里应用适当的缩放。

```csharp
		public float4 Evaluate (SmallXXHash4 hash, float4 x, float4 y) =>
			BaseGradients.Square(hash, x, y) * (2f / 0.53528f);
		
		public float4 Evaluate (SmallXXHash4 hash, float4 x, float4 y, float4 z) =>
			BaseGradients.Octahedron(hash, x, y, z) * (1f / 0.56290f);
```

### 单纯形梯度

现在我们可以创建一个使用直线、圆和球体基础渐变的 `Simplex` 渐变类型。我们暂时不缩放它们。

```csharp
	public struct Simplex : IGradient {

		public float4 Evaluate (SmallXXHash4 hash, float4 x) =>
			BaseGradients.Line(hash, x);

		public float4 Evaluate (SmallXXHash4 hash, float4 x, float4 y) =>
			BaseGradients.Circle(hash, x, y);

		public float4 Evaluate (SmallXXHash4 hash, float4 x, float4 y, float4 z) =>
			BaseGradients.Sphere€(hash, x, y, z);

		public float4 EvaluateCombined (float4 value) => value;
	}
```

为了能够可视化单纯形梯度噪声变体，请将它们的条目添加到 `NoiseVisualization.NoiseType`。

```csharp
	public enum NoiseType {
		Perlin€, PerlinTurbulence, Value€, ValueTurbulence,
		Simplex€, SimplexTurbulence, SimplexValue, SimplexValueTurbulence,
		VoronoiWorleyF1, VoronoiWorleyF2, VoronoiWorleyF2MinusF1,
		VoronoiChebyshevF1, VoronoiChebyshevF2, VoronoiChebyshevF2MinusF1
	}
```

还将它们添加到作业数组中的适当位置。

```csharp
		{
			Job<Simplex1D<Simplex>>.ScheduleParallel,
			Job<Simplex1D<Simplex>>.ScheduleParallel,
			Job<Simplex2D<Simplex>>.ScheduleParallel,
			Job<Simplex2D<Simplex>>.ScheduleParallel,
			Job<Simplex3D<Simplex>>.ScheduleParallel,
			Job<Simplex3D<Simplex>>.ScheduleParallel
		},
		{
			Job<Simplex1D<Turbulence<Simplex>>>.ScheduleParallel,
			Job<Simplex1D<Turbulence<Simplex>>>.ScheduleParallel,
			Job<Simplex2D<Turbulence<Simplex>>>.ScheduleParallel,
			Job<Simplex2D<Turbulence<Simplex>>>.ScheduleParallel,
			Job<Simplex3D<Turbulence<Simplex>>>.ScheduleParallel,
			Job<Simplex3D<Turbulence<Simplex>>>.ScheduleParallel
		},
```

这给了我们函数单纯形噪声，但我们仍然需要对其进行标准化。

### 一维单纯形噪声

为了归一化一维单纯形噪声，我们必须找到其未缩放的最大值。就像柏林噪声一样，只有当相邻内核的梯度彼此指向时才能达到最大值。因此，核的最大梯度函数可以描述为“m(x)=xf(x)=x(1-x^2)^3”。

![[images/simplex-noise/simplex-gradient-noise/1d-maximum.png]]

*相邻核的最大幅度及其总和。*

两个内核的总和在“x=1/2”时达到最大值。非标度噪声的最大幅度为“2m(1/2)=(3/4)^3=27/64”。但由于 `Line` 生成的可变因子最大为 2，因此我们必须将结果加倍。归一化因子是其倒数：“32/27”。将其包含在 `Simplex.Evaluate` 的 1D 版本中。

```csharp
		public float4 Evaluate (SmallXXHash4 hash, float4 x) =>
			BaseGradients.Line(hash, x) * (32f / 27f);
```

最终结果与一维柏林噪声非常相似。

![[images/simplex-noise/simplex-gradient-noise/1d-simplex.png]]

![[images/simplex-noise/simplex-gradient-noise/1d-perlin.png]]

*一维单纯形和 Perlin 噪声。*

### 2D 单纯形噪声

在二维中，我们有两个候选最大值，它们与衰减和的最小值一致：边的中点和三角形的中心。

边缘最大值为`(lm_e)/2=(sqrt(2)/(2sqrt(3)))(16/27)=(8sqrt(2))/(27sqrt(3))~~0.2419`。

中心最大值为`rm_c=(sqrt(2)/3)(1000/1944)=(1000sqrt(2))/5832~~0.2425`。

![[images/simplex-noise/simplex-gradient-noise/2d-maxima-visualization.png]]

*Maxima 用梯度可视化；白色最高。*

由于中心最大值是最大的，我们通过使用“1/(lm_c)=5832/(1000sqrt(2))”缩放来标准化 2D 单纯形噪声。

```csharp
		public float4 Evaluate (SmallXXHash4 hash, float4 x, float4 y) =>
			BaseGradients.Circle(hash, x, y) * (5.832f / sqrt(2f));
```

![[images/simplex-noise/simplex-gradient-noise/2d-simplex.png]]

![[images/simplex-noise/simplex-gradient-noise/2d-perlin.png]]

*2D 单纯形和 Perlin 噪声。*

![[images/simplex-noise/simplex-gradient-noise/2d-simplex-turbulence.png]]

![[images/simplex-noise/simplex-gradient-noise/2d-perlin-turbulence.png]]

*2D 单纯形和 Perlin 湍流噪声。*

### 3D 单纯形噪声

为了标准化 3D 梯度，我们首先计算短边最大值 `(l_sm_s)/2=(125sqrt(3))/1024~~0.2114`。

其次，其中间的长边最大值为“(l_lm_l)/2=1/8=0.125”。事实上，它的内核相距很远，以至于它有两个最大值，而不是中间的一个。但我们不需要计算这些，因为它们保证小于短边最大值。

![[images/simplex-noise/simplex-gradient-noise/3d-maxima-long-edge.png]]

*沿长边有两个最大值。*

面三角形和四面体内部也没有单一最大值，内核相距太远。没有任何地方超过短边最大值。

![[images/simplex-noise/simplex-gradient-noise/3d-maxima-visualization.png]]

*Maxima 用梯度可视化；白色最高。*

因此，我们的归一化因子是“2/(l_sm_s)=1024/(125sqrt(3))”。

```csharp
		public float4 Evaluate (SmallXXHash4 hash, float4 x, float4 y, float4 z) =>
			BaseGradients.Sphere(hash, x, y, z) * (1024f / (125f * sqrt(3f)));
```

![[images/simplex-noise/simplex-gradient-noise/3d-simplex.png]]

![[images/simplex-noise/simplex-gradient-noise/3d-perlin.png]]

![[images/simplex-noise/simplex-gradient-noise/3d-simplex-rotated-xy.png]]

![[images/simplex-noise/simplex-gradient-noise/3d-perlin-rotated-xy.png]]

*3D 单纯形和 Perlin 噪声；无旋转和 45° XY 旋转。*

![[images/simplex-noise/simplex-gradient-noise/3d-simplex-turbulence.png]]

![[images/simplex-noise/simplex-gradient-noise/3d-perlin-turbulence.png]]

![[images/simplex-noise/simplex-gradient-noise/3d-simplex-turbulence-rotated-xy.png]]

![[images/simplex-noise/simplex-gradient-noise/3d-perlin-turbulence-rotated-xy.png]]

*3D 单纯形和 Perlin 噪声；无旋转和 45° XY 旋转。*

![[images/simplex-noise/simplex-gradient-noise/3d-sphere-simplex.png]]

![[images/simplex-noise/simplex-gradient-noise/3d-sphere-perlin.png]]

*球体上的 3D 单纯形和 Perlin 噪声。*

想知道下一个教程什么时候发布？密切关注我的 [Patreon](https://www.patreon.com/catlikecoding) 页面！

执照

存储库

PDF

---

## 署名与许可

- 原作者：Jasper Flick（Catlike Coding）
- 原文：[Simplex 噪声](https://catlikecoding.com/unity/tutorials/pseudorandom-noise/simplex-noise/)
- 网站许可说明：[https://catlikecoding.com/license/](https://catlikecoding.com/license/)
- 本文为英文教程的完整中文翻译与 Markdown 整理，代码片段保持原样，图示已下载并本地嵌入。
- 教程正文及配图按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可分享；本译文沿用相同许可。
- 教程中的代码与项目素材按原作者声明采用 MIT-0。
