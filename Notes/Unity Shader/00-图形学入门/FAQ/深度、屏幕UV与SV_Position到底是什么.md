---
title: 深度、屏幕 UV 与 SV_Position 到底是什么
aliases:
  - 从零理解深度缓冲
  - Shader 手册第12章补充FAQ
tags:
  - Unity
  - URP
  - 图形学入门
  - 深度
  - FAQ
created: 2026-09-16
updated: 2026-09-16
---

# 深度、屏幕 UV 与 SV_Position 到底是什么

这篇 FAQ 专门补充 [[Unity6.7-URP-ShaderLab与HLSL语法手册#12 深度与屏幕纹理|语法手册第 12 章]]。不要求你已经会投影矩阵；先理解每个数在回答什么问题，再读代码。

> [!abstract] 先回答你的原问题
> “拿到 UV，再去读取深度”这个方向是对的。
>
> 更准确地说：**根据当前片元在画面上的位置，计算屏幕 UV；用这个地址读取相机深度纹理，得到该位置记录的一个深度数值。**
>
> Viewport 是绘制区域，不是保存 UV 的容器。深度纹理保存深度，UV 是你用来查询它的地址。
>
> 读出的数值通常还不是以场景单位表示的距离。需要“前方多远”，就线性化；需要“世界里的哪个点”，就结合 UV 和相机矩阵重建位置。

**阅读顺序：**Q1～Q4 理解“查什么”；Q5～Q9 理解 `SV_Position.xyzw`；Q10～Q16 理解“查到后怎么办”；Q17～Q20 用代码和小题检查理解。

本文以普通网格绘制、单相机、全尺寸视口、常规透视投影为主；正交相机另行解释。数字例子是教学计算，不是某一台机器的运行截图。API 与 URP 方法依据文末及相应段落的官方资料核对；未在你的 Unity 工程中编译、运行示例。

## Q1：深度的 UV 是“记录在 Viewport 上”的吗？

不太准确。这里有三个不同的东西：

| 名词 | 可以怎样理解 | 它回答什么问题 |
|---|---|---|
| Viewport，视口 | 这次绘制使用的矩形区域 | 三角形映射到哪一块画面？ |
| 屏幕 UV | 用两个比例表示的图像地址 | 去这张图的哪个位置查？ |
| 深度缓冲／深度纹理 | 按图像位置排列的一张深度表 | 那个位置存的深度是多少？ |

想象一张有 800 列、600 行的表格。每格保存一个深度数值。

你可以用“第几列、第几行”定位一格，也可以用“横向到 25%、纵向到 50%”定位附近的位置。后者就是 UV 的基本意思。

**地址不需要跟着每一个深度值一起存进去。** 表格有行列布局，你根据位置就能找到它。

因此，“深度的 UV”更适合叫作**采样深度纹理用的屏幕 UV**。它不是深度值自带的属性，也不是模型展开贴图时制作的 Mesh UV。

## Q2：屏幕 UV 怎么得到？和模型 UV 有什么区别？

普通模型贴图的 UV 来自网格顶点，经过插值到达片元；屏幕 UV 可以根据片元当前所在的图像位置计算。

假设绘制目标为 `800 × 600`，当前片元位于像素中心 `(200.5, 300.5)`。暂时采用与纹理一致的坐标方向，那么：

```text
u = 200.5 / 800 ≈ 0.250625
v = 300.5 / 600 ≈ 0.500833
```

这就把“像素单位的位置”变成了“图像宽高的比例”。`.5` 表示像素中心，例如第一格的中心通常是 `0.5`，不是 `0`。

| 对比项 | 模型 UV | 屏幕 UV |
|---|---|---|
| 来源 | Mesh 中的纹理坐标 | 当前片元在渲染图像中的位置 |
| 常见用途 | 在物体表面贴花纹 | 读取相机深度、场景颜色 |
| 移动相机以后 | 同一表面点的模型 UV 通常不变 | 同一表面点对应的屏幕 UV 通常改变 |
| 是否必须有 Mesh UV | 通常需要 | 根据 `SV_POSITION` 计算时不需要 |

第 12 章用的是：

```hlsl
// 在片元函数内；这里的 positionCS 必须是 SV_POSITION 输入。
float2 screenUV = GetNormalizedScreenSpaceUV(IN.positionCS);
```

**不要因为参数名叫 `positionCS`，就把顶点阶段尚未除以 w 的裁剪坐标直接传进去。** 这个用法需要的是片元位置。Unity 的 [URP 变换方法文档](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/use-built-in-shader-methods-transformations.html)把该方法的输入说明为像素位置。

上面的“除以宽高”帮助理解归一化的核心。真正写 URP Shader 时保留库函数；实际实现还可能处理屏幕方向等约定，见 [ShaderVariablesFunctions.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/ShaderVariablesFunctions.hlsl)。

> [!note] 视口和纹理不一定一样大
> 本文数字例子假设视口覆盖整个目标。若视口只是大纹理的一小块，“视口内 50%”不一定是“整张纹理的 50%”。还要考虑偏移、缩放，以及渲染目标方向、动态分辨率或 XR 布局。不要给所有项目硬编码一个 `800 × 600`，也不要不检查就额外翻转 Y。

## Q3：Depth Buffer 和 Camera Depth Texture 是同一个东西吗？

**用途要分开理解，底层存储是否共享由渲染管线决定。**

| 对象／操作 | 主要用途 |
|---|---|
| Depth Buffer，深度缓冲 | 绘制时进行深度测试，并按设置更新深度 |
| Camera Depth Texture，相机深度纹理 | 向 Shader 提供可以读取的场景深度 |
| `SampleSceneDepth(uv)` | 在相机深度纹理的指定地址读取一个数 |
| `ZTest` | 控制当前绘制如何进行深度比较 |
| `ZWrite` | 控制当前绘制是否写入深度 |

URP 可以通过深度预通道生成深度，也可以在某个时机从已有深度复制或解析出可采样资源。因此，**采样到的内容由生成方式和生成时机决定，不能当成“现在正在写入的深度缓冲的实时查询”。**

`SampleSceneDepth` 的资源入口可查看 Unity 的 [DeclareDepthTexture.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl)。具体生成路径以项目所用 Renderer 和包版本为准。

读深度也不会自动执行你的遮挡判断：

```hlsl
float d = SampleSceneDepth(screenUV); // 读取数据
```

这句没有要求 GPU 丢弃当前片元。普通遮挡主要由 `ZTest` 等状态处理；`ZWrite Off` 也不代表关闭深度测试。参见 [ZTest](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-ZTest.html) 和 [ZWrite](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-ZWrite.html)。

## Q4：深度是从哪里来的？一个位置能记录前后所有物体吗？

普通情况下，来自几何位置经过投影后的深度。

```text
三角形顶点的位置
    ↓ 顶点变换
裁剪空间位置 (xc, yc, zc, wc)
    ↓ 裁剪、透视除法、视口映射、光栅化
当前片元的图像位置与设备深度
    ↓ 深度测试通过，并且允许写深度
深度缓冲相应位置得到更新
    ↓ 管线在合适时机提供可采样资源
其他效果可以读取相机深度纹理
```

这是理解数据来源的图，不是 GPU 每一步的严格执行时刻表；硬件可以提前做部分深度测试。[Microsoft 光栅化阶段说明](https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-rasterizer-stage)

因此，普通片元函数即使只通过 `SV_Target` 返回颜色，GPU 仍然可以按几何位置进行深度测试和写入。**你不需要把颜色的某个通道当作深度返回。** 特殊效果可以另外输出 `SV_Depth` 覆盖用于测试／写入的深度，但那是额外机制，不是本文的默认情况。[Microsoft 系统值语义](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics)

设同一画面位置有前景箱子和后方墙壁：

```text
相机 ─── 箱子表面 ───────── 墙壁
             ↑                 ↑
          前方 2 单位         前方 8 单位
```

在常规不透明绘制和深度状态下，该位置最终保留箱子表面的深度。**普通深度纹理不是一条保存“箱子 2、墙壁 8、后面还有谁”的列表。** 单凭它不能恢复被箱子挡住的墙。

这里按每位置一个深度来入门。MSAA 可能每像素保存多个样本的深度，但也不是按前后层次保存所有物体。

## Q5：SV_Position 是什么？positionCS 这个名字有什么特殊作用？

看这段声明：

```hlsl
float4 positionCS : SV_POSITION;
```

分开读：

| 部分 | 含义 |
|---|---|
| `float4` | 四个浮点分量，可以访问 `.x`、`.y`、`.z`、`.w` |
| `positionCS` | 程序员起的字段名，`CS` 通常是 Clip Space 的缩写 |
| `: SV_POSITION` | 系统值语义，告诉图形管线这个字段承担位置接口的作用 |

**字段名可以改，系统语义才决定管线如何处理它。** 把字段改名为 `myPosition` 并同步修改引用，不会因此改变坐标变换规则。

`SV` 表示 System Value。`SV_Position` 和常见大写写法 `SV_POSITION` 指的是同一个语义。这个语义在不同阶段承担不同作用，不能只看名字就断定数值仍处在同一个空间。[Microsoft HLSL 语义说明](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics)

## Q6：顶点着色器输出的 SV_Position.xyzw 分别是什么？

在本文的顶点／片元流程里，顶点着色器输出的是**齐次裁剪空间位置**：

```hlsl
OUT.positionCS = TransformObjectToHClip(IN.positionOS);
```

| 分量 | 顶点输出中的含义 | 现在能不能直接当屏幕数据？ |
|---|---|---|
| `x` | 裁剪空间横向分量 `xc` | 不能直接当像素坐标或 UV |
| `y` | 裁剪空间纵向分量 `yc` | 不能直接当像素坐标或 UV |
| `z` | 裁剪空间深度分量 `zc` | 不能直接当深度纹理中的值 |
| `w` | 齐次分量 `wc`，参与裁剪和后续除法 | 不是 Alpha，也不是随手填的第四个数 |

你不必先掌握齐次坐标的全部数学。先把它理解成：**这个位置还带着一个需要参与计算的分母。**

后续透视除法的核心是：

```text
xNDC = xc / wc
yNDC = yc / wc
zNDC = zc / wc
```

NDC 是 Normalized Device Coordinates，即标准化设备坐标。它还要经过视口映射，才变成像素单位的位置。

对 Unity 常规透视相机，可把相机前方的正距离记为 `d = -positionVS.z`；通常投影矩阵令 `wc = d`。横向位置相同但更远的点，除以更大的 `w` 后，更靠近画面中心，这与“近大远小”有关。**标准正交投影的 w 通常为 1，所以不能把 w 永远理解成距离。**

`TransformObjectToHClip` 的输出空间见 [Unity 6.7 URP 变换方法](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/use-built-in-shader-methods-transformations.html)。

## Q7：能用数字演示从顶点位置到屏幕位置吗？

可以。这里只演示坐标计算，采用 D3D 风格的 NDC 深度范围、普通非反转深度、顶端为屏幕 Y 起点，视口为 `800 × 600`。

某点的裁剪空间位置为：

```text
(xc, yc, zc, wc) = (0.5, 0, 1.1, 2)
```

先除以 `w = 2`：

```text
NDC = (0.25, 0, 0.55)
```

再进行视口映射：

```text
屏幕 x = (0.25 × 0.5 + 0.5) × 800 = 500
屏幕 y = (0.5 - 0 × 0.5) × 600 = 300
设备深度 = 0.55
```

请注意这些数的区别：

| 数据       |    数值 | 含义                 |
| -------- | ----: | ------------------ |
| 裁剪空间 `x` |   0.5 | 还没有除以 w 的横向分量      |
| NDC `x`  |  0.25 | 除以 w 后的横向分量        |
| 屏幕 `x`   |   500 | 像素单位的位置            |
| 屏幕 `u`   | 0.625 | `500 / 800`，图像横向比例 |
| 裁剪空间 `z` |   1.1 | 尚未除以 w 的深度分量       |
| 设备深度     |  0.55 | 本例中用于深度缓冲的深度表示     |

这里算出的 `(500, 300)` 是几何点的连续投影位置。实际光栅化是在三角形覆盖范围内产生片元；某个附近的像素中心可以是 `(500.5, 300.5)`，不应把每个顶点想成必然对应一个片元。

也不要把上面的 Y 公式原样套进所有 Unity 后端。它是指定方向下的教学公式。

## Q8：为什么片元阶段的 positionCS 不再是裁剪空间？xyzw 又是什么？

因为 `SV_POSITION` 是一个由管线特殊处理的接口。顶点输出之后，GPU 已经执行了裁剪、除法、映射和光栅化等工作。片元输入拿到的是**当前片元的位置数据**。

```text
顶点阶段：OUT.positionCS : SV_POSITION
          裁剪空间位置
                ↓ GPU 特殊处理
片元阶段：IN.positionCS : SV_POSITION
          当前片元的窗口／屏幕位置数据
```

字段名沿用 `positionCS`，只是源代码沿用了同一个结构体，**不是“数值仍在 Clip Space”的保证**。

先以 **Direct3D 的标准片元输入定义**解释四个分量：

| 分量 | 片元输入中的含义 |
|---|---|
| `x` | 当前片元在渲染目标中的横向位置，以像素为单位 |
| `y` | 当前片元在渲染目标中的纵向位置，以像素为单位 |
| `z` | 当前片元的设备深度；本文常规深度范围下通常为 0～1 |
| `w` | 当前片元对应的齐次 w：先对顶点的 `1/w` 作屏幕线性插值，再取倒数 |

例如一个所有顶点 `wc = 2`、设备深度都为 `0.55` 的平面三角形，在覆盖 `(500.5, 300.5)` 时，D3D 片元输入可理解为：

```text
SV_Position = (500.5, 300.5, 0.55, 2)
```

**片元的 w 不是因为“做过除法”就必然变成 1，也不能一律写成 `1 / 原来的 w`。** D3D 的确切定义见 [Direct3D 11.3 规范 §16.3](https://microsoft.github.io/DirectX-Specs/d3d/archive/D3D11_3_FunctionalSpec.htm)。

### 为什么有教程说片元 w 是倒数？

原生 OpenGL / GLSL 的 `gl_FragCoord.w` 采用的是 `1/w`，因此上面恒定 `wc = 2` 的例子中，它的第四分量是 `0.5`。这与 D3D 的输入定义不同。[Khronos GLSL 4.60 规范：gl_FragCoord](https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html)

Unity 会把 HLSL 编译到不同图形后端，编译器可能做相应的兼容转换。**不能只凭某篇 OpenGL 教程，就断言 Unity 所有平台上的 `IN.positionCS.w` 都是倒数；也不要把某个 D3D 结果当作未经验证的跨平台承诺。**

本 FAQ 后面的 URP 写法用 `.xy` 得到屏幕 UV，用深度纹理或显式世界位置求距离，不依赖对片元 `.w` 的猜测。

> [!tip] 最需要记住的对照
> 顶点输出：`xyzw` 是齐次裁剪坐标。
>
> 片元输入：`xy` 是像素位置，`z` 是当前片元的设备深度，`w` 要按 API／编译约定理解。
>
> 这个结论针对字段确实带有 `SV_POSITION` 的情形。一个仅仅叫 `positionCS`、却放在 `TEXCOORD0` 里的普通插值数据，不会自动变成屏幕像素坐标。

## Q9：什么时候应该除以 w？为什么有的代码除，有的不除？

先确认手里的数据是什么。

| 手里的数据 | 求屏幕位置／UV 时怎么处理 |
|---|---|
| 真正的齐次裁剪空间位置 | 概念上先用 `.xy / .w` 得到 NDC，再做范围和方向映射 |
| 片元阶段的 `SV_POSITION` | `.xy` 已经是像素位置，按渲染尺寸归一化；不要再做裁剪空间透视除法 |
| 由 `ComputeScreenPos` 计算并通过普通插值通道传递的结果 | 是另一种投影坐标表示，常见用法是在片元里 `.xy / .w` |

所以这句是第 12 章的正常用法：

```hlsl
float2 screenUV = GetNormalizedScreenSpaceUV(IN.positionCS);
```

而这句在同一上下文中是错误思路：

```hlsl
// 错误：IN.positionCS 是片元 SV_POSITION，不是顶点的裁剪空间输出。
float2 screenUV = IN.positionCS.xy / IN.positionCS.w;
```

**并不是 Shader 中不能除以 w，而是不能把一种表示对应的公式套到另一种表示上。**

## Q10：读出的 rawDepth 到底是什么？为什么不是距离？

```hlsl
float rawDepth = SampleSceneDepth(screenUV);
```

结果是那个地址记录的**原始设备深度**，通常是 0～1 范围内的一个数。它不是 RGB，不是世界坐标，也不是“有几米远”。Unity 的 [深度重建示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-reconstruct-world-position.html)说明了采样值范围及其与 NDC 的区别。

透视投影为了实现近大远小，要进行除以 `w` 的计算。深度也参与这个过程，使通常的设备深度与前向距离不是直线关系。

下面自己算一个例子。设：

```text
Near = 1
Far  = 11
d    = 沿相机正前方方向的距离，范围为 1～11
```

对于本例采用的普通透视投影、近 0 远 1 编码：

```text
rawDepth = Far / (Far - Near)
         - Far × Near / ((Far - Near) × d)

代入本例：rawDepth = 1.1 - 1.1 / d
```

| 前向距离 d | 普通深度：近 0，远 1 | 同一投影的反转深度：近 1，远 0 |
|---:|---:|---:|
| 1 | 0 | 1 |
| 2 | 0.55 | 0.45 |
| 3 | 约 0.733333 | 约 0.266667 |
| 6 | 约 0.916667 | 约 0.083333 |
| 11 | 1 | 0 |

从 `d = 1` 到 `d = 2`，原始深度改变 `0.55`；从 `d = 2` 到 `d = 3`，只改变约 `0.183333`。同样前进 1 单位，深度数值变化不同——这就是这里说的**非线性**。

因此，`rawDepth = 0.5` **不表示处于 Near 和 Far 的中点**。

Reverse-Z／Reversed-Z 是把近远的数值方向反过来。它不等于“已经线性化”。写跨平台代码时使用 `UNITY_REVERSED_Z` 和 Unity 提供的参数，不要死记“白一定远、黑一定近”。

## Q11：LinearEyeDepth 做了什么？_ZBufferParams 是什么？

```hlsl
float eyeDepth = LinearEyeDepth(rawDepth, _ZBufferParams);
```

可以读成：

> 根据当前相机的深度编码参数，把刚才采样出的设备深度，换算为沿相机前方方向的距离。

**“线性化”是改变深度数值的表示，不是把图像拉直，也不是多采样几次。**

`_ZBufferParams` 是 Unity 为当前相机准备的一组换算参数，与近远裁剪面、反转深度约定有关。它不是另一张纹理。参见 [Unity 内置 Shader 变量](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-UnityShaderVariables.html)。

常见透视版函数的运算核心为：

```hlsl
eyeDepth = 1.0 / (_ZBufferParams.z * rawDepth + _ZBufferParams.w);
```

继续上一节 `Near = 1`、`Far = 11` 的普通深度例子：

```text
_ZBufferParams.z = -10 / 11
_ZBufferParams.w = 1

rawDepth = 0.55
eyeDepth = 1 / ((-10/11) × 0.55 + 1)
         = 1 / 0.5
         = 2
```

所以刚才的 `0.55` 被还原成了前方 `2` 个场景单位。

**不要先手动把 Reverse-Z 翻转，再把原本匹配反转深度的 `_ZBufferParams` 传进去。** 参数本来就负责对应的解码。

另一个常见函数 `Linear01Depth(rawDepth, _ZBufferParams)` 在这种透视流程下相当于 `eyeDepth / Far`。它在近裁剪面对应 `Near / Far`，不一定是 0；如果你要“Near 为 0、Far 为 1”，应计算 `(eyeDepth - Near) / (Far - Near)`。

这些函数重载的实现和适用范围见 [Unity Core RP Common.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl)。本节的两参数深度解码不适用于标准正交投影，也不能直接用于所有斜裁剪投影。

## Q12：eyeDepth 不是相机到物体的距离吗？

它是距离的一种，但需要说明方向：**沿相机正前方轴测量的距离**，不是相机到该点的直线长度。

用相机空间举例：相机在原点，正前方为 `-Z`。

```text
A = (0, 0, -4)
B = (3, 0, -4)
```

| 点 | eyeDepth | 到相机原点的直线距离 |
|---|---:|---:|
| A | 4 | 4 |
| B | 4 | √(3² + 4²) = 5 |

A 和 B 都在“相机前方 4 单位的平面”上，所以 `eyeDepth` 一样；B 还向侧面偏了 3 单位，斜着量的直线距离更长。

```text
              B ●
               /│
     直线距离5 / │ 侧向偏移3
             /  │
相机 O ─────────● A
        前向距离4
```

Unity 常规相机空间中：

```hlsl
float eyeDepth = -positionVS.z;
float distanceToCamera = length(positionVS);
```

这里假设点位于相机前方，且使用标准相机变换。若项目约定 1 单位等于 1 米，你才可以把这些数读成米。

## Q13：片元的 IN.positionCS.z 和采样出的 rawDepth 有什么区别？

**前者属于当前正在画的表面；后者属于深度纹理在这个地址记录的表面。**

假设你正在画一片透明水面，深度纹理已经记录了不透明池底：

```text
同一个屏幕 UV：

相机 ─── 水面 ───────── 池底
         前方3单位       前方5单位
         当前片元        深度纹理中的表面
```

| 表达式 | 在这个例子里代表谁 |
|---|---|
| 片元 `IN.positionCS.z` | 水面当前片元的设备深度 |
| `SampleSceneDepth(screenUV)` | 池底记录在相机深度纹理中的设备深度 |

两者可能不同，也可能因为纹理中记录的恰好就是自己而相近。**不能根据 `SV_POSITION` 的存在推断它读过深度缓冲。** 它的位置数据来自当前图元的光栅化。

全屏效果更容易混淆：全屏三角形的 `SV_POSITION.z` 是那个三角形自己的深度，不是画面中山、墙、人物的深度；要查询场景，仍然需要读场景深度。

## Q14：拿到深度以后，应该接着做什么？

这取决于你想得到哪一种信息，并不是每种情况都必须先线性化再重建。

```text
当前片元 SV_POSITION.xy
          ↓ 归一化
       screenUV
          ↓ SampleSceneDepth
       rawDepth
          ├─ 需要前向距离 → LinearEyeDepth → eyeDepth
          │                                  ↓
          │                          雾、接触渐变等计算
          │
          └─ 需要世界位置 → 调整为 NDC 深度
                                             ↓ 加上 UV、逆视图投影矩阵
                                      scenePositionWS
                                             ↓
                                      世界高度、直线距离等计算
```

重新逐句读第 12 章第一段代码：

```hlsl
// 1. 当前片元在画面的哪个位置？得到查询地址。
float2 screenUV = GetNormalizedScreenSpaceUV(IN.positionCS);

// 2. 这个地址在相机深度纹理里记录了什么？得到一个设备深度值。
float rawDepth = SampleSceneDepth(screenUV);

// 3. 对常规透视投影，把设备深度换算为场景表面的前向距离。
float eyeDepth = LinearEyeDepth(rawDepth, _ZBufferParams);
```

前两句没有求出实际距离。第三句才在做距离换算，而且得到的是**刚才采样到的场景表面**的前向距离。

如果只是想观察远近，可以继续写：

```hlsl
// 将“前方 0～10 单位”映射到黑～白；更远的值夹到白色。
float gray = saturate(eyeDepth / 10.0);
return half4(gray, gray, gray, 1);
```

这里的 `/ 10.0` 是为了显示而选的尺度；它不是深度解码的一部分。未写深度的背景应先排除，见 Q17。

## Q15：为什么 UV 加上深度，就可以恢复世界位置？

对透视相机，画面上的一个地址对应一条从相机出发的射线。

```text
只知道 UV：
相机 ────── A ─────── B ─────── C
           这条射线上的多个点都可能投影到同一位置

再知道这个地址记录的深度：
相机 ─────────────── B
                    可以确定记录表面在射线上的位置
```

UV 告诉你往哪个方向找；深度和相机投影规则帮助你确定找多远；相机在世界中的位置和朝向则把结果放回世界。

代码如下，假设 `screenUV` 已经与深度纹理及当前相机匹配：

```hlsl
float rawDepth = SampleSceneDepth(screenUV);

#if UNITY_REVERSED_Z
    float ndcDepth = rawDepth;
#else
    float ndcDepth = lerp(UNITY_NEAR_CLIP_VALUE, 1.0, rawDepth);
#endif

float3 scenePositionWS = ComputeWorldSpacePosition(
    screenUV, ndcDepth, UNITY_MATRIX_I_VP);
```

三个参数的工作分别是：

| 参数 | 作用 |
|---|---|
| `screenUV` | 提供画面中的横纵位置 |
| `ndcDepth` | 提供符合当前投影约定的 NDC 深度 |
| `UNITY_MATRIX_I_VP` | 当前相机视图投影矩阵的逆，负责反向变换 |

### 为什么要先调整 rawDepth？

纹理采样值是 0～1，但 NDC 深度的约定可能不同。上面的代码采用 [Unity 6.7 官方重建示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-reconstruct-world-position.html)的处理方式：非反转分支中，如果近端 NDC 为 `-1`，就把 0～1 改映射到 -1～1；如果近端为 `0`，数值保持不变。

例如：

```text
rawDepth = 0.75

NDC 范围 0～1 时：   ndcDepth = 0.75
NDC 范围 -1～1 时：  ndcDepth = -1 + 2 × 0.75 = 0.5
```

**范围转换不是线性化。** 这里的 `0.5` 仍然不是场景单位的距离。

也不要把 `LinearEyeDepth` 算出的 `5` 传给这个位置的 `ndcDepth` 参数。逆投影矩阵需要的是投影后的坐标表示，不是你已经换算好的前向距离。

### 逆矩阵内部在做什么？

概念上，它把 UV 映射回 NDC 横纵坐标，与 NDC 深度组成齐次坐标，再乘逆矩阵，最后除以结果的 w。Unity 的函数负责对应的坐标方向处理。实现可见 [Common.hlsl 的 ComputeWorldSpacePosition](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl)。

这里又出现了“除以 w”，但除的是**逆变换新得到的齐次位置的 w**，不是拿片元 `SV_POSITION.xy` 随意再除一次。

不需要从纹理里读取原始顶点 w：齐次坐标允许整体按同一个比例缩放，重建时可以从 NDC 构造 w 为 1 的代表，逆变换后的最终除法会消除这个比例。

> [!note] 恢复的是哪个点？
> 恢复的是深度纹理记录的表面点。在水面例子中是池底，在全屏效果中是场景表面。它不是当前绘制网格的位置，也不是被遮挡物体的位置。精度受深度存储、采样和矩阵匹配影响。

## Q16：能把 UV、rawDepth、eyeDepth、世界位置放在同一个例子里吗？

设一个便于手算的相机：位于世界原点，看向世界 `-Z`；透视投影的水平和垂直视场角都为 90°，宽高比为 1，`Near = 1`、`Far = 11`。使用普通近 0 远 1 深度。

深度纹理在 `UV = (0.75, 0.5)` 记录了 `rawDepth = 0.825`。

**第一步：把深度换算为前向距离。**

```text
0.825 = 1.1 - 1.1 / d
1.1 / d = 0.275
d = 4
```

**第二步：根据 UV 得到方向位置。** 本例纵向在正中间，不涉及 Y 翻转差别：

```text
xNDC = 0.75 × 2 - 1 = 0.5
yNDC = 0
```

**第三步：利用本例 90° 投影的关系恢复位置。**

```text
xNDC = x / d → x = 0.5 × 4 = 2
y = 0
z = -d = -4

世界位置 = (2, 0, -4)
```

| 名称 | 结果 | 它回答什么 |
|---|---|---|
| `screenUV` | `(0.75, 0.5)` | 画面哪里？ |
| `rawDepth` | `0.825` | 纹理中存的设备深度是多少？ |
| `eyeDepth` | `4` | 沿相机前方方向多远？ |
| `scenePositionWS` | `(2, 0, -4)` | 在世界的哪个位置？ |
| 到相机的直线距离 | `√20 ≈ 4.472` | 从相机到这个点斜着量有多远？ |

真实相机的视场角、位置和旋转可以不同，`ComputeWorldSpacePosition` 用矩阵统一处理这些差别。

## Q17：给我一段把这些概念接起来的 URP 代码，好吗？

下面是一组**放进已有网格 Pass 的代码片段，不是完整 Shader 文件**。它展示结构体、顶点函数和片元函数的联系。已有同名声明时应替换，不能重复粘贴。

Pass 需要通过 `#pragma vertex Vert`、`#pragma fragment Frag` 指定入口，并包含：

```hlsl
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl"

struct Attributes
{
    float3 positionOS : POSITION;
};

struct Varyings
{
    float4 positionCS : SV_POSITION;
};

Varyings Vert(Attributes IN)
{
    Varyings OUT;
    // 此处输出的是齐次裁剪空间位置。
    OUT.positionCS = TransformObjectToHClip(IN.positionOS);
    return OUT;
}

half4 Frag(Varyings IN) : SV_Target
{
    // 到这里，SV_POSITION.xy 已经是当前片元的像素位置。
    float2 screenUV = GetNormalizedScreenSpaceUV(IN.positionCS);
    float rawDepth = SampleSceneDepth(screenUV);

    // 本例把默认远端清除值当作背景，显示黑色。
    // 这是背景启发式判断，恰在远端的几何也可能被当作背景。
    #if UNITY_REVERSED_Z
        if (rawDepth <= 0.0)
            return half4(0, 0, 0, 1);
    #else
        if (rawDepth >= 1.0)
            return half4(0, 0, 0, 1);
    #endif

    // 转为重建所需要的 NDC 深度，注意这里没有先 LinearEyeDepth。
    #if UNITY_REVERSED_Z
        float ndcDepth = rawDepth;
    #else
        float ndcDepth = lerp(UNITY_NEAR_CLIP_VALUE, 1.0, rawDepth);
    #endif

    float3 scenePositionWS = ComputeWorldSpacePosition(
        screenUV, ndcDepth, UNITY_MATRIX_I_VP);

    // 从重建出的场景点求前向距离；常规透视和正交相机都可采用。
    float3 scenePositionVS = TransformWorldToView(scenePositionWS);
    float sceneEyeDepth = -scenePositionVS.z;

    float gray = saturate(sceneEyeDepth / 10.0);
    return half4(gray, gray, gray, 1);
}
```

这里没有 Mesh UV，也没有使用 `IN.positionCS.w`。输出灰度只是为了让你观察读到的场景深度。

如果要在普通场景里观察，可以用一个覆盖部分画面的测试 Quad，设置 `Cull Off`、`ZWrite Off`、`ZTest Always`、`Blend Off`，放在透明队列；让场景中的箱子、地面使用官方 URP/Lit。**前提是配置深度纹理在这个测试绘制之前已生成**，例如使用不透明之后复制深度的配置或合适的预通道。这个 Quad 的效果是把它覆盖的部分显示成场景深度灰度图。

要确认以下实际条件：

1. URP Asset 和当前相机启用了或请求了 Depth Texture。
2. 用 Frame Debugger 确认相机深度资源在读取它的 Pass 之前已经准备好。仅写 `#include` 不会请求管线生成资源。
3. 要被记录的物体参与了对应的深度生成过程；预通道路径下，自定义 Shader 需要匹配的深度 Pass 和一致的裁剪／位移。

自定义 Renderer Feature 还需要声明深度输入和合适的执行时机。全屏 Blit、XR、相机堆叠等流程应使用对应的输入结构与资源约定，不能直接照搬这个普通网格片段。

> [!tip] 正交相机为什么也可以走这条路？
> 标准正交投影没有透视式的 `1/d` 深度关系，所以不能直接套 Q11 的透视解码公式。匹配相机的逆视图投影矩阵能反向处理它自身的投影：先重建场景位置，再用相机空间 `-z` 得到前向距离。背景仍应先排除。

## Q18：水面与池底相减，得到的就是水深吗？

需要先说明两种深度必须在**同一个坐标定义、同一种单位**下比较。

在 Q13 的例子里，如果水面前向距离为 3、池底为 5，那么：

```text
前向深度差 = 5 - 3 = 2
```

可以把这个差值映射到透明度，做接触处变淡的效果：

```hlsl
// 局部示意：三个输入都需要由你的 Shader 提供。
// surfaceEyeDepth 是当前表面的前向距离，sceneEyeDepth 是采样表面的前向距离。
float gap = max(sceneEyeDepth - surfaceEyeDepth, 0.0);
float fade = saturate(gap / max(_FadeDistance, 0.0001));
```

当前表面的距离可以通过顶点阶段传递世界位置获得：

```hlsl
// Varyings 增加：
float3 positionWS : TEXCOORD0;

// Vert 增加，使用与位置输出相同的几何变形结果：
OUT.positionWS = TransformObjectToWorld(IN.positionOS);

// Frag 中求当前表面前向距离：
float surfaceEyeDepth = -TransformWorldToView(IN.positionWS).z;
```

但“沿相机前方的距离差”不自动等于“沿世界竖直方向的水深”，也不一定等于沿观察射线的长度；相机倾斜时这些长度会不同。若需要世界空间中的长度或高度，应重建位置后按照所需方向计算。

也不能用 `rawDepth - surfaceEyeDepth`：这相当于用编码数值减场景单位，含义不一致。

## Q19：为什么我采样后全白、全黑，或者看不到透明物体？

| 现象 | 常见原因与检查方向 |
|---|---|
| 直接输出 rawDepth 几乎全白／全黑 | 透视设备深度分布不均匀，并受 Reverse-Z 影响；先排除资源问题，再换成线性距离调试 |
| 输出 eyeDepth 全白 | 直接输出的值大于 1；按观察范围缩放，例如 `saturate(eyeDepth / 10)` |
| 怎么移动物体都几乎没变化 | 深度资源未生成、Pass 读取过早、读错相机资源，或被测物体没有进入深度生成路径 |
| 透明玻璃在画面里有，深度图里没有 | 普通透明材质通常关闭深度写入，而且相机深度纹理可能在透明物体绘制前已生成 |
| 给透明物体开 ZWrite，依然读不到 | 可采样深度纹理的生成时机仍可能更早；写当前深度缓冲不等于更新已生成的深度纹理 |
| 重建出来上下颠倒或位置错乱 | UV 方向／范围、NDC 深度范围或矩阵与纹理不匹配；检查是否额外翻转 Y 或错误地传入线性深度 |
| 相机切成正交后数值不对 | 仍使用了针对常规透视的 `_ZBufferParams` 解码方式 |
| 背景出现极远点或异常图案 | 把未写入几何的清除深度当成了有效表面 |

深度纹理不会随时囊括“你肉眼看到的一切”。读数前，先明确它记录了哪些绘制、截至哪个时刻。

## Q20：读完以后，我应该能回答哪些问题？

先自己回答，再核对。

**1. Viewport 是不是保存屏幕 UV 的一张表？**

不是。它是绘制区域；屏幕 UV 是查询图像的地址，深度资源保存地址对应的数值。

**2. 顶点阶段 `positionCS.xy = (0.2, 0.4)`，可以直接当屏幕 UV 吗？**

不可以。若它是真正的裁剪空间位置，还需要考虑 w、NDC 范围以及屏幕方向。

**3. 片元 `SV_POSITION.xy = (200.5, 300.5)`，它还是裁剪坐标吗？**

不是。在本文的常规网格片元输入中，它已经是像素单位的位置。

**4. 顶点把 w 输出为 2，片元的 w 一定是 0.5 吗？**

不是。D3D 与原生 GLSL 定义不同；即使限定 D3D，三角形内部还涉及插值，不能随便取某一个顶点的 w 来代表整片三角形。

**5. 深度纹理读到 0.8，表示离相机 0.8 米吗？**

不表示。先看投影及深度编码，按需要解码。

**6. eyeDepth 为 5，表示到相机的直线距离必然是 5 吗？**

不一定。它通常是前向距离，偏离画面中心的点可能有更大的直线距离。

**7. 重建位置之前，一定要先 LinearEyeDepth 吗？**

不需要。第 12 章的重建接口使用 UV、NDC 深度和逆视图投影矩阵。

**8. 相机深度纹理能告诉我被箱子挡住的墙在哪里吗？**

通常不能。那个位置若记录的是箱子，就只能由这份数据重建箱子表面。

**9. 当前水面片元的 z 与同位置采样到的池底深度，是同一个表面的信息吗？**

不是。当前片元位置来自正在画的水面，采样结果来自深度纹理记录的池底。

## 资料与核对范围

相关笔记：[[从零理解图形学渲染管线]]、[[从零认识计算机图形学-GAMES101与GAMES202学习地图]]、[[UV插值与纹理采样如何正确使用]]、[[图元装配在什么阶段发生]]。

本篇于 2026-09-16 对照 Unity 6000.7 文档、Microsoft Direct3D 规范和 Khronos GLSL 规范整理。正文各关键结论就近链接来源；其中最容易混淆的两项分别是 [URP 深度重建所用的坐标表示](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-reconstruct-world-position.html)以及 [Direct3D 片元位置的 w 定义](https://microsoft.github.io/DirectX-Specs/d3d/archive/D3D11_3_FunctionalSpec.htm)。

链接到 Unity Graphics `master` 的文件用于核对函数原理与导航，不声称它们就是你安装的 Unity 6.7 包版本。实际工程应在 Packages 内检查同名函数及 Renderer 资源生成路径。本文示例经过数字和文本静态核对，没有声称通过 Unity Editor 编译或目标平台运行验证。
