# 第 105 课 · 二维 Value Noise

> 学习目标：实现 Value Noise——对四个格角的随机值做平滑插值，把马赛克变成连续斑块。

哈希格点噪声每格突变像马赛克。Value Noise 对相邻格点插值，让颜色平滑过渡。

---

## 1. 完整代码

```hlsl
Shader "Lesson/105_ValueNoise"
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

            float hash21(float2 coord)
            {
                float2 fractCoord = frac(coord * float2(123.34, 345.45));
                fractCoord += dot(fractCoord, fractCoord + 34.345);
                return frac(fractCoord.x * fractCoord.y);
            }

            float valueNoise(float2 coord)
            {
                float2 cell = floor(coord);
                float2 fracCoord = frac(coord);
                float2 smoothCoord = fracCoord * fracCoord * (3.0 - 2.0 * fracCoord);

                float cornerBottomLeft  = hash21(cell);
                float cornerBottomRight = hash21(cell + float2(1.0, 0.0));
                float cornerTopLeft     = hash21(cell + float2(0.0, 1.0));
                float cornerTopRight    = hash21(cell + float2(1.0, 1.0));

                return lerp(lerp(cornerBottomLeft, cornerBottomRight, smoothCoord.x),
                            lerp(cornerTopLeft, cornerTopRight, smoothCoord.x),
                            smoothCoord.y);
            }

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
                float noiseValue = valueNoise(IN.uv * 8.0);
                float3 color = float3(noiseValue, noiseValue, noiseValue);
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

画面是平滑连续的灰度斑块，比第 95 课的马赛克柔和得多。

---

## 2. 取四个角的随机值

坐标拆成整数 `cell` 和小数 `fracCoord`：`cell` 代表在哪个格子，`fracCoord` 代表格子内的位置（0~1）。然后取四个角的哈希值：左下、右下、左上、右上。

---

## 3. 平滑插值

直接用 `fracCoord` 插值是线性的，格点边界会有棱角。用「平滑阶梯」曲线代替：

```hlsl
float2 smoothCoord = fracCoord * fracCoord * (3.0 - 2.0 * fracCoord);
```

这条曲线在 0 和 1 处斜率为零——格点边界两侧切线相同，过渡自然无折痕。然后用 `lerp` 沿 X、Y 各插一次，就是双线性插值。

---

## 4. `f*f*(3-2f)` 就是 smoothstep

这个多项式其实是 `smoothstep(0, 1, f)` 的等价形式，两处斜率都为零。用它而不是 `smoothstep`，代码更直白地表明「我在做平滑插值」。

---

## 5. 试着改一改

| 效果 | 写法 |
|------|------|
| 噪声更大块像山丘 | `8.0` 改成 `2.0` |
| 噪声更细腻像烟雾 | `8.0` 改成 `32.0` |
| 回到线性插值、出现棱角 | `smoothCoord` 改成 `fracCoord` |
| 暖色调噪声 | 输出 `float3(n, n*0.8, n*0.6)` |

---

## 6. 练习

练习代码里 `noiseValue = 0.0`。调用 `valueNoise(IN.uv * 8.0)` 输出灰度。

### 答案解析

```hlsl
float noiseValue = valueNoise(IN.uv * 8.0);
float3 color = float3(noiseValue, noiseValue, noiseValue);
```

`IN.uv * 8.0` 放大坐标控制噪声粗细；`valueNoise(...)` 对四个格角插值，返回平滑 0~1 灰度。每个像素根据自己在格子内的位置得到插值结果，画面就是平滑流动的噪声。

试着把 8.0 换成 4.0，看噪声是否更大更柔和。

---

## 7. 【小灶解析】专家补充

### ① Value Noise 是「噪声家族的地基」

它是所有后续噪声（FBM、云、大理石）的底层积木。**理解它的两步——「格点随机值 + 双线性平滑插值」**，整个噪声模块就通了。

### ② `f*f*(3-2f)` 是历史悠久的技巧

这个多项式比 `smoothstep` 更早在图形学界流行，因为显式、快速、可移植。**知道它等价于 smoothstep**，读别人的 shader 时就不会被「奇怪的多项式」吓到。

### ③ 双线性插值 = 两次线性插值

「先在 X 方向插两次，再在 Y 方向插一次」就是双线性插值。这是图像缩放、纹理采样、噪声平滑共用的核心算法。**Value Noise 的本质，就是把 hash 格点值用双线性插值「磨平」。**
