# 第 03 课 · clamp：把数值限制在范围内

> 学习目标：使用 `clamp()` 将数值限制在范围内。

颜色的每个通道必须在 0.0 到 1.0 之间，超出范围的值会被 GPU 自动截断。但「自动截断」是被动的、不可控的；`clamp` 函数让我们**主动、显式地**把值限制在指定范围内，从而精确控制渐变从哪里开始、到哪里结束。

---

## 1. 完整代码

```hlsl
Shader "Lesson/03_ClampGradient"
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
                // 先缩放偏移，再用 clamp 限制在 0~1
                float brightness = clamp(IN.uv.x * 1.6 - 0.3, 0.0, 1.0);
                return half4(brightness, brightness, brightness, 1);
            }
            ENDHLSL
        }
    }
}
```

跑起来步骤同前：建 `.shader` → 建材质 → Shader 下拉框选 `Lesson → 03_ClampGradient` → 拖到 Cube 上。你会看到一个**中间有渐变、左右两边是纯黑和纯白「平台」**的效果。

---

## 2. clamp 是什么

`clamp(x, min, max)` 把 `x` 限制在 `[min, max]` 范围内：

- `x < min` → 返回 `min`
- `x > max` → 返回 `max`
- 否则 → 返回 `x` 本身

```hlsl
float brightness = clamp(IN.uv.x * 1.6 - 0.3, 0.0, 1.0);
```

这行先把 `IN.uv.x` 缩放偏移，让渐变只发生在画面中间部分，再用 `clamp` 确保值不超界。

---

## 3. 不用 clamp 会发生什么

`IN.uv.x * 1.6 - 0.3` 的范围是 **-0.3 到 1.3**，超出了颜色的 0~1 范围：

- 左侧约 20% 会是负数 → GPU 自动截断到 0（出现一片纯黑的「平台」）
- 右侧约 20% 超过 1 → GPU 自动截断到 1（出现一片纯白的「平台」）

> 准确说：`x * 1.6 - 0.3` 要到 x = 0.1875 处才由负转正，所以左侧约 18.75% 是黑的；右侧同样约 18.75% 是白的。

有趣的是：**即使不写 `clamp`，颜色也不会「爆掉」**——因为 GPU 在把颜色写进画面时，会强制把小于 0 的截成 0、大于 1 的截成 1（这叫做 **clipping / 截断**）。那为什么还要 `clamp`？因为「自动截断」是写死的、只能截在 0 和 1；而 `clamp` 让你**主动声明边界**，还能截在任意范围（比如 `0.2 ~ 0.8`），代码意图也更清楚。

加上 `clamp` 之后，边界处的值被明确控制，渐变在特定位置开始和结束。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 渐变更陡、过渡区更窄（更接近「硬切」） | 把 `1.6` 改成 `3.0` |
| 左侧黑色平台更宽 | 把 `-0.3` 改成 `-0.6` |
| 变成竖直方向 | 把 `IN.uv.x` 改成 `IN.uv.y` |
| 只保留红色 | `return half4(brightness, 0.0, 0.0, 1.0);` |

---

## 5. 练习

练习代码里 `brightness = 0.0`（全黑）。用 `clamp(IN.uv.x * 1.6 - 0.3, 0.0, 1.0)` 计算 `brightness`，观察渐变的起始和结束位置。

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
float brightness = clamp(IN.uv.x * 1.6 - 0.3, 0.0, 1.0);
```

- `IN.uv.x * 1.6 - 0.3`：缩放因子 1.6 让渐变更陡，偏移 -0.3 让它稍微往左移。
- `clamp(..., 0.0, 1.0)` 把小于 0 的值拉回 0（左侧纯深色），把大于 1 的值压到 1（右侧纯亮色）。

进阶：把 `1.6` 改成 `3.0`，渐变过渡区域会变得更窄，更像 `step`。

---

## 6. 【小灶解析】专家补充

### ① 截断（Clipping）是自动发生的

把颜色写进画面（Render Target）时，硬件会把小于 0 的通道截成 0、大于 1 的截成 1——这是「写死」的硬件行为，不是可选项。所以本课第 3 节里「不写 clamp 也不会爆掉」。但**「不爆掉」≠「可控」**：自动截断只能截在 0 和 1，而 clamp 能截在任意区间（如 `clamp(x, 0.2, 0.8)`）。TA 写 Shader 时倾向于显式 clamp，把「这里会发生什么」讲清楚。

### ② clamp 与 saturate 的关系

`clamp(x, 0, 1)` 就是 `saturate(x)`。第 02 课径向渐变里我们用的 `saturate`，本质就是「把值夹回 0~1」的特例。什么时候用哪个？**只需要 0~1 就用 `saturate`（更简洁），需要自定义范围就用 `clamp`**。

### ③ 「缩放 + 偏移」是 Shader 里最常用的数学手法

本课那行 `IN.uv.x * 1.6 - 0.3`，本质是直线公式 `y = kx + b`：

- `k`（这里 1.6）控制**坡度**——越大越陡；
- `b`（这里 -0.3）控制**平移**——让曲线左右移动。

把 UV 的 0~1 重新映射到任意区间、把渐变精确放到任何位置、任何宽度，靠的全是这一招。建议你反复调 `k` 和 `b`，直觉建立起来后，后面 90% 的 Shader 数学都会顺手。

### ④ clamp 的两个「兄弟」：step 与 smoothstep

- `step(edge, x)`：`x < edge` 返回 0，否则返回 1——**硬切**，没有渐变过渡。
- `smoothstep(a, b, x)`：在 `[a, b]` 之间做平滑过渡——**软切**。

你刚才把 `1.6` 改成 `3.0` 时，过渡区被压得越来越窄、越来越「硬」，正是朝着 `step` 的方向走。理解了 clamp / step / smoothstep 这三件套，你就掌握了「控制数值区间」的全部基本工具。
