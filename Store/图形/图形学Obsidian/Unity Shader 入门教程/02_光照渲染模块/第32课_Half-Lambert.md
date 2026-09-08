# 第 32 课 · Half-Lambert

> 学习目标：用 Half-Lambert 让背光面也保留一定亮度，理解「映射范围」这个技巧。

标准 Lambert 背光面全黑；Half-Lambert 把 `dot(normal, lightDir)` 的 [-1, 1] 压缩到 [0, 1]，暗部不再死黑。

---

## 1. 完整代码

```c
Shader "Lesson/32_HalfLambert"
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

                float3 baseColor = float3(0.35, 0.6, 0.9);
                float diffuse = dot(normal, lightDir) * 0.5 + 0.5;   // Half-Lambert

                float3 color = baseColor * diffuse;
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

场景准备同第 31 课。球体背光面不再全黑，整体更柔和、更有立体感。

---

## 2. 标准 Lambert 的问题

标准 Lambert 用 `max(dot(normal, lightDir), 0.0)`，背光面直接截断为 0，整片漆黑。在游戏和卡通渲染里，这个效果看起来太死，背光区域失去所有细节。

---

## 3. Half-Lambert 怎么改

```hlsl
float diffuse = dot(normal, lightDir) * 0.5 + 0.5;
```

把 `dot(normal, lightDir)` 的范围从 [-1, 1] 压缩到 [0, 1]：

- 正对光（dot = 1.0）→ `1.0 * 0.5 + 0.5 = 1.0`（100%，最亮）
- 垂直光（dot = 0.0）→ `0.0 * 0.5 + 0.5 = 0.5`（50%，中等）
- 背对光（dot = -1.0）→ `-1.0 * 0.5 + 0.5 = 0.0`（0%，最暗）

暗部不再完全黑，立体感更柔和。这个技巧最早来自《半条命》的美术团队，因此得名 Half-Lambert。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 暗部更亮、对比更低 | `* 0.5 + 0.5` 改成 `* 0.4 + 0.6` |
| 更接近标准 Lambert | `* 0.5 + 0.5` 改成 `* 0.8 + 0.2` |
| 拉高对比度 | 在外面套 `pow(diffuse, 2.0)`，只有正对光区域很亮 |

---

## 5. 练习

练习代码里 `diffuse = 0.0`，球体全黑。用 Half-Lambert 公式补全 TODO，算出正确的漫反射亮度。

### 答案解析

```hlsl
float diffuse = dot(normal, lightDir) * 0.5 + 0.5;
```

初始状态 `diffuse = 0.0` 球体一片黑。去掉 `max`，直接用 `dot(normal, lightDir) * 0.5 + 0.5`，把 [-1, 1] 映射到 [0, 1]，背光面也能保留亮度。

试着把系数从 `0.5 + 0.5` 改成 `0.6 + 0.4`，看看暗部会不会更亮。

---

## 6. 【小灶解析】专家补充

### ① Half-Lambert 的出处

这个技巧由 Valve 在《半条命》（Half-Life）里推广开——因此得名 Half-Lambert。它和「卡通/手游」风格的柔和光影高度契合，是游戏美术里最常用的漫反射变体之一。

### ② 本质：一次线性映射

`x * 0.5 + 0.5` 就是数学里的「把 [-1,1] 线性映射到 [0,1]」。同一招你在法线可视化（第 33 课 `normal * 0.5 + 0.5`）还会再见。**记住这个「缩放 + 平移」的映射套路，它是 Shader 里最通用的操作之一**。

### ③ 和「环境光」的区别

第 31 课的环境光是把一个**常数**加到结果上（`ambient + diffuse`）；Half-Lambert 是把**输入范围**压缩再输出。前者是「加法兜底」，后者是「改变曲线形状」。两种都能让暗部变亮，但手感不同：环境光让暗部是一个均匀的底，Half-Lambert 让暗部保留原有的明暗梯度。
