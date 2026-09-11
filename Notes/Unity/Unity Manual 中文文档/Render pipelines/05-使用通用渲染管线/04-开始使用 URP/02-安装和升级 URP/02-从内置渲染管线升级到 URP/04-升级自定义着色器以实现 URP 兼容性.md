# 升级自定义着色器以实现 URP 兼容性

> 原文：[Convert custom shaders for URP compatibility](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-shaders/birp-urp-custom-shader-upgrade-guide.html)


为内置渲染管线编写的自定义着色器与通用渲染管线 (URP) 不兼容，无法使用渲染管线转换器 (Render Pipeline Converter) 将其自动升级。相反，必须重新编写着色器代码的不兼容部分才能使用 URP。

此外，也可以在 Shader Graph 中重新创建自定义着色器。有关更多信息，请参阅 [ShaderGraph](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest) 相关文档。

> **注意**：升级到 URP 时，场景中使用自定义着色器的所有材质都会变为洋红色（亮粉色）以指示错误，以便于您识别这些材质。

本指南通过以下部分演示了如何从内置渲染管线升级自定义无光照着色器以实现与 URP 完全兼容：

- 查看内置渲染管线着色器示例。
- 使自定义着色器与 URP 兼容。
- 为着色器启用平铺和偏移。
- 查看完整着色器代码。

## 内置渲染管线着色器示例

以下着色器是一个简单的无光照着色器，适用于内置渲染管线。本指南演示了如何升级此着色器以兼容 URP。

```
Shader "Custom/UnlitShader"
{
    Properties
    {
        [NoScaleOffset] _MainTex("Main Texture", 2D) = "white" {}
        _Color("Color", Color) = (1,1,1,1)
    }

    SubShader
    {
        Tags { "RenderType" = "Opaque" }

        Pass
        {
            CGPROGRAM

            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float4 position : SV_POSITION;
                float2 uv: TEXCOORD0;
            };

            float4 _Color;
            sampler2D _MainTex;

            v2f vert(appdata_base v)
            {
                v2f o;

                o.position = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;

                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                fixed4 texel = tex2D(_MainTex, i.uv);
                return texel * _Color;
            }
            ENDCG
        }
    }
}
```

## 使自定义着色器与 URP 兼容

内置渲染管线着色器有两个问题，可在检视面板窗口中看到这两个问题：

- 指示**材质属性位于另一个常量缓冲区中**的警告。
- **SRP Batcher** 属性显示**不兼容**。

以下步骤展示了如何解决这些问题并使着色器与 URP 和 SRP Batcher 兼容。

1. 将 `CGPROGRAM` 和 `ENDCG` 更改为 `HLSLPROGRAM` 和 `ENDHLSL`。
2. 更新 include 语句以引用 `Core.hlsl` 文件。

```cpp
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
```

   **注意**：`Core.hlsl` 包含核心 SRP 库、URP 着色器变量以及矩阵定义和变换，但不包括光照函数和默认结构。
3. 向着色器标签添加 `"RenderPipeline" = "UniversalPipeline"`。

```cpp
Tags { "RenderType" = "Opaque" "RenderPipeline" = "UniversalPipeline" }
```

   **注意**：URP 不支持所有 ShaderLab 标签。有关 URP 支持哪些标签的更多信息，请参阅 [URP ShaderLab Pass 标签](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-shaders/urp-shaderlab-pass-tags.html)。
4. 将 `struct v2f` 代码块替换为以下 `struct Varyings` 代码块。此操作会更改结构以使用 `Varyings` 而不是 `v2f` 的 URP 命名规则，并更新着色器以使用 URP 的正确变量。

```cpp
struct Varyings
{
    // The positions in this struct must have the SV_POSITION semantic.
    float4 positionHCS  : SV_POSITION;
    float2 uv : TEXCOORD0;
};
```
5. 在 include 语句下方和 `Varyings` 结构上方，定义一个名称为 `Attributes` 的新结构。这等同于内置渲染管线的 appdata 结构，但具有新的 URP 命名规则。
6. 将下面显示的变量添加到 `Attributes` 结构中。

```cpp
struct Attributes
{
    float4 positionOS   : POSITION;
    float2 uv : TEXCOORD0;
};
```
7. 更新 `v2f vert` 函数定义以使用新的 `Varyings` 结构，并将 `Attributes` 结构的实例作为输入，如下所示。

```cpp
Varyings vert(Attributes IN)
```
8. 更新 vert 函数以输出 `Varyings` 结构的实例，并使用 `TransformObjectToHClip` 函数从对象空间转换为裁剪空间。该函数还需要获取输入 `Attributes` UV 并将其传递给输出 `Varyings` UV。

```cpp
Varyings vert(Attributes IN)
{
    Varyings OUT;

    OUT.positionHCS = TransformObjectToHClip(IN.positionOS.xyz);
    OUT.uv = IN.uv;

    return OUT;
}
```

   **注意**：URP 着色器使用后缀来表示空间。`OS` 表示对象空间，`HCS` 表示齐次裁剪空间。
9. 在着色器使用的属性周围放置一个 `CBUFFER` 代码块以及 `UnityPerMaterial` 参数。

```cpp
CBUFFER_START(UnityPerMaterial)
float4 _Color;
sampler2D _MainTex;
CBUFFER_END
```

   **注意**：要使着色器与 SRP Batcher 兼容，必须在 `CBUFFER` 代码块中声明所有材质属性。即使着色器有多个通道，所有通道也必须使用相同的 `CBUFFER` 代码块。
