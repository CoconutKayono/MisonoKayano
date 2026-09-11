# 01｜搭建 Shader 与暴露材质参数

## 场景：读懂一个 Shader 文件的外壳

完整代码见 [BasicTexture.shader](示例/BasicTexture.shader)。结构可以先按下面的缩略图理解；省略的函数须参考完整文件，不能单独编译此缩略图。

~~~c
Shader "FAQ/Syntax/BasicTexture"
{
    Properties { /* 材质面板 */ }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="SRPDefaultUnlit" }
            ZWrite On
            Cull Back

            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            // 资源声明、结构体、vert、frag
            ENDHLSL
        }
    }
}
~~~

| 写法                        | 作用                | 容易误解之处                  |
| ------------------------- | ----------------- | ----------------------- |
| Shader "路径/名称"            | 决定材质 Shader 菜单名称  | 不要求和文件名相同               |
| Properties                | 定义材质可保存的属性        | 不自动替你声明 HLSL 变量         |
| SubShader                 | 提供一套管线/平台实现       | 不是所有 SubShader 都顺序执行    |
| Pass                      | 一次渲染阶段的程序与状态      | URP 不会无条件依次绘制所有自定义 Pass |
| Tags                      | 向 Unity 提供分类、调度信息 | 标签本身不执行颜色计算             |
| HLSLPROGRAM…ENDHLSL       | 包围 GPU 程序代码       | Blend 等状态写在它外面          |
| #pragma vertex / fragment | 指定阶段入口函数          | vert、frag 是自定义函数名       |
| #include                  | 引入函数和宏            | 头文件路径随管线而不同             |

Queue、RenderType、RenderPipeline 通常放在 SubShader Tags；LightMode 放在 Pass Tags。它们的位置不能靠名称相似就互换。

## 场景：给美术开放颜色、强度与贴图

**放在 Properties 中：**

~~~c
[MainColor] _BaseColor("Tint", Color) = (1,1,1,1)
[MainTexture] _BaseMap("Base Map", 2D) = "white" {}
_Strength("Strength", Range(0,2)) = 1
_Scroll("UV Speed XY", Vector) = (0.1,0,0,0)
~~~

左边 _BaseColor 是代码名称；引号里的 Tint 是面板名称。ShaderLab 属性声明行通常没有 HLSL 式的分号。

**放在 HLSLPROGRAM 内、函数外：**

~~~c
TEXTURE2D(_BaseMap);
SAMPLER(sampler_BaseMap);

CBUFFER_START(UnityPerMaterial)
    float4 _BaseColor;
    float4 _BaseMap_ST;
    float4 _Scroll;
    float _Strength;
CBUFFER_END
~~~

颜色和 Vector 对应四个分量；Range 通常对应 float。_BaseMap_ST.xy 保存平铺、.zw 保存偏移，具体使用见第 04 篇。

逐材质的**数值变量**统一放入 UnityPerMaterial 常量缓冲区，纹理和采样器声明放在外面。多个 Pass 应保持相同材质缓冲布局。[Unity Properties 参考](https://docs.unity3d.com/cn/6000.0/Manual/SL-Properties.html)

## 常用面板类型与装饰

| 写法 | 场景 | 注意 |
| --- | --- | --- |
| Float | 无滑条的数值输入 | 并非 C# 字段 |
| Range(0,1) | 强度、阈值、混合权重 | 面板范围不代替 Shader 内的边界处理 |
| Color | 染色 | 有颜色处理语义，不能总当普通 Vector 等同看待 |
| Vector | 方向、速度、四个参数 | 通常读取 .xy 或 .xyz |
| 2D | 普通纹理 | HLSL 里另声明纹理与采样器 |
| [HDR] | HDR 发光颜色 | 允许高亮颜色，不自动开启 Bloom |
| [Normal] | 法线纹理槽提示 | 采样后仍需法线解码 |
| [NoScaleOffset] | 不展示贴图平铺与偏移 | 不代表自动完成你的 UV 逻辑 |
| [Toggle(_RIM_ON)] | 材质功能开关 | 还需关键字声明与条件代码，见第 08 篇 |

不要只根据面板出现了一个参数就认为它影响画面；必须在 frag 或 vert 的计算里使用相应变量。

## 场景：从 C# 改材质颜色

已有 Material 引用 material 时：

~~~csharp
material.SetColor("_BaseColor", Color.cyan);
material.SetFloat("_Strength", 0.8f);
material.SetVector("_Scroll", new Vector4(0.1f, 0, 0, 0));
~~~

属性名必须和 Shader 完全一致。修改共享材质会影响共用它的对象；大量逐对象参数需另行考虑材质实例与 MaterialPropertyBlock 的性能取舍。

基础模板只有 _BaseMap 与 _BaseColor。要使用 _Strength、_Scroll，请补上本节两处声明，并在后续计算中使用它们。

导航：[[00-按使用场景查语法|场景目录]] · 下一篇：[[02-HLSL数据与函数怎么写]]
