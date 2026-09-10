# A 阶段检查点｜把几何与颜色数据变成可解释的画面

目标：使用一个最小 URP 材质，切换世界法线、UV、世界位置、方向点积和颜色渐变视图，预测改变输入后的结果。本文件包含完整 Shader 与步骤，可以脱离其他卡片使用。

## 1. 实验范围与必要概念

位置描述点在哪里；法线描述表面朝向；UV 是模型给定的二维纹理坐标。世界空间是场景共同使用的坐标系，物体空间是 Mesh 自身的坐标系。点积 `dot(N,L)` 在两个向量都归一化时等于夹角余弦；归一化使非零向量长度变为 1。

显示设备不能直接把负法线或任意世界坐标当作颜色：本例将单位法线 `[-1,1]` 映射为 `0.5N+0.5`，将世界位置映射为 `0.5+sP`，其中 `s` 为每世界单位的颜色变化量。位置和 UV 视图会显式裁到 `[0,1]`，因此饱和区域不能用来读取范围外的原始值。

采用 Unity URP、普通单相机 Forward、Linear 色彩空间、SDR 输出。建立测试材质，不更改生产材质。关闭后处理、Depth Priming、SSAO 和额外 Renderer Feature；关闭动态分辨率，并用默认普通 MeshRenderer。使用有法线和 UV 的 Sphere 观察朝向，使用面向相机的 Quad 观察 UV 和渐变。本例不依赖场景灯光。

这是一份单 Pass 教学 Shader，不提供阴影、DepthNormals、运动矢量、实例化和 XR 的完整支持。包接口参考 Core/URP 17.0.4 的固定源码；当前没有在 Unity Editor 编译或运行。

## 2. 完整 Shader

保存为 `AStageDataLab.shader`，放入 URP 项目的 `Assets/KnowledgeCards/`。创建材质并选择 `Encyclopedia/AStageDataLab`。

```shaderlab
Shader "Encyclopedia/AStageDataLab"
{
    Properties
    {
        [Enum(WorldNormal,0,UV,1,WorldPosition,2,NdotL,3,ColorCompare,4)]
        _Mode("View", Float) = 0
        _PositionScale("World Position Scale", Float) = 0.1
        _LightDirection("World Surface To Light", Vector) = (0,1,0,0)
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "DataView"
            Tags { "LightMode"="UniversalForward" }
            Cull Back
            ZWrite On
            ZTest LEqual
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            CBUFFER_START(UnityPerMaterial)
                float4 _LightDirection;
                float _Mode;
                float _PositionScale;
            CBUFFER_END

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float2 uv : TEXCOORD0;
            };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionWS : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
                float2 uv : TEXCOORD2;
            };
            float3 UnitOrZero(float3 v)
            {
                return v * rsqrt(max(dot(v, v), 1e-12));
            }
            float DecodeSRGB01(float e)
            {
                return e <= 0.04045 ? e / 12.92
                    : pow((e + 0.055) / 1.055, 2.4);
            }
            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionWS = TransformObjectToWorld(input.positionOS.xyz);
                output.positionCS = TransformWorldToHClip(output.positionWS);
                output.normalWS = TransformObjectToWorldNormal(input.normalOS, false);
                output.uv = input.uv;
                return output;
            }
            half4 Frag(Varyings input) : SV_Target
            {
                float3 n = UnitOrZero(input.normalWS);
                float3 c;
                if (_Mode < 0.5)
                    c = n * 0.5 + 0.5;
                else if (_Mode < 1.5)
                    c = float3(saturate(input.uv), 0);
                else if (_Mode < 2.5)
                    c = saturate(input.positionWS * _PositionScale + 0.5);
                else if (_Mode < 3.5)
                {
                    float value = saturate(dot(n, UnitOrZero(_LightDirection.xyz)));
                    c = float3(value, value, value);
                }
                else
                {
                    float t = saturate(input.uv.x);
                    float value = input.uv.y >= 0.5 ? t : DecodeSRGB01(t);
                    c = float3(value, value, value);
                }
                return half4(c, 1);
            }
            ENDHLSL
        }
    }
}
```

