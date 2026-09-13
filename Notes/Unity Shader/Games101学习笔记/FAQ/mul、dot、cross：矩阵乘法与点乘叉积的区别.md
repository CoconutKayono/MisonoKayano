# mul、dot、cross：矩阵乘法与点乘叉积的区别

> mul 是矩阵变换？还是 dot 是？还是 cross 是？我在看 GAMES101 第二、第三节课。

**在 HLSL 中，把矩阵作用到一个向量上，通常写 `mul(M, v)`；`dot` 是点乘，`cross` 是叉积。** 三者不是同一种“乘法”。

## 1. 按输入、输出和目的区分

| 写法 | 数学含义 | 输出 | 常见用途 |
| --- | --- | --- | --- |
| `mul(M, v)` | 矩阵乘列向量 $Mv$ | 向量 | 将点或向量变换到另一个位置或坐标空间 |
| `mul(A, B)` | 矩阵乘矩阵 $AB$ | 矩阵 | 合并多个变换 |
| `dot(a, b)` | 点乘 $\mathbf a\cdot\mathbf b$ | 数 | 求投影、判断夹角关系 |
| `cross(a, b)` | 三维叉积 $\mathbf a\times\mathbf b$ | 三维向量 | 构造法线、计算面积 |

函数定义见微软官方文档：[mul](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-mul)、[dot](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-dot)、[cross](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-cross)。

**矩阵存放变换规则，mul 执行乘法；具体是缩放还是旋转，由矩阵内容决定。** 不是看到 mul 就一定在做几何变换。

## 2. 用同一个向量看区别

设 $v=(3,2)$，缩放矩阵为：

$$
M=\begin{pmatrix}2&0\\0&2\end{pmatrix}
$$

那么：

$$
Mv=(6,4),\qquad (3,2)\cdot(1,0)=3
$$

前者把整个向量放大，后者测量它沿右方的分量。

HLSL 形式：

```hlsl
float2 v = float2(3, 2);
float2x2 M = float2x2(2, 0, 0, 2);
float2 scaled = mul(M, v);                     // (6, 4)
float projected = dot(v, float2(1, 0));         // 3
float3 n = cross(float3(3, 0, 0), float3(0, 2, 0)); // (0, 0, 6)
```

最后一行的结果长度为 6，是两条边撑开的面积；空间朝向结合坐标系约定理解。

## 3. 矩阵乘法里面也有点乘，为什么？

矩阵乘列向量时，**每一行与输入向量点乘，得到输出的一个分量**：

$$
\begin{pmatrix}m_{11}&m_{12}\\m_{21}&m_{22}\end{pmatrix}
\begin{pmatrix}x\\y\end{pmatrix}
=\begin{pmatrix}m_{11}x+m_{12}y\\m_{21}x+m_{22}y\end{pmatrix}
$$

因此，一个矩阵变换可以用多次 dot 算出来。单次 dot 得到一个数，把各行的结果组成向量，才得到整个矩阵乘向量的输出。

这就是你可能觉得它们相似的原因：计算存在联系，但完整运算不同。

## 4. mul 的顺序和重载

HLSL 规定：`mul` 左参数若为向量，按行向量处理；右参数若为向量，按列向量处理。因此 `mul(M,v)` 和 `mul(v,M)` 一般不同。两个同维向量传给 `mul(a,b)` 时则得到标量点积；为了表达清楚，点乘通常直接写 `dot(a,b)`。[微软官方：mul 参数与重载](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-mul)

对于列向量约定下的组合变换，可以写：

```hlsl
// T、R、S 为已构造的 float4x4；p 为 float4 位置。
float4 transformed = mul(T, mul(R, mul(S, p)));
```

读作“先 S，再 R，再 T”。三维位置的齐次坐标通常写 `float4(position, 1)`；方向用 `float4(direction, 0)`，使平移不影响方向。法线在非均匀缩放下需要逆转置等专门处理，不能直接当普通方向套同一矩阵。

## 5. 现在怎么记最够用？

> **mul：套矩阵规则。dot：得到一个数。cross：得到垂直向量。**

其中 cross 在输入共线时得到零向量，零向量没有方向。先掌握这些常见用途，再按输入类型处理 mul 的其他情况。

相关笔记：[[FAQ索引]] · [[向量加法与点乘：定义、几何意义和记忆方法]] · [[叉积：为什么是向量、为什么用sin、如何记忆]] · [[变换顺序：为什么TRS是先缩放再旋转最后平移]]
