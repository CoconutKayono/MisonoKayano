# 第 39 课 · Phong 光照模型

> 学习目标：把环境光、漫反射、高光三项合并成一个完整的光照函数，理解 Phong 模型的组成。

Phong 是最经典的实时光照模型：三项分别计算再相加。本课还让光源绕球体旋转，直观看到高光点随光移动。

---

## 1. 完整代码

```hlsl
Shader "Lesson/39_Phong"
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

                // 光源随时间绕球体旋转
                float3 lightPosition = float3(cos(_Time.y) * 2.0, sin(_Time.y) * 2.0, 1.0);
                float3 lightDir = normalize(lightPosition - IN.positionWS);

                // —— Phong 三件套 ——
                float ambient = 0.2;                                        // 环境光
                float diffuse = max(dot(normal, lightDir), 0.0);            // 漫反射
                float3 reflectDir = reflect(-lightDir, normal);             // 反射方向
                float specular = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);  // 高光

                float3 objectColor = float3(0.9, 0.45, 0.2);
                float3 color = (ambient + diffuse + specular) * objectColor;
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

场景准备同第 31 课。球体上有一个会移动的高光点，明暗交界线也随时间变化。

---

## 2. Phong 模型的三个组成部分

```hlsl
float3 color = (ambient + diffuse + specular) * objectColor;
```

- **环境光（ambient）**：固定基础亮度，不依赖方向，系数 0.2 让物体至少有 20% 亮度。
- **漫反射（diffuse）**：粗糙表面的均匀散射，`max(dot(normal, lightDir), 0.0)` 让朝向光的地方亮、背向光的地方暗。
- **高光（specular）**：光滑面的镜面反射，`pow(max(dot(viewDir, reflectDir), 0.0), 32.0)` 在反射光对着眼睛的地方产生亮点。指数越大亮点越小越锐。

---

## 3. 动态光源

```hlsl
float3 lightPosition = float3(cos(_Time.y) * 2.0, sin(_Time.y) * 2.0, 1.0);
```

`_Time.y` 是 Unity 内置的秒数（单位：秒）。光源每帧都在绕球体旋转，光方向变了，高光点和明暗交界线随之移动。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 高光变大变柔 | 指数 `32.0` 改成 `8.0` |
| 高光变成小亮点 | 指数 `32.0` 改成 `128.0` |
| 暗部更暗、对比更强 | `ambient` 从 `0.2` 改成 `0.05` |
| 球体变橙色材质 | `objectColor` 改成 `float3(0.9, 0.5, 0.1)` |

---

## 5. 练习

练习区 `shininess` 已经设好、代码可运行。把高光指数从 32.0 改到不同值（如 4.0、64.0、256.0），观察高光如何变化。

### 答案解析

Phong 模型的完整合并：

```hlsl
float3 color = (ambient + diffuse + specular) * objectColor;
```

三项分别计算：`ambient = 0.2`（固定 20% 白光）、`diffuse = max(dot(normal, lightDir), 0.0)`（方向相关漫射）、`specular = pow(max(dot(viewDir, reflectDir), 0.0), 32.0)`（高光）。指数 32.0 是中等偏光滑，类似喷漆表面；从 4.0 到 256.0 可以模拟从橡皮到镜面的各种材质。

试着把 `specular` 前乘一个系数（如 `specular * 0.3`），看高光会变暗多少。

---

## 6. 【小灶解析】专家补充

### ① 光照 = 分项相加

Phong 的核心思想是**把复杂的光照拆成几个独立项，分别计算再相加**。这一招贯穿整个实时光照史：Phong 拆三项，PBR 拆成更物理的漫反射 + 镜面反射两项。学会「拆项 + 相加」，你就能读懂任何光照模型。

### ② reflect 的用法

HLSL 里 `reflect(incidentDir, normal)` 返回入射方向关于法线的镜像方向。这里传 `-lightDir` 是因为 `lightDir` 指向光源，而反射需要「光从光源射向表面」的方向，所以要取反。**这个取反是新手最常见的坑**。

### ③ 高光 vs 漫反射：材质的分水岭

漫反射决定「颜色」，高光决定「光滑度」。金属、玻璃高光强而小；橡皮、粉笔几乎没有高光。**看一个材质，先看它有没有高光、高光多大多亮，就能反推出它的粗糙度**——这是 TA 分析材质的第一直觉。