`UnitOrZero` 对极小向量采用保护性处理，不把没有法线的 Mesh 变成有效输入；正常非零法线仍是实验前提。非均匀缩放下使用逆转置语义变换法线，在片元阶段重新归一化。Shader 输出的是线性数值，最终由管线输出路径完成显示编码；这里不手动调用输出 sRGB 编码。

## 3. 先预测，再修改

| 视图 | 修改 | 预期与理由 |
| --- | --- | --- |
| WorldNormal | 只平移物体 | 对应表面位置的法线颜色不因平移改变；旋转会改变世界朝向 |
| UV | 移动或旋转物体 | 对应顶点的 UV 不变；屏幕覆盖会变化 |
| WorldPosition | 在未饱和处向 +X 平移 1，Scale=0.1 | 线性红通道增加 0.1；显示编码值不会简单增加 0.1 |
| NdotL | 光方向由 `(0,1,0)` 改为 `(0,2,0)` | 因归一化而保持相同明暗；方向改为 `(1,0,0)` 才改变照明朝向 |
| ColorCompare | 在 Quad 的 `u=0.5` 附近比较两半 | `v≥0.5` 输出线性 0.5，另一半输出约 0.214041；前者更亮 |

最后一项在无额外映射的标准 SDR sRGB 输出下，两半显示编码中点分别约 `0.735357` 和 `0.5`。这里只对一条标量渐变做数学解码，没有采样纹理，因此不是 GPU 自动 sRGB 纹理解码的运行验证。截图像素还可能受到抗锯齿、显示转换与取样位置影响，不能直接当作 Shader 输出值。

## 4. 把 A06—A08 的数据检查接上

使用 Mesh 审计脚本记录顶点属性、stride、索引与子网格；使用纹理审计脚本记录当前纹理的实际图形格式和 sRGB 设置。它们不参与此 Shader 编译，下面的表可以手工填写：

| 记录 | 必须写明的内容 |
| --- | --- |
| Mesh | 顶点数、索引格式、每个 stream 的 stride；不要将顶点数写成几何角点数 |
| 一张颜色 Ramp | 颜色编码、导入格式、Mip 数、颜色与数值的用途 |
| 一张阈值遮罩 | 0.5 的语义、sRGB 是否符合约定、允许误差 |
| 资源容量 | 按格式计算的有效载荷；另列工具测量，不能混填 |
| 更新频率 | 何时上传、每次更新多少元素、是否确实需要 CPU 读回 |

Mesh/纹理审计脚本及详细步骤集中在 [实验说明](Unity%20Shader/图形学Obsidian/Unity%20Shader%20入门教程v2/实验/README.md)。没有测试贴图时，本检查点的五个可视化视图仍可独立完成；资产审计项保留待做。

## 5. 阶段通过条件

当你能在不看答案的情况下解释五项预测，并对一个自己的模型记录 Mesh 布局与一种贴图的数据语义，就完成本阶段的基础迁移。对不上时，应记录输入、项目设置和实际观察，回到对应模型查原因，不能把不一致归为“Unity 就是这样”。

当前交付状态：实验文件已生成；配套公式有 Python 数值校验；Unity 编译、画面观察与读者掌握程度均尚未确认。不要将这份检查表当成已经完成的测试报告。

变换函数源码：[SpaceTransforms.hlsl，固定提交 275a7f9](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.core/ShaderLibrary/SpaceTransforms.hlsl)。颜色公式：[W3C sRGB 转换代码](https://www.w3.org/TR/css-color-4/#color-conversion-code)。教程环境：[Unity URP 自定义 Shader 法线](https://docs.unity3d.com/6000.0/Documentation/Manual/urp/writing-shaders-urp-unlit-normals.html)。
