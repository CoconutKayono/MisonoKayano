# 第 68 课 · Smoothstep 基础

> 学习目标：用 `smoothstep` 的 S 形曲线把距离变成遮罩，做出柔边竖带。

核心是这两行——用 S 形曲线把一个距离值变成一个遮罩：

```hlsl
float distanceToCenter = abs(IN.uv.x - 0.5);
float bandMask = 1.0 - smoothstep(0.0, 0.25, distanceToCenter);
```

---

## 1. 完整代码

```hlsl
Shader "Lesson/68_SmoothstepBand"
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
                float distanceToCenter = abs(IN.uv.x - 0.5);
                float bandMask = 1.0 - smoothstep(0.0, 0.25, distanceToCenter);

                return half4(float3(bandMask, bandMask, bandMask), 1);
            }
            ENDHLSL
        }
    }
}
```

画面是一条中间白、两侧黑的柔边竖带。

---

## 2. step 和 smoothstep 的区别

`step(edge, x)` 是硬切换：x 小于 edge 返回 0，否则返回 1，边缘是一条锐利的线。`smoothstep(edge0, edge1, x)` 是 S 形过渡：在 edge0 到 edge1 之间平滑地从 0 变到 1，边缘柔和。

类比：`step` 是电灯开关，一按瞬间亮灭；`smoothstep` 是调光器，从暗慢慢过渡到亮。

---

## 3. 这段代码做了什么

`abs(IN.uv.x - 0.5)` 计算每个像素到画面中线（0.5）的距离：中线处 0（最近）、边缘处 0.5（最远）。`smoothstep(0.0, 0.25, distanceToCenter)` 把距离映射成 0~1：距离 0 → 输出 0（最亮），距离 0.25 → 输出 1（最暗）。最后 `1.0 - ...` 翻转，中间亮、两边暗，形成中间白色竖带。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 白带变窄、边缘更硬 | `0.25` 改成 `0.1` |
| 白带铺满、中间最亮 | `0.25` 改成 `0.5` |
| 变成水平白带 | `IN.uv.x - 0.5` 改成 `IN.uv.y - 0.5` |
| 中间黑、两边白 | 去掉 `1.0 -` |

---

## 5. 练习

练习代码里 `bandMask = 0.0`。改成正确表达式，让画面出现中间白、两侧黑的竖带。

### 答案解析

```hlsl
float distanceToCenter = abs(IN.uv.x - 0.5);
float bandMask = 1.0 - smoothstep(0.0, 0.25, distanceToCenter);
```

`abs(IN.uv.x - 0.5)` 算出像素到中线的水平距离（0~0.5）。`smoothstep(0.0, 0.25, distanceToCenter)` 把 0~0.25 的距离平滑映射成 0~1，超过 0.25 维持 1（全黑）。`1.0 -` 翻转后中心最亮、边缘最暗。起始 `bandMask = 0.0` 画面全黑。

试着把 `smoothstep` 第一个参数从 `0.0` 改成 `0.1`，看白带内侧出现渐变过渡的变化。

---

## 6. 【小灶解析】专家补充

### ① smoothstep 的两个阈值 = 过渡带

`edge0` 和 `edge1` 之间的距离就是「过渡带宽度」：两者越近边缘越硬，越远越柔和。**调柔边，就是调这两个阈值**。

### ② smoothstep 内置了抗锯齿

`smoothstep` 在过渡带里做平滑插值，天然消除 `step` 的锯齿。所以画形状时用 `smoothstep` 比 `step` 更「干净」。第 29 课专门讲过这个对比。

### ③ smoothstep 的曲线不是线性的

它用三次多项式 `3t² - 2t³` 平滑，起点和终点斜率为 0，视觉上过渡更自然。需要更「急」的过渡可以改用 `pow` 或手动构造曲线。
