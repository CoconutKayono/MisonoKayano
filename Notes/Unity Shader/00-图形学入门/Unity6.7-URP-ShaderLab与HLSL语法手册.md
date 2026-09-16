---
title: Unity 6.7 URP — ShaderLab 与 HLSL 语法手册
aliases:
  - URP Shader 语法速查
  - Unity 6.7 着色器笔记
tags:
  - Unity
  - URP
  - ShaderLab
  - HLSL
created: 2026-09-16
updated: 2026-09-16
unity_target: "6000.7 / Unity 6.7 Beta"
document_type: 学习笔记与语法速查
---

# Unity 6.7 URP — ShaderLab 与 HLSL 语法手册

> [!info] 版本与范围
> 本文依据 **Unity 6.7（6000.7）官方手册**整理；2026-09-16 读取的页面标记为 **Unity 6.7 Beta**。HLSL 语言规则同时参考 Microsoft Learn。主要面向 **URP 的 3D Universal Renderer、手写顶点/片元 Shader**。
> 未读取你的项目或实际安装的 URP 包，也未在 Unity Editor 中编译示例。涉及包内部结构、变体和特定渲染路径时，以项目中的包源码为最终依据。本文不是 Shader Graph、2D Renderer 或完整 HLSL 语言规范的替代品。

> [!tip] Obsidian 使用
> 将本文件复制到任意 Vault；使用阅读视图或实时预览查看。目录使用 Obsidian 原生标题链接，提示框、表格和代码块均不依赖第三方插件。完整 Shader 使用 `hlsl` 代码块，便于获得基础高亮；其外层仍是 ShaderLab。

## 目录

