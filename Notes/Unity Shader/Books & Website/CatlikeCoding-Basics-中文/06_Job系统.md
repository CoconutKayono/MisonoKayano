# Job 系统（Jobs）

*让分形动起来（Animating a Fractal）*

> 本教程由 Catlike Coding 的 [Jasper Flick](https://catlikecoding.com/) 撰写，原文地址：[Jobs](https://catlikecoding.com/unity/tutorials/basics/jobs/)。本文为简体中文翻译版，代码保留原文，仅翻译讲解文字。

- 用对象层级构建一个分形。
- 展平层级。
- 摆脱游戏对象，改为程序化绘制。
- 用 Job 更新分形。
- 并行更新分形的各个部分。

这是关于学习 Unity 基础知识的系列教程中的第六篇。这次我们将创建一个动画分形。我们从一个常规的游戏对象层级开始，然后慢慢过渡到 Job 系统，一路上测量性能。

本教程使用 Unity 2020.3.6f1 制作。

![由 97,656 个球体构成的分形。](https://catlikecoding.com/unity/tutorials/basics/jobs/tutorial-image.jpg)

## 分形

一般来说，分形是某种具有自相似性的东西，简单说就是它的较小部分看起来与较大部分相似。例子有海岸线和许多植物。例如一棵树的树枝可以看起来像树干，只是更小。同样，它的小枝看起来像树枝的小号版本。还有数学和几何分形。一些例子包括曼德博（Mandelbrot）集合和朱利亚（Julia）集合、科赫雪花、门格尔海绵，以及谢尔宾斯基三角形。

几何分形可以通过从一个初始形状开始、然后把它的更小副本附着到自身上来构造，这些副本随后又生成它们自己的更小版本，依此类推。理论上这可以永远进行下去，创建出数量无限的形状，却占据有限的空间。我们可以在 Unity 里创建类似的东西，但只能深到几个层级，之后性能就会退化得太厉害。

我们将在[上一篇教程](05_计算着色器.md)的同一个项目里创建分形，只是不用图表。

### 创建分形

先创建一个 `Fractal` 组件类型来表示我们的分形。给它一个可配置的深度整数来控制分形的最大深度。最小深度是一，那将只由初始形状构成。最大值我们用八，这相当高了，但不至于高到意外让你的机器失去响应。深度四是一个合理的默认值。

```diff
+using UnityEngine;

+public class Fractal : MonoBehaviour {

+	[SerializeField, Range(1, 8)]
+	int depth = 4;
+}
```

我们用球体作为初始形状，可以通过 *GameObject / 3D Object / Sphere* 创建。把它放在世界原点，把分形组件附加到它上面，并给它一个简单材质。我把它做成黄色，最初使用 URP。从它上面移除 `SphereCollider` 组件，让游戏对象尽可能简单。

![分形 Inspector。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/fractal-inspector.png)

要把球体变成分形，我们必须生成它的克隆体。这可以通过调用 `Instantiate` 方法、以自身作为参数来完成。要传入对 `Fractal` 实例自身的引用，我们可以用 `this` 关键字，所以我们将调用 `Instantiate(this)`，进入运行模式后用它生成分形。

我们本可以在 `Awake` 方法里克隆分形，但那样克隆体的 `Awake` 方法也会立即被调用，立即创建另一个实例，依此类推。这会一直继续直到 Unity 崩溃，因为它递归地调用了太多方法，而且这发生得非常快。

要避免立即递归，我们可以改为添加一个 `Start` 方法，在里面调用 `Instantiate`。`Start` 是另一个 Unity 事件方法，像 `Awake` 一样也在组件创建后被调用一次。区别是 `Start` 不是立即被调用，而是在组件的 `Update` 方法第一次被调用之前——无论它有没有 `Update`。在那时创建的新组件会在下一帧得到它们的第一次更新。这意味着实例化每帧只发生一次。

```diff
+	void Start () {
+		Instantiate(this);
+	}
```

如果现在进入运行模式，你会看到每一帧都创建一个新克隆体。先是原始分形的一个克隆体，然后是第一个克隆体的克隆体，再然后是第二个克隆体的克隆体，依此类推。这个过程只有到你的机器内存耗尽才会停止，所以你应该在那之前退出运行模式。

![创建无限克隆体。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/infinite-clones.png)

要强制执行最大深度，我们必须在达到最大深度时中止实例化。最直接的做法是给生成的子分形递减配置的深度。

```diff
	void Start () {
+		Fractal child = Instantiate(this);
+		child.depth = depth - 1;
	}
```

然后我们可以在 `Start` 开头检查深度是否为 1 或更小。如果是，我们就不该再深入，中止方法。我们可以通过从中返回来实现，孤立地使用 `return` 语句，因为这是一个 `void` 方法，不返回任何东西。

```diff
	void Start () {
+		if (depth <= 1) {
+			return;
+		}

		Fractal child = Instantiate(this);
		child.depth = depth - 1;
	}
```

为了容易看出配置的深度确实对每个新子分形递减，把它们的 `name` 属性设为 *Fractal* 后跟一个空格和深度。整数可以通过加法运算符追加到文本字符串后面。这会生成数字的文本表示，然后是一个新的拼接字符串。

```diff
	void Start () {
+		name = "Fractal " + depth;

		…
	}
```

![深度递减的四个分形层级。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/four-levels.png)

深度确实逐级递减，创建了正确数量的克隆体后过程停止。要让新分形成为其直接父分形的真正子级，我们必须把它们的父级设为生成它们的那个分形。

```diff
		Fractal child = Instantiate(this);
		child.depth = depth - 1;
+		child.transform.SetParent(transform, false);
```

![分形层级。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/fractal-hierarchy.png)

这给了我们一个简单的游戏对象层级，但它看起来仍像一个球体，因为它们全部重叠。要改变这一点，把子级变换的 local position 设为 `Vector3.right`。这把它放在父级右侧一个单位处，所以我们所有的球体最终沿 X 轴排成一行并相互接触。

```diff
		child.transform.SetParent(transform, false);
+		child.transform.localPosition = Vector3.right;
```

![排成一行的球体。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/spheres-in-a-row.png)

自相似性的思想是，较小部分看起来像较大部分，所以每个子级都应该比它的父级小。我们直接把它的尺寸减半，把它的 local scale 设为均匀的 0.5。因为缩放也作用于子级，这意味着层级每向下一步，尺寸就减半。

```diff
		child.transform.localPosition = Vector3.right;
+		child.transform.localScale = 0.5f * Vector3.one;
```

![尺寸递减的球体。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/spheres-decreasing-size.png)

要让球体再次接触，我们必须减小它们的偏移。父级和子级的本地半径原来都是 0.5，所以偏移 1 让它们接触。由于子级的尺寸减半了，它的本地半径现在是 0.25，所以偏移应减小到 0.75。

```diff
		child.transform.localPosition = 0.75f * Vector3.right;
		child.transform.localScale = 0.5f * Vector3.one;
```

![相互接触的球体。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/spheres-touching.png)

### 多个子级

每层只生成一个子级，产生一排尺寸递减的球体，这不是一个有趣的分形。所以让我们每步加第二个子级，复制创建子级的代码，复用 `child` 变量。唯一的区别是，额外的子级我们用 `Vector3.up`，它把子级放在父级上方而不是右侧。

```diff
		Fractal child = Instantiate(this);
		child.depth = depth - 1;
		child.transform.SetParent(transform, false);
		child.transform.localPosition = 0.75f * Vector3.right;
		child.transform.localScale = 0.5f * Vector3.one;

+		child = Instantiate(this);
+		child.depth = depth - 1;
+		child.transform.SetParent(transform, false);
+		child.transform.localPosition = 0.75f * Vector3.up;
+		child.transform.localScale = 0.5f* Vector3.one;
```

预期是每个分形部分现在都有两个子级，最多四层深。

![带多个子级的球体，错误](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/spheres-multiple-children-incorrect.png)

看起来并不是这样。我们在分形顶部得到了过多的层级。这是因为当我们克隆一个分形来创建它的第二个子级时，我们已经给了它第一个子级。这个子级现在也被克隆了，因为 `Instantiate` 复制传给它的整个游戏对象层级。

解决方案是，在两个子级都创建之后才建立父子关系。为了让这更容易，让我们把创建子级的代码移到一个单独的 `CreateChild` 方法里，它返回子分形。它做的一切都相同，只是不设置父级，并且偏移方向变成一个参数。

```diff
+	Fractal CreateChild (Vector3 direction) {
+		Fractal child = Instantiate(this);
+		child.depth = depth - 1;
+		child.transform.localPosition = 0.75f * direction;
+		child.transform.localScale = 0.5f * Vector3.one;
+		return child;
+	}
```

从 `Start` 移除创建子级的代码，改为调用 `CreateChild` 两次，以向上和向右向量作为参数。用变量记录子级，然后用它们在之后设置父级。

```diff
	void Start () {
		name = "Fractal " + depth;

		if (depth <= 1) {
			return;
		}

+		Fractal childA = CreateChild(Vector3.up);
+		Fractal childB = CreateChild(Vector3.right);

+		childA.transform.SetParent(transform, false);
+		childB.transform.SetParent(transform, false);
	}
```

![带多个子级的球体，正确](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/spheres-multiple-children-correct.png)

### 重新定向

现在我们得到一个每个部分正好两个子级的分形，除了最大深度处没有任何子级的最小部分。这些子级总是以相同方式定位：一个在上、一个在右。然而，分形子级附着在父级上，可以看作是从父级生长出来的。所以它们的朝向也相对于父级是有道理的。对子级来说，父级就是地面，这使它的偏移方向等于它的本地向上轴。

我们可以通过添加一个 `Quaternion` 来支持每个部分不同的朝向，把它赋给子级的 local rotation，使它的朝向相对于父级的朝向。

```diff
	Fractal CreateChild (Vector3 direction, Quaternion rotation) {
		Fractal child = Instantiate(this);
		child.depth = depth - 1;
		child.transform.localPosition = 0.75f * direction;
+		child.transform.localRotation = rotation;
		child.transform.localScale = 0.5f * Vector3.one;
		return child;
	}
```

在 `Start` 里，第一个子级位于父级上方，所以它的朝向不变。我们可以用 `Quaternion.identity` 来表示，即表示无旋转的单位四元数。第二个子级在右侧，所以我们必须让它绕 Z 轴顺时针旋转 90°。我们可以通过静态的 `Quaternion.Euler` 方法来做，它根据沿 X、Y 和 Z 轴的欧拉角创建旋转。前两个轴传零，Z 传 −90°。

```diff
		Fractal childA = CreateChild(Vector3.up, Quaternion.identity);
		Fractal childB = CreateChild(Vector3.right, Quaternion.Euler(0f, 0f, -90f));
```

![重新定向的分形子级。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/spheres-reoriented.png)

### 完成分形

让我们继续生长分形，加第三个子级，这次偏移到左侧，绕 Z 轴旋转 90°。这完成了我们在 XY 平面上的分形。

```diff
		Fractal childA = CreateChild(Vector3.up, Quaternion.identity);
		Fractal childB = CreateChild(Vector3.right, Quaternion.Euler(0f, 0f, -90f));
+		Fractal childC = CreateChild(Vector3.left, Quaternion.Euler(0f, 0f, 90f));

		childA.transform.SetParent(transform, false);
		childB.transform.SetParent(transform, false);
+		childC.transform.SetParent(transform, false);
```

![2D 分形。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/fractal-2d.png)

> **我们也能加一个向下偏移的子级吗？**
>
> 可以，但这只对根分形部分有意义，因为在其他所有情况下，子级最终会藏进它父级的父级里。为了简单，我不给根单独加一个额外子级。

通过再加两个子级，把分形带进第三维，偏移为向前和向后，外加绕 X 轴 90° 和 −90° 的旋转。

```diff
		Fractal childA = CreateChild(Vector3.up, Quaternion.identity);
		Fractal childB = CreateChild(Vector3.right, Quaternion.Euler(0f, 0f, -90f));
		Fractal childC = CreateChild(Vector3.left, Quaternion.Euler(0f, 0f, 90f));
+		Fractal childD = CreateChild(Vector3.forward, Quaternion.Euler(90f, 0f, 0f));
+		Fractal childE = CreateChild(Vector3.back, Quaternion.Euler(-90f, 0f, 0f));

		childA.transform.SetParent(transform, false);
		childB.transform.SetParent(transform, false);
		childC.transform.SetParent(transform, false);
+		childD.transform.SetParent(transform, false);
+		childE.transform.SetParent(transform, false);
```

![3D 分形。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/fractal-3d.png)

一旦你确定分形是正确的，可以试试配置更大的深度，比如六。

![深度 6 分形。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/fractal-depth-6.png)

在这个深度，你会注意到分形所描述的棱锥的侧面显示出谢尔宾斯基三角形的图案。使用正交投影时最容易看到。

![谢尔宾斯基三角形图案。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/sierpinski-triangle-pattern.png)

### 动画

我们可以通过给它加动画让分形活起来。创造无穷运动最简单的方式是让每个部分沿它本地向上轴旋转，放在一个新的 `Update` 方法里。这可以通过在分形的 `Transform` 组件上调用 `Rotate` 来完成。这应用一个随时间累积的旋转，让它旋转起来。如果第二个参数用 `Time.deltaTime`、另外两个用零，那么最终的旋转速度是每秒一度。让我们把它放大到每秒 22.5°，这样 16 秒完成一次完整的 360° 旋转。由于分形的四面对称，这个动画看起来每四秒循环一次。

```diff
+	void Update () {
+		transform.Rotate(0f, 22.5f * Time.deltaTime, 0f);
+	}
```

动画分形。

分形的每个部分都以完全相同的方式旋转，但由于整个分形的递归性质，这产生了一种越深越复杂的运动。

### 性能

我们的动画分形可能是个好主意，但它的运行速度也应该足够快。深度小于六的分形应该没问题，但更高就可能出问题。所以我分析了一些构建产物。

![用 URP 和分形深度 6 分析构建产物。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/profiler-build-urp-depth-6.png)

我分别分析了深度为 6、7、8 的分形构建产物。我得到了每帧调用 `Update` 方法所花平均毫秒数的大致估计，以及 URP 和 BRP 的平均每秒帧数。我关掉 VSync，以便最好地感受它在我的机器上究竟能跑多快。我还用了 *IL2CPP* 而不是 *Mono* 作为 *Scripting Backend*，它位于 player 项目设置的 *Other Settings / Configuration* 下。

> **Mono 和 IL2CPP 的区别是什么？**
>
> 后者通常生成比 Mono 运行时环境所能提供的更优化的原生代码。

| Depth | MS | URP | BRP |
|---|---|---|---|
| 6 | 2 | 125 | 80 |
| 7 | 8 | 24 | 15 |
| 8 | 40 | 4 | 3 |

结果是深度 6 没问题，但我的机器在深度 7 时就很吃力，而深度 8 是一场灾难。太多时间花在调用 `Update` 方法上。仅此一项就会把帧率限制在最高 25FPS，但最终结果差得多——URP 是 4，BRP 是 3。

Unity 的默认球体有很多顶点，所以试着做同样的实验、但把分形的网格换成渲染便宜得多的立方体是有道理的。做完之后我发现得到相同的结果，这表明瓶颈是 CPU，不是 GPU。

![用立方体代替球体的深度 6 分形。](https://catlikecoding.com/unity/tutorials/basics/jobs/fractal/fractal-depth-6-cubes.png)

注意，使用立方体时分形自相交，因为立方体比球体伸出得多得多。深度 4 处的一些部分最终会碰到第 1 级的根。那些部分向上的子级最终会穿入根，而该层级其他的会碰到第 2 级的部分，依此类推。

## 展平层级

我们分形的递归层级、以及它所有独立移动的部分，是 Unity 很吃力处理的东西。它必须孤立地更新各部分，计算它们的对象到世界转换矩阵，然后裁剪它们，最后用 GPU 实例化或 SRP Batcher 渲染它们。因为我们确切知道分形如何工作，我们可以用比 Unity 通用方法更高效的策略。通过简化层级、去掉它的递归性质，我们也许能提高性能。

### 清理

重构分形层级的第一步是移除当前方法。删除 `Start`、`CreateChild` 和 `Update` 方法。

```diff
-	//void Start () { … }

-	//Fractal CreateChild (Vector3 direction, Quaternion rotation) { … }

-	//void Update () { … }
```

不再复制根游戏对象，我们把它用作所有分形部分的根容器。所以从分形游戏对象上移除 `MeshFilter` 和 `MeshRenderer` 组件。然后给 `Fractal` 添加网格和材质的配置字段。通过 Inspector 把它们设为我们之前用的球体和材质。

```diff
+	[SerializeField]
+	Mesh mesh;

+	[SerializeField]
+	Material material;
```

![调整过的分形游戏对象。](https://catlikecoding.com/unity/tutorials/basics/jobs/flat-hierarchy/adjusted-fractal.png)

我们会对分形部分使用相同的方向和旋转。这次我们把这些存储在静态数组里，方便以后访问。

```diff
+	static Vector3[] directions = {
+		Vector3.up, Vector3.right, Vector3.left, Vector3.forward, Vector3.back
+	};

+	static Quaternion[] rotations = {
+		Quaternion.identity,
+		Quaternion.Euler(0f, 0f, -90f), Quaternion.Euler(0f, 0f, 90f),
+		Quaternion.Euler(90f, 0f, 0f), Quaternion.Euler(-90f, 0f, 0f)
+	};
```

### 创建部分

现在我们要重新审视如何创建一个部分。为此添加一个新的 `CreatePart` 方法，最初是一个无参数的 void 方法。

```diff
+	void CreatePart () {}
```

在 `Awake` 方法里调用它。这次我们不需要防范无限递归，所以不必等到 `Start`。

```diff
+	void Awake () {
+		CreatePart();
+	}
```

我们将在 `CreatePart` 里手动构造一个新的游戏对象。做法是调用 `GameObject` 构造方法。通过传入字符串参数给它 *Fractal Part* 这个名字。用一个变量记录它，然后让分形根成为它的父级。

```diff
	void CreatePart () {
+		var go = new GameObject("Fractal Part");
+		go.transform.SetParent(transform, false);
	}
```

![带第一个部分的分形。](https://catlikecoding.com/unity/tutorials/basics/jobs/flat-hierarchy/first-fractal-part.png)

这给了我们一个只有 `Transform` 组件、什么都没有的游戏对象。要让它可见，我们必须给它加更多组件，通过在游戏对象上调用 `AddComponent` 来实现。先做一次。

```diff
		var go = new GameObject("Fractal Part");
		go.transform.SetParent(transform, false);
+		go.AddComponent();
```

`AddComponent` 是一个泛型方法，可以添加任何类型的组件。它像方法的模板，为每种需要的组件类型都有一个特定版本。我们通过在方法名后、尖括号内追加想要的类型来指定。对 `MeshFilter` 这么做。

```diff
		go.AddComponent<MeshFilter>();
```

这给游戏对象添加了一个 `MeshFilter`，它也被返回了。我们需要把网格赋给它的 `mesh` 属性，可以直接在方法调用的结果上做。

```diff
		go.AddComponent<MeshFilter>().mesh = mesh;
```

对 `MeshRenderer` 组件做同样的事，设置它的材质。

```diff
		go.AddComponent<MeshFilter>().mesh = mesh;
+		go.AddComponent<MeshRenderer>().material = material;
```

我们的分形部分现在会被渲染了，所以进入运行模式后会出现一个球体。

### 存储信息

不让每个部分自己更新，我们改为从带有 `Fractal` 组件的单个根对象控制整个分形。这对 Unity 容易得多，因为它只需管理一个更新的游戏对象，而不是潜在的成千上万个。但要做到这点，我们需要在单个 `Fractal` 组件里记录所有部分的数据。

我们至少需要知道部分的方向和旋转。我们可以通过把它们存储在数组里来记录。但与其为向量和四元数分别用数组，我们通过创建一个新的 `FractalPart` 结构体类型把它们分组在一起。这像定义类，只是用 `struct` 关键字而不是 `class`。因为我们只会在 `Fractal` 内部需要这个类型，把它定义在那个类内部，连同它的字段。出于同样的原因，不要把它设为 public。

```diff
public class Fractal : MonoBehaviour {

+	struct FractalPart {
+		Vector3 direction;
+		Quaternion rotation;
+	}

	…
}
```

这个类型将作为打包在一起、被当作单个值（而非对象）处理的简单数据容器。要让 `Fractal` 里的其他代码能访问这个嵌套类型里的字段，它们需要被设为 public。注意，这只在 `Fractal` 内部暴露这些字段，因为结构体本身在 `Fractal` 内部是私有的。

```diff
	struct FractalPart {
+		public Vector3 direction;
+		public Quaternion rotation;
	}
```

为了正确定位、旋转和缩放一个分形部分，我们需要访问它的 `Transform` 组件，所以也给结构体加一个引用它的字段。

```diff
	struct FractalPart {
		public Vector3 direction;
		public Quaternion rotation;
+		public Transform transform;
	}
```

现在我们可以在 `Fractal` 内部定义一个分形部分数组的字段。

```diff
+	FractalPart[] parts;
```

虽然可以把所有部分放进单个大数组，但我们改为让同一层级的所有部分拥有各自的数组。这让以后处理层级更容易。我们通过把 `parts` 字段变成数组的数组来记录所有这些数组。这种数组的元素类型是 `FractalPart[]`，所以它自己的类型定义为该类型后跟一对空方括号，像任何其他数组一样。

```diff
	FractalPart[][] parts;
```

在 `Awake` 开头创建这个新的顶层数组，其大小等于分形深度。这种情况下大小声明在第一对方括号里，第二对留空。

```diff
	void Awake () {
+		parts = new FractalPart[depth][];

		CreatePart();
	}
```

每个层级得到自己的数组，分形只有单个部分的根层级也是。所以先为单个元素创建一个新的 `FractalPart` 数组，把它赋给第一层。

```diff
		parts = new FractalPart[depth][];
+		parts[0] = new FractalPart[1];
```

之后我们必须为其他层级创建数组。每一层是前一层大小的五倍，因为我们给部分五个子级。把层级数组的创建变成一个循环，记录数组长度，并在每次迭代末尾乘以五。

```diff
		parts = new FractalPart[depth][];
+		int length = 1;
+		for (int i = 0; i < parts.Length; i++) {
			parts[i] = new FractalPart[length];
+			length *= 5;
+		}
```

因为长度是整数，且我们只在循环内使用它，我们可以把它合并进 `for` 语句，把初始化和调整部分变成逗号分隔的列表。

```diff
		parts = new FractalPart[depth][];
-		//int length = 1;
		for (int i = 0, length = 1; i < parts.Length; i++, length *= 5) {
			parts[i] = new FractalPart[length];
-			//length *= 5;
		}
```

| 层级 | 部分数 | 累计 |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 5 | 6 |
| 3 | 25 | 31 |
| 4 | 125 | 156 |
| 5 | 625 | 781 |
| 6 | 3,125 | 3,906 |
| 7 | 15,625 | 19,531 |
| 8 | 78,125 | 97,656 |

### 创建所有部分

要检查我们是否正确创建部分，给 `CreatePart` 加一个层级索引参数，并把它追加到部分的名字里。注意层级索引从零开始并递增，而之前方法里我们递减子级的配置深度。

```diff
	void CreatePart (int levelIndex) {
		var go = new GameObject("Fractal Part " + levelIndex);
		…
	}
```

第一个部分的层级索引传零。然后跟着一个遍历所有层级的循环，从索引 1 开始，因为我们先显式做了顶层的那单个部分。我们要嵌套循环，所以给层级迭代变量用更具体的名字，比如 `li`。

```diff
	void Awake () {
		…

		CreatePart(0);
+		for (int li = 1; li < parts.Length; li++) {}
	}
```

每次层级迭代，先存储该层 parts 数组的引用。然后遍历该层的所有部分并创建它们，这次分形部分迭代变量用 `fpi` 这样的名字。

```diff
		for (int li = 1; li < parts.Length; li++) {
+			FractalPart[] levelParts = parts[li];
+			for (int fpi = 0; fpi < levelParts.Length; fpi++) {
+				CreatePart(li);
+			}
		}
```

![所有分形部分，按层创建。](https://catlikecoding.com/unity/tutorials/basics/jobs/flat-hierarchy/all-fractal-parts.png)

因为子级有不同的方向和旋转，我们需要区分它们。做法是给 `CreatePart` 加一个子级索引，我们也可以把它加进游戏对象的名字。

```diff
	void CreatePart (int levelIndex, int childIndex) {
		var go = new GameObject("Fractal Part L" + levelIndex + " C" + childIndex);
		…
	}
```

根部分不是另一个部分的子级，所以我们用索引零，因为它可以看作是地面的向上子级。

```diff
		CreatePart(0, 0);
```

在每层的循环里，我们必须循环五个子级索引。我们可以通过每次迭代递增子级索引、并在合适时重置为零来做。或者，我们可以在另一个嵌套循环里显式创建五个子级。这要求我们每次迭代把分形部分索引增加五，而不是只加一。

```diff
		for (int li = 1; li < parts.Length; li++) {
			FractalPart[] levelParts = parts[li];
			for (int fpi = 0; fpi < levelParts.Length; fpi += 5) {
+				for (int ci = 0; ci < 5; ci++) {
					CreatePart(li, ci);
+				}
			}
		}
```

![同时显示层级和子级索引。](https://catlikecoding.com/unity/tutorials/basics/jobs/flat-hierarchy/parts-level-child-index.png)

我们还必须确保各部分有正确的尺寸。同一层的所有部分有相同的缩放，且不改变。所以我们只需在创建每个部分时设置一次。给 `CreatePart` 加一个参数，用它设置均匀缩放。

```diff
	void CreatePart (int levelIndex, int childIndex, float scale) {
		var go = new GameObject("Fractal Part L" + levelIndex + " C" + childIndex);
+		go.transform.localScale = scale * Vector3.one;
		…
	}
```

根部分的缩放是 1。之后缩放每层减半。

```diff
+		float scale = 1f;
		CreatePart(0, 0, scale);
		for (int li = 1; li < parts.Length; li++) {
+			scale *= 0.5f;
			FractalPart[] levelParts = parts[li];
			for (int fpi = 0; fpi < levelParts.Length; fpi += 5) {
				for (int ci = 0; ci < 5; ci++) {
					CreatePart(li, ci, scale);
				}
			}
		}
```

### 重建分形

要重建分形的结构，我们必须直接定位所有部分，这次在世界空间。因为我们不使用变换层级，位置会随着分形动画而改变，所以我们要在 `Update` 里不断设置它们，而不是在 `Awake`。但首先我们需要存储各部分的数据。

先把 `CreatePart` 改成返回一个新的 `FractalPart` 结构体值。

```diff
+	FractalPart CreatePart (int levelIndex, int childIndex, float scale) {
		…

+		return new FractalPart();
	}
```

然后用它的子级索引和静态数组设置部分的方向和旋转，以及它的游戏对象的 `Transform` 组件的引用。我们可以通过把新部分存进变量、设置它的字段、然后返回它来做。另一种做同样事情的方式是使用对象或结构体初始化器。这是一个花括号内的列表，跟在构造方法调用的参数列表后面。

```diff
		return new FractalPart() {};
```

我们可以把对任何被创建对象的字段或属性的赋值放进里面，作为逗号分隔的列表。

```diff
		return new FractalPart() {
+			direction = directions[childIndex],
+			rotation = rotations[childIndex],
+			transform = go.transform
		};
```

而如果构造方法调用没有参数，且我们包含初始化器，就允许跳过空的参数列表。

```diff
-		//return new FractalPart() {
+		return new FractalPart {
			…
		};
```

在 `Awake` 里把返回的部分复制到正确的数组元素。根部分是第一个数组的第一个元素。对于其他部分，它是当前层级数组的元素，索引等于分形部分索引。因为我们以五为步长增加该索引，所以还要加上子级索引。

```diff
+		parts[0][0] = CreatePart(0, 0, scale);
		for (int li = 1; li < parts.Length; li++) {
			scale *= 0.5f;
			FractalPart[] levelParts = parts[li];
			for (int fpi = 0; fpi < levelParts.Length; fpi += 5) {
				for (int ci = 0; ci < 5; ci++) {
+					levelParts[fpi + ci] = CreatePart(li, ci, scale);
				}
			}
		}
```

接着创建一个新的 `Update` 方法，遍历所有层级和它们的所有部分，把相关的分形部分数据存进变量。我们再次从第二层开始循环，因为根部分不移动，总是位于原点。

```diff
+	void Update () {
+		for (int li = 1; li < parts.Length; li++) {
+			FractalPart[] levelParts = parts[li];
+			for (int fpi = 0; fpi < levelParts.Length; fpi++) {
+				FractalPart part = levelParts[fpi];
+			}
+		}
+	}
```

要相对它的父级定位一个部分，我们还需要访问父级的 `Transform` 组件。为此也要记录父级 parts 数组。父级是那个数组中索引等于当前部分索引除以五的元素。这之所以有效，是因为我们执行整数除法，所以没有余数。因此索引 0–4 的部分得到父级索引 0，索引 5–9 的部分得到父级索引 1，依此类推。

```diff
		for (int li = 1; li < parts.Length; li++) {
+			FractalPart[] parentParts = parts[li - 1];
			FractalPart[] levelParts = parts[li];
			for (int fpi = 0; fpi < levelParts.Length; fpi++) {
+				Transform parentTransform = parentParts[fpi / 5].transform;
				FractalPart part = levelParts[fpi];
			}
		}
```

现在我们可以设置部分相对其指定父级的位置。先让它的 local position 等于父级的位置，加上部分的方向乘以其本地缩放。因为缩放是均匀的，我们只用缩放的 X 分量就够。

```diff
				Transform parentTransform = parentParts[fpi / 5].transform;
				FractalPart part = levelParts[fpi];
+			part.transform.localPosition =
+				parentTransform.localPosition +
+				part.transform.localScale.x * part.direction;
```

![部分彼此太近。](https://catlikecoding.com/unity/tutorials/basics/jobs/flat-hierarchy/parts-distance-incorrect.png)

这让部分离它们的父级太近，因为我们用部分自己的缩放来缩放距离。由于缩放每层减半，我们必须把最终偏移增加到 150%。

```diff
				part.transform.localPosition =
					parentTransform.localPosition +
+				1.5f * part.transform.localScale.x * part.direction;
```

![部分距离正确。](https://catlikecoding.com/unity/tutorials/basics/jobs/flat-hierarchy/parts-distance-correct.png)

我们还必须应用部分的旋转。做法是把它赋给对象的 local rotation。让我们在设置位置之前做。

```diff
+			part.transform.localRotation = part.rotation;		
				part.transform.localPosition =
					parentTransform.localPosition +
					1.5f * part.transform.localScale.x * part.direction;
```

但我们还必须传播父级的旋转。旋转可以通过四元数乘法堆叠。与普通数字乘法不同，这种情况下顺序很重要。得到的四元数表示这样的旋转：先执行第二个四元数的旋转，再应用第一个四元数的旋转。因此在变换层级中，先执行子级的旋转，再执行父级的旋转。所以正确的四元数乘法顺序是父级-子级。

```diff
				part.transform.localRotation =
+				parentTransform.localRotation * part.rotation;
```

最后，父级的旋转也应该影响其偏移的方向。我们可以通过执行四元数-向量乘法，把一个四元数旋转应用到一个向量上。

```diff
				part.transform.localPosition =
					parentTransform.localPosition +
+				parentTransform.localRotation *
+					(1.5f * part.transform.localScale.x * part.direction);
```

![恢复的分形。](https://catlikecoding.com/unity/tutorials/basics/jobs/flat-hierarchy/fractal-restored.png)

### 再次动画

要让分形再次动起来，我们必须重新引入另一个旋转。这次我们创建一个四元数来表示当前 delta time 的旋转，角速度与之前相同。在 `Update` 开头做。

```diff
	void Update () {
+		Quaternion deltaRotation = Quaternion.Euler(0f, 22.5f * Time.deltaTime, 0f);

		…
	}
```

让我们从根部分开始。在循环之前获取它，把它的旋转乘以 delta 旋转。

```diff
		Quaternion deltaRotation = Quaternion.Euler(0f, 22.5f * Time.deltaTime, 0f);

+		FractalPart rootPart = parts[0][0];
+		rootPart.rotation *= deltaRotation;
```

`FractalPart` 是一个结构体，是值类型，所以改变它的局部变量不会改变其他任何东西。我们必须把它复制回它的数组元素——替换旧数据——才能记住它的旋转已经改变。

```diff
		FractalPart rootPart = parts[0][0];
		rootPart.rotation *= deltaRotation;
+		parts[0][0] = rootPart;
```

我们还要调整根的 `Transform` 组件的旋转。这会让分形再次旋转，但只绕着它的根。

```diff
		FractalPart rootPart = parts[0][0];
		rootPart.rotation *= deltaRotation;
+		rootPart.transform.localRotation = rootPart.rotation;
		parts[0][0] = rootPart;
```

要让所有其他部分旋转，我们必须把同样的 delta 旋转也乘进它们的旋转。因为一切都绕着它本地的向上轴旋转，delta 旋转是最右侧的操作数。在应用部分游戏对象的最终旋转之前做。最后也要把调整后的部分数据复制回数组。

```diff
			for (int fpi = 0; fpi < levelParts.Length; fpi++) {
				Transform parentTransform = parentParts[fpi / 5].transform;
				FractalPart part = levelParts[fpi];
+			part.rotation *= deltaRotation;
				part.transform.localRotation =
					parentTransform.localRotation * part.rotation;
				part.transform.localPosition =
					parentTransform.localPosition +
					parentTransform.localRotation *
						(1.5f * part.transform.localScale.x * part.direction);
+			levelParts[fpi] = part;
			}
```

### 再次测量性能

此时我们的分形看起来和动画都跟以前完全一样，但有了新的展平对象层级，以及负责更新整个东西的单个组件。让我们用相同的构建设置再分析一次，看看这个新方法是否表现更好。

![用 URP 和分形深度 6 分析构建产物。](https://catlikecoding.com/unity/tutorials/basics/jobs/flat-hierarchy/profiler-build-urp-depth-6.png)

| Depth | MS | URP | BRP |
|---|---|---|---|
| 6 | 2 | 150 | 95 |
| 7 | 8 | 32 | 17 |
| 8 | 43 | 5 | 3 |

与递归方法相比，平均帧率在各处都提高了。对我而言，URP 的深度 7 现在达到 30FPS。`Update` 期间花的时间没有明显减少，深度 8 时甚至似乎略增，但渲染期间被更简单的层级补偿了。使用立方体得到大致相同的性能。

我们可以得出结论，新方法确实是一种改进，但单靠它仍不足以支持深度 7 或 8 的分形。

## 程序化绘制

因为我们的分形现在有展平的对象层级，它的结构设计与之前教程的图表相同：单个对象带大量几乎相同的子级。通过程序化渲染图表的点、而不是每个点一个游戏对象，我们大幅提高了它的性能。这提示我们可以对分形应用同样的方法。

尽管对象层级是展平的，分形部分确实仍有递归的层级关系。这使它从根本上不同于有独立点的图表。这种层级依赖使它不适合迁移到计算着色器。但仍可能通过单条程序化命令绘制同一层的所有部分，避免成千上万个游戏对象的开销。

> **用计算着色器更新分形可能吗？**
>
> 可能，但不方便，因为父部分必须在它们的子级之前更新。这种依赖要求把工作拆成多个连续的阶段，就像我们一层一层地迭代。由于大多数层级没有很多部分——从 GPU 的角度看——它的并行处理能力无法被高效利用。
>
>
> 可以应用混合方法：除最后一层外的所有层用 CPU，最后一层用 GPU。但本教程聚焦于 CPU，而且最后我们会发现瓶颈是 GPU，不是 CPU。

### 移除游戏对象

我们首先移除游戏对象。这也意味着我们不再有 `Transform` 组件来存储世界位置和旋转。相反，我们把这些存储在 `FractalPart` 的额外字段里。

```diff
	struct FractalPart { 
		public Vector3 direction, worldPosition;
		public Quaternion rotation, worldRotation;
-	//public Transform transform;
	}
```

从 `CreatePart` 移除所有游戏对象代码。我们只需保留它的子级索引参数，因为其他参数只在创建游戏对象时使用。

```diff
	FractalPart CreatePart (int childIndex) {
-		//var go = new GameObject("Fractal Part L" + levelIndex + " C" + childIndex);
-		//go.transform.localScale = scale * Vector3.one;
-		//go.transform.SetParent(transform, false);
-		//go.AddComponent<MeshFilter>().mesh = mesh;
-		//go.AddComponent<MeshRenderer>().material = material;

		return new FractalPart {
			direction = directions[childIndex],
			rotation = rotations[childIndex] //,
-		//transform = go.transform
		};
	}
```

现在我们可以把方法缩减为单个表达式。

```diff
	FractalPart CreatePart (int childIndex) => new FractalPart {
		direction = directions[childIndex],
		rotation = rotations[childIndex]
+	};
```

相应地调整 `Awake` 里的代码。从现在起我们在这里不再处理缩放。

```diff
-		//float scale = 1f;
		parts[0][0] = CreatePart(0);
		for (int li = 1; li < parts.Length; li++) {
-			//scale *= 0.5f;
			FractalPart[] levelParts = parts[li];
			for (int fpi = 0; fpi < levelParts.Length; fpi += 5) {
				for (int ci = 0; ci < 5; ci++) {
					levelParts[fpi + ci] = CreatePart(ci);
				}
			}
		}
```

在 `Update` 里，我们现在必须把根的旋转赋给它的世界旋转字段，而不是赋给 `Transform` 组件的旋转。

```diff
		FractalPart rootPart = parts[0][0];
		rootPart.rotation *= deltaRotation;
		rootPart.worldRotation = rootPart.rotation;
		parts[0][0] = rootPart;
```

对所有其他部分也要做同样的调整，包括它们的旋转和位置。我们在这里也重新引入递减的缩放。

```diff
+		float scale = 1f;
		for (int li = 1; li < parts.Length; li++) {
+			scale *= 0.5f;
			FractalPart[] parentParts = parts[li - 1];
			FractalPart[] levelParts = parts[li];
			for (int fpi = 0; fpi < levelParts.Length; fpi++) {
-				//Transform parentTransform = parentParts[fpi / 5].transform;
+				FractalPart parent = parentParts[fpi / 5];
				FractalPart part = levelParts[fpi];
				part.rotation *= deltaRotation;
				part.worldRotation = parent.worldRotation * part.rotation;
				part.worldPosition =
+				parent.worldPosition +
+				parent.worldRotation * (1.5f * scale * part.direction);
				levelParts[fpi] = part;
			}
		}
```

### 变换矩阵

`Transform` 组件提供用于渲染的变换矩阵。因为我们的部分不再有这些组件，我们需要自己创建矩阵。我们把它们存储在每个层级一个的数组里，就像存储部分一样。为此添加一个 `Matrix4x4[][]` 字段，并在 `Awake` 里与其他数组一起创建它的所有数组。

```diff
	FractalPart[][] parts;

+	Matrix4x4[][] matrices;

	void Awake () {
		parts = new FractalPart[depth][];
+		matrices = new Matrix4x4[depth][];
		for (int i = 0, length = 1; i < parts.Length; i++, length *= 5) {
			parts[i] = new FractalPart[length];
+			matrices[i] = new Matrix4x4[length];
		}

		…
	}
```

创建变换矩阵最简单的方式是调用静态的 `Matrix4x4.TRS` 方法，以位置、旋转和缩放作为参数。它返回一个我们可以复制进数组的 `Matrix4x4` 结构体。第一个是 `Update` 里的根矩阵，由它的世界位置、世界旋转和缩放一创建。

```diff
		parts[0][0] = rootPart;
+		matrices[0][0] = Matrix4x4.TRS(
+			rootPart.worldPosition, rootPart.worldRotation, Vector3.one
+		);
```

> **TRS 是什么意思？**
>
> 它代表平移-旋转-缩放（translation-rotation-scale）。此处的平移（translation）意思是重新定位或偏移。

以同样方式在循环里创建所有其他矩阵，这次使用变量 scale。

```diff
			scale *= 0.5f;
			FractalPart[] parentParts = parts[li - 1];
			FractalPart[] levelParts = parts[li];
+			Matrix4x4[] levelMatrices = matrices[li];
			for (int fpi = 0; fpi < levelParts.Length; fpi++) {
				…

+				levelMatrices[fpi] = Matrix4x4.TRS(
+					part.worldPosition, part.worldRotation, scale * Vector3.one
+				);
			}
```

此时进入运行模式不会显示分形，因为我们还没有可视化各部分。但我们确实计算了它们的变换矩阵。如果我们让深度 6 或更大的分形运行一会儿，某个时刻 Unity 会开始记录错误。错误告诉我们四元数到矩阵的转换失败，因为输入四元数无效。

转换失败是因为浮点精度限制。随着我们不断把四元数相互相乘，连续的小误差累积，直到结果不再被识别为有效旋转。这是由我们每次更新累积的许多非常小的旋转造成的。

解决方案是每次更新从全新的四元数开始。我们可以通过把旋转角度作为一个单独的 float 字段存储在 `FractalPart` 里，而不是调整它的本地旋转。

```diff
	struct FractalPart { 
		public Vector3 direction, worldPosition;
		public Quaternion rotation, worldRotation;
+		public float spinAngle;
	}
```

在 `Update` 里，我们回到使用旋转 delta 角的旧方法，然后把它加到根的旋转角上。根的世界旋转变成它的配置旋转，再叠加上一个绕 Y 轴、等于它当前旋转角的新旋转。

```diff
-		//Quaternion deltaRotation = Quaternion.Euler(0f, 22.5f * Time.deltaTime, 0f);
+		float spinAngleDelta = 22.5f * Time.deltaTime;
		FractalPart rootPart = parts[0][0];
-		//rootPart.rotation *= deltaRotation;
+		rootPart.spinAngle += spinAngleDelta;
		rootPart.worldRotation =
			rootPart.rotation * Quaternion.Euler(0f, rootPart.spinAngle, 0f);
		parts[0][0] = rootPart;
```

所有其他部分也一样，父级的世界旋转叠加在上面。

```diff
-				//part.rotation *= deltaRotation;
+				part.spinAngle += spinAngleDelta;
				part.worldRotation =
					parent.worldRotation *
+				(part.rotation * Quaternion.Euler(0f, part.spinAngle, 0f));
```

### 计算缓冲区

要渲染各部分，我们需要把它们的矩阵发送给 GPU。我们像图表那样用计算缓冲区。区别是这次 CPU 填充缓冲区而不是 GPU，而且我们每层用一个单独的缓冲区。添加一个缓冲区数组的字段，并在 `Awake` 里创建它们。一个 4×4 矩阵有十六个 float 值，所以缓冲区的步长是十六乘以四字节。

```diff
+	ComputeBuffer[] matricesBuffers;

	void Awake () {
		parts = new FractalPart[depth][];
		matrices = new Matrix4x4[depth][];
+		matricesBuffers = new ComputeBuffer[depth];
+		int stride = 16 * 4;
		for (int i = 0, length = 1; i < parts.Length; i++, length *= 5) {
			parts[i] = new FractalPart[length];
			matrices[i] = new Matrix4x4[length];
+			matricesBuffers[i] = new ComputeBuffer(length, stride);
		}

		…
	}
```

我们还必须在新的 `OnDisable` 方法里释放缓冲区。为了让热重载能工作，也要把 `Awake` 改成 `OnEnable`。

```diff
	void OnEnable () {
		parts = new FractalPart[depth][];
		matrices = new Matrix4x4[depth][];
		matricesBuffers = new ComputeBuffer[depth];
		…
	}

+	void OnDisable () {
+		for (int i = 0; i < matricesBuffers.Length; i++) {
+			matricesBuffers[i].Release();
+		}
+	}
```

为了整洁，在 `OnDisable` 末尾也清除所有数组引用。反正我们在 `OnEnable` 里创建新的。

```diff
	void OnDisable () {
		for (int i = 0; i < matricesBuffers.Length; i++) {
			matricesBuffers[i].Release();
		}
+		parts = null;
+		matrices = null;
+		matricesBuffers = null;
	}
```

通过添加一个 `OnValidate` 方法，它只是先后调用 `OnDisable` 和 `OnEnable`、重置分形，这也使得在运行模式下通过 Inspector 改变分形深度变得容易。`OnValidate` 方法在组件通过 Inspector 或撤销/重做操作发生改变后被调用。

```diff
+	void OnValidate () {
+		OnDisable();
+		OnEnable();
+	}
```

然而，这只有在运行模式且分形当前激活时才能工作。我们可以通过检查某个数组是否不为 `null` 来验证，用 `!=` 不等运算符。

```diff
	void OnValidate () {
+		if (parts != null) {
			OnDisable();
			OnEnable();
+		}
	}
```

除此之外，`OnValidate` 也会在我们通过 Inspector 禁用组件时被调用。这会先触发分形重置，然后又把它禁用。我们可以通过同时检查 `Fractal` 组件是否启用——用它的 `enabled` 属性——来避免。只有两个条件都为真时才重置分形。我们用布尔 `&&` AND 运算符把检查合并成单个条件表达式。

```diff
		if (parts != null && enabled) {
			OnDisable();
			OnEnable();
		}
```

最后，要把矩阵上传到 GPU，在 `Update` 末尾对所有缓冲区调用 `SetData`，以相应的矩阵数组作为参数。

```diff
	void Update () {
		…

+		for (int i = 0; i < matricesBuffers.Length; i++) {
+			matricesBuffers[i].SetData(matrices[i]);
+		}
	}
```

> **我们难道不应该避免向 GPU 发送数据吗？**
>
> 尽可能避免，是的。但这种情况我们别无选择，我们必须以某种方式把矩阵发送给 GPU，而这是最有效的方式。

### 着色器

现在我们必须再次创建一个支持程序化绘制的着色器。要设置对象到世界矩阵，我们可以取图表的 *PointGPU.hlsl* 的代码，复制到一个新的 *FractalGPU.hlsl* 文件里，并为我们的分形做适配。这意味着它不使用 `float3` 位置缓冲区，而是用 `float4x4` 矩阵缓冲区。而且我们可以直接复制矩阵，不必在着色器里构造它。

```diff
#if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)
	StructuredBuffer<float4x4> _Matrices;
#endif

-//float _Step;

void ConfigureProcedural () {
	#if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)
+		unity_ObjectToWorld = _Matrices[unity_InstanceID];
	#endif
}

void ShaderGraphFunction_float (float3 In, out float3 Out) {
	Out = In;
}

void ShaderGraphFunction_half (half3 In, out half3 Out) {
	Out = In;
}
```

我们分形的 URP 着色器图也是 *Point URP GPU* 着色器图的简化副本。顶点位置节点完全相同，只是现在我们依赖 *FractalGPU* HLSL 文件。而且不再基于世界位置着色，一个 *Base Color* 颜色属性就够了。

![分形着色器图。](https://catlikecoding.com/unity/tutorials/basics/jobs/procedural-drawing/shader-graph.png)

BRP 表面着色器也比它的图等价物简单。它需要一个不同的名字，包含正确的文件，以及一个用于反照率的 *BaseColor* 颜色属性。颜色属性的工作方式像 smoothness，只是用 `Color` 而不是 range，且默认值是四分量。我在 `Input` 结构体里保留了世界位置，即使不再需要，因为空结构体无法编译。

```diff
Shader "Fractal/Fractal Surface GPU" {

	Properties {
+		_BaseColor ("Base Color", Color) = (1.0, 1.0, 1.0, 1.0)
		_Smoothness ("Smoothness", Range(0,1)) = 0.5
	}

	SubShader {
		CGPROGRAM
		#pragma surface ConfigureSurface Standard fullforwardshadows addshadow
		#pragma instancing_options assumeuniformscaling procedural:ConfigureProcedural
		#pragma editor_sync_compilation

		#pragma target 4.5

		#include "FractalGPU.hlsl"

		struct Input {
			float3 worldPos;
		};

+		float4 _BaseColor;
		float _Smoothness;

		void ConfigureSurface (Input input, inout SurfaceOutputStandard surface) {
+			surface.Albedo = _BaseColor.rgb;
+			surface.Smoothness = _Smoothness;
		}
		ENDCG
	}

	FallBack "Diffuse"
}
```

### 绘制

最后，要再次绘制分形，我们必须在 `Fractal` 里记录矩阵缓冲区的标识符。

```diff
+	static readonly int matricesId = Shader.PropertyToID("_Matrices");
```

然后在 `Update` 末尾调用 `Graphics.DrawMeshInstancedProcedural`，每个层级一次，用正确的缓冲区。我们对所有层级简单地用相同的边界：一个边长为三的立方体。

```diff
+		var bounds = new Bounds(Vector3.zero, 3f * Vector3.one);
		for (int i = 0; i < matricesBuffers.Length; i++) {
+			ComputeBuffer buffer = matricesBuffers[i];
+			buffer.SetData(matrices[i]);
+			material.SetBuffer(matricesId, buffer);
+			Graphics.DrawMeshInstancedProcedural(mesh, 0, material, bounds, buffer.count);
		}
```

> **为什么边界大小用 3？**
>
> 根层的直径是 1。下一层的直径是 0.5，朝所有方向延伸。所以前两层的最大直径是 1 + 0.5 + 0.5 = 2。第三层在两侧各加 0.25，所以总直径变成 2.5，依此类推。因此某个大深度的分形直径等于 `1+1+1/2+1/4+1/8+…=2+sum_(i=1)^n 1/2^i`。
>
>
> 对于理论上的无限深度分形，这个和永远持续，但这是一个著名的收敛无穷级数：`lim_(n->oo) sum_(i=1)^n 1/2^i = 1`。这在直觉上说得通，因为从 0 向 1 走的每一步，都把你还需要走的距离减半，所以你每步都更接近，但永远无法在有限步内到达 1。所以我们的分形保证能装进一个三单位宽的包围盒里。

![只有最深一层。](https://catlikecoding.com/unity/tutorials/basics/jobs/procedural-drawing/only-deepest-level.png)

我们的分形再次出现，但看起来只有最深的层被渲染了。帧调试器会显示所有层都被渲染了，但它们都错误地使用了最后一层的矩阵。这是因为绘制命令被排队稍后执行。所以我们最后设置的是哪个缓冲区，就全被哪个缓冲区使用。

解决方案是把每个缓冲区链接到特定的绘制命令。我们可以通过一个 `MaterialPropertyBlock` 对象来做。为它添加一个静态字段，并在 `OnEnable` 里创建它的新实例（如果还不存在的话）。

```diff
+	static MaterialPropertyBlock propertyBlock;

	…

	void OnEnable () {
		…

+		if (propertyBlock == null) {
+			propertyBlock = new MaterialPropertyBlock();
+		}
	}
```

只在当前值为 `null` 时才赋值，可以用 `??=` 空合并赋值简化为单个表达式。

```diff
-		//if (propertyBlock == null) {
		propertyBlock ??= new MaterialPropertyBlock();
-		//}
```

在 `Update` 里，把缓冲区设置在属性块上，而不是直接设置在材质上。然后把块作为额外参数传给 `Graphics.DrawMeshInstancedProcedural`。这会让 Unity 复制该块当时的配置，并把它用于那条特定的绘制命令，覆盖为材质设置的内容。

```diff
			ComputeBuffer buffer = matricesBuffers[i];
			buffer.SetData(matrices[i]);
+			propertyBlock.SetBuffer(matricesId, buffer);
			Graphics.DrawMeshInstancedProcedural(
				mesh, 0, material, bounds, buffer.count, propertyBlock
			);
		}
```

> **为什么分形在场景窗口里闪烁？**
>
> 这是一个编辑器时序 bug，可能发生在场景窗口，但不会发生在游戏窗口或构建产物里。为游戏窗口打开 VSync 可能让它变好或变坏，取决于你的编辑器布局。

### 性能

现在我们的分形又完整了，让我们再测量一次它的性能，最初渲染球体。

![用 URP 和分形深度 6 分析构建产物。](https://catlikecoding.com/unity/tutorials/basics/jobs/procedural-drawing/profiler-build-urp-depth-6.png)

| Depth | MS | URP | BRP |
|---|---|---|---|
| 6 | 0.7 | 160 | 96 |
| 7 | 3 | 54 | 35 |
| 8 | 13 | 11 | 7 |

`Update` 现在花的时间少多了。就 FPS 而言，深度 6 和 8 略有改善，而深度 7 渲染速度几乎翻倍。URP 接近 60FPS。而当我们试立方体时，看到了显著改善。

| Depth | MS | URP | BRP |
|---|---|---|---|
| 6 | 0.4 | 470 | 175 |
| 7 | 2 | 365 | 155 |
| 8 | 11 | 86 | 85 |

帧率大幅提升，这清楚表明 GPU 现在是瓶颈。`Update` 时间也略有下降。这可能是因为渲染球体时设置缓冲区数据停滞得更久，因为 CPU 被迫等待 GPU 读完缓冲区。

### 随游戏对象移动

创建我们自己的变换矩阵的一个副作用是，我们的分形现在忽略了它游戏对象的变换。我们可以通过在 `Update` 里把游戏对象的旋转和位置并入根对象矩阵来修复。

```diff
		rootPart.worldRotation =
+			transform.rotation *
+			(rootPart.rotation * Quaternion.Euler(0f, rootPart.spinAngle, 0f));
+		rootPart.worldPosition = transform.position;
```

我们也可以应用游戏对象的缩放。然而，如果游戏对象是复杂层级的一部分，包含非均匀缩放和旋转，它可能经历非仿射变换导致剪切。这种情况下它没有明确定义的缩放。因此 `Transform` 组件没有简单的世界空间缩放属性。它们有 `lossyScale` 属性，用来表明它可能不是精确的仿射缩放。我们简单地用那个缩放的 X 分量，忽略任何非均匀缩放。

```diff
+		float objectScale = transform.lossyScale.x;
		matrices[0][0] = Matrix4x4.TRS(
			rootPart.worldPosition, rootPart.worldRotation, objectScale * Vector3.one
		);

		float scale = objectScale;
```

也把调整后的世界位置和缩放应用到边界上。

```diff
		var bounds = new Bounds(rootPart.worldPosition, 3f * objectScale * Vector3.one);
```

## Job 系统

在这一点上我们的 C# 代码已经尽可能快了，但我们可以切换到不同的方法，利用 Unity 的 Job 系统。这应该能进一步减少我们的 `Update` 时间，提高性能，或腾出空间让更多代码运行而不拖慢。

Job 系统的思想是尽可能高效地利用 CPU 的并行处理能力，利用它的多个核心和特殊的 SIMD 指令——即单指令多数据。这是通过把工作片段定义为单独的 Job 来实现的。这些 Job 像普通 C# 代码那样编写，但随后用 Unity 的 Burst 编译器编译，它执行激进的优化和并行化——这通过强制执行一些普通 C# 没有的结构约束而成为可能。

### Burst 包

Burst 是一个单独的包，所以通过包管理器为你的 Unity 版本安装最新版本。以我的情况是 Burst 版本 1.4.8。它依赖 Mathematics 包 1.2.1，所以那个包也会被安装或升级到 1.2.1。

要为 `Fractal` 创建 Job，我们必须使用 `Unity.Burst`、`Unity.Collections` 和 `Unity.Jobs` 命名空间里的代码。

```diff
+using Unity.Burst;
+using Unity.Collections;
+using Unity.Jobs;
using UnityEngine;
```

### 原生数组

Job 不能使用对象，只允许简单值和结构体类型。仍可以使用数组，但我们必须把它们转换成泛型的 `NativeArray` 类型。这是一个包含指向原生机器内存指针的结构体，这些内存存在于我们 C# 代码使用的常规托管内存堆之外。所以它绕开了默认的内存管理开销。

要创建分形部分的原生数组，我们需要用 `NativeArray<FractalPart>` 类型。因为我们使用多个这样的数组，我们真正需要的是它的数组。矩阵的多个数组也一样。

```diff
+	NativeArray<FractalPart>[] parts;

+	NativeArray<Matrix4x4>[] matrices;
```

现在我们必须从 `OnEnable` 开头创建新的原生数组的数组。

```diff
		parts = new NativeArray<FractalPart>[depth];
		matrices = new NativeArray<Matrix4x4>[depth];
```

并为每个层级创建新的原生数组，使用相应 `NativeArray` 类型的构造方法，它需要两个参数。第一个参数是数组的大小。第二个参数表明原生数组预期存在多久。因为我们每帧持续使用相同的数组，必须用 `Allocator.Persistent`。

```diff
		for (int i = 0, length = 1; i < parts.Length; i++, length *= 5) {
			parts[i] = new NativeArray<FractalPart>(length, Allocator.Persistent);
			matrices[i] = new NativeArray<Matrix4x4>(length, Allocator.Persistent);
			matricesBuffers[i] = new ComputeBuffer(length, stride);
		}
```

我们还必须改变部分创建循环里的变量类型来匹配。

```diff
		parts[0][0] = CreatePart(0);
		for (int li = 1; li < parts.Length; li++) {
+			NativeArray<FractalPart> levelParts = parts[li];
			…
		}
```

`Update` 里的循环里也一样。

```diff
+			NativeArray<FractalPart> parentParts = parts[li - 1];
+			NativeArray<FractalPart> levelParts = parts[li];
+			NativeArray<Matrix4x4> levelMatrices = matrices[li];
```

最后，就像计算缓冲区一样，我们在 `OnDisable` 用完它们时必须显式释放它们的内存。做法是在原生数组上调用 `Dispose`。

```diff
		for (int i = 0; i < matricesBuffers.Length; i++) {
			matricesBuffers[i].Release();
+			parts[i].Dispose();
+			matrices[i].Dispose();
		}
```

此时分形仍然同样工作。唯一的区别是我们现在用原生数组而不是托管 C# 数组。这可能表现更差，因为从托管 C# 代码访问原生数组有一点额外开销。一旦我们使用 Burst 编译的 Job，这个开销就不存在了。

### Job 结构体

要定义一个 Job，我们必须创建一个实现 Job 接口的结构体类型。实现接口就像扩展类，只是接口不继承现有功能，而是要求你自己包含特定功能。我们将在 `Fractal` 内部创建一个 `UpdateFractalLevelJob` 结构体，实现 `IJobFor`，这是最灵活的 Job 接口类型。

```diff
public class Fractal : MonoBehaviour {

+	struct UpdateFractalLevelJob : IJobFor {}

	…
}
```

> **为什么接口叫 IJobFor？**
>
> 惯例是所有接口类型都加 *I* 前缀——代表 interface，所以这个接口叫 *JobFor* 加 *I* 前缀。它是一个 Job 接口，专门用于在 `for` 循环内运行的功能。

`IJobFor` 接口要求我们添加一个 `Execute` 方法，它有一个整数参数、不返回任何东西。参数代表 `for` 循环的迭代变量。接口强制的一切都必须是 public，所以这个方法必须是 public。

```diff
	struct UpdateFractalLevelJob : IJobFor {

+		public void Execute (int i) {}
	}
```

思想是 `Execute` 方法取代我们 `Update` 方法最内层循环的代码。要做到这一点，那段代码需要的所有变量都必须作为字段添加到 `UpdateFractalLevelJob`。把它们设为 public，这样我们以后能设置它们。

```diff
	struct UpdateFractalLevelJob : IJobFor {

+		public float spinAngleDelta;
+		public float scale;

+		public NativeArray<FractalPart> parents;
+		public NativeArray<FractalPart> parts;

+		public NativeArray<Matrix4x4> matrices;

		public void Execute (int i) {}
	}
```

我们可以更进一步，用 `ReadOnly` 和 `WriteOnly` 属性表明我们只需要对某些原生数组做部分访问。最内层循环只读 parents 数组，只写 matrices 数组。它既读又写 parts 数组，这是默认假设，所以没有对应的属性。

```diff
+		[ReadOnly]
		public NativeArray<FractalPart> parents;

		public NativeArray<FractalPart> parts;

+		[WriteOnly]
		public NativeArray<Matrix4x4> matrices;
```

如果多个进程并行修改相同的数据，那么谁先做什么就变成任意的了。如果两个进程设置相同的数组元素，最后一个赢。如果一个进程获取另一个进程设置的元素，它要么得到旧值要么得到新值。最终结果取决于精确的时序，而我们无法控制它，这可能导致非常难检测和修复的不一致行为。这些现象被称为竞争条件。`ReadOnly` 属性表明这些数据在 Job 执行期间保持不变，这意味着进程可以安全地并行读取它，因为结果总是相同的。

编译器强制 Job 不写 `ReadOnly` 数据、不读 `WriteOnly` 数据。如果我们不小心这么做了，编译器会告诉我们犯了语义错误。

### 执行 Job

`Execute` 方法将取代我们 `Update` 方法的最内层循环。把相关代码复制到方法里，并在需要的地方调整，让它使用 Job 的字段和参数。

```diff
		public void Execute (int i) {
			FractalPart parent = parents[i / 5];
			FractalPart part = parts[i];
			part.spinAngle += spinAngleDelta;
			part.worldRotation =
				parent.worldRotation *
				(part.rotation * Quaternion.Euler(0f, part.spinAngle, 0f));
			part.worldPosition =
				parent.worldPosition +
				parent.worldRotation * (1.5f * scale * part.direction);
+			parts[i] = part;

+			matrices[i] = Matrix4x4.TRS(
				part.worldPosition, part.worldRotation, scale * Vector3.one
			);
		}
```

修改 `Update`，在层级循环里创建一个新的 `UpdateFractalLevelJob` 值并设置它的所有字段。然后修改最内层循环，让它调用 Job 的 `Execute` 方法。这样我们保持完全相同的功能，只是代码迁移到了 Job。

```diff
		for (int li = 1; li < parts.Length; li++) {
			scale *= 0.5f;
+			var job = new UpdateFractalLevelJob {
+				spinAngleDelta = spinAngleDelta,
+				scale = scale,
+				parents = parts[li - 1],
+				parts = parts[li],
+				matrices = matrices[li]
+			};
-			//NativeArray<FractalPart> parentParts = parts[li - 1];
-			//NativeArray<FractalPart> levelParts = parts[li];
-			//NativeArray<Matrix4x4> levelMatrices = matrices[li];
			for (int fpi = 0; fpi < parts[li].Length; fpi++) {
+				job.Execute(fpi);
			}
		}
```

但我们不必为每次迭代显式调用 `Execute` 方法。思想是我们调度 Job，让它自己执行循环。做法是对它调用 `Schedule`，带两个参数。第一个是我们想要的迭代次数，等于我们正在处理的 parts 数组的长度。第二个是一个 `JobHandle` 结构体值，用于在 Job 之间强制执行顺序依赖。我们最初用这个结构体的默认值——通过 `default` 关键字——它不强制任何约束。

```diff
			var job = new UpdateFractalLevelJob {
				…
			};
+			job.Schedule(parts[li].Length, default);
-			//for (int fpi = 0; fpi < parts[li].Length; fpi++) {
-			//	job.Execute(fpi);
-			//}
```

`Schedule` 不会立即运行 Job，它只是为稍后处理调度它。它返回一个 `JobHandle` 值，可用于跟踪 Job 的进度。我们可以通过调用 handle 上的 `Complete` 来延迟我们代码的进一步执行，直到 Job 完成。

```diff
			job.Schedule(parts[li].Length, default).Complete();
```

### 调度

此时我们每层调度一个 Job 并立即等待它完成。结果是我们的分形仍然像以前那样顺序更新，尽管我们已经切换到了 Job。我们可以通过把完成推迟到调度完所有 Job 之后，来稍微放宽这一点。做法是让 Job 相互依赖，在调度时把上一个 Job handle 传给下一个。然后我们在循环结束后调用 `Complete`，触发整个 Job 序列的执行。

```diff
+		JobHandle jobHandle = default;
		for (int li = 1; li < parts.Length; li++) {
			scale *= 0.5f;
			var job = new UpdateFractalLevelJob {
				…
			};
-			//job.Schedule(parts[li].Length, default).Complete();
+			jobHandle = job.Schedule(parts[li].Length, jobHandle);
		}
+		jobHandle.Complete();
```

此时我们不再需要把各个 Job 存进变量，只需记录最后一个 handle。

```diff
+			jobHandle = new UpdateFractalLevelJob {
				…
			}.Schedule(parts[li].Length, jobHandle);
-			//jobHandle = job.Schedule(parts[li].Length, jobHandle);
```

性能分析器会显示，Job 最终可能运行在工作线程而不是主线程上。但它们也可能运行在主线程上，因为主线程反正要等 Job 完成，所以此刻 Job 在哪里运行没有区别。调度的 Job 也可能最终运行在不同的线程上，尽管它们仍有顺序依赖。

![用 URP 和分形深度 8 分析构建产物；主线程等待工作线程完成。](https://catlikecoding.com/unity/tutorials/basics/jobs/job-system/scheduled-on-worker-thread.png)

把所有 Job 打包一起运行、只等待最后一个完成的好处是，这使延迟等待完成成为可能。一个常见的例子是在 `Update` 里调度所有 Job，做一些其他事情，然后通过在 `LateUpdate` 方法里调用 `Complete` 来延迟等待——`LateUpdate` 在所有常规 `Update` 方法完成后被调用。也可以把完成推迟到下一帧甚至更晚。但我们不这么做，因为我们需要 Job 每帧完成，而且除了之后把矩阵上传到 GPU 之外没有别的事可做。

### Burst 编译

经过所有这些改动，我们还没看到任何性能改善。那是因为我们目前没有使用 Burst 编译器。我们必须通过给 Job 结构体附加 `BurstCompile` 属性，显式指示 Unity 用 Burst 编译我们的 Job 结构体。

```diff
+	[BurstCompile]
	struct UpdateFractalLevelJob : IJobFor { … }
```

![用 Burst 编译。](https://catlikecoding.com/unity/tutorials/basics/jobs/job-system/burst-compiled.png)

帧调试器现在表明我们在使用 Burst 编译版本的 Job。由于 Burst 应用的优化，它们跑得稍快，但此刻收益不大。

你可能会注意到，在编辑器里刚进入运行模式时性能差得多。这是因为 Burst 编译在编辑器里是按需的，就像着色器编译一样。当 Job 第一次运行时，它会由 Burst 编译，同时用常规 C# 编译版本来运行 Job。Burst 编译一完成，编辑器就会切换到运行 Burst 版本。我们可以通过把 `BurstCompile` 属性的 `CompileSynchronously` 属性设为 `true`，强制编辑器在需要时立即编译 Job 的 Burst 版本——让 Unity 停顿直到编译完成。属性的属性可以通过在它们的参数列表里包含赋值来设置。

```diff
	[BurstCompile(CompileSynchronously = true)]
```

就像着色器编译一样，这不影响构建产物，因为一切都在构建过程中编译。

### Burst Inspector

你可以通过 *Burst Inspector* 窗口检查 Burst 生成的汇编代码，通过 *Jobs / Burst / Open Inspector...* 打开。它显示 Burst 为项目里所有 Job 生成的低级指令。我们的 Job 会作为 *Fractal.UpdateFractalLevelJob - (IForJob)* 包含在 *Compile Targets* 列表里。

我不会详细分析生成的代码，性能改善必须自己说话。但切换到最右侧的显示模式——*.LVM IR Optimization Diagnostic*——来了解 Burst 做了什么，是有用的。目前它对我包含这些备注：

```csharp
Remark: IJobFor.cs:43:0: loop not vectorized: loop control flow is not understood by vectorizer
Remark: NativeArray.cs:162:0: Stores SLP vectorized with cost -3 and with tree size 2
```

第一条备注意味着 Burst 无法重写代码、用 SIMD 指令合并多次迭代。最简单的例子是做一个像 `data[i] = 2f * data[i]` 的 Job。使用 SIMD 指令，Burst 可以改变它，让这个操作对多个索引同时执行，理想情况下最多同时八个。这样合并操作被称为向量化，因为对单个值的指令被替换为对向量的指令。

当 Burst 表明控制流不被理解时，意味着有复杂的条件块。我们没有那些，但默认情况下 Burst 安全检查是启用的，它们强制读/写属性并检测 Job 之间的其他依赖问题，比如试图并行运行两个写同一数组的 Job。这些检查用于开发，在构建产物里被移除。我们也可以为 Burst inspector 停用它们以查看最终结果，通过禁用 *Safety Checks* 开关。你也可以按 Job 禁用，或通过 *Jobs / Burst / Safety Checks* 菜单为整个项目禁用。你通常保持安全检查在编辑器里启用，并在构建产物里测试性能，除非你想最大化编辑器性能。

```csharp
Remark: IJobFor.cs:43:0: loop not vectorized: call instruction cannot be vectorized
Remark: NativeArray.cs:148:0: Stores SLP vectorized with cost -3 and with tree size 2
```

没有安全检查后，Burst 仍然无法向量化循环，这次是因为一个 call 指令挡了路。这意味着有一个 Burst 无法优化掉的方法调用，它永远无法被向量化。

第二条备注表明 Burst 找到了一种把多个独立操作向量化成单个 SIMD 指令的方法。例如，多个独立值的加法被合并成单个向量加法。成本 −3 表明这实际消除了三条指令。

> **SLP 是什么意思？**
>
> 它是 superword-level parallelism（超字级并行）的缩写。

### Mathematics 库

我们目前使用的代码没有为 Burst 优化。Burst 无法优化掉的 call 指令对应我们调用的静态 `Quaternion` 方法。Burst 专门优化为与 Unity 的 Mathematics 库一起工作，后者在设计时考虑了向量化。

Mathematics 库的代码包含在 `Unity.Mathematics` 命名空间里。

```diff
using Unity.Jobs;
+using Unity.Mathematics;
using UnityEngine;
```

该库被设计得类似于着色器数学代码。思想是静态地使用 `Unity.Mathematics.math` 类型，就像我们在图表函数库里静态使用 `UnityEngine.Mathf` 那样。

```diff
using Unity.Mathematics;
using UnityEngine;

+using static Unity.Mathematics.math;
```

然而，这会在尝试对 `float4x4` 和 `quaternion` 类型调用某些方法时产生冲突，因为 `math` 有与那些类型完全相同名字的方法。这会让编译器抱怨我们在试图对一个方法调用方法，这是不可能的。要避免，添加 `using` 语句，表明当我们写那些词时，默认应把它们解释为类型。做法是写 `using` 后跟一个标签、一个赋值和一个完全限定类型。标签我们简单用类型名，尽管也可以用不同的标签。

```diff
using static Unity.Mathematics.math;
+using float4x4 = Unity.Mathematics.float4x4;
+using quaternion = Unity.Mathematics.quaternion;
```

现在把 `Vector3` 的所有用法替换为 `float3`，除了我们在 `Update` 里用于缩放边界的那个向量。我不一一列出这些改动，我们马上修错误。然后也把 `Quaternion` 的所有用法替换为 `quaternion`。注意唯一区别是 Mathematics 类型不大写。之后把 `Matrix4x4` 的所有用法替换为 `float4x4`。

做完之后，把 `directions` 数组的向量方向属性替换为来自 `math` 的相应方法。

```diff
	static float3[] directions = {
+		up(), right(), left(), forward(), back()
	};
```

我们还必须调整 `rotations` 数组的初始化。Mathematics 库用弧度而不是度，所以把所有 `90f` 实例改为 `0.5f * PI`。此外，`quaternion` 有分别绕 X、Y、Z 轴创建旋转的方法，比通用的 `Euler` 方法更高效。

```diff
	static quaternion[] rotations = {
		quaternion.identity,
		quaternion.RotateZ(-0.5f * PI), quaternion.RotateZ(0.5f * PI),
		quaternion.RotateX(0.5f * PI), quaternion.RotateX(-0.5f * PI)
	};
```

我们也必须把 `Update` 里的旋转角 delta 转换成弧度。

```diff
		float spinAngleDelta = 0.125f * PI * Time.deltaTime;
```

下一步是调整 `UpdateFractalLevelJob.Execute`。先把 `Euler` 方法调用替换为更快的 `RotateY` 变体。然后把所有涉及四元数的乘法替换为 `mul` 方法的调用。最后，我们可以通过用 `math.float3` 方法、以 scale 作为单个参数，创建一个均匀缩放向量。

```diff
			part.worldRotation = mul(parent.worldRotation,
+			mul(part.rotation, quaternion.RotateY(part.spinAngle))
+		);
			part.worldPosition =
				parent.worldPosition +
+			mul(parent.worldRotation, 1.5f * scale * part.direction);
			parts[i] = part;

			matrices[i] = float4x4.TRS(
				part.worldPosition, part.worldRotation, float3(scale)
			);
```

以同样的方式调整 `Update` 里根部分的更新代码。

```diff
		rootPart.worldRotation = mul(transform.rotation,
+		mul(rootPart.rotation, quaternion.RotateY(rootPart.spinAngle))
+	);
		rootPart.worldPosition = transform.position;
		parts[0][0] = rootPart;
		float objectScale = transform.lossyScale.x;
		matrices[0][0] = float4x4.TRS(
			rootPart.worldPosition, rootPart.worldRotation, float3(objectScale)
		);
```

> **Transform 的 position 和 rotation 类型不对吗？**
>
> 确实，但 `Vector3` 和 `float3` 类型之间、以及 `Quaternion` 和 `quaternion` 类型之间都有隐式转换。

此时 Burst inspector 不再抱怨 call 指令（注意：在更新的 Unity 版本里它可能仍然抱怨，但这不是大问题）。它仍然无法向量化循环，因为返回类型无法向量化。这是因为我们的数据太大，无法向量化循环的多次迭代。这没关系，因为我们使用 Mathematics 库，Burst 仍能向量化单次迭代里的很多操作，尽管 Burst inspector 不会提到这个。

```csharp
Remark: quaternion.cs:330:0: loop not vectorized: instruction return type cannot be vectorized
Remark: NativeArray.cs:162:0: Stores SLP vectorized with cost -6 and with tree size 2
```

此时构建产物里深度 8 分形的 `Update` 平均只需 5.5ms。所以我们相比非 Job 方法大致把更新速度翻倍了。我们可以通过给 `BurstCompile` 构造方法传两个参数，启用更多 Burst 优化，跑得更快。这些是常规构造参数，必须写在属性赋值之前。

第一个参数我们用 `FloatPrecision.Standard`，第二个用 `FloatMode.Fast`。fast 模式允许 Burst 重排数学运算，例如把 `a + b * c` 重写为 `b * c + a`。这可以提高性能，因为有 madd——乘加——指令，它比单独的加法指令后跟乘法更快。着色器编译器默认这么做。通常重排运算没有逻辑差异，但由于浮点限制，改变顺序会产生略微不同的结果。你可以假设这些差异无关紧要，所以总是启用这个优化，除非你有好的理由不。

```diff
	[BurstCompile(FloatPrecision.Standard, FloatMode.Fast, CompileSynchronously = true)]
```

结果是更新时长进一步下降，到平均大约 4.5ms。

> **FloatPrecision 呢？**
>
> `FloatPrecision` 参数控制 `sin` 和 `cos` 方法的精度。我们不直接用它们，但它们在创建四元数时被使用。降低三角精度可以加速，但以我的情况没有明显区别。

### 发送更少数据

我们变换矩阵的底行总是包含相同的向量：(0, 0, 0, 1)。因为它总是一样，我们可以丢弃它，把矩阵数据的大小减少 25%。这意味着更少的内存使用和更少的从 CPU 到 GPU 的数据传输。

先把 `float4x4` 的所有用法替换为 `float3x4`，它表示三行四列的矩阵。然后减小 `OnEnable` 里计算缓冲区的步长，从十六个 float 减到十二个。

```diff
		int stride = 12 * 4;
```

`float3x4` 没有 `TRS` 方法，我们必须在 `Execute` 里自己组装矩阵。做法是先用旋转调用 `float3x3` 创建一个 3×3 的旋转和缩放矩阵，然后把缩放乘进去。最终矩阵通过用四个列向量调用 `float3x4` 来创建，这些列向量是 3×3 矩阵的三列——存储在它的 `c0`、`c1` 和 `c2` 字段里——后跟部分的位置。

```diff
+			float3x3 r = float3x3(part.worldRotation) * scale;
			matrices[i] = float3x4(r.c0, r.c1, r.c2, part.worldPosition);
```

对 `Update` 里的根部分做同样的事。

```diff
+		float3x3 r = float3x3(rootPart.worldRotation) * objectScale;
		matrices[0][0] = float3x4(r.c0, r.c1, r.c2, rootPart.worldPosition);
```

因为我们不在 `float3x4` 类型上调用方法，所以与 `math.float3x4` 方法没有冲突，我们不需要为它写 `using` 语句，`float4x4` 也不需要。

```diff
-//using float3x4 = Unity.Mathematics.float3x4;
```

最后，调整 `ConfigureProcedural`，让我们逐行复制矩阵，加上缺失的一行。

```diff
#if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)
	StructuredBuffer<float3x4> _Matrices;
#endif

void ConfigureProcedural () {
	#if defined(UNITY_PROCEDURAL_INSTANCING_ENABLED)
+		float3x4 m = _Matrices[unity_InstanceID];
+		unity_ObjectToWorld._m00_m01_m02_m03 = m._m00_m01_m02_m03;
+		unity_ObjectToWorld._m10_m11_m12_m13 = m._m10_m11_m12_m13;
+		unity_ObjectToWorld._m20_m21_m22_m23 = m._m20_m21_m22_m23;
+		unity_ObjectToWorld._m30_m31_m32_m33 = float4(0.0, 0.0, 0.0, 1.0);
	#endif
}
```

这个改动之后，我的平均 `Update` 时长降到了 4ms。所以我通过只存储和传输最少量的数据，赢得了半毫秒。

### 使用多个核心

我们已到达单个 CPU 核心优化的终点，但我们可以更进一步。更新图表时，所有父部分必须在它们的子部分之前更新，所以我们无法摆脱 Job 之间的顺序依赖。但同一层的所有部分是独立的，可以以任何顺序更新，甚至可以并行。这意味着我们可以把单个 Job 的工作分散到多个 CPU 核心。做法是对 Job 调用 `ScheduleParallel` 而不是 `Schedule`。这个方法需要一个新的第二个参数，表示批次数。让我们先设为 1 看看会发生什么。

```diff
			jobHandle = new UpdateFractalLevelJob {
				…
			}.ScheduleParallel(parts[li].Length, 1, jobHandle);
```

![在多个线程上运行。](https://catlikecoding.com/unity/tutorials/basics/jobs/job-system/multiple-threads.png)

我们的 Job 现在被拆分，并在多个 CPU 核心上并行运行，更新我们的分形部分。以我的情况，这把总 `Update` 时间降到平均 1.9ms。你能得到多少减少，取决于有多少 CPU 核心可用，这受限于你的硬件，以及多少其他进程占用了线程。

批次数控制迭代如何分配给线程。每个线程循环处理一个批次，做一点记账，然后循环处理另一个批次，直到工作完成。经验法则是：当 `Execute` 做的工作很少时，你应该试大批次数；当 `Execute` 做很多工作时，你应该试小批次数。我们的情况 `Execute` 做了相当多的工作，所以批次 1 是合理的默认值。但因为我们给每个部分五个子级，试试批次 5。

```diff
			jobHandle = new UpdateFractalLevelJob {
				…
			}.ScheduleParallel(parts[li].Length, 5, jobHandle);
```

这进一步把我的平均 `Update` 时间降到 1.7ms。用更大的批次数没有进一步改善，甚至稍慢，所以我保持 5。

### 最终性能

如果我们现在评估完全 Burst 优化的分形的性能，会发现更新时长已经变得无关紧要。GPU 总是瓶颈。渲染球体时，我们得到的帧率不比以前高。但渲染立方体时，深度 8 分形现在两种 RP 都超过 100FPS。

| Depth | MS | URP | BRP |
|---|---|---|---|
| 6 | 0.1 | 480 | 180 |
| 7 | 0.26 | 360 | 160 |
| 8 | 1.7 | 160 | 110 |

下一篇教程是[有机多样性](07_有机多样性.md)。

[教程许可协议](https://catlikecoding.com/unity/tutorials/license/) · [本教程项目仓库](https://bitbucket.org/catlikecodingunitytutorials/basics-06-jobs/) · [PDF 版本](https://catlikecoding.com/unity/tutorials/basics/jobs/Jobs.pdf)
