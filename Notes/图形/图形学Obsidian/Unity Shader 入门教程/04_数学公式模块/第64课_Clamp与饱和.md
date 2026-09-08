# 第 64 课 · Clamp 与饱和

> 学习目标：用 `clamp` 把超出范围的值截断，理解「饱和」的含义。

核心就是这一行——把超出范围的值截断：

```hlsl
float clampedValue = clamp(IN.uv.x * 1.8 - 0.4, 0.0, 1.0);
```

---

## 1. 完整代码

```hlsl
Shader "Lesson/64_Clamp"
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
                float clampedValue = clamp(IN.uv.x * 1.8 - 0.4, 0.0, 1.0);
                return half4(float3(clampedValue, clampedValue, clampedValue), 1);
            }
            ENDHLSL
        }
    }
}
```

画面是一段两端「顶死」的渐变：左边纯黑、右边纯白、中间平滑过渡。

---

## 2. clamp 是什么

`clamp(x, min, max)` 把 x 限制在 min 到 max 之间，超出就截断：

- x 比 min 小，就返回 min
- x 比 max 大，就返回 max
- x 在中间，就原样返回

类比：音量旋钮最小 0%、最大 100%，拧过头也只停在 100%，不会再大。

---

## 3. 这段代码做了什么

`IN.uv.x * 1.8 - 0.4` 先对 x 坐标做线性变换——放大并左移，让渐变在画面偏左就开始、偏右就结束。没有 `clamp`，x 接近 1.0 时结果会超过 1.0（溢出变死白），x 接近 0.0 时结果为负（变死黑）。加上 `clamp(..., 0.0, 1.0)` 后，左边强制纯黑、右边强制纯白、中间平滑过渡。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 渐变区间变短，大部分非黑即白 | `1.8` 改成 `4.0` |
| 渐变从左边界开始 | `-0.4` 改成 `0.0` |
| 最亮只到 60%，无纯白 | 上限 `1.0` 改成 `0.6` |
| 最暗只到 30%，无纯黑 | 下限 `0.0` 改成 `0.3` |

---

## 5. 练习

练习代码里 `clampedValue = 0.0`。改成正确表达式，把 `IN.uv.x * 1.8 - 0.4` 限制在 0~1 之间。

### 答案解析

```hlsl
float clampedValue = clamp(IN.uv.x * 1.8 - 0.4, 0.0, 1.0);
```

`IN.uv.x * 1.8 - 0.4` 是线性变换，把 x 拉伸并左移，让过渡区间收缩在画面中部。加上 `clamp(..., 0.0, 1.0)` 后超出部分被截断，两端成为纯黑和纯白。起始 `clampedValue = 0.0` 画面全黑，替换后还原渐变。

试着把上限 `1.0` 改成 `0.7`，看高光端被截断后的变化。

---

## 6. 【小灶解析】专家补充

### ① HLSL 还有个 saturate

`clamp(x, 0.0, 1.0)` 太常用了，HLSL 专门给了个简写：**`saturate(x)`**，就是「夹到 0~1」。颜色计算里几乎每步都有人用 `saturate`，看到它要知道它等于 `clamp(x, 0, 1)`。

### ② clamp 防止「越界」的连锁灾难

颜色、亮度、混合比例这些值一旦超出 0~1，会引发死白、死黑、负光等诡异效果。**养成习惯：任何可能越界的值，进颜色前先 clamp/saturate**。这是写 shader 的基本卫生。

### ③ clamp 不只管颜色

`clamp` 也能限制坐标（防止采样越界）、限制速度、限制角度。它是「把数值约束在安全区」的通用工具，不只是颜色专用。
