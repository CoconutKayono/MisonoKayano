# 第 80 课 · SDF 形状融合

> 学习目标：把圆角矩形、圆形用 `smin` 融合，再分别绘制填充层和轮廓层，做成一个有机复合形状。

这是数学模块的综合课：SDF 形状、平滑最小值、填充与描边全部用上。

---

## 1. 完整代码

```hlsl
Shader "Lesson/80_SdfBlend"
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

            float sdRoundBox(float2 point, float2 halfSize, float cornerRadius)
            {
                float2 distanceComponents = abs(point) - halfSize;
                return length(max(distanceComponents, float2(0.0, 0.0))) - cornerRadius
                     + min(max(distanceComponents.x, distanceComponents.y), 0.0);
            }

            float sdCircle(float2 point, float radius)
            {
                return length(point) - radius;
            }

            float smin(float distanceA, float distanceB, float blendWidth)
            {
                float blendFactor = clamp(0.5 + 0.5 * (distanceB - distanceA) / blendWidth, 0.0, 1.0);
                return lerp(distanceB, distanceA, blendFactor)
                     - blendWidth * blendFactor * (1.0 - blendFactor);
            }

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

                float body = sdRoundBox(centeredUV + float2(0.05, 0.0), float2(0.18, 0.12), 0.08);
                float lobe = sdCircle(centeredUV - float2(0.14, 0.02), 0.16);
                float distanceField = smin(body, lobe, 0.16);

                float fill = 1.0 - smoothstep(0.0, 0.012, distanceField);
                float outline = 1.0 - smoothstep(0.018, 0.028, abs(distanceField));

                float3 backgroundColor = float3(0.05, 0.05, 0.08);
                float3 fillColor = float3(0.2, 0.6, 1.0);
                float3 outlineColor = float3(1.0, 1.0, 0.2);

                float3 color = backgroundColor;
                color = lerp(color, fillColor, fill);
                color = lerp(color, outlineColor, outline);
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

画面是一个蓝色填充、黄色描边的融合形状，像圆角矩形「长」出一个圆形突起。

---

## 2. 为什么不直接用 min

`min(a, b)` 硬取最小值——两个形状在交界处突然切换、边缘生硬。`smin(a, b, k)` 是平滑最小值：在形状接近区域距离场被「软化」，连接处自然圆润，像两团泥巴捏在一起。参数 k 控制融合柔软度，越大越圆润，趋近 0 退化成硬 min。

---

## 3. 形状的位置

两个形状都有偏移：`body` 用 `centeredUV + float2(0.05, 0)` 向左偏移（主体），`lobe` 用 `centeredUV - float2(0.14, 0.02)` 向右偏移（圆形突起）。偏移让两形状重叠，`smin` 在重叠区产生圆润融合。

---

## 4. 填充层和轮廓层

```hlsl
float fill = 1.0 - smoothstep(0.0, 0.012, distanceField);
float outline = 1.0 - smoothstep(0.018, 0.028, abs(distanceField));
```

融合后的 `distanceField` 既能做填充也能做轮廓：`fill` 在 d < 0（内部）亮；`outline` 用 `abs(d)` 对称检测边界——不管在里还是外，靠近 0 都有响应，形成一圈细细的描边。

---

## 5. 试着改一改

| 效果 | 写法 |
|------|------|
| 融合区变窄、接近硬边 | `smin` 的 `0.16` 改成 `0.04` |
| 突起变小 | `lobe` 半径 `0.16` 改成 `0.08` |
| 融合变硬切 | `smin` 换成 `min` |
| 轮廓变黄 | `outlineColor` 改成 `float3(1.0, 1.0, 0.2)`（默认已是黄） |

---

## 6. 练习

练习代码里 `distanceField = 0.0`、`fill = 0.0`、`outline = 0.0`。用 `smin` 融合两个形状，再用 `smoothstep` 构造填充层和轮廓层。

### 答案解析

```hlsl
float distanceField = smin(body, lobe, 0.16);
float fill = 1.0 - smoothstep(0.0, 0.012, distanceField);
float outline = 1.0 - smoothstep(0.018, 0.028, abs(distanceField));
```

`smin(body, lobe, 0.16)` 平滑合并两个距离场，融合宽度约 0.16。`fill` 用 `smoothstep(0.0, 0.012, d)` 做很窄的柔化，内部几乎全 1；`outline` 用 `abs(d)` 对称检测边界，产生一条宽约 0.01 的发光轮廓线。

试着把 `smin` 第三个参数从 `0.16` 改成 `0.3`，看融合区更大时形状的变化。

---

## 7. 【小灶解析】专家补充

### ① abs(d) 是「描边」的标准做法

填充看 `d < 0`，描边看 `abs(d) ≈ 0`。**`smoothstep` 套在 `abs(距离场)` 上**，就能在任何 SDF 形状外圈描一条等宽的边。UI 描边、角色勾线、发光边缘都靠它。

### ② 分层渲染：背景 → 填充 → 描边

本课的 `color` 三步走：先背景、再 `lerp` 进填充、再 `lerp` 进描边。**一层一层叠**，比一次算一个复杂颜色公式清晰得多。这是 shader 绘图的通用结构。

### ③ 恭喜完成数学模块

到这里，你已经掌握了 shader 的「核心数学积木」：`clamp`/`frac`/`lerp`/`smoothstep`/`remap`/`sin`/`atan2`、SDF 形状、旋转矩阵、平滑最小值。加上前面的基础入门、光照渲染、图案纹理，你已经具备独立写 2D 程序化 shader、以及理解 3D 光照的能力。下一步无论是做特效、后处理还是程序化材质，这些积木都会反复出现。
