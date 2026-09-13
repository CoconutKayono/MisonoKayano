# 第 28 课 · SDF 圆环

> 学习目标：理解有符号距离场（SDF）的基本思想，用它画一个带平滑边缘的圆环。

SDF（Signed Distance Field，有符号距离场）的核心是：**每个像素都存着「到形状边界的有符号距离」**。圆环的 SDF 是 `abs(length(centeredUV) - radius)`。

---

## 1. 完整代码

```hlsl
Shader "Lesson/28_SDFRing"
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
                float2 uv : TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionHCS : SV_POSITION;
                float2 uv : TEXCOORD0;
            };

            Varyings vert (Attributes IN)
            {
                Varyings OUT;
                OUT.positionHCS = TransformObjectToHClip(IN.positionOS.xyz);
                OUT.uv = IN.uv;
                return OUT;
            }

            half4 frag (Varyings IN) : SV_Target
            {
                float2 centeredUV = IN.uv - 0.5;

                float radius = 0.3;             // 圆环半径
                float thickness = 0.02;         // 圆环厚度（半宽）
                float edgeSmoothness = 0.006;   // 抗锯齿过渡宽度

                float distanceToRingEdge = abs(length(centeredUV) - radius);   // 到圆周的距离
                float ringMask = 1.0 - smoothstep(thickness, thickness + edgeSmoothness, distanceToRingEdge);
                return half4(ringMask, ringMask, ringMask, 1);
            }
            ENDHLSL
        }
    }
}
```

跑起来步骤同前，Shader 选 `Lesson → 28_SDFRing`。画面中央出现一个平滑的白色圆环。

---

## 2. 圆环的 SDF

```hlsl
float distanceToRingEdge = abs(length(centeredUV) - radius);
```

`length(centeredUV)` 是到中心的距离，减去 `radius` 后，圆周上为 0，向内向外都为正。再取 `abs`，得到「到圆周的**有符号距离**」。

---

## 3. 阈值化得到圆环

```hlsl
float ringMask = 1.0 - smoothstep(thickness, thickness + edgeSmoothness, distanceToRingEdge);
```

`distanceToRingEdge < thickness`（离圆周很近）时遮罩为 1，`> thickness + edgeSmoothness` 时为 0，中间平滑过渡——这就是一圈圆环。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 更粗的圆环 | 把 `thickness` 改成 `0.06` |
| 更小的圆环 | 把 `radius` 改成 `0.15` |
| 更柔和的边缘 | 把 `edgeSmoothness` 改成 `0.02` |
| 更硬的边缘 | 把 `edgeSmoothness` 改成 `0.002` |

---

## 5. 练习

练习代码里 `ringMask = 0.0`（全背景色）。用 SDF 计算圆环遮罩。

### 答案解析

```hlsl
float distanceToRingEdge = abs(length(centeredUV) - radius);
float ringMask = 1.0 - smoothstep(thickness, thickness + edgeSmoothness, distanceToRingEdge);
```

`abs(length(centeredUV) - radius)` 是圆环的 SDF：圆周上为 0，向内向外距离逐渐增大。`smoothstep(thickness, thickness + edgeSmoothness, ...)` 把这个距离场阈值化，`thickness` 控制粗细，`edgeSmoothness` 控制边缘柔度。

调整 `thickness = 0.06` 得到更粗的圆环，`radius = 0.15` 让圆更小，`edgeSmoothness = 0.02` 让边缘更柔和。

---

## 6. 【小灶解析】专家补充

### ① SDF 为什么「有符号」

普通距离永远是正的；SDF 的「有符号」指：点在形状**内部**是负、**外部**是正、**边界**是 0。圆环的 `abs(length(centeredUV) - radius)` 是「到边界的距离」但**不分内外**（取了绝对值），所以严格说它是「无符号的 SDF 变体」——但思想完全一致：**先算到边界的距离场，再阈值化**。

### ② SDF 是程序化图形的「通用语言」

圆、矩形、圆环、甚至任意多边形，都能写成一个 SDF 函数。有了 SDF，你就能：画出图形（阈值化）、给图形描边（abs + 阈值化）、做抗锯齿（smoothstep）、做布尔运算（max/min）。**SDF 是程序化绘制和字体渲染（如 TextMeshPro 的 SDF 字体）的核心技术**。

### ③ 本课与第 18 课是同一个东西

第 18 课《圆形描边》用的就是 `abs(distanceToCenter - radius)`，本课用 SDF 的框架重新组织了一遍。这不是重复——**同一个数学，一旦你意识到它叫 SDF，就打开了一整套成熟的技术生态**（布尔运算、平滑混合、Ray Marching 3D 建模）。概念升级，比多学一个新函数更重要。
