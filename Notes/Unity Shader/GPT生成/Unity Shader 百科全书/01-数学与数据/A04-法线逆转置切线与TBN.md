# A04｜法线逆转置、切线与 TBN：正确维持表面的方向关系

> **法线的任务是保持与表面切向量垂直。非均匀缩放改变表面后，通常必须用逆转置变换法线；只把错误法线归一化不能恢复垂直关系。TBN 则定义了切线空间细节怎样映射到表面。**

## 1. 自包含的前置概念

本卡用于解释缩放后的错误明暗、法线贴图方向、镜像 UV 接缝和 NPR 描边法线。适用于传统 Mesh 的 URP Shader；不要求读过其他卡片。

- **向量**表达方向和长度；`dot(a,b)` 是对应分量相乘后求和。在正交单位坐标系中，非零向量点积为零表示垂直。
- **normalize(v)** 将非零向量除以长度；改变长度但不改变方向。
- **cross(a,b)** 构造垂直于两个输入的向量；交换输入会反向，平行输入产生零。
- **矩阵 A**在这里是物体到世界仿射变换的左上三阶部分；**逆 A⁻¹**撤销可逆变换，**转置 Aᵀ**交换行列。
- **表面切向量 t**沿表面变化；**法线 n**与该处切平面垂直。顶点法线也可能经作者编辑，用于着色近似，不一定等于每个三角形的面法线。

使用列向量推导。文档基线是本地 Unity **6.7 Beta / 6000.7，2026-06-26**。源码核对 Graphics `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`，URP/Core RP 17.0.4；不将其宣称为 6.7 的逐行实现。

## 2. 从垂直约束推导逆转置

原始表面满足 `nᵀt=0`。普通表面切向量经过变换后是 `t'=A t`。需要寻找 n'，让变换后的表面仍满足：

$$
n'^T t'=0
$$

若选择 `n'=A⁻ᵀn`，其中 `A⁻ᵀ=(A⁻¹)ᵀ`，则：

$$
(A^{-T}n)^T(At)=n^T A^{-1}A t=n^T t=0
$$

这就是逆转置的来源：**保持法线对表面切向量的正交约束**。最后可把 n' 单位化供光照使用；单位化不负责修正方向。

平移不出现在公式中，因为两个表面点共同平移后，其差向量不变。A 不可逆时，例如某轴缩放为零，逆转置没有正常定义；不能指望事后 `normalize` 修复已经塌缩的几何。

## 3. 一个可以手算的反例

原始 `n=(1,1,0)`、`t=(1,-1,0)`，点积为零。沿 X 放大两倍：`A=diag(2,1,1)`。

| 量 | 变换后结果 | 与 t' 的点积 |
| --- | --- | --- |
| 表面切向量 `t'=A t` | `(2,-1,0)` | — |
| 错误法线 `A n` | `(2,1,0)` | 3，已经不垂直 |
| 正确法线 `A⁻ᵀn` | `(0.5,1,0)` | 0 |

把错误法线和切向量都单位化后，点积仍为 0.6；正确法线单位化后与单位切向量的点积仍为 0。

若光方向是单位 +Y：错误单位法线的 `N·L≈0.447214`，正确结果约 `0.894427`。在卡通阈值 0.6 下，一个落入暗部，一个进入亮部。错误会被离散色阶放大，而不只是轻微的亮度误差。

## 4. 什么时候可以简化

纯旋转 R 满足 `R⁻ᵀ=R`，因此普通方向与法线都可使用 R。若 A 是非零统一缩放乘旋转，普通变换与逆转置结果相差一个正比例长度因子，归一化后可一致。

对一般非均匀缩放或剪切，这种简化不成立。不要因某模型恰好没有暴露错误，就设置错误的统一缩放假设。固定源码中的 `TransformObjectToWorldNormal` 在普通分支使用逆转置关系，在 `UNITY_ASSUME_UNIFORM_SCALING` 分支中允许简化。[SpaceTransforms.hlsl](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.core/ShaderLibrary/SpaceTransforms.hlsl)

源码可能将相同数学关系写成 `mul(normalOS, worldToObject3x3)`。这是行向量乘逆矩阵，等价于列向量形式的逆转置；不能只因为没有出现 `transpose` 字符串就断言实现漏了转置。

负行列式还涉及朝向翻转。对两条边 u、v：

$$
(Au)\times(Av)=\det(A)\,A^{-T}(u\times v)
$$

