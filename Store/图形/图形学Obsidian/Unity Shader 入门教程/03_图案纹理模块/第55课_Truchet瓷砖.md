# 第 55 课 · Truchet 瓷砖

> 学习目标：用 `hash21` 给每个格子生成随机数，决定瓷砖朝哪个方向翻转。

Truchet 瓷砖是经典的程序化图案：每个格子里放一个「L」形，随机选择它的旋转方向。

---

## 1. 完整代码

```hlsl
Shader "Lesson/55_TruchetTiles"
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

            // 把二维整数坐标映射成 0~1 的伪随机数
            float hash21(float2 coord)
            {
                float2 fractCoord = frac(float2(coord.x * 0.1031, coord.y * 0.1030));
                fractCoord += dot(fractCoord, float2(fractCoord.y + 19.19, fractCoord.x + 33.33));
                return frac(fractCoord.x * fractCoord.y);
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
                float tileCount = 8.0;
                float2 scaledUV = IN.uv * tileCount;
                float2 cellIndex = floor(scaledUV);   // 格子编号
                float2 localUV = frac(scaledUV) - 0.5; // 格内局部坐标，居中

                float randomValue = hash21(cellIndex); // 每个格子的随机值

                // 随机值 < 0.5 时，把局部坐标沿 x 翻转
                if (randomValue < 0.5)
                {
                    localUV.x = -localUV.x;
                }

                // 画 L 形：左侧一竖 + 顶部一横
                float leftBar = step(-0.5, localUV.x) * step(-0.5, localUV.y)
                              * step(localUV.x, -0.4) * step(localUV.y, 0.5);
                float topBar  = step(-0.5, localUV.x) * step(-0.5, localUV.y)
                              * step(localUV.x, 0.5)  * step(localUV.y, -0.4);

                float tileMask = max(leftBar, topBar);
                float3 color = lerp(float3(0.08, 0.08, 0.1), float3(0.9, 0.75, 0.4), tileMask);
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

画面是 8×8 的 Truchet 瓷砖，每个格子的 L 形朝向随机。

---

## 2. hash21：给每个格子一个随机数

```hlsl
float hash21(float2 coord)
{
    float2 fractCoord = frac(float2(coord.x * 0.1031, coord.y * 0.1030));
    fractCoord += dot(fractCoord, float2(fractCoord.y + 19.19, fractCoord.x + 33.33));
    return frac(fractCoord.x * fractCoord.y);
}
```

`hash21` 把任意整数坐标 `(x, y)` 映射成 0~1 的伪随机数：**同一个格子永远得到同一个值，不同格子得到不同值**。这个「确定性随机」是程序化纹理的关键——不用真正随机，只需看起来乱。

---

## 3. 用随机值决定朝向

```hlsl
float randomValue = hash21(cellIndex);
if (randomValue < 0.5)
{
    localUV.x = -localUV.x;
}
```

`cellIndex = floor(scaledUV)` 是格子编号，`hash21(cellIndex)` 得到该格子的随机值。随机值小于 0.5 时把局部坐标沿 x 翻转，相当于把 L 形镜像一下，形成两种朝向的随机组合。

---

## 4. 画 L 形

```hlsl
float leftBar = step(-0.5, localUV.x) * step(-0.5, localUV.y)
              * step(localUV.x, -0.4) * step(localUV.y, 0.5);
float topBar  = step(-0.5, localUV.x) * step(-0.5, localUV.y)
              * step(localUV.x, 0.5)  * step(localUV.y, -0.4);
```

`localUV` 居中后范围约 -0.5~0.5。`leftBar` 用四个 `step` 的乘积圈出「左侧竖条」，`topBar` 圈出「顶部横条」，`max(leftBar, topBar)` 合并成 L 形。

---

## 5. 试着改一改

| 效果 | 写法 |
|------|------|
| 格子变大 | `tileCount` 从 `8.0` 改成 `4.0` |
| L 形变粗 | `-0.4` 改成 `-0.3` |
| 翻转变旋转（更复杂） | `localUV.x = -localUV.x` 改成 `localUV = float2(localUV.y, -localUV.x)` |
| 换颜色 | `float3(0.9, 0.75, 0.4)` 换成其他颜色 |

---

## 6. 练习

练习代码里 `localUV` 翻转的那一行是 TODO。补全：当 `randomValue < 0.5` 时把 `localUV.x` 取反，让瓷砖随机翻转。

### 答案解析

```hlsl
if (randomValue < 0.5)
{
    localUV.x = -localUV.x;
}
```

`hash21(cellIndex)` 给每个格子一个稳定随机值，`localUV.x = -localUV.x` 沿竖轴镜像 L 形。没有翻转时所有 L 形朝向一致，图案单调；翻转后形成经典 Truchet 瓷砖的随机组合。

试着把「沿 x 翻转」改成「沿 y 翻转」（`localUV.y = -localUV.y`），图案会是另一种随机分布。

---

## 7. 【小灶解析】专家补充

### ① hash 是程序化纹理的「随机数种子」

真正随机每次刷新都不一样，画面会闪烁。`hash21` 把**坐标**当种子，同一个位置永远同一个结果，既「随机」又稳定。之后画波点、图案重复（第 58、62 课）都用它。

### ② floor 和 frac 再次成对出现

`cellIndex = floor(scaledUV)` 告诉我「第几个格子」，`localUV = frac(scaledUV) - 0.5` 告诉我「格子里哪个位置（且居中）」。这是所有「分格图案」的固定起手式。

### ③ Truchet 是「图案组合学」的起点

Truchet 瓷砖的本质：**每个格子只有有限种状态，随机选一种**。这种「格子 + 状态枚举 + 随机」的思路，能扩展出无数程序化图案，是 TA 做程序化材质的核心思维。
