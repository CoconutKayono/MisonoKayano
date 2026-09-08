# 第 73 课 · SDF 矩形

> 学习目标：用有符号距离场（SDF）计算每个像素到矩形边界的距离，画出带柔边的矩形。

矩形的 SDF 用几行代码算距离：

```hlsl
float sdBox(float2 point, float2 halfSize)
{
    float2 distanceComponents = abs(point) - halfSize;
    return length(max(distanceComponents, float2(0.0, 0.0)))
         + min(max(distanceComponents.x, distanceComponents.y), 0.0);
}
```

---

## 1. 完整代码

```hlsl
Shader "Lesson/73_SdfBox"
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

            float sdBox(float2 point, float2 halfSize)
            {
                float2 distanceComponents = abs(point) - halfSize;
                return length(max(distanceComponents, float2(0.0, 0.0)))
                     + min(max(distanceComponents.x, distanceComponents.y), 0.0);
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
                float distanceToBox = sdBox(centeredUV, float2(0.2, 0.12));
                float boxMask = 1.0 - smoothstep(0.0, 0.01, distanceToBox);

                return half4(float3(boxMask, boxMask, boxMask), 1);
            }
            ENDHLSL
        }
    }
}
```

画面是一个带 0.01 柔边的白色矩形。

---

## 2. 什么是 SDF

SDF（Signed Distance Field，有符号距离场）给每个像素一个距离值：负值在形状内部、0 正好在边界、正值在外部。知道距离后，一个 `smoothstep` 就能画出带柔软边缘的形状，不需要复杂的光栅化判断。

---

## 3. sdBox 的逻辑

`point` 是像素相对矩形中心的位置，`halfSize` 是半宽/半高（`float2(0.2, 0.12)` 表示宽 0.4、高 0.24）。`abs(point) - halfSize` 利用对称性只看第一象限：结果为负说明 x 或 y 分量在矩形内，为正说明超出。`length(max(d, 0))` 算外部角落区域的距离，`min(max(d.x, d.y), 0)` 算内部和外侧边的贡献，两者相加得到完整 SDF 值。

---

## 4. 用 smoothstep 变成遮罩

`distanceToBox < 0`（内部）→ smoothstep 输出 0 → 遮罩 1（白）；`> 0.01`（外部）→ 遮罩 0（黑）；0~0.01 之间柔和过渡。`0.01` 是边缘柔化宽度，越小边缘越硬。

---

## 5. 试着改一改

| 效果 | 写法 |
|------|------|
| 正方形 | `float2(0.2, 0.12)` 改成 `float2(0.3, 0.3)` |
| 细长横条 | 改成 `float2(0.4, 0.05)` |
| 边缘更模糊 | `0.01` 改成 `0.05` |
| 边缘柔化更宽 | `smoothstep(0.0, 0.01, ...)` 改成 `smoothstep(-0.01, 0.01, ...)` |

---

## 6. 练习

练习代码里 `distanceToBox = 0.0`。调用 `sdBox(centeredUV, float2(0.2, 0.12))` 计算距离，让画面显示白色矩形。

### 答案解析

```hlsl
float distanceToBox = sdBox(centeredUV, float2(0.2, 0.12));
```

`centeredUV = IN.uv - 0.5` 把原点移到中心，`sdBox` 计算每个像素到半宽 0.2、半高 0.12 矩形的有符号距离。`1.0 - smoothstep(0.0, 0.01, distanceToBox)` 把负值（内部）转成 1、正值（外部）转成 0。起始 `distanceToBox = 0.0` 让全屏都被视为「恰在边界」。

试着把 `float2(0.2, 0.12)` 改成 `float2(0.1, 0.25)`，看竖条形状。

---

## 7. 【小灶解析】专家补充

### ① SDF 是「形状的数学描述」

SDF 用「到边界的距离」描述形状，比「在不在里面」信息更丰富——它还能知道「离边界多远」。这让形状的缩放、圆角、融合、描边都能用数学算出来。

### ② sdBox 公式要背下来

`abs(p) - b` + `length(max(d,0))` + `min(max(d.x,d.y),0)` 是矩形 SDF 的标准公式，业界通用。它和圆角矩形（第 74 课）、融合（第 75 课）直接相关，背下来以后到处用。

### ③ 距离函数的「远近」决定平滑

`max(distanceComponents, float2(0,0))` 里的 `max` 是「负数变 0」——内部点的贡献归零，只留外部距离。理解这个「正负分区」是看懂所有 SDF 的关键。