当 `det(A)<0`，变换后边叉积与逆转置后的原始面法线有符号差。这联系到绕序、正反面和镜像处理，不意味着 GPU 面剔除会改用顶点法线。

## 5. TBN 是怎样的一套局部坐标

法线贴图通常给出一个**切线空间法线**。它不是直接写世界法线，而是使用每个表面位置的三个局部方向作为坐标基：

| 轴 | 名字 | 含义 |
| --- | --- | --- |
| T | Tangent，切线 | 通常与纹理 U 的局部变化方向关联 |
| B | Bitangent，副切线 | 通常与纹理 V 的局部变化方向关联 |
| N | Normal，法线 | 沿表面法线方向 |

在正交单位基的简化模型中，切线空间法线 `nTS=(x,y,z)` 对应：

$$
n_{WS}=\operatorname{normalize}(xT+yB+zN)
$$

平坦法线 `nTS=(0,0,1)` 应还原为 N。若这个基本检查都失败，先排查基、通道解码和乘法方向。

例：`T=(0,0,1)`、`B=(0,1,0)`、`N=(-1,0,0)`。此时 `nTS=(0.6,0,0.8)` 转为世界法线 `(-0.8,0,0.6)`。TBN 改变坐标描述，不会“自动算出材质高光”。

### 5.1 HLSL 中矩阵构造和乘法必须配套

若用 `float3x3(T,B,N)` 构造三行，采用 `mul(nTS,tangentToWorld)`，结果就是 `xT+yB+zN`。若把同一个矩阵改为 `mul(tangentToWorld,nTS)`，一般会得到另一个结果。

最不易误读的教学写法是直接相加：

```hlsl
float3 normalWS = normalize(
    normalTS.x * tangentWS +
    normalTS.y * bitangentWS +
    normalTS.z * baseNormalWS);
```

实际生产中的切线基可能因插值、非均匀缩放和烘焙约定偏离理想正交基；切线空间来回变换不能无条件把转置当逆。固定 Core RP 源码为相关变换提供了不同函数，应按数据含义选择，而不是仅按名字里的 World/Tangent 互换调用。

## 6. 为什么 tangent.w 和负缩放符号不能丢

Unity Mesh 的切线常用四个分量：xyz 存切线，w 存重建副切线的手性符号。它不是方向齐次坐标中的“是否受平移”开关。

在本卡采用的基构造中：

$$
B=h\,\operatorname{cross}(N,T),\qquad
h=tangent.w\times sign_{object}
$$