- [[#01 三个层次与渲染流程]]
- [[#02 ShaderLab 文件结构]]
- [[#03 Properties 材质属性]]
- [[#04 Tags 与 URP Pass]]
- [[#05 GPU 渲染状态]]
- [[#06 编译指令与关键字]]
- [[#07 HLSL 基础语法]]
- [[#08 HLSL 函数速查]]
- [[#09 纹理与采样]]
- [[#10 坐标空间与法线]]
- [[#11 URP 光照与阴影]]
- [[#12 深度与屏幕纹理]]
- [[#13 常量缓冲与实例化]]
- [[#14 完整示例 A 纹理与颜色 Unlit]]
- [[#15 完整示例 B 主光源与实时阴影]]
- [[#16 透明与裁剪改造]]
- [[#17 常见错误与检查顺序]]
- [[#18 官方资料与包源码导航]]

## 01 三个层次与渲染流程

| 层次            | 负责什么                        | 典型语法                        |
| ------------- | --------------------------- | --------------------------- |
| ShaderLab     | 材质属性、SubShader、Pass、渲染状态与分类 | `Properties`、`Tags`、`Blend` |
| HLSL 语言       | GPU 上的数据类型、函数与运算            | `float3`、`struct`、`mul`     |
| Unity / URP 库 | 跨平台宏、空间变换、灯光和阴影访问           | `TEXTURE2D`、`GetMainLight`  |

`TransformObjectToHClip` 是 Unity 提供的函数，`SAMPLE_TEXTURE2D` 是 Unity 宏；它们不是 HLSL 语言原生关键字。

```text
Mesh 顶点数据 ──→ 顶点着色器 vert ──→ 裁剪/光栅化/插值 ──→ 片元着色器 frag
                      ↑                                  ↑
                 对象与相机矩阵                    材质、纹理、灯光数据
                                                         ↓
                                             深度/模板测试、混合、写入目标
```

这是概念流程；GPU 可以提前进行部分深度测试，不能据此假设片元函数总在测试之前执行。

- 顶点阶段：通常逐顶点执行，把对象空间位置变成齐次裁剪空间位置。
- 片元阶段：对光栅化产生的片元计算输出；片元不必与最终屏幕像素一一对应。
- 顶点输出到片元输入的数据默认进行透视正确插值。
- Renderer 决定什么时候调用哪个 Pass。写在文件里的 Pass 不代表每帧都执行。

## 02 ShaderLab 文件结构

下面是**结构示意**，省略的函数体使其不能单独编译。可复制的完整文件见 [[#14 完整示例 A 纹理与颜色 Unlit]]。

```hlsl
Shader "Study/URP/Example"
{
    Properties
    {
        _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
    }

    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" }
        LOD 100
        Cull Back

        Pass
        {
            Name "Forward"
            Tags { "LightMode" = "UniversalForwardOnly" }
            ZWrite On

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            // include、类型、变量和 Vert / Frag 函数定义
            ENDHLSL
        }
    }

    Fallback Off
    // CustomEditor "命名空间.自定义ShaderGUI类名"
}
```

| 结构 | 作用与使用要点 |
|---|---|
| `Shader "菜单/名称"` | 定义 Shader 名称；也是 `Shader.Find` 使用的名字 |
| `Properties {}` | 定义可序列化到材质的属性；可以为空或省略 |
| `SubShader {}` | 一组适用方案；Unity 根据管线、硬件等选择支持的方案 |
| `Pass {}` | 一次绘制所需的着色程序和状态 |
| `Name "Forward"` | 命名 Pass；与 `LightMode` 调度标签不同 |
| `HLSLPROGRAM … ENDHLSL` | 编译该 Pass 的 HLSL 程序 |
| `HLSLINCLUDE … ENDHLSL` | 放在 Shader/SubShader 层共享声明和函数；不会创建绘制 Pass |
| `UsePass "其他Shader/PASSNAME"` | 复用其他 Shader 中命名的 Pass，引用名称使用大写 Pass 名 |
| `Fallback "其他Shader"` / `Fallback Off` | 当前方案不可用时继续寻找后备 Shader，或禁止后备 |
| `CustomEditor "类全名"` | 使用自定义材质 Inspector |
| `LOD 100` | Shader LOD 阈值，不是自动按距离切换的 Mesh LOD |

> [!warning] URP 与旧教程
> 新 URP Shader 使用 `HLSLPROGRAM` 和 URP 的 `.hlsl` 库。不要把 `UnityCG.cginc`、`Lighting.cginc`、Surface Shader 的 `#pragma surface`、Built-in 的 `ForwardBase/ForwardAdd` 搬进来。
> URP 不支持 Built-in Surface Shader 和 `GrabPass` 工作流；读取场景颜色见 [[#12 深度与屏幕纹理]]。

共享材质缓冲时，推荐在 `HLSLINCLUDE` 或同一个自定义 `.hlsl` 中只维护一份声明。`UsePass` 会连同被引用 Pass 的属性依赖和实现约束一起带入，不适合盲目补齐阴影或深度。

依据：[6.7 代码块](https://docs.unity3d.com/6000.7/Documentation/Manual/shader-shaderlab-code-blocks.html)、[UsePass](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-UsePass.html)、[LOD](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-ShaderLOD.html)、[Surface Shader 范围](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-SurfaceShaders.html)。

## 03 Properties 材质属性

### 3.1 声明格式与类型

```hlsl
[可选特性] _变量名 ("Inspector 显示名称", 属性类型) = 默认值
```

ShaderLab 属性声明末尾不写分号；HLSL 变量声明末尾需要分号。属性名大小写必须与 HLSL、C# 访问名一致。

| 类型 | 声明示例 | HLSL 对应 |
|---|---|---|
| 浮点 | `_Intensity ("Intensity", Float) = 1` | `float _Intensity;` |
| 滑条 | `_Roughness ("Roughness", Range(0,1)) = 0.5` | `float` 或合适的 `half` |
| 整数 | `_Count ("Count", Integer) = 4` | `int _Count;` |
| 旧整数 | `_Legacy ("Legacy", Int) = 1` | 旧类型实际由浮点存储；新代码用 `Integer` |
| 颜色 | `_Tint ("Tint", Color) = (1,1,1,1)` | `float4` / `half4` |
| 向量 | `_Direction ("Direction", Vector) = (0,1,0,0)` | `float4` |
| 二维纹理 | `_BaseMap ("Base Map", 2D) = "white" {}` | `TEXTURE2D` + `SAMPLER` |
| 立方体纹理 | `_Env ("Environment", Cube) = "" {}` | `TEXTURECUBE` + `SAMPLER` |
| 三维纹理 | `_Volume ("Volume", 3D) = "" {}` | `TEXTURE3D` + `SAMPLER` |
| 纹理数组 | `_Layers ("Layers", 2DArray) = "" {}` | `TEXTURE2D_ARRAY` + `SAMPLER` |
| 立方体数组 | `_Envs ("Environments", CubeArray) = "" {}` | 对应立方体数组资源；受平台能力约束 |

6.7 手册还列出 `Vector, 2` / `Vector, 3` / `Vector, 4` 的 Inspector 分量显示控制：

```hlsl
_Scroll ("Scroll", Vector, 2) = (0.1, 0.0, 0.0, 0.0)
```

只显示两个输入框，但仍提供四个默认值，HLSL 仍按 `float4` 声明。

### 3.2 常用属性特性

| 特性 | 作用 |
|---|---|
| `[MainTexture]` | 指定 `Material.mainTexture` 对应的纹理 |
| `[MainColor]` | 指定 `Material.color` 对应的颜色 |
| `[HDR]` | HDR 颜色输入或 HDR 纹理提示 |
| `[Normal]` | 提示该纹理应为法线贴图 |
| `[NoScaleOffset]` | 隐藏纹理 Tiling / Offset 控件 |
| `[HideInInspector]` | 隐藏 Inspector 属性，属性仍存在 |
| `[Gamma]` | 为需要按 sRGB 解释的 Float / Vector 标注颜色空间处理 |
| `[PerRendererData]` | 标记按 Renderer 提供的纹理数据；不自动实现实例化 |

常见 MaterialPropertyDrawer 写法：

```hlsl
[Toggle(_ALPHATEST_ON)] _AlphaClip ("Alpha Clip", Float) = 0
[Enum(UnityEngine.Rendering.CullMode)] _Cull ("Cull", Float) = 2
[KeywordEnum(Off, Add, Multiply)] _DetailMode ("Detail Mode", Float) = 0
[Header(Surface)] _Metallic ("Metallic", Range(0,1)) = 0
[Space(8)] _Smoothness ("Smoothness", Range(0,1)) = 0.5
```

`[Toggle]` 负责编辑器交互；还需要编译对应关键字。`[KeywordEnum]` 按属性名生成关键字，例如 `_DETAILMODE_ADD`。

### 3.3 与 HLSL 的连接

```hlsl
// Properties 中有 _BaseColor 和 _BaseMap；这里仍需声明 GPU 侧变量。
CBUFFER_START(UnityPerMaterial)
    float4 _BaseColor;
    float4 _BaseMap_ST;
    float _Cutoff;
CBUFFER_END

TEXTURE2D(_BaseMap);
SAMPLER(sampler_BaseMap);
```

- `Properties` 不会替你写出 HLSL 声明。
- `_BaseMap_ST.xy` 是平铺，`.zw` 是偏移。使用 `TRANSFORM_TEX(uv, _BaseMap)` 应用。
- `_BaseMap_TexelSize` 常用于纹素大小：`(1/width, 1/height, width, height)`；需要时显式声明。
- `Range` 限制 Inspector 滑条，不保证脚本或 GPU 运行时数值被夹紧。
- 矩阵、数组、Buffer 通常通过脚本绑定，在 HLSL 中声明，不作为普通 `Properties` 类型。
- 声明 `_Surface`、`_Blend` 等同名属性，不会自动得到官方 Lit Inspector 的状态联动逻辑。

依据：[6.7 Properties 参考](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-Properties.html)、[URP 纹理属性示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-unlit-texture.html)。

## 04 Tags 与 URP Pass

### 4.1 SubShader 标签

```hlsl
Tags
{
    "RenderPipeline" = "UniversalPipeline"
    "RenderType" = "Opaque"
    "Queue" = "Geometry"
}
```

| 标签 | 常用值 | 实际作用 |
|---|---|---|
| `RenderPipeline` | `UniversalPipeline` | 标记适用于 URP |
| `RenderType` | `Opaque` / `TransparentCutout` / `Transparent` | 分类元数据；不会自动开启混合 |
| `Queue` | `Geometry` / `AlphaTest` / `Transparent` | 默认渲染队列 |
| `ForceNoShadowCasting` | `True` / `False` | 可禁止投射阴影，不等于控制接收阴影 |
| `PreviewType` | `Sphere` / `Plane` / `Skybox` | 材质预览形状 |

| 队列 | 常用数值 | 典型内容 |
|---|---:|---|
| Background | 1000 | 背景 |
| Geometry | 2000 | 普通不透明物体 |
| AlphaTest | 2450 | 裁剪植被、栅栏 |
| Transparent | 3000 | 透明材质 |
| Overlay | 4000 | 需要靠后绘制的内容 |

可以写 `"Queue" = "Geometry+10"`。材质的 Render Queue 覆盖值可能高于 Shader 默认值的优先级。队列不等于关闭深度测试；`Overlay` 也不会自动穿透所有物体。

`IgnoreProjector` 是 Built-in 的标签，不是 URP Decal 的开关。[6.7 SubShader Tags](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-SubShaderTags.html)

### 4.2 Pass 标签与 LightMode

```hlsl
Pass
{
    Name "ForwardLit"
    Tags { "LightMode" = "UniversalForwardOnly" }
    // ...
}
```

| LightMode | 用途 | 要点 |
|---|---|---|
| `UniversalForward` | 前向光照 Pass | 延迟路径不能仅靠它补齐 GBuffer |
| `UniversalForwardOnly` | 始终走前向的表面 Pass | 可用于前向和延迟 Renderer 中的前向材质 |
| `UniversalGBuffer` | 写入延迟渲染 GBuffer | 输出必须遵守 URP GBuffer 编码，不能返回普通最终颜色 |
| `SRPDefaultUnlit` | 默认无显式 LightMode 的 Pass | 常用于 Unlit / 额外绘制，仍依赖 Renderer 选择 |
| `ShadowCaster` | 从光源视角绘制阴影深度 | 负责投射阴影 |
| `DepthOnly` | 相机深度 Pass | 深度预通道需要时调用 |
| `DepthNormalsOnly` | 深度与法线预通道 | 6.7 标签文档用于 ForwardOnly / Deferred 配合 SSAO |
| `Meta` | 烘焙光照所需的表面信息 | 编辑器烘焙时使用 |
| `MotionVectors` | 运动矢量 | 自定义位移需正确处理历史位置 |
| `Universal2D` | 2D Renderer 光照 | 与本文 3D 示例的输入/流程不同 |

包内源码中还可能看到 `DepthNormals`；应检查当前 Renderer 实际请求的 `ShaderTagId`，不要把不同名称视为任何路径下都可互换。

> [!important] 多 Pass 不是顺序脚本
> 两个相同 `LightMode` 的 Pass 不保证都会被默认 Renderer 绘制。描边等额外绘制应核对调度规则，必要时用 Render Objects / 自定义 Renderer Feature 明确选择 Pass。

在 GBuffer Pass 中，`"UniversalMaterialType" = "Lit"` 或 `"SimpleLit"` 帮助延迟管线区分材质模型；标签本身不会实现 PBR。

依据：[6.7 URP Pass Tags](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-shaders/urp-shaderlab-pass-tags.html)。

## 05 GPU 渲染状态

### 5.1 常用状态

多数状态可放在 `SubShader` 层作为默认值，也可在 `Pass` 层覆盖。Renderer 也可能通过渲染状态覆盖机制改变它们。

| 状态 | 示例 | 含义 |
|---|---|---|
| 面剔除 | `Cull Back` | 剔除背面；还可 `Front`、`Off` |
| 深度写入 | `ZWrite On` | 写入深度；`Off` 不写入 |
| 深度测试 | `ZTest LEqual` | 按深度比较决定是否通过 |
| 混合 | `Blend SrcAlpha OneMinusSrcAlpha` | 源与目标颜色按因子组合 |
| 混合运算 | `BlendOp Add` | 还常见 `Sub`、`RevSub`、`Min`、`Max` |
| 颜色通道 | `ColorMask RGB` | 只写 RGB；`RGBA` 全写，`0` 全禁写 |
| 深度偏移 | `Offset -1, -1` | 斜率因子与单位偏移；须在目标平台验证效果 |
| 覆盖率 | `AlphaToMask On` | 通常结合 MSAA，将 Alpha 转成采样覆盖率 |

`ZTest` 常用比较：`Never`、`Less`、`Equal`、`LEqual`、`Greater`、`NotEqual`、`GEqual`、`Always`。常规材质使用 `LEqual`，不要因底层 Reverse-Z 就自行把它换成 `GEqual`。

`ZWrite Off` 与 `ZTest Always` 不同：前者仍可被前面的物体遮住；后者总是通过深度比较。

`Cull Off` 只让两面都绘制，不会自动修正背面法线或实现物理正确的双面光照。

状态可引用材质属性：

```hlsl
// Properties 中：
[Enum(UnityEngine.Rendering.CullMode)] _Cull ("Cull", Float) = 2
[Toggle] _ZWrite ("ZWrite", Float) = 1

// Pass / SubShader 中：
Cull [_Cull]
ZWrite [_ZWrite]
```

依据：[Cull](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-Cull.html)、[ZTest](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-ZTest.html)、[ZWrite](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-ZWrite.html)、[Offset](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-Offset.html)、[ColorMask](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-ColorMask.html)、[AlphaToMask](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-AlphaToMask.html)。

### 5.2 Blend 速查

对 `BlendOp Add`，颜色混合为：

```text
结果 = 源颜色 × 源因子 + 目标已有颜色 × 目标因子
```

| 效果 | Blend | 片元输出要求 |
|---|---|---|
| 不混合 | `Blend Off` | 直接输出 |
| 普通透明 | `Blend SrcAlpha OneMinusSrcAlpha` | 输出未乘 Alpha 的 RGB |
| 预乘透明 | `Blend One OneMinusSrcAlpha` | RGB 已乘 Alpha，只乘一次 |
| 加法 | `Blend One One` | RGB 自身含发光强度 |
| Alpha 控制加法 | `Blend SrcAlpha One` | Alpha 控制叠加强度 |
| 乘法 | `Blend DstColor Zero` | 源 RGB 调制目标 RGB |

独立设置 RGB 和 Alpha 因子：

```hlsl
Blend SrcAlpha OneMinusSrcAlpha, One OneMinusSrcAlpha
```

这样 RGB 为常规透明合成，目标 Alpha 为 `src.a + dst.a * (1-src.a)`。只写前两个因子时，Alpha 也使用相同因子，不一定得到想要的合成 Alpha。

因子包括 `Zero`、`One`、`SrcColor`、`DstColor`、`SrcAlpha`、`DstAlpha` 及对应 `OneMinus...`。不要把 Add 的公式直接推广到所有 BlendOp；高级混合和 MRT 独立混合还有平台约束。[6.7 Blend](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-Blend.html)

### 5.3 Stencil 模板测试

```hlsl
Stencil
{
    Ref 1
    ReadMask 1
    WriteMask 1
    Comp Always
    Pass Replace
    Fail Keep
    ZFail Keep
}
```

该例在通过深度与模板测试时把最低位写为 1，其余位保持不变。另一个绘制可用：

```hlsl
Stencil
{
    Ref 1
    ReadMask 1
    WriteMask 0
    Comp Equal
    Pass Keep
}
```

| 字段 | 含义 |
|---|---|
| `Ref` | 0～255 的参考值 |
| `ReadMask` / `WriteMask` | 控制参与比较/写入的位，不是颜色通道 |
| `Comp` | 比较 `(Ref & ReadMask)` 与 `(Stencil & ReadMask)` |
| `Pass` | 模板、深度都通过时的操作 |
| `Fail` | 模板测试失败时的操作 |
| `ZFail` | 模板通过、深度失败时的操作 |

操作：`Keep`、`Zero`、`Replace`、`IncrSat`、`DecrSat`、`Invert`、`IncrWrap`、`DecrWrap`。也可用 `CompFront` / `CompBack` 等控制正背面。

这些片段仍需安排先写后读的绘制顺序；URP 延迟渲染等功能可能占用模板位，不能任意覆盖整个缓冲。[6.7 Stencil](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-Stencil.html)

## 06 编译指令与关键字

### 6.1 常见 pragma

```hlsl
#pragma vertex Vert
#pragma fragment Frag
#pragma target 3.0
#pragma multi_compile_fog
#pragma multi_compile_instancing
#pragma shader_feature_local_fragment _ALPHATEST_ON
```

| 指令 | 作用 |
|---|---|
| `vertex` / `fragment` | 指定阶段入口函数；名称可自定但必须一致 |
| `target` | 声明最低着色器能力级别；不是画质档位 |
| `require` | 声明所需 GPU 特性，如 `2darray` |
| `multi_compile` | 为声明的组合生成变体，仍可能受管线/自定义剥离影响 |
| `shader_feature` | 面向材质功能，构建时可去掉未使用组合 |
| `dynamic_branch` | 用统一变量控制动态分支，不为每个状态生成静态变体 |
| `multi_compile_fog` | 声明雾变体；仍需调用雾函数 |
| `multi_compile_instancing` | 声明传统实例化变体；仍需实例化宏 |
| `only_renderers` / `exclude_renderers` | 限定图形 API；误用会造成某些平台没有可用 Shader |
| `skip_variants` | 去掉含指定关键字的变体 |

`#pragma target 4.5` 常用于需要较高能力的实现，但不要为了“更快”盲目升高。Geometry / Hull / Domain 并非所有 URP 目标平台都支持，例如 Metal 不支持几何着色器。

依据：[6.7 pragma 参考](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-PragmaDirectives.html)、[GPU 能力与 target](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-ShaderCompileTargets.html)。

### 6.2 关键字声明与条件编译

```hlsl
// 两种状态：不开启，或开启 _DETAIL_ON。
#pragma shader_feature_local _DETAIL_ON

// 三种互斥编译状态：无关键字、模式 A、模式 B。
#pragma multi_compile _ MODE_A MODE_B

#if defined(_DETAIL_ON)
    color.rgb *= detail.rgb;
#endif
```

- 同一行声明一个关键字集合；不同的行产生组合乘积，例如 `2 × 3 × 2 = 12`。
- `_` 用作“没有关键字”的占位。
- `_local` 将关键字限制在 Shader 的本地作用域。
- `_fragment` 表示功能仅用于片元阶段；节省效果随图形 API / 编译后端而异。
- 通过脚本启用运行时关键字时，要保证该组合在构建中被保留。
- `Material.SetFloat("_AlphaClip", 1)` 本身不等于启用 `_ALPHATEST_ON`。

动态分支与预处理分支不同：

```hlsl
#pragma dynamic_branch _DEBUG_VIEW

// 动态关键字用 HLSL if，不用 #if defined 判断其运行时值。
if (_DEBUG_VIEW)
{
    color.rgb = float3(1, 0, 1);
}
```

`#if` 在预处理/编译时选择代码；`if` 由编译器生成运行时代码，可能被优化为分支或条件选择。

依据：[6.7 声明关键字](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-MultipleProgramVariants-declare.html)、[关键字条件代码](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-MultipleProgramVariants-make-conditionals.html)。

## 07 HLSL 基础语法

### 7.1 类型与精度

| 类型 | 用途与注意事项 |
|---|---|
| `float` | 通常用于位置、UV、深度和高精度计算 |
| `half` | 可用于颜色、方向等；实际精度取决于 Unity 精度模型和后端 |
| `int` / `uint` | 有符号/无符号整数，索引与位运算 |
| `bool` | 逻辑条件；不要推断它在 GPU 缓冲中占 1 字节 |
| `float2/3/4` | 向量；`half`、整数、布尔也有向量类型 |
| `float3x3/4x4` | 矩阵；前一个数字是行数 |
| `void` | 无返回值函数 |

```hlsl
float distanceWS = 12.5;
half roughness = half(0.4);
float2 uv = float2(0.25, 0.75);
half3 tint = half3(1.0, 0.5, 0.2);
float4 position = float4(0.0, 1.0, 0.0, 1.0);
uint flags = 3u;
bool enabled = true;
```

不要把 `half` 理解为“任何平台都节省一半常量缓冲空间”。大世界位置、细密 UV、高频变化用低精度容易抖动。`fixed` 属于旧 Unity/Cg 教程常见写法，新 URP 代码优先使用 `half` / `float`。

类型依据：[Microsoft HLSL 数据类型](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-data-types)、[Unity 6.7 的 16 位精度](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-Use16BitPrecisionInShaders.html)。

### 7.2 分量访问与构造

```hlsl
float4 value = float4(0.1, 0.2, 0.3, 0.4);
float3 rgb = value.rgb;       // 与 value.xyz 相同
float2 swapped = value.yx;
float3 repeated = value.xxx;
value.xy = float2(1, 2);
float4 white = 1.0;          // 标量广播到四个分量

// value.xr：错误，同一次 swizzle 不混用 xyzw / rgba。
// value.xx = float2(1,2)：错误，不能重复写同一分量。
```

矩阵的 `m[row][column]` 从 0 开始索引。行列的数学意义与缓冲区的 row-major / column-major 存储方式是两个问题。[HLSL 向量与矩阵规则](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-per-component-math)

### 7.3 运算符

| 类别 | 运算符 / 示例 | 注意 |
|---|---|---|
| 算术 | `+ - * / %` | 向量通常按分量运算 |
| 比较 | `< <= > >= == !=` | 向量比较得到布尔向量 |
| 逻辑 | `!`、`&&`、`\|\|` | 跨编译器代码不要依赖它们保护非法纹理访问或除零 |
| 位运算 | `&`、`\|`、`^`、`~`、`<<`、`>>` | 用整数类型；与逻辑运算不同 |
| 条件 | `condition ? a : b` | 不保证一定产生分支或只计算选中的一侧 |
| 赋值 | `= += -= *= /=` | 与 C 风格语法接近 |
| 转换 | `(float)count`、`float3(v)` | 数值类型转换 |

```hlsl
float3 a = float3(1, 2, 3);
float3 b = float3(4, 5, 6);
float3 componentProduct = a * b; // (4,10,18)，不是点积
float scalarProduct = dot(a, b); // 32

if (any(a > b)) { /* 至少一个分量成立 */ }
if (all(a < b)) { /* 所有分量成立 */ }

float ratio = 1.0 / 2.0;        // 0.5
int integerRatio = 1 / 2;        // 0
```

`asfloat` / `asuint` 是位模式重解释，与 `(float)` / `(uint)` 的数值转换不同。整数除法、数组越界和未初始化变量都应显式处理。[HLSL 运算符](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-operators)

### 7.4 结构体、数组和函数

```hlsl
struct SurfaceInfo
{
    float3 normalWS;
    half3 albedo;
    half opacity;
}; // 结构体末尾需要分号

static const float PI_VALUE = 3.14159265;
static const float weights[3] = { 0.25, 0.5, 0.25 };

half3 ApplyTint(half3 color, half3 tint) // 默认参数方向是 in
{
    return color * tint;
}

void SplitColor(in half4 color, out half3 rgb, out half alpha)
{
    rgb = color.rgb;
    alpha = color.a;
}

void ScaleValue(inout float value, float scale)
{
    value *= scale;
}
```

`in` 读取输入，`out` 写出结果，`inout` 同时读写。每条返回路径都应正确赋值输出参数。函数支持重载；普通实时 Shader 代码不要设计递归。

局部结构体可初始化为零：`SurfaceInfo s = (SurfaceInfo)0;`。这避免未初始化，但零不一定是正确业务默认值，例如 PBR 的 `occlusion` 通常应为 1。[HLSL 函数语法](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-function-syntax)

### 7.5 控制流与预处理

```hlsl
if (mask > 0.5) { color *= 2.0; }
else { color *= 0.5; }

[unroll]
for (int i = 0; i < 4; ++i)
{
    total += values[i];
}

[loop]
for (uint j = 0; j < count; ++j)
{
    if (j >= 16u) break;
}

#ifndef STUDY_COMMON_INCLUDED
#define STUDY_COMMON_INCLUDED
// 自定义公共 .hlsl 的声明和函数
#endif
```

还有 `while`、`do…while`、`switch`、`break`、`continue`、`return`。`[unroll]` / `[loop]` 指导循环生成，`[branch]` / `[flatten]` 指导条件分支；它们不是无条件的性能提升开关。循环次数和分支分歧应在目标硬件上测量。[HLSL 控制流](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-flow-control)

自定义头文件用 `#include "StudyCommon.hlsl"` 引入；需要共享 Unity 专用 pragma 时，应核对 `#include_with_pragmas` 的使用条件，不要假设普通 include 会处理所有 Unity pragma。

### 7.6 语义与插值

```hlsl
struct Attributes
{
    float3 positionOS : POSITION;
    float3 normalOS   : NORMAL;
    float4 tangentOS  : TANGENT;
    float2 uv         : TEXCOORD0;
    half4 color       : COLOR;
};

struct Varyings
{
    float4 positionCS : SV_POSITION;
    float2 uv         : TEXCOORD0;
    float3 normalWS   : TEXCOORD1;
    nointerpolation uint materialId : TEXCOORD2;
};
```

| 语义 | 含义 |
|---|---|
| `POSITION` | 顶点输入位置，不自动转换空间 |
| `NORMAL` / `TANGENT` | 网格法线 / 切线；切线 w 存放手性符号 |
| `TEXCOORDn` | 顶点 UV 通道或阶段间通用数据槽，并不限于 UV |
| `COLOR` | 顶点颜色 |
| `SV_POSITION` | 顶点输出为齐次裁剪位置；片元输入已经是光栅化后的屏幕位置 |
| `SV_Target` / `SV_Target0` | 片元颜色输出 |
| `SV_Target1` 等 | MRT 输出；管线必须实际绑定对应 Render Target |
| `SV_Depth` | 自定义深度输出；可能影响提前深度测试 |
| `SV_VertexID` / `SV_InstanceID` | 系统提供的顶点 / 实例索引，受平台能力约束 |

`nointerpolation` 不插值，整数阶段间数据通常需要它；`noperspective` 去掉透视校正，`centroid` / `sample` 与多重采样相关。跨平台双面判断优先使用 Unity 的 `FRONT_FACE_TYPE`、`FRONT_FACE_SEMANTIC` 和 `IS_FRONT_VFACE` 宏。

> [!warning] 名字不改变语义
> 即使字段名一直叫 `positionCS`，进入片元阶段后的 `SV_POSITION.xy` 也已是像素位置。不要再把它当顶点阶段的裁剪坐标做一次 `xy / w`。

依据：[Microsoft HLSL Semantics](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics)。

### 7.7 延伸语法：Buffer 与 Compute

Compute 使用独立 `.compute` 文件，属于 HLSL 应用，不写 ShaderLab 的 `Shader / SubShader / Pass` 外壳，也不会因放进项目而自动执行。

```hlsl
#pragma kernel Fill

RWTexture2D<float4> _Result;
uint _Width;
uint _Height;

[numthreads(8, 8, 1)]
void Fill(uint3 id : SV_DispatchThreadID)
{
    if (id.x >= _Width || id.y >= _Height)
        return;

    float2 uv = (float2(id.xy) + 0.5) / float2(_Width, _Height);
    _Result[id.xy] = float4(uv, 0.0, 1.0);
}
```

需要脚本创建支持随机写入的目标纹理、绑定参数，并调用 Dispatch。组数按 `ceil(width/8)`、`ceil(height/8)` 计算；边界检查处理不能整除的尺寸。

| 名称 | 含义 |
|---|---|
| `StructuredBuffer<T>` | 结构化只读缓冲 |
| `RWStructuredBuffer<T>` | 结构化可读写缓冲 |
| `RWTexture2D<T>` | 可通过整数坐标写入的二维资源 |
| `groupshared` | 同一个线程组共享的数据 |
| `SV_DispatchThreadID` | 整次 Dispatch 中的线程坐标 |
| `SV_GroupID` | 线程组坐标 |
| `SV_GroupThreadID` | 组内线程坐标 |
| `SV_GroupIndex` | 组内线性线程索引 |

线程组间不能用普通组内屏障实现全局同步；使用组内屏障时，同组线程必须一致到达它。片元 Shader 的导数、隐式纹理 LOD 工作方式也不能直接套到常规 Compute。

依据：[Microsoft RWTexture2D](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/sm5-object-rwtexture2d)、[numthreads](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/sm5-attributes-numthreads)。

## 08 HLSL 函数速查

以下是片元/顶点代码常用的函数；大多数标量函数也接受向量并逐分量计算。

| 函数 | 作用 | 常见用途 |
|---|---|---|
| `abs(x)` | 绝对值 | 对称图案 |
| `min(a,b)` / `max(a,b)` | 最小/最大值 | 限制数值 |
| `clamp(x,a,b)` | 限制到 `[a,b]` | 通用夹紧 |
| `saturate(x)` | 限制到 `[0,1]` | 遮罩、光照系数 |
| `floor(x)` / `ceil(x)` | 向下/向上取整 | 网格分块 |
| `round(x)` / `trunc(x)` | 舍入/截去小数 | 离散化 |
| `frac(x)` | `x-floor(x)` | 循环 UV；`frac(-0.2)=0.8` |
| `fmod(x,y)` | 浮点余数 | 与 `frac` 的负数行为不同 |
| `lerp(a,b,t)` | `a+(b-a)*t` | 插值；不会自动夹紧 t |
| `step(edge,x)` | `x<edge` 为 0，否则 1 | 硬边遮罩 |
| `smoothstep(a,b,x)` | 两端夹紧的平滑过渡 | 软边；要求合理的 `a<b` |
| `pow(x,y)` | 幂 | 非负基底上的指数曲线 |
| `sqrt(x)` / `rsqrt(x)` | 平方根/平方根倒数 | 长度相关运算 |
| `exp` / `exp2` / `log` / `log2` | 指数与对数 | 衰减和曝光 |
| `sin` / `cos` / `tan` | 三角函数，角度为弧度 | 波动 |
| `atan2(y,x)` | 按象限求角度 | 极坐标 |
| `radians` / `degrees` | 角度制互换 | 输入转换 |
| `dot(a,b)` | 点积 | N·L、投影 |
| `cross(a,b)` | 三维叉积 | 构建垂直方向 |
| `length(v)` / `distance(a,b)` | 向量长度/两点距离 | 距离场 |
| `normalize(v)` | 归一化 | 方向；避免输入零向量 |
| `reflect(I,N)` | 反射方向 | I 指向表面，N 应归一化 |
| `refract(I,N,eta)` | 折射方向 | eta 为折射率之比 |
| `mul(a,b)` | 线性代数乘法 | 矩阵变换 |
| `transpose(m)` | 转置 | 调整矩阵方向 |
| `any(v)` / `all(v)` | 布尔归约 | 向量条件 |
| `clip(x)` | 任一分量小于 0 则丢弃片元 | Alpha Clip |
| `ddx(x)` / `ddy(x)` | 屏幕局部导数 | 片元阶段纹理与抗锯齿 |
| `fwidth(x)` | `abs(ddx(x))+abs(ddy(x))` | 自适应软边 |

函数签名与阶段要求见 [Microsoft HLSL Intrinsics](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-intrinsic-functions)。

### 8.1 三个小例子

```hlsl
// 线性渐变：uv.x 由 0 到 1 时从左色变化到右色。
half3 gradient = lerp(leftColor, rightColor, saturate(uv.x));

// 硬裁剪：小于阈值被丢弃，等于阈值时不因 clip(0) 被丢弃。
clip(alpha - cutoff);

// 片元阶段，对有符号距离 d 的边界做平滑；d < 0 为内部。
float width = max(fwidth(d), 1e-5);
float coverage = 1.0 - smoothstep(-width, width, d);
```

`saturate(dot(N,L))` 只夹紧点积，不会替你归一化 N 和 L。导数依赖邻近片元；把导数或隐式 LOD 采样放进不一致的动态分支/循环可能产生不稳定结果。

### 8.2 矩阵乘法不要混淆

```hlsl
float4 transformed = mul(matrix, position); // 将 position 当列向量
float4 other = mul(position, matrix);       // 将 position 当行向量
float4x4 componentWise = matrixA * matrixB; // 按分量相乘
float4x4 composed = mul(matrixA, matrixB);  // 矩阵乘法
```

URP 中优先使用坐标变换辅助函数，减少乘法顺序与平台差异错误。[HLSL 矩阵运算](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-per-component-math)

## 09 纹理与采样

### 9.1 URP 标准写法

```hlsl
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

TEXTURE2D(_BaseMap);
SAMPLER(sampler_BaseMap);

// 以下数值声明应与其他材质参数合并进唯一的 UnityPerMaterial。
CBUFFER_START(UnityPerMaterial)
    float4 _BaseMap_ST;
CBUFFER_END

// 顶点或片元阶段应用平铺与偏移：
float2 uv = TRANSFORM_TEX(inputUV, _BaseMap);

// 片元阶段，隐式选择 mip：
half4 texel = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, uv);
```

纹理是资源，Sampler 控制过滤与寻址；两者不是颜色值。`SAMPLER(sampler_BaseMap)` 的常规命名使其采用该纹理对应的采样设置。

### 9.2 采样宏速查

| 宏示例 | 用途 |
|---|---|
| `SAMPLE_TEXTURE2D(tex,samp,uv)` | 普通二维纹理采样，隐式 LOD |
| `SAMPLE_TEXTURE2D_LOD(tex,samp,uv,lod)` | 指定 mip 级别 |
| `SAMPLE_TEXTURE2D_GRAD(tex,samp,uv,dx,dy)` | 显式提供梯度 |
| `LOAD_TEXTURE2D(tex,pixelXY)` | 整数像素坐标读取，无常规过滤采样 |
| `SAMPLE_TEXTURECUBE(tex,samp,dir)` | 用方向采样立方体纹理 |
| `SAMPLE_TEXTURE2D_ARRAY(tex,samp,uv,layer)` | 采样数组中的某层 |
| `SAMPLE_TEXTURE3D(tex,samp,uvw)` | 三维纹理采样 |

宏由 SRP Core 的平台头文件实现。不要假定所有宏在所有阶段、Shader Target 和平台上都可用。

顶点阶段通常显式指定 LOD：

```hlsl
float height = SAMPLE_TEXTURE2D_LOD(_HeightMap, sampler_HeightMap, uv, 0).r;
positionOS.y += height * amplitude;
```

原生 HLSL 对应概念是 `Texture2D.Sample` 和 `SampleLevel`；Unity 的宏负责跨后端映射。[Sample](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-sample)、[SampleLevel](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-samplelevel)

### 9.3 颜色空间与法线贴图

- Base Color 等颜色纹理通常按 sRGB 导入，在 Linear 项目中由正确的纹理设置负责解码。
- Metallic、Roughness、Mask、Height 等数据纹理通常关闭 sRGB。
- 法线贴图按 Normal map 导入，用 `UnpackNormalScale` 等函数解码；不要把压缩后的 RGB 一律当成 `rgb * 2 - 1`。
- HDR 环境 Cubemap 可能需要对应的 HDR 解码流程；普通 `SAMPLE_TEXTURECUBE(...).rgb` 不等于完整环境反射系统。

依据：[6.7 URP 纹理示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-unlit-texture.html)。

## 10 坐标空间与法线

### 10.1 空间命名

| 后缀 | 空间 | 示例 |
|---|---|---|
| OS | 对象空间 Object | `positionOS`、`normalOS` |
| WS | 世界空间 World | `positionWS`、`normalWS` |
| VS | 观察空间 View | `positionVS` |
| CS / HCS | 齐次裁剪空间 Clip | 顶点阶段的 `positionCS` |
| NDC | 归一化设备坐标 | 通常由裁剪坐标除以 w 得到；z 范围与平台有关 |
| TS | 切线空间 Tangent | 法线贴图的 `normalTS` |

```text
对象空间 --对象矩阵--> 世界空间 --视图矩阵--> 观察空间
观察空间 --投影矩阵--> 齐次裁剪空间
齐次裁剪空间 --透视除法--> NDC --视口变换--> 屏幕像素
```

### 10.2 常用变换函数

引入 `Core.hlsl` 后使用：

| 函数 | 作用 |
|---|---|
| `TransformObjectToWorld(positionOS)` | 对象位置 → 世界位置 |
| `TransformWorldToObject(positionWS)` | 世界位置 → 对象位置 |
| `TransformWorldToView(positionWS)` | 世界位置 → 观察位置 |
| `TransformWorldToHClip(positionWS)` | 世界位置 → 齐次裁剪位置 |
| `TransformObjectToHClip(positionOS)` | 对象位置 → 齐次裁剪位置 |
| `TransformObjectToWorldDir(directionOS)` | 转换方向，不包含平移 |
| `TransformObjectToWorldNormal(normalOS)` | 正确处理法线变换，包括非均匀缩放 |
| `GetWorldSpaceViewDir(positionWS)` | 从表面指向视点的向量 |
| `GetWorldSpaceNormalizeViewDir(positionWS)` | 归一化视线方向，兼顾投影类型 |
| `GetVertexPositionInputs(positionOS)` | 一次取得常见位置数据 |
| `GetVertexNormalInputs(normalOS,tangentOS)` | 取得世界空间切线、副切线、法线 |
| `GetNormalizedScreenSpaceUV(positionCS)` | 片元阶段可用屏幕 `SV_POSITION` 得到归一化 UV |

```hlsl
VertexPositionInputs p = GetVertexPositionInputs(IN.positionOS);
OUT.positionCS = p.positionCS;
OUT.positionWS = p.positionWS;
```

`VertexPositionInputs.positionNDC` 是库里的齐次屏幕相关表示；需要 UV 时遵守其 w 除法约定或用专门辅助函数，不要只凭字段名假设 `.xy` 已在 0～1。

位置的齐次 w 通常为 1；方向为 0。法线必须垂直于表面，非均匀缩放下不能直接当普通方向变换。[6.7 空间变换](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/use-built-in-shader-methods-transformations.html)

### 10.3 切线空间法线到世界空间

下面为**函数内部片段**，假设已有合法网格切线、纹理声明和对应 Varyings 字段。

```hlsl
// 顶点阶段
VertexNormalInputs basis = GetVertexNormalInputs(IN.normalOS, IN.tangentOS);
OUT.normalWS = basis.normalWS;
OUT.tangentWS = basis.tangentWS;
OUT.bitangentWS = basis.bitangentWS;

// 片元阶段
half3 normalTS = UnpackNormalScale(
    SAMPLE_TEXTURE2D(_NormalMap, sampler_NormalMap, IN.uv), _NormalScale);

float3 N = normalize(IN.normalWS);
float3 T = normalize(IN.tangentWS);
float3 B = normalize(IN.bitangentWS);
float3 normalWS = normalize(normalTS.x * T + normalTS.y * B + normalTS.z * N);
```

需要时显式引入 `Packages/com.unity.render-pipelines.core/ShaderLibrary/Packing.hlsl`。`GetVertexNormalInputs` 的双参数版本处理切线 w 与对象负缩放手性。片元阶段再次归一化，因为插值会改变长度。高质量实现还可能需要正交化 TBN。

### 10.4 常用内置数据

| 名称 | 内容 |
|---|---|
| `_Time` | 常规时间数据：`(t/20, t, 2t, 3t)` |
| `_SinTime` / `_CosTime` | 不同频率的时间正弦 / 余弦 |
| `_WorldSpaceCameraPos` | 相机世界位置；通用视线计算优先用 URP 函数 |
| `_ScreenParams` | 屏幕相关参数，xy 为宽高 |
| `_ScaledScreenParams` | 考虑缩放的屏幕尺寸；屏幕采样常用 xy |
| `_ZBufferParams` | 深度线性化参数 |
| `UNITY_MATRIX_M` / `UNITY_MATRIX_V` / `UNITY_MATRIX_P` | 对象、视图、投影矩阵 |
| `UNITY_MATRIX_VP` / `UNITY_MATRIX_I_VP` | 视图投影矩阵及其逆矩阵 |

不要重新声明 Unity 已提供的内置变量；Built-in 文档里列出的旧光照数组也不等于 URP 的光源接口。[内置变量参考](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-UnityShaderVariables.html)

## 11 URP 光照与阴影

### 11.1 常用 include

| 文件 | 用途 |
|---|---|
| `universal/ShaderLibrary/Core.hlsl` | URP 基础、变换、平台宏 |
| `universal/ShaderLibrary/Lighting.hlsl` | 光照入口，关联 BRDF、GI、实时灯光等 |
| `universal/ShaderLibrary/RealtimeLights.hlsl` | 主灯、附加灯、光照循环 |
| `universal/ShaderLibrary/Shadows.hlsl` | 阴影采样与偏移 |
| `universal/ShaderLibrary/SurfaceData.hlsl` | PBR 表面数据结构 |
| `universal/ShaderLibrary/DeclareDepthTexture.hlsl` | 场景深度读取 |
| `universal/ShaderLibrary/DeclareOpaqueTexture.hlsl` | 不透明场景颜色读取 |
| `core/ShaderLibrary/Packing.hlsl` | 法线等数据解码 |

表格中的 `universal/`、`core/` 分别是 `Packages/com.unity.render-pipelines.universal/` 与 `Packages/com.unity.render-pipelines.core/` 的缩写；真正代码应写完整包路径。

### 11.2 主光源与 Lambert

```hlsl
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

// 片元函数内
Light sun = GetMainLight();
half3 N = normalize(IN.normalWS);
half ndotl = saturate(dot(N, sun.direction));
half3 diffuse = albedo * sun.color * ndotl
              * sun.distanceAttenuation * sun.shadowAttenuation;
```

| `Light` 字段 | 含义 |
|---|---|
| `direction` | 从表面指向灯光的光照方向 |
| `color` | 光的颜色与强度数据 |
| `distanceAttenuation` | 距离等衰减 |
| `shadowAttenuation` | 阴影衰减 |
| `layerMask` | 渲染层匹配所需信息 |

无参数 `GetMainLight()` 不会完成当前片元的实时阴影查询。要接收阴影，使用带阴影坐标的重载。`LightingLambert` 可替代手写 `color * saturate(dot(...))`。[6.7 光照方法](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/use-built-in-shader-methods-lighting.html)

### 11.3 阴影的两件事

| 需求 | 要做什么 |
|---|---|
| 接收阴影 | 正确编译变体、计算阴影坐标、采样阴影、乘入光照 |
| 投射阴影 | 提供 `ShadowCaster` Pass，并打开 Renderer / Light 对应设置 |

主灯阴影常见变体：

```hlsl
#pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE _MAIN_LIGHT_SHADOWS_SCREEN
```

当前**不透明表面**片元中计算坐标的思路：

```hlsl
float4 shadowCoord;
#if defined(_MAIN_LIGHT_SHADOWS_SCREEN)
    shadowCoord = ComputeScreenPos(TransformWorldToHClip(IN.positionWS));
#else
    shadowCoord = TransformWorldToShadowCoord(IN.positionWS);
#endif

Light sun = GetMainLight(shadowCoord, IN.positionWS, half4(1, 1, 1, 1));
```

这里的白色 shadow mask 只适合不接入烘焙 Shadowmask 的简化流程。屏幕空间阴影还要求 Renderer Feature 和接收物体的深度数据正确；透明表面不能直接照搬这条屏幕采样分支。

级联阴影可在片元阶段根据世界位置计算级联选择，避免把跨级联边界的阴影坐标只在顶点阶段计算后直接插值。软阴影还需声明与当前包相符的软阴影变体；仅开启灯光 Soft Shadows 不会自动补齐自定义 Shader 的代码。

ShadowCaster 中通常需要 `ApplyShadowBias`、近裁剪面处理以及点光/聚光的方向处理。顶点位移、Alpha Clip 应在颜色、深度、阴影 Pass 中保持一致，不能借用一个不理解该效果的 Lit Pass。[6.7 阴影方法](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/use-built-in-shader-methods-shadows.html)

### 11.4 Unity 6.7 的附加光循环

> [!important] 与旧教程的差别
> 6.7 官方示例使用 **`_CLUSTER_LIGHT_LOOP`** 和 **`USE_CLUSTER_LIGHT_LOOP`**。不要将旧版 `_FORWARD_PLUS` / `USE_FORWARD_PLUS` 与这套代码随意混用。

以下是可接入完整光照 Shader 的**独立函数片段**。依赖 `Lighting.hlsl`；在对应 Pass 加上两个 pragma。示例计算直接漫反射，不处理烘焙 GI、Light Cookies、Rendering Layers 或附加灯阴影变体。

```hlsl
#pragma multi_compile _ _ADDITIONAL_LIGHTS
#pragma multi_compile _ _CLUSTER_LIGHT_LOOP

half3 StudyDiffuseFromLight(Light source, half3 normalWS)
{
    return source.color * saturate(dot(normalWS, source.direction))
         * source.distanceAttenuation * source.shadowAttenuation;
}

half3 StudyAdditionalDiffuse(float3 worldPos, half3 normalWS, float4 screenPos)
{
    // 光照循环宏依赖这个名字和这些字段。
    InputData inputData = (InputData)0;
    inputData.positionWS = worldPos;
    inputData.normalWS = normalize(normalWS);
    inputData.viewDirectionWS = GetWorldSpaceNormalizeViewDir(worldPos);
    inputData.normalizedScreenSpaceUV = GetNormalizedScreenSpaceUV(screenPos);

    half3 sum = 0;
    #if defined(_ADDITIONAL_LIGHTS)
        // Forward+ 中非主方向光需额外遍历。
        #if USE_CLUSTER_LIGHT_LOOP
            UNITY_LOOP for (uint i = 0;
                i < min(URP_FP_DIRECTIONAL_LIGHTS_COUNT, MAX_VISIBLE_LIGHTS); ++i)
            {
                Light source = GetAdditionalLight(i, worldPos, half4(1,1,1,1));
                sum += StudyDiffuseFromLight(source, inputData.normalWS);
            }
        #endif

        uint count = GetAdditionalLightsCount();
        LIGHT_LOOP_BEGIN(count)
            Light source = GetAdditionalLight(lightIndex, worldPos, half4(1,1,1,1));
            sum += StudyDiffuseFromLight(source, inputData.normalWS);
        LIGHT_LOOP_END
    #endif
    return sum;
}
```

在片元函数中调用 `StudyAdditionalDiffuse(IN.positionWS, N, IN.positionCS)`，将结果乘 albedo 加入主灯结果。Forward Renderer 的 Additional Lights 应使用 **Per Pixel**；上面没有实现 Per Vertex 分支。

Forward+ 下 `GetAdditionalLightsCount()` 返回 0，并不表示没有附加灯；必须通过配套宏遍历聚类数据。宏中需要的 `inputData` 是实际代码依赖，不只是随意命名的局部变量。

依据：[Unity 6.7 Forward / Forward+ 附加灯示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/use-built-in-shader-methods-additional-lights-fplus.html)。

### 11.5 PBR 接口与完整 Lit 的差距

典型 PBR 接口是：

```hlsl
// 结构示意：必须先正确填充全部所需字段，不能把两个零结构直接当完整 Lit。
SurfaceData surfaceData = (SurfaceData)0;
InputData inputData = (InputData)0;

// surfaceData：albedo、metallic / specular、smoothness、normalTS、
//              emission、occlusion、alpha，以及版本相关字段。
// inputData：世界位置、世界法线、视线方向、阴影坐标、烘焙 GI、
//            screen UV、shadow mask 等。

// half4 color = UniversalFragmentPBR(inputData, surfaceData);
```

函数输出取决于数据初始化、关键字和管线资源。`occlusion=0` 会错误压暗间接光；没有正确的 GI / 反射输入也不会自动得到官方 Lit 的表现。完整实现请对照**同版本**的 `LitInput.hlsl`、`LitForwardPass.hlsl`、`Lighting.hlsl`。

## 12 深度与屏幕纹理

### 12.1 场景深度

```hlsl
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl"

// 片元函数内：positionCS 是 SV_POSITION 输入。
float2 screenUV = GetNormalizedScreenSpaceUV(IN.positionCS);
float rawDepth = SampleSceneDepth(screenUV);
float eyeDepth = LinearEyeDepth(rawDepth, _ZBufferParams);
```

`rawDepth` 通常不是线性距离；`eyeDepth` 也不是相机到物体的欧氏距离。上面的 `_ZBufferParams` 线性化写法针对常见透视相机流程；正交相机应使用适配投影的处理，或通过下面的逆矩阵重建位置。

根据深度重建世界位置：

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

需要提供 Camera Depth Texture；URP Asset / 相机设置和 Pass 执行时间决定纹理何时可读。天空等未写深度区域需要单独排除；透明物体不保证写入该纹理。

依据：[6.7 深度重建示例](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-reconstruct-world-position.html)。

### 12.2 场景颜色

```hlsl
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareOpaqueTexture.hlsl"

half3 sceneColor = SampleSceneColor(screenUV);
```

需要 Opaque Texture 或对应 Renderer 提供资源。`_CameraOpaqueTexture` 是在指定时机生成的不透明场景颜色副本，不是随时能读到的“当前帧缓冲”；通常不含后续透明物体。折射和自定义全屏效果必须同时考虑采样时机、Renderer Feature 输入声明、动态分辨率与 XR。

`RenderGraph` 是 URP 的资源和 Pass 调度机制，不是替换 ShaderLab 的新语法。全屏 Blit Shader 还应对照包里的 `Blit.hlsl` 和相应 Renderer Feature，不能直接套网格顶点输入。

## 13 常量缓冲与实例化

### 13.1 SRP Batcher

```hlsl
CBUFFER_START(UnityPerMaterial)
    float4 _BaseMap_ST;
    float4 _BaseColor;
    float _Cutoff;
    float _Intensity;
CBUFFER_END
```

- 材质的数值属性统一放进 `UnityPerMaterial`。
- 纹理和 Sampler 声明在缓冲外。
- 所有相关 Pass 使用一致的材质缓冲布局。
- 不要用 `#ifdef` 有条件地增删缓冲成员；对不同变体保持布局一致。
- 引入 URP 库管理内置 `UnityPerDraw`；不要手工重复声明对象矩阵。
- SRP Batcher 减少 CPU 状态准备开销，不代表把所有对象合并成一次 Draw Call。

即使没有写入 `Properties`，需要按材质变化的数值也要按一致布局设计。只被 ShaderLab 渲染状态使用的属性与 HLSL 中实际读取的常量应区分处理。

`float3`、数组和矩阵在常量缓冲中的排列存在对齐规则；不要用 C# 字段大小简单相加猜测 GPU 布局。自己管理 Buffer 时需要核对结构步长和图形后端。[6.7 SRP Batcher](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shaders-in-universalrp-srp-batcher.html)、[HLSL 常量打包规则](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-packing-rules)

### 13.2 传统 GPU Instancing 宏

| 宏 / 指令 | 所在位置 / 作用 |
|---|---|
| `#pragma multi_compile_instancing` | 编译实例化变体 |
| `UNITY_VERTEX_INPUT_INSTANCE_ID` | 在输入结构体中携带实例信息 |
| `UNITY_SETUP_INSTANCE_ID(IN)` | 在变换之前建立当前实例上下文 |
| `UNITY_TRANSFER_INSTANCE_ID(IN,OUT)` | 片元需要实例数据时传递 ID |
| `UNITY_INSTANCING_BUFFER_START(Props)` | 定义实例数据缓冲 |
| `UNITY_DEFINE_INSTANCED_PROP(float4,_Tint)` | 声明实例属性 |
| `UNITY_INSTANCING_BUFFER_END(Props)` | 结束实例缓冲 |
| `UNITY_ACCESS_INSTANCED_PROP(Props,_Tint)` | 读取当前实例属性 |

仅加 pragma 不会自动实现每实例颜色。材质、Mesh、调用方式和渲染路径也要满足实例化要求；普通 Renderer 的 SRP Batcher 路径、传统 GPU Instancing、GPU Resident Drawer / DOTS Instancing 是不同机制。

XR 单通道立体通常还涉及 `UNITY_VERTEX_OUTPUT_STEREO`、`UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO`、`UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX`。下面的基础示例未声明 XR 或 DOTS 支持。

宏的通用含义可从 [Unity 6.7 Built-in 实例化文档入口](https://docs.unity3d.com/6000.7/Documentation/Manual/gpu-instancing-shader.html)继续查阅；该文档的管线示例属于 Built-in，不能原样移植到 URP。URP 应结合当前包的 `UnityInstancing.hlsl` 和实际绘制路径核对。

## 14 完整示例 A 纹理与颜色 Unlit

保存为 `StudyTextureUnlit.shader`，在材质 Shader 菜单选择 `Study/URP67/TextureUnlit`。

功能：纹理、颜色、Tiling / Offset、场景雾。用于 3D Universal Renderer；没有光照、阴影投射、DepthOnly、运动矢量或 XR 扩展。

```hlsl
Shader "Study/URP67/TextureUnlit"
{
    Properties
    {
        [MainTexture] _BaseMap ("Base Map", 2D) = "white" {}
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
    }

    SubShader
    {
        Tags
        {
            "RenderPipeline" = "UniversalPipeline"
            "RenderType" = "Opaque"
            "Queue" = "Geometry"
        }

        Pass
        {
            Name "Unlit"
            Tags { "LightMode" = "SRPDefaultUnlit" }

            Cull Back
            ZWrite On
            ZTest LEqual
            Blend Off

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma target 3.0
            #pragma multi_compile_fog

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            CBUFFER_START(UnityPerMaterial)
                float4 _BaseMap_ST;
                float4 _BaseColor;
            CBUFFER_END

            TEXTURE2D(_BaseMap);
            SAMPLER(sampler_BaseMap);

            struct Attributes
            {
                float3 positionOS : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float2 uv : TEXCOORD0;
                half fogFactor : TEXCOORD1;
            };

            Varyings Vert(Attributes IN)
            {
                Varyings OUT = (Varyings)0;
                OUT.positionCS = TransformObjectToHClip(IN.positionOS);
                OUT.uv = TRANSFORM_TEX(IN.uv, _BaseMap);
                OUT.fogFactor = ComputeFogFactor(OUT.positionCS.z);
                return OUT;
            }

            half4 Frag(Varyings IN) : SV_Target
            {
                half4 color = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, IN.uv);
                color *= _BaseColor;
                color.rgb = MixFog(color.rgb, IN.fogFactor);
                return color;
            }
            ENDHLSL
        }
    }
    Fallback Off
}
```

> [!note] Alpha 与透明
> 这个示例即使输出 Alpha 小于 1，RGB 也仍是正常的不透明写入，因为 `Blend Off`。透明需要一起配置队列、混合和深度写入，见 [[#16 透明与裁剪改造]]。

基础结构依据：[URP 纹理 Shader](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-shaders-urp-unlit-texture.html)。此处代码为整理后的学习示例，不是官方完整 Unlit Shader 的原样副本。

## 15 完整示例 B 主光源与实时阴影

保存为 `StudyMainLight.shader`，在材质选择 `Study/URP67/MainLight`。

功能：主方向光 Lambert、纹理颜色、普通/级联/屏幕空间主灯阴影、场景雾；另含深度 Pass。`_AmbientColor` 是手动环境补光，不是 Light Probe、APV 或烘焙 GI。

> [!important] 示例边界
> 这是不透明的学习 Shader。它能接收其他物体的阴影，但没有 `ShadowCaster`，因此自身不投影。没有完整 PBR、附加光、Light Cookies、Rendering Layers、SSAO 法线 Pass、MotionVectors 或 XR。
> Atlas 阴影未加入软阴影质量变体。使用屏幕空间阴影时还需启用对应 Renderer Feature。生产项目需按实际功能补齐 Pass 和关键字。

```hlsl
Shader "Study/URP67/MainLight"
{
    Properties
    {
        [MainTexture] _BaseMap ("Base Map", 2D) = "white" {}
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        _AmbientColor ("Manual Ambient", Color) = (0.08, 0.08, 0.08, 1)
    }

    SubShader
    {
        Tags
        {
            "RenderPipeline" = "UniversalPipeline"
            "RenderType" = "Opaque"
            "Queue" = "Geometry"
        }

        // 所有 Pass 共用完全相同的材质缓冲布局。
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

        CBUFFER_START(UnityPerMaterial)
            float4 _BaseMap_ST;
            float4 _BaseColor;
            float4 _AmbientColor;
        CBUFFER_END

        TEXTURE2D(_BaseMap);
        SAMPLER(sampler_BaseMap);

        struct Attributes
        {
            float3 positionOS : POSITION;
            float3 normalOS : NORMAL;
            float2 uv : TEXCOORD0;
        };

        struct Varyings
        {
            float4 positionCS : SV_POSITION;
            float2 uv : TEXCOORD0;
            float3 positionWS : TEXCOORD1;
            half3 normalWS : TEXCOORD2;
            half fogFactor : TEXCOORD3;
        };

        Varyings Vert(Attributes IN)
        {
            Varyings OUT = (Varyings)0;
            VertexPositionInputs p = GetVertexPositionInputs(IN.positionOS);
            OUT.positionCS = p.positionCS;
            OUT.positionWS = p.positionWS;
            OUT.normalWS = TransformObjectToWorldNormal(IN.normalOS);
            OUT.uv = TRANSFORM_TEX(IN.uv, _BaseMap);
            OUT.fogFactor = ComputeFogFactor(p.positionCS.z);
            return OUT;
        }
        ENDHLSL

        Pass
        {
            Name "MainLight"
            Tags { "LightMode" = "UniversalForwardOnly" }
            Cull Back
            ZWrite On
            ZTest LEqual
            Blend Off

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma target 3.0
            #pragma multi_compile_fog
            #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE _MAIN_LIGHT_SHADOWS_SCREEN

            half4 Frag(Varyings IN) : SV_Target
            {
                half3 albedo = SAMPLE_TEXTURE2D(
                    _BaseMap, sampler_BaseMap, IN.uv).rgb * _BaseColor.rgb;
                half3 N = normalize(IN.normalWS);

                float4 shadowCoord;
                #if defined(_MAIN_LIGHT_SHADOWS_SCREEN)
                    shadowCoord = ComputeScreenPos(
                        TransformWorldToHClip(IN.positionWS));
                #else
                    shadowCoord = TransformWorldToShadowCoord(IN.positionWS);
                #endif

                Light sun = GetMainLight(
                    shadowCoord, IN.positionWS, half4(1, 1, 1, 1));

                half ndotl = saturate(dot(N, sun.direction));
                half3 direct = sun.color * ndotl
                    * sun.distanceAttenuation * sun.shadowAttenuation;

                half3 color = albedo * (_AmbientColor.rgb + direct);
                color = MixFog(color, IN.fogFactor);
                return half4(color, 1);
            }
            ENDHLSL
        }

        Pass
        {
            Name "DepthOnly"
            Tags { "LightMode" = "DepthOnly" }
            Cull Back
            ZWrite On
            ZTest LEqual
            ColorMask 0

            HLSLPROGRAM
            #pragma vertex VertDepth
            #pragma fragment FragDepth
            #pragma target 3.0

            float4 VertDepth(Attributes IN) : SV_POSITION
            {
                return TransformObjectToHClip(IN.positionOS);
            }

            half4 FragDepth() : SV_Target
            {
                return 0;
            }
            ENDHLSL
        }
    }
    Fallback Off
}
```

### 15.1 在 Unity 中验证

1. 使用 3D Universal Renderer，确认项目/当前质量级别选择了 URP Asset。
2. 给平面使用此 Shader，给上方立方体使用官方 `Universal Render Pipeline/Lit`。
3. 创建或启用 Directional Light，开启主灯阴影；立方体开启 Cast Shadows。
4. 检查平面收到阴影；改变光照角度，观察 Lambert 明暗。
5. 调整级联数量，移动相机经过级联边界；需要屏幕空间阴影时启用相应 Feature。
6. 在 Shader Inspector 看编译错误和 SRP Batcher 状态，在 Frame Debugger 看实际执行的 Pass。
7. 打包到目标图形 API，检查关键字剥离后表现。编辑器正常不代表所有构建变体都已保留。

若要接入 [[#11 URP 光照与阴影]] 中的附加灯函数，在 MainLight Pass 中加入其两个 pragma 与函数，并在应用 albedo 前把附加光加到 `direct`。Forward 路径要选择 Per Pixel；没有实现的 Rendering Layers / Cookies 不会因此自动支持。

## 16 透明与裁剪改造

以下修改针对 **示例 A**；先复制 Shader 并修改 Shader 名称，避免同名资产冲突。

### 16.1 普通 Alpha 透明

替换 SubShader 中的分类和队列：

```hlsl
"RenderType" = "Transparent"
"Queue" = "Transparent"
```

替换 Pass 状态：

```hlsl
ZWrite Off
Blend SrcAlpha OneMinusSrcAlpha, One OneMinusSrcAlpha
```

保留 `ZTest LEqual`。片元输出保持未预乘的 RGB，Alpha 控制透明度。透明通常依赖排序，交叉或自相交模型可能仍有错误；不是把 `ZWrite` 开回去就能全面解决。

### 16.2 预乘 Alpha

使用透明队列和 `ZWrite Off`，混合改为：

```hlsl
Blend One OneMinusSrcAlpha
```

在示例 A 的 `MixFog` 之后、`return` 之前插入：

```hlsl
color.rgb *= color.a;
```

这适合纹理存储为**未预乘** RGB 的当前流程。如果输入本身已预乘，不能再次乘 Alpha；雾、Emission 和纹理边缘也要按所选合成约定处理。

### 16.3 Alpha Clip 硬裁剪

在 Properties 加入：

```hlsl
_Cutoff ("Cutoff", Range(0, 1)) = 0.5
```

在原有 `UnityPerMaterial` 中加入：

```hlsl
float _Cutoff;
```

修改标签，并保留不透明的混合和深度设置：

```hlsl
// SubShader Tags
"RenderType" = "TransparentCutout"
"Queue" = "AlphaTest"

// Pass 状态
Blend Off
ZWrite On
```

在 `color *= _BaseColor;` 后插入：

```hlsl
clip(color.a - _Cutoff);
```

这是始终开启的硬裁剪。若需要开关，再添加 `[Toggle(_ALPHATEST_ON)]`、对应 pragma 与条件编译；不要只增加 Toggle。

| 行为 | 普通透明 | Alpha Clip |
|---|---|---|
| 半透明 | 支持连续透明度 | 只保留或丢弃 |
| 常见深度写入 | Off | On |
| 常见队列 | Transparent | AlphaTest |
| 排序问题 | 常见 | 通常按不透明流程处理 |
| 阴影轮廓 | 需要专门设计 | ShadowCaster 需重复相同裁剪 |

### 16.4 让多 Pass 轮廓一致

给 Shader 添加位移、溶解或裁剪后，应同步检查：

- 颜色 Pass：可见轮廓。
- ShadowCaster：投影轮廓。
- DepthOnly / DepthNormals：相机深度、SSAO、屏幕空间效果。
- MotionVectors：前后帧位置，影响 TAA 等功能。
- Meta：烘焙所使用的表面信息。

共享位移/裁剪函数能减少不同 Pass 行为不一致的问题，但每个 Pass 仍要明确调用。

## 17 常见错误与检查顺序

### 17.1 症状对照

| 症状 | 优先检查 |
|---|---|
| 材质粉色 | Console 第一条编译错误、包路径、入口函数、RenderPipeline 标签 |
| 材质完全不可见 | Cull、ZTest、队列、Pass LightMode、是否被 clip 全丢弃 |
| 设置 Alpha 仍不透明 | Blend、Queue、ZWrite 是否成套配置 |
| 光照全黑 | 法线是否有效、是否归一化、灯光设置、手动环境光/GI 输入 |
| 贴图不跟随 Tiling | `_BaseMap_ST` 声明与 `TRANSFORM_TEX` 是否存在 |
| 接收阴影但不投影 | 是否实现 ShadowCaster；Renderer 是否允许投影 |
| 投影正常但自身不接收 | 是否采样阴影并乘 `shadowAttenuation` |
| 级联边界出现三角形色块 | 阴影坐标是否只在顶点计算再跨级联插值 |
| Forward 正常、Deferred 异常 | UniversalForwardOnly 或正确 GBuffer Pass、DepthNormals 配套 |
| Forward+ 没有附加光 | `_CLUSTER_LIGHT_LOOP`、宏循环、`inputData` 字段 |
| SSAO 缺失 | Renderer 请求的法线 Pass、法线编码与关键字 |
| 深度全白或全黑 | 深度纹理未生成/读取时机错误，或误解 Reverse-Z |
| 法线贴图发黑/翻转 | 导入类型、解码方式、切线、TBN 手性和归一化 |
| 物体移动时抖动 | 世界坐标/UV 是否错误使用 half |
| SRP Batcher 不兼容 | UnityPerMaterial、Pass 布局、额外常量缓冲、运行时属性路径 |
| 编辑器正常，构建异常 | 变体剥离、平台能力、Renderer / Quality 配置差异 |
| 描边第二个 Pass 不出现 | 默认 Renderer 是否真正调度它 |

### 17.2 调试颜色

在片元函数中临时返回：

```hlsl
return half4(1, 0, 1, 1);                    // 排除复杂光照计算
return half4(IN.uv, 0, 1);                   // 检查 UV
return half4(normalize(IN.normalWS) * 0.5 + 0.5, 1); // 法线可视化
return half4(shadow, shadow, shadow, 1);      // 检查已计算的阴影值
```

这些是互斥的调试片段，每次只保留一种，并确保相应字段/变量存在。

推荐顺序：**编译 → Pass 是否绘制 → 顶点变换 → 纹理/UV → 法线 → 单灯 → 阴影 → 附加灯 → 目标平台**。一次只恢复一组功能，避免错误相互遮掩。

### 17.3 性能检查

- 先确认瓶颈是 CPU、GPU 运算、纹理带宽还是透明 Overdraw。
- 片元覆盖面积大的效果尤其要注意多次采样与透明叠加。
- 少量关键字也可能产生大量组合；保留确实需要的变体。
- 能安全移到顶点阶段的计算可以减少次数，但插值可能改变质量。
- `half`、分支、循环展开、`clip` 的收益要实际测量，不能只凭语法判断。

## 18 官方资料与包源码导航

### 18.1 版本核对方法

1. 在编辑器 About / 项目 `ProjectSettings/ProjectVersion.txt` 查看完整版本，例如 `6000.7.0b…`。
2. 在 Package Manager / 包的 `package.json` 查看实际 URP 信息；不要仅凭 Editor 的次版本推断包号。
3. 从 Project 窗口的 Packages 找到 Universal RP 与 Core RP 源码。物理位置可能是包缓存、嵌入包或编辑器内置包。
4. 阅读和当前安装内容一致的文档/源码。网络仓库 `master` 可能超前于当前版本。

### 18.2 优先看的包内文件

下列是包内部路径导航，不是本机已确认存在的文件链接。

```text
com.unity.render-pipelines.universal/
├─ Shaders/
│  ├─ Lit.shader
│  ├─ Unlit.shader
│  ├─ LitInput.hlsl
│  ├─ LitForwardPass.hlsl
│  ├─ ShadowCasterPass.hlsl
│  └─ DepthOnlyPass.hlsl
└─ ShaderLibrary/
   ├─ Core.hlsl
   ├─ Lighting.hlsl
   ├─ RealtimeLights.hlsl
   ├─ Shadows.hlsl
   ├─ Input.hlsl
   ├─ SurfaceData.hlsl
   ├─ ShaderVariablesFunctions.hlsl
   ├─ DeclareDepthTexture.hlsl
   └─ DeclareOpaqueTexture.hlsl

com.unity.render-pipelines.core/ShaderLibrary/
├─ Common.hlsl
├─ SpaceTransforms.hlsl
├─ Packing.hlsl
└─ UnityInstancing.hlsl
```

按问题定位：空间变换看 `SpaceTransforms.hlsl`；屏幕位置/雾看 `ShaderVariablesFunctions.hlsl`；关键字与 Pass 看 `Lit.shader`；灯光循环看 `RealtimeLights.hlsl`；阴影坐标与过滤看 `Shadows.hlsl`。

公开源码：[Unity Technologies / Graphics](https://github.com/Unity-Technologies/Graphics)。应选择匹配版本的分支或标签，不要把最新开发分支当作 6.7 项目实际源码。

### 18.3 主要文档入口

| 内容 | 官方资料 |
|---|---|
| ShaderLab 属性 | [6.7 Properties](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-Properties.html) |
| SubShader 分类 | [6.7 Tags](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-SubShaderTags.html) |
| URP Pass 调度 | [6.7 Pass Tags](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-shaders/urp-shaderlab-pass-tags.html) |
| 编译入口和限制 | [6.7 pragma](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-PragmaDirectives.html) |
| 关键字 | [6.7 关键字声明](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-MultipleProgramVariants-declare.html) |
| URP 光照 | [6.7 光照方法](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/use-built-in-shader-methods-lighting.html) |
| Forward+ 附加光 | [6.7 光照循环](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/use-built-in-shader-methods-additional-lights-fplus.html) |
| 实时阴影 | [6.7 阴影方法](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/use-built-in-shader-methods-shadows.html) |
| SRP Batcher | [6.7 常量缓冲要求](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/shaders-in-universalrp-srp-batcher.html) |
| HLSL 类型 | [Microsoft 数据类型](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-data-types) |
| HLSL 阶段接口 | [Microsoft Semantics](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics) |
| HLSL 内置函数 | [Microsoft Intrinsics](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-intrinsic-functions) |


---

> [!note] 整理与验证记录
> 官方资料核对日期：2026-09-16。6.7 页面为 Beta 文档；正文把完整文件、局部片段与结构示意分别标明。
> 文档进行 Markdown 结构与内部链接检查；Shader 示例仅作静态核对，未声称在 Unity 6.7 Editor 或各平台通过编译、运行验证。
