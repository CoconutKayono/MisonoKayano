# 第 47 课 · 卡通渲染 (Toon Shading)

> 学习目标：用 if-else 把连续光照切成固定色阶，结合轮廓线，实现完整的卡通渲染。

卡通渲染（NPR，非真实感渲染）：把连续明暗量化成几个固定档位，再加一条轮廓线，模拟漫画/动画风格。

---

## 1. 完整代码

```hlsl
Shader "Lesson/47_ToonShading"
{
    SubShader
    {
        Tags
        {
            "RenderType" = "Opaque"
            "RenderPipeline" = "UniversalPipeline"
        }

        Pass
        {
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
            };

            struct Varyings
            {
                float4 positionHCS : SV_POSITION;
                float3 normalWS : TEXCOORD0;
                float3 positionWS : TEXCOORD1;
            };

            Varyings vert (Attributes IN)
            {
                Varyings OUT;
                OUT.positionHCS = TransformObjectToHClip(IN.positionOS.xyz);
                OUT.normalWS = TransformObjectToWorldNormal(IN.normalOS);
                OUT.positionWS = TransformObjectToWorld(IN.positionOS.xyz);
                return OUT;
            }

            half4 frag (Varyings IN) : SV_Target
            {
                float3 normal = normalize(IN.normalWS);
                float3 viewDir = normalize(GetCameraPositionWS() - IN.positionWS);

                // 光源随时间旋转
                float3 lightDir = normalize(float3(cos(_Time.y * 0.5), sin(_Time.y * 0.5), 0.5));

                // —— 卡通分级（4 档）——
                float3 objectColor = float3(0.85, 0.55, 0.4);
                float intensity = dot(normal, lightDir);
                float3 color;
                if (intensity > 0.75)      color = objectColor * 1.0;
                else if (intensity > 0.45) color = objectColor * 0.7;
                else if (intensity > 0.2)  color = objectColor * 0.45;
                else                       color = objectColor * 0.25;

                // —— 轮廓线 ——
                float outlineThickness = 0.12;
                float edgeFactor = 1.0 - dot(normal, viewDir);
                float outlineMask = smoothstep(0.0, outlineThickness, edgeFactor);
                color = lerp(color, float3(0.0, 0.0, 0.0), outlineMask * 0.8);

                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

场景准备同第 31 课。球体光影分成几个硬朗色阶，边缘有一圈黑边，光源随时间旋转、阴影边界「跳变」。

---

## 2. 卡通分级是什么

```hlsl
float intensity = dot(normal, lightDir);
if (intensity > 0.75)      color = objectColor * 1.0;
else if (intensity > 0.45) color = objectColor * 0.7;
else if (intensity > 0.2)  color = objectColor * 0.45;
else                       color = objectColor * 0.25;
```

普通光照是连续渐变的；卡通渲染把连续值「量化」成固定档位（0.25 / 0.45 / 0.7 / 1.0）。阈值之间没有平滑过渡，边界是「跳」过去的——这就是卡通感的关键。

---

## 3. 轮廓线怎么实现

```hlsl
float edgeFactor = 1.0 - dot(normal, viewDir);
float outlineMask = smoothstep(0.0, outlineThickness, edgeFactor);
color = lerp(color, float3(0.0, 0.0, 0.0), outlineMask * 0.8);
```

球体边缘处法线和视线垂直，`dot(normal, viewDir)` 接近 0，`edgeFactor` 接近 1。`smoothstep` 把它转成 0~1 的遮罩，`outlineThickness` 控制轮廓粗细，`lerp` 把轮廓区混成黑色。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 阴影更粗糙（3 档） | 删掉一个 `else if`，只剩三档 |
| 轮廓线变细 | `outlineThickness` 从 `0.12` 改成 `0.2` |
| 轮廓线变全黑 | `outlineMask * 0.8` 改成 `outlineMask * 1.0` |

---

## 5. 练习

练习区的分级和轮廓已设好、可运行。把 4 档亮度系数（1.0, 0.7, 0.45, 0.25）改成（1.0, 0.6, 0.3, 0.1），观察阴影对比度的变化。

### 答案解析

`intensity = dot(normal, lightDir)` 按阈值分级：高于 0.75 最亮，低于 0.2 最暗。改成（1.0, 0.6, 0.3, 0.1）后，暗部更暗、对比更强。轮廓线 `outlineThickness` 越大黑边越粗。

试着把最低档系数从 0.25 改成 0.0，看阴影区会不会变成完全的黑。

---

## 6. 【小灶解析】专家补充

### ① if-else 与 floor 是同一件事

第 36 课用 `floor(x * N) / (N-1)` 做分级，本课用 if-else 做分级——**结果相同**。if-else 的优势是每档可以设任意阈值、任意颜色（不要求等距）；floor 的优势是紧凑、改档位数只改一个数字。两种写法都要会。

### ② 轮廓线其实是「边缘光反过来用」

本课的 `edgeFactor = 1 - dot(normal, viewDir)` 和第 34 课边缘光一模一样，只是这里把它混成**黑色**（描边）而不是白色（发光）。同一根公式，正反两种用法。

### ③ 完整的 NPR 工具箱

Toon Shading 只是 NPR 的入门：色阶、描边、轮廓光、假阴影（第 35 课）都是 NPR 的常用零件。游戏里的《塞尔达》《无主之地》风格，本质就是这些零件的排列组合。你已经把 NPR 的地基都摸了一遍。
