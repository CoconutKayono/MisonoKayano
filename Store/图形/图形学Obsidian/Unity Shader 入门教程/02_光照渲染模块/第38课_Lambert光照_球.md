# 第 38 课 · Lambert 光照（球）

> 学习目标：在真实球体上实现最基础的 Lambert 漫反射，理解「法线点乘光方向」的几何意义。

漫反射是最简单的光照模型，模拟粗糙表面把光均匀散射到各方向。你看到的木头、石头、布料，大部分都是这种反光。

---

## 1. 完整代码

```hlsl
Shader "Lesson/38_LambertSphere"
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
                float3 normalOS : NORMAL;
            };

            struct Varyings
            {
                float4 positionHCS : SV_POSITION;
                float3 normalWS : TEXCOORD0;
                float3 positionWS : TEXCOORD1;
            };

            Varyings vert (Attributes IN)
            {
                Varyings OUT;
                OUT.positionHCS = TransformObjectToHClip(IN.positionOS.xyz);
                OUT.normalWS = TransformObjectToWorldNormal(IN.normalOS);
                OUT.positionWS = TransformObjectToWorld(IN.positionOS.xyz);
                return OUT;
            }

            half4 frag (Varyings IN) : SV_Target
            {
                float3 normal = normalize(IN.normalWS);
                float3 lightDir = normalize(float3(-0.4, 0.6, 0.7));

                float3 baseColor = float3(0.6, 0.8, 0.35);
                float diffuse = max(dot(normal, lightDir), 0.0);
                float3 color = baseColor * (0.15 + 0.85 * diffuse);
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

场景准备同第 31 课。球体正对光的地方最亮，侧面变暗，背对光的地方只剩 15% 底色。

---

## 2. `dot(normal, lightDir)` 是什么意思

```hlsl
float diffuse = max(dot(normal, lightDir), 0.0);
```

`dot(normal, lightDir)` 计算法线方向和光线方向有多对齐：

- 完全一致（法线正对光源）→ 1.0（100% 亮度）
- 垂直（法线与光线成 90°）→ 0.0（0%）
- 背向光源 → 负数，`max(..., 0.0)` 截断成 0

这就是「余弦定律」：表面受光量正比于入射角的余弦。

---

## 3. 亮度合成

```hlsl
float3 color = baseColor * (0.15 + 0.85 * diffuse);
```

`0.15` 是底色（防止完全黑透），`0.85 * diffuse` 是光照强度。两者加起来，亮部接近 100%、暗部保留 15% 的基础亮度——这正是第 31 课「环境光 + 漫反射」的另一种写法。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 暗部更亮、对比降低 | `0.15` 改成 `0.4` |
| 亮部过曝、高光区变白 | `0.85` 改成 `1.5` |
| 光源从左移到右 | `lightDir` 的 x 从 `-0.4` 改成 `0.8` |

---

## 5. 练习

练习代码里 `diffuse = 0.0`，球体只有暗底色。补全 TODO，计算正确的漫反射值让球体出现明暗渐变。

### 答案解析

```hlsl
float diffuse = max(dot(normal, lightDir), 0.0);
```

初始状态 `diffuse = 0.0`，球体只有 `baseColor * 0.15` 的暗底色，是一团深色圆。改成 `max(dot(normal, lightDir), 0.0)` 后，法线和光方向越对齐 `diffuse` 越接近 1.0，对应像素越亮。

试着把 `max(dot(normal, lightDir), 0.0)` 改成 `dot(normal, lightDir) * 0.5 + 0.5`，看暗部会发生什么变化（这就是第 32 课的 Half-Lambert）。

---

## 6. 【小灶解析】专家补充

### ① Lambert 是光照的地基

Lambert 模型假设表面是「理想漫反射体」——光打上去被均匀散射到所有方向，所以从任何角度看亮度都一样。它是几乎所有光照模型的底层项：Phong、Blinn-Phong、PBR 都包含这一项。**把 `dot(normal, lightDir)` 吃透，光照就入门了**。

### ② 真实引擎里的 Lambert

Unity 的 URP Lit shader 里，漫反射项等价于 `NdotL * 光照颜色 * 衰减`——比本课多了「光照颜色」和「衰减」两个因子（第 37、46 课会覆盖）。本课是它的最小内核。

### ③ `0.15 + 0.85 * diffuse` 是一套「手感公式」

`0.15` 是美术手动留的暗部亮度，`0.85` 控制亮部强度。真实引擎里这些叫「环境光强度」「漫反射强度」材质参数。你会逐渐发现：**光照公式的「手感」往往就在这几个系数的配比里**。
