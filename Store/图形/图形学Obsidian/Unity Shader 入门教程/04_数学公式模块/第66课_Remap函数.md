# 第 66 课 · Remap 函数

> 学习目标：实现 `remap` 辅助函数，把一个值从一个区间线性映射到另一个区间。

`remap` 把 `uv.x` 从 [0,1] 映射到 [-1,1]，再取绝对值，就能做出从边缘到中心的对称渐变。

---

## 1. 完整代码

```hlsl
Shader "Lesson/66_Remap"
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

            // 把 value 从 [inMin, inMax] 线性映射到 [outMin, outMax]
            float remap(float value, float inMin, float inMax, float outMin, float outMax)
            {
                float ratio = (value - inMin) / (inMax - inMin);
                return lerp(outMin, outMax, ratio);
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
                float remappedValue = remap(IN.uv.x, 0.0, 1.0, -1.0, 1.0);
                remappedValue = abs(remappedValue);

                float3 color = lerp(float3(0.2, 0.85, 1.0), float3(1.0, 0.25, 0.6), remappedValue);
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

画面是一个从中心蓝色向两侧粉色扩散的对称渐变。

---

## 2. remap 是什么

把一个已知范围内的值线性转换到新范围：

```hlsl
float remap(float value, float inMin, float inMax, float outMin, float outMax)
{
    float ratio = (value - inMin) / (inMax - inMin);
    return lerp(outMin, outMax, ratio);
}
```

第一行求出 value 在原区间里的比例（0%~100%），第二行把这个比例映射到目标区间。例如 `remap(0.25, 0, 1, -1, 1)`：0.25 在 [0,1] 里是 25%，放进 [-1,1] 就是 -0.5。

---

## 3. 取绝对值产生 V 形

`remap(IN.uv.x, 0.0, 1.0, -1.0, 1.0)` 把 x 从 [0,1] 变成 [-1,1]：左边缘 -1、中心 0、右边缘 +1。取 `abs` 后左右两边缘都变 1、中心变 0——一个从中心向两边增大的 V 形。

---

## 4. 用 lerp 上色

```hlsl
float3 color = lerp(float3(0.2, 0.85, 1.0), float3(1.0, 0.25, 0.6), remappedValue);
```

`remappedValue` 中心为 0、两边为 1，`lerp` 让中心是蓝色、两边是粉色，形成对称渐变。

---

## 5. 试着改一改

| 效果 | 写法 |
|------|------|
| 输出范围改为 0~2，中心变色但不达粉色 | `remap(IN.uv.x, 0,1, 0.0, 2.0)` |
| 不取绝对值，渐变不对称 | 删掉 `remappedValue = abs(remappedValue)` |
| 变纵向渐变 | `IN.uv.x` 改成 `IN.uv.y` |
| 换成暖色渐变 | 两个颜色改成橙→红 |

---

## 6. 练习

练习代码里 `remap` 函数已定义，但 `remappedValue` 还没算。用 `remap` 把 `IN.uv.x` 从 [0,1] 映射到 [-1,1] 再取绝对值。

### 答案解析

```hlsl
float remappedValue = remap(IN.uv.x, 0.0, 1.0, -1.0, 1.0);
remappedValue = abs(remappedValue);
```

`remap(IN.uv.x, 0,1, -1,1)` 把 x 从 [0,1] 线性拉伸到 [-1,1]。`abs` 把 [-1,0] 翻折到 [0,1]，左右对称：中心 0 是蓝色，两边 1 是粉色。起始 `remappedValue = 0.0` 画面全蓝。

试着把 `abs(remappedValue)` 改成 `remappedValue * remappedValue`，用平方代替绝对值，渐变曲线会不同。

---

## 7. 【小灶解析】专家补充

### ① remap 是「归一化公式」的封装

`remap` 里第一行 `(value - inMin) / (inMax - inMin)` 就是第 63 课的归一化公式。它把「映射到 [0,1]」和「lerp 到目标区间」两步合成了一个函数，复用率极高。

### ② 自己写工具函数是好习惯

`remap`、`hash21`、`smin` 这类小函数，写一次到处用。TA 的项目里都会积累一批自己的 shader 工具函数库。**看到重复三行的逻辑，就该抽成函数**。

### ③ abs 是「对称」的开关

`abs` 把负半轴翻到正半轴，任何「以中心为轴左右对称」的图案都可以用它：V 形渐变、对称光晕、对称波纹。配合 remap 把中心放到 0，效果最直观。
