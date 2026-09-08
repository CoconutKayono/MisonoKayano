# 第 04 课 · pow：调整对比度

> 学习目标：用 `pow()` 调整对比度。

上一课我们能把渐变「限制」在某个范围（clamp）。这一课换个角度：**不改变范围，改变曲线的形状**。亮度默认是线性的（0 到 1 匀速前进），`pow(亮度, n)` 可以弯曲这条曲线，让渐变变快或变慢——视觉上就是对比度的变化。

---

## 1. 完整代码

```hlsl
Shader "Lesson/04_PowContrast"
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
                float brightness = pow(IN.uv.x, 2.0);   // ★ 对线性渐变做指数运算
                return half4(brightness, brightness, brightness, 1);
            }
            ENDHLSL
        }
    }
}
```

跑起来步骤同前，Shader 选 `Lesson → 04_PowContrast`。效果是：物体左边大部分是深色，靠近右边才迅速变亮——不再是第 02 课那种「均匀地从黑到白」。

---

## 2. pow 怎么改变曲线

`pow(x, n)` 对 0~1 的值做指数运算（就是 `x` 的 `n` 次方）：

- `n = 1.0`：原样，线性渐变
- `n = 2.0`：开头慢、结尾快（更多深色）
- `n = 0.5`：开头快、结尾慢（更多亮色）

```hlsl
float brightness = pow(IN.uv.x, 2.0);
```

`IN.uv.x` 是线性的 0→1。`pow(IN.uv.x, 2.0)` 等于 `IN.uv.x * IN.uv.x`，把这条直线压成一条「往下凹」的曲线：同样的距离里，浅色部分更少、深色更多。

直观理解：0.5 的平方是 0.25，所以 UV 走到一半（0.5）时，亮度才 0.25（只有四分之一）——前半段被压暗了；而 0.9 的平方是 0.81，越靠近 1 变化越快。

---

## 3. 试着改一改

改变指数 n，感受曲线的变化：

| n 值 | 代码 | 效果 |
|------|------|------|
| `0.5` | `pow(IN.uv.x, 0.5)` | 渐变偏亮 |
| `1.0` | `pow(IN.uv.x, 1.0)` | 线性（默认） |
| `2.0` | `pow(IN.uv.x, 2.0)` | 渐变偏暗 |
| `4.0` | `pow(IN.uv.x, 4.0)` | 明暗对比更强 |

---

## 4. 练习

练习代码里 `brightness = 0.0`（全黑）。用 `pow(IN.uv.x, 2.0)` 计算 `brightness`，看渐变曲线和线性有什么不同。

初始状态：

```hlsl
half4 frag (Varyings IN) : SV_Target
{
    float brightness = 0.0;             // 全黑
    return half4(brightness, brightness, brightness, 1);
}
```

### 答案解析

```hlsl
float brightness = pow(IN.uv.x, 2.0);
```

`pow(IN.uv.x, 2.0)` = `IN.uv.x * IN.uv.x`，把线性 0→1 压成二次曲线。视觉上，渐变的起始段颜色变化很慢，接近 1 的地方变化很快。

进阶：把指数从 2.0 改成 0.5（等于 `sqrt(IN.uv.x)`），曲线反过来——起始变化快、结尾变化慢。

---

## 5. 【小灶解析】专家补充

### ① pow 的数学本质：一条可以弯曲的「亮度曲线」

对 0~1 的 `x`：

- `n > 1`：曲线被**往下压**（0.5 → 0.25），整体偏暗；
- `n < 1`：曲线被**往上抬**（0.5 → 0.707），整体偏亮；
- `n = 1`：就是对角线，不变。

这条「曲线怎么弯」的直觉，是后面理解 gamma、颜色空间、光照衰减的通用工具。你其实已经掌握了一种「用幂函数重塑亮度分布」的通用手法。

### ② pow(x, 0.5) 就是 sqrt(x)

`pow(x, 0.5)` 数学上等于 `sqrt(x)`（开平方）。HLSL 里两种写法都行，语义完全一样。同理 `pow(x, 2.0)` 直接写 `x * x` 更省。所以记住：**整数次幂用连乘，0.5 次幂用 sqrt，一般次幂才用 pow**。

### ③ pow 与 gamma（伽马）——TA 必懂的颜色空间

显示器显示颜色时不是线性的，而是带一条约 2.2 的「gamma 曲线」。于是图形学里有两件天天要做的事：

- `pow(color, 1/2.2)` ≈ 把 sRGB 颜色**线性化**（转线性空间）
- `pow(color, 2.2)` ≈ 把线性颜色**伽马编码**（转回 sRGB）

Unity 里有个设置叫 **Color Space: Linear / Gamma**，背后就是这个 pow 在起作用。所以 pow 不只是「调对比度」，它是整个「颜色空间」话题的核心算子——这是 TA 和普通美术拉开差距的硬知识。

### ④ pow 的两个坑：负数和开销

- **负数**：`pow(-1.0, 0.5)` 在实数里无意义，GPU 上会得到 NaN（或未定义），污染后续计算。所以用 pow 前习惯先 `saturate`/`clamp` 保证输入在 0~1（或非负）。
- **开销**：pow 底层走的是指数/对数运算，比加减乘贵。能用连乘（n 是整数）或 sqrt（n=0.5）就别用通用 pow。

### ⑤ 「对比度」和「亮度分布」不是一回事

本课的 pow 其实是在调**明暗分布**（暗部多还是亮部多），而「对比度」通常指**明暗的跨度**——另一种常见做法是围绕中点拉伸：`(x - 0.5) * k + 0.5`（k>1 对比更强）。两者都能让画面「更有感觉」，但机制不同，将来做后处理或调色时会分别用到。