10. 更新 `frag` 函数以使用 `Varyings` 输入和 `half4` 类型，如下所示。`frag` 函数现在必须使用此类型，因为 URP 着色器不支持固定类型。

```cpp
half4 frag(Varyings IN) : SV_Target
{
    half4 texel = tex2D(_MainTex, IN.uv);
    return texel * _Color;
}
```

此自定义无光照着色器现在已与 SRP Batcher 兼容，并可在 URP 中使用。您可以在检视面板窗口中进行此检查：

- **材质属性位于另一个常量缓冲区中**的警告不再显示。
- **SRP Batcher** 属性显示**兼容**。

## 为着色器启用平铺和偏移

虽然着色器现在已与 URP 和 SRP Batcher 兼容，但如果不做出进一步的更改，则无法使用 **Tiling** 和 **Offset** 属性。要将此功能添加到自定义无光照着色器，请按照以下步骤操作。

1. 将属性 `_MainTex` 以及对此属性的所有引用重命名为 `_BaseMap`。此操作会使着色器代码更接近于标准 URP 着色器规则。
2. 从 `_BaseMap` 属性中删除 `[NoScaleOffset]` ShaderLab 属性。此时，您可以在着色器的检视面板窗口中看到 **Tiling** 和 **Offset** 属性。
3. 将 `[MainTexture]` ShaderLab 属性添加到 `_BaseMap` 属性，将 `[MainColor]` 属性添加到 `_Color` 属性。此操作会告知编辑器从项目的另一部分或编辑器中请求主纹理或主颜色时要返回哪个属性。着色器的 `Properties` 部分现在应该如下所示：

```cpp
Properties
{
    [MainTexture] _BaseMap("Main Texture", 2D) = "white" {}
    [MainColor] _Color("Color", Color) = (1,1,1,1)
}
```
4. 在 `CBUFFER` 代码块上方添加 `TEXTURE2D(_BaseMap)` 和 `SAMPLER(sampler_BaseMap)` 宏。这些宏定义了纹理和采样器状态变量以供后续使用。有关采样器状态的更多信息，请参阅[使用采样器状态](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-SamplerStates.html)。

```cpp
TEXTURE2D(_BaseMap);
SAMPLER(sampler_BaseMap);
```
5. 将 `CBUFFER` 代码块中的 `sampler2D _BaseMap` 变量更改为 `float4 _BaseMap_ST`。此变量现在存储了检视面板中设置的平铺和偏移值。

```cpp
CBUFFER_START(UnityPerMaterial)
float4 _Color;
float4 _BaseMap_ST;
CBUFFER_END
```
6. 更改 `frag` 函数可使用宏访问纹理而不是直接使用 `tex2D`。为此，请将 `tex2D` 替换为 `SAMPLE_TEXTURE2D` 宏，并将 `sampler_BaseMap` 添加为附加参数，如下所示：

```cpp
half4 frag(Varyings IN) : SV_Target
{
    half4 texel = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, IN.uv);
    return texel * _Color;
}
```
7. 在 `vert` 函数中，将 `OUT.uv` 更改为使用宏，而不是直接将纹理坐标作为 `IN.uv` 进行传递。为此，请将 `IN.uv` 替换为 `TRANSFORM_TEX(IN.uv, _BaseMap)`。`vert` 函数现在应该如下所示：

```cpp
Varyings vert(Attributes IN)
{
    Varyings OUT;

    OUT.positionHCS = TransformObjectToHClip(IN.positionOS.xyz);
    OUT.uv = TRANSFORM_TEX(IN.uv, _BaseMap);

    return OUT;
}
```

   **注意**：在 `CBUFFER` 代码块之后定义 `vert` 函数非常重要，因为 `TRANSFORM_TEX` 宏使用带有 `_ST` 后缀的参数。

此着色器现在具有经过颜色修改的纹理，并与 SRP Batcher 完全兼容。它还完全支持 **Tiling** 和 **Offset** 属性。

要查看完整着色器代码的示例，请参阅本页的部分。

## 完整着色器代码

```
Shader "Custom/UnlitShader"
{
    Properties
    {
        _BaseMap("Base Map", 2D) = "white" {}
        _Color("Color", Color) = (1,1,1,1)
    }

    SubShader
    {
        Tags { "RenderType" = "Opaque" "RenderPipeline" = "UniversalPipeline" }

        Pass
        {
            HLSLPROGRAM

            #pragma vertex vert
            #pragma fragment frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            struct Attributes
            {
                float4 positionOS   : POSITION;
                float2 uv: TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionCS  : SV_POSITION;
                float2 uv: TEXCOORD0;
            };

            TEXTURE2D(_BaseMap);
            SAMPLER(sampler_BaseMap);

            CBUFFER_START(UnityPerMaterial)
            float4 _Color;
            float4 _BaseMap_ST;
            CBUFFER_END

            Varyings vert(Attributes IN)
            {
                Varyings OUT;

                OUT.positionCS = TransformObjectToHClip(IN.positionOS.xyz);
                OUT.uv = TRANSFORM_TEX(IN.uv, _BaseMap);

                return OUT;
            }

            half4 frag(Varyings IN) : SV_Target
            {
                float4 texel = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, IN.uv);
                return texel * _Color;
            }
            ENDHLSL
        }
    }
}
```

---

## 文档导航

- 上一页：[[03-将内置渲染管线的资源和质量级别转换为 URP]]
- 目录：[[00-从内置渲染管线升级到 URP]]
- 下一页：[[05-将质量设置从内置渲染管线转换到 URP。]]
