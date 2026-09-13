# 第 67 课 · Sin/Cos 曲线

> 学习目标：用 `sin` 把坐标变成流动的波浪线，理解频率、振幅、相位。

`sin()` 能把一个值变成「来回摇摆」的运动，用在 y 坐标上就是波浪线。

---

## 1. 完整代码

```hlsl
Shader "Lesson/67_SineWave"
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
                float waveY = sin(IN.uv.x * 6.2831853 + _Time.y) * 0.25 + 0.5;

                float distanceToWave = abs(IN.uv.y - waveY);
                float lineMask = 1.0 - smoothstep(0.0, 0.01, distanceToWave);

                float3 backgroundColor = float3(0.04, 0.05, 0.09);
                float3 lineColor = float3(0.2, 0.6, 1.0);
                float3 color = lerp(backgroundColor, lineColor, lineMask);
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

画面是一条在画布上向左流动的蓝色波浪线。

---

## 2. sin 输出什么

`sin()` 返回值在 -1 到 +1 之间循环。直接当坐标会超出画布，所以要先缩放再偏移：

- `* 0.25`：把振幅从 ±1 压缩到 ±0.25，波浪不会碰到边缘
- `+ 0.5`：把中心线从 0 移到画布正中（UV 的 0.5）

---

## 3. 频率、相位各管什么

- `IN.uv.x * 6.2831853`：6.2831853 就是 2π，表示「一整圈」。uv.x 从 0 到 1 乘 2π，波形横向恰好完成一个完整周期。想更密就乘更大的数。
- `+ _Time.y`：`_Time.y` 是不断增大的秒数，加在 `sin` 参数里相当于每帧推动波形向左移动，形成动画。

---

## 4. 把 y 变成一条线

```hlsl
float distanceToWave = abs(IN.uv.y - waveY);
float lineMask = 1.0 - smoothstep(0.0, 0.01, distanceToWave);
```

用当前像素的 `IN.uv.y` 减去波形上的 y，取绝对值得到「到波浪线的距离」，再用 `smoothstep` 把距离映射成亮度：距离为 0 处最亮（白），远处为 0（背景色）。

---

## 5. 试着改一改

| 效果 | 写法 |
|------|------|
| 三个周期的密集波浪 | `6.2831853` 改成 `18.849`（6π） |
| 幅度增大、几乎触及上下边 | `0.25` 改成 `0.45` |
| 线条变粗、边缘模糊 | `0.01` 改成 `0.05` |
| 流速加快 | `_Time.y` 改成 `_Time.y * 3.0` |

---

## 6. 练习

练习代码里 `waveY = 0.5`。替换成正确的正弦波计算，让一条蓝色波浪线流动起来。

### 答案解析

```hlsl
float waveY = sin(IN.uv.x * 6.2831853 + _Time.y) * 0.25 + 0.5;
```

起始 `waveY = 0.5` 是一条固定水平线。`IN.uv.x * 6.2831853` 让波形横向走完一个完整周期，`+ _Time.y` 让相位随时间偏移形成流动，`* 0.25 + 0.5` 把 ±1 压缩并居中到画布中间区域。

试着把 `* 0.25` 改成 `* 0.48`，体验波峰几乎碰到画布顶部的极限感。

---

## 7. 【小灶解析】专家补充

### ① sin 的「三段式」套路

任何正弦波的形状都由三件事决定：**频率**（乘多大的数，决定密不密）、**振幅**（乘 0.25，决定高不高）、**相位/偏移**（加什么，决定移不移动）。记住频率、振幅、相位三个词，波形你就全会调了。

### ② sin 是「平滑循环」的 frac

`frac` 循环有硬跳变，`sin` 循环是平滑的 -1~1 来回摆。需要「柔和循环」就用 `sin`，需要「硬边重复」就用 `frac`。

### ③ 波形 + 距离 = 线条

「先算波形曲线上的 y，再算像素到它的距离，最后 smoothstep 上色」是画任意曲线（波浪、圆、贝塞尔）的通用方法。曲线本身只是「一个 y 关于 x 的函数」。
