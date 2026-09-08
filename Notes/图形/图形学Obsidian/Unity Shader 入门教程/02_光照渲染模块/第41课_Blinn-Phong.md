# 第 41 课 · Blinn-Phong

> 学习目标：用半向量替代反射向量计算高光，理解 Blinn-Phong 与 Phong 的区别。

Phong 需要计算反射向量；Blinn-Phong 换了一种更快的方式——只用半向量。

---

## 1. 完整代码

```hlsl
Shader "Lesson/41_BlinnPhong"
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
                float3 lightDir = normalize(float3(-0.4, 0.6, 0.7));

                float3 halfVector = normalize(lightDir + viewDir);   // 半向量
                float specular = pow(max(dot(normal, halfVector), 0.0), 48.0);

                float diffuse = max(dot(normal, lightDir), 0.0);
                float3 baseColor = float3(0.35, 0.6, 0.9);
                float3 color = baseColor * (0.12 + 0.88 * diffuse) + float3(1.0, 1.0, 1.0) * specular;
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

场景准备同第 31 课。球体上有一个集中而明显的白色高光点。

---

## 2. 半向量是什么

```hlsl
float3 halfVector = normalize(lightDir + viewDir);
```

`lightDir` 指向光源，`viewDir` 指向相机。两者相加再归一化，得到指向它们正中间的方向——**半向量**。

Phong 判断「反射光是否打到眼睛」（`dot(reflectDir, viewDir)`），Blinn-Phong 改为判断「法线是否对准半向量」（`dot(normal, halfVector)`）。两者视觉相近，但半向量计算量更小，是实时渲染更常用的方案。

---

## 3. pow 控制高光大小

```hlsl
float specular = pow(max(dot(normal, halfVector), 0.0), 48.0);
```

`dot(normal, halfVector)` 在 0~1 之间（0% 表示法线和半向量垂直，100% 表示完全对齐）。`pow` 的指数越大高光越小越集中（镜面），越小越宽越散（磨砂）。48.0 是中等偏高的光泽度。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 高光变大变散（磨砂球） | `48.0` 改成 `8.0` |
| 高光缩成亮点（玻璃球） | `48.0` 改成 `128.0` |
| 高光变暖黄色 | `float3(1.0, 1.0, 1.0)` 改成 `float3(1.0, 0.8, 0.4)` |
| 高光移到右侧 | `lightDir` 改成 `normalize(float3(0.8, 0.2, 0.7))` |

---

## 5. 练习

练习代码里 `halfVector = viewDir`（用视线方向替代半向量）。替换为正确的 `halfVector = normalize(lightDir + viewDir)`，让球体出现白色高光。

### 答案解析

```hlsl
float3 halfVector = normalize(lightDir + viewDir);
```

初始状态 `halfVector = viewDir`，导致 `dot(normal, halfVector)` 结果不对，高光出现在球体正中心而不是受光面。改成 `normalize(lightDir + viewDir)` 后，`dot(normal, halfVector)` 在法线对准半向量的区域最大，`pow` 之后形成集中的白色亮斑。

试着把 48.0 改成 200.0，感受极高光泽度下高光集中成一个针尖大小的亮点。

---

## 6. 【小灶解析】专家补充

### ① 为什么半向量更快

Phong 要 `reflect`（一次反射 + 两次点乘）；Blinn-Phong 只需 `normalize(lightDir + viewDir)` 一次加法归一化。当相机和光源都离物体较远时，半向量几乎恒定，甚至可以每帧只算一次。**用「半向量」替代「反射向量」，是实时渲染里最经典的优化之一**。

### ② 高光到底在哪

直觉上高光在「光被镜子反射到你眼睛」的位置。Phong 直接描述这个位置；Blinn-Phong 用「法线对准半向量」间接描述。两者在大多数角度下几乎重合，只有在掠射角（视线几乎平行于表面）时才有可见差异，此时 Blinn-Phong 更稳定、更像真实材质。

### ③ 高光的颜色

本课高光是纯白 `float3(1.0)`。真实材质里，高光颜色可以独立于漫反射颜色——金属的高光带金属色，塑料的高光偏白。这就是后面 PBR 里「specular 颜色」的来源。
