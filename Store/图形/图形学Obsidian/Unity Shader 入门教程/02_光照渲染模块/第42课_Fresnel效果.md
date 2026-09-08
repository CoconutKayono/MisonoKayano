# 第 42 课 · Fresnel 效果

> 学习目标：理解菲涅尔效应，让球体边缘比中心更亮。

Fresnel 来自物理：视线以掠射角（接近水平）看向表面时，反射更强。着色器里用 `pow(1 - dot(normal, viewDir), n)` 模拟。

---

## 1. 完整代码

```hlsl
Shader "Lesson/42_Fresnel"
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
                float3 viewDir = normalize(GetCameraPositionWS() - IN.positionWS);

                float fresnelFactor = pow(1.0 - max(dot(normal, viewDir), 0.0), 5.0);

                float3 baseColor = float3(0.2, 0.35, 0.5);
                float3 color = baseColor * 0.2 + float3(1.0, 1.0, 1.0) * fresnelFactor;
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

场景准备同第 31 课。球体中心暗、边缘一圈发白亮光，像水面或玻璃的质感。

---

## 2. Fresnel 是什么

物理上，光线以较小角度（接近正面）射向水面时折射多、反射少；以较大角度（掠射，接近水平）射向水面时反射多。所以从高处俯视湖面能看到湖底，从远处水平看去湖面像镜子。

着色器里用它来模拟：视角越偏（越接近球体边缘），材质越亮或越反光。

---

## 3. 公式拆解

```hlsl
float fresnelFactor = pow(1.0 - max(dot(normal, viewDir), 0.0), 5.0);
```

- `dot(normal, viewDir)`：球体中心（法线正对镜头）接近 1.0，边缘（法线几乎垂直于视线）接近 0.0。
- `1.0 - dot(...)`：翻转——边缘大、中心小。
- `pow(..., 5.0)`：把效果更集中在边缘，指数越大亮边越窄。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| Fresnel 扩散到更大面积 | `5.0` 改成 `2.0` |
| Fresnel 极度集中边缘 | `5.0` 改成 `10.0` |
| 蓝色边缘光（冰面/水下） | `float3(1.0, 1.0, 1.0)` 改成 `float3(0.5, 0.8, 1.0)` |

---

## 5. 练习

练习代码里 `fresnelFactor = 0.0`，球体只有暗底色。补全 TODO，让边缘产生白色发光。

### 答案解析

```hlsl
float fresnelFactor = pow(1.0 - max(dot(normal, viewDir), 0.0), 5.0);
```

初始状态 `fresnelFactor = 0.0`，球体是 `baseColor * 0.2` 的暗底。`1.0 - dot(normal, viewDir)` 让边缘大、中心小，`pow(..., 5.0)` 把效果集中到窄边缘带，最终 `float3(1.0) * fresnelFactor` 加到底色上，边缘变白亮。

试着把指数从 5.0 改成 1.5，看 Fresnel 会不会扩散到球体中心区域。

---

## 6. 【小灶解析】专家补充

### ① Fresnel 和「边缘光」是同一个公式

第 34 课的边缘光和本课的 Fresnel 数学上完全一样：`pow(1 - dot(n, v), n)`。区别只是「怎么用」——边缘光把它当发光遮罩（加白边），Fresnel 把它当物理反射率（控制反射强度）。**同一根公式，两种叙事**。

### ② Schlick 近似：真实引擎的 Fresnel

真实引擎（PBR）用的 Fresnel 是 **Schlick 近似**：`F0 + (1 - F0) * pow(1 - dot(n, v), 5.0)`，其中 `F0` 是正视角的基础反射率（金属高、非金属约 0.04）。本课的 `pow(1 - dot(n,v), 5.0)` 就是 Schlick 里 `F0 = 0` 的特例。你已经摸到了 PBR 的边。

### ③ 为什么是「指数 5」

Schlick 用固定的指数 5，是因为它足够接近真实 Fresnel 曲线，又便宜。所以你在各种 shader 里看到 `pow(1 - NdotV, 5.0)`，几乎都是 Fresnel/Schlick 的痕迹。