`sign_object` 表示物体变换的奇数次负缩放/朝向翻转信息。Core RP 的 `CreateTangentToWorld` 使用切线符号与 `GetOddNegativeScale()` 组合。[固定源码：切线基构造](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.core/ShaderLibrary/SpaceTransforms.hlsl#L228)

镜像 UV 可能需要不同的切线手性；负缩放又可能改变对象朝向。两个符号不能默认都为 +1。若 N=+Z、T=+X，则 h=+1 时 B=+Y，h=−1 时 B=−Y。

注意法线纹理的通道定义和导入解码也是约定的一部分。一般 RGB `[0,1]→[-1,1]` 的教学解码不能无条件替代 Unity 各压缩格式的正式法线解包函数。这里假定 `normalTS` 已正确解码，不讲具体压缩格式。

## 7. 一个可嵌入的教学 HLSL 函数

此函数可放在包含 URP `Core.hlsl` 的 HLSL 程序中；它是完整函数，**不是完整 ShaderLab 材质**。输入是有效、非退化的模型法线/切线及已解码切线空间法线，物体变换可逆，模型切线 w 为有效符号。

```hlsl
float3 ResolveTeachingNormalWS(
    float3 meshNormalOS,
    float4 meshTangentOS,
    float3 decodedNormalTS)
{
    float3 n = normalize(TransformObjectToWorldNormal(meshNormalOS));
    float3 t = TransformObjectToWorldDir(meshTangentOS.xyz, false);

    // 教学选择：剔除沿 n 的分量，再单位化。
    // 要求 t 与 n 不平行，且长度正常。
    t = normalize(t - n * dot(t,n));
    float handedness = meshTangentOS.w * GetOddNegativeScale();
    float3 b = cross(n,t) * handedness;

    return normalize(decodedNormalTS.x * t +
                     decodedNormalTS.y * b +
                     decodedNormalTS.z * n);
}
```

减去 `n*dot(t,n)` 是去掉 t 沿法线的投影，得到与 n 正交的切线。**这是一种明确的教学正交化选择，不声称逐行复刻 URP Lit 或所有法线烘焙规范。** 生产材质应与法线贴图烘焙器、切线生成方式和实际 Shader 路径保持一致；随意改变正交化位置也可能改变接缝表现。

如果法线/切线来自 VS 插值，插值可能改变长度与正交性，需要在合适的片元步骤处理。不要把每顶点得到单位 N 当成片元输入一定单位化的保证。

## 8. 可复制的 Unity 数值反例

保存为 `A04NormalLab.cs`，挂到空对象，在组件菜单运行“Print Normal Experiment”。脚本只打印数学结果，不依赖场景模型。

```csharp
using UnityEngine;

public class A04NormalLab : MonoBehaviour
{
    [ContextMenu("Print Normal Experiment")]
    private void PrintExperiment()
    {
        var matrix = Matrix4x4.Scale(new Vector3(2,1,1));
        var n = new Vector3(1,1,0);
        var t = new Vector3(1,-1,0);
        Vector3 transformedTangent = matrix.MultiplyVector(t).normalized;
        Vector3 wrong = matrix.MultiplyVector(n).normalized;
        Vector3 correct = matrix.inverse.transpose.MultiplyVector(n).normalized;
        Debug.Log($"Wrong perpendicularity: {Vector3.Dot(wrong,transformedTangent):F6}");
        Debug.Log($"Correct perpendicularity: {Vector3.Dot(correct,transformedTangent):F6}");
        Debug.Log($"Wrong N dot Y: {Vector3.Dot(wrong,Vector3.up):F6}");
        Debug.Log($"Correct N dot Y: {Vector3.Dot(correct,Vector3.up):F6}");
    }
}
```

预期依次约为 `0.600000、0.000000、0.447214、0.894427`。四阶矩阵在此仅含非零缩放；取逆转置后乘普通向量，使用的正是需要的三阶部分。

视觉检查可使用带平滑法线的斜面或 Sphere，施加 `(2,1,1)` 缩放，分别把错误/正确 N 显示为 `N*0.5+0.5` 或与世界光点积。单纯轴对齐平面的法线可能碰巧不暴露错误，不能作为唯一测试模型。

## 9. 对 NPR 的具体意义

- **主体明暗：** 错误法线直接移动色阶边界，不能只靠阈值补偿整个模型。
- **美术法线：** 可以刻意改变阴影形状；这种编辑是作者策略，仍须定义空间并正确变换。
- **反壳描边：** 用作外扩的平滑方向不一定与主体着色法线相同；硬边重复顶点可能产生裂缝。先区分两种数据用途，再决定如何烘焙或存储。
- **法线贴图：** TBN/手性错误会使局部明暗翻转；通过调高光强度难以真正修复。

GPU 没有专门理解“逆转置法线”的艺术语义，实际执行的是程序给出的矩阵与向量运算。不要在每个顶点或片元里无必要地求完整矩阵逆；Unity 已提供变换所需矩阵与库函数。真实成本取决于变体、编译和平台。

## 10. 自测、验证状态与引用

1. 逆转置保持什么约束？**法线对变换后表面切向量的垂直关系。**
2. 错误法线单位化后能否自动变正确？**不能。**
3. `tangent.w` 是齐次方向分量吗？**这里不是，它是切线基手性数据。**
4. 平坦切线空间法线 `(0,0,1)` 应输出什么？**基法线 N。**
5. 为什么负缩放既关系法线又关系绕序？**逆转置与几何边叉积之间存在行列式符号，面朝向与着色方向必须区分。**

配套 Python 验证本卡数值反例、TBN 基转换和正负手性；Unity C# / HLSL 示例做了接口与逻辑核对，尚未在 Editor 编译或实机验证。

本地文档根目录：`E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。已核对 `Manual/urp/writing-shaders-urp-unlit-normals.html`、`ScriptReference/Vector3.Cross.html`；源码符号为 `TransformObjectToWorldNormal`、`CreateTangentToWorld`、`TransformTangentToWorld`、`GetOddNegativeScale`，均位于上面固定提交的 `SpaceTransforms.hlsl`。

下一张：[A05｜线性颜色、sRGB 与 HDR 数值](A05-线性颜色sRGB与HDR数值.md)。本卡所需的法线、逆转置和 TBN 定义已在正文内完整给出。
