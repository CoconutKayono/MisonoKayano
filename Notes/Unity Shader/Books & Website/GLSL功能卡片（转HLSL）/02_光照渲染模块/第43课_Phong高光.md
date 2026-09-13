# 第 43 课 · Phong 高光

> 学习目标：在漫反射球体上加一个镜面高光点，理解反射向量与高光的关系。

漫反射模拟粗糙表面的散射，高光模拟光滑表面的镜面反射：光打到表面「弹开」，恰好对着你眼睛的那个点会非常亮。

---

## 1. 完整代码

```hlsl
Shader "Lesson/43_PhongSpecular"
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

                float3 reflectDir = reflect(-lightDir, normal);   // 反射方向
                float specular = pow(max(dot(reflectDir, viewDir), 0.0), 32.0);

                float diffuse = max(dot(normal, lightDir), 0.0);
                float3 baseColor = float3(0.9, 0.5, 0.2);
                float3 color = baseColor * (0.1 + 0.9 * diffuse) + float3(1.0, 1.0, 1.0) * specular;
                return half4(color, 1);
            }
            ENDHLSL
        }
    }
}
```

场景准备同第 31 课。漫反射球体上出现一个闪亮的高光点，像金属、塑料或水面上的反光。

---

## 2. reflect 和 dot(reflectDir, viewDir) 在做什么

```hlsl
float3 reflectDir = reflect(-lightDir, normal);
float specular = pow(max(dot(reflectDir, viewDir), 0.0), 32.0);
```

第一步，`reflect(-lightDir, normal)` 把「光线方向取反后对法线做镜像」，得到反射光方向。第二步，`dot(reflectDir, viewDir)` 看反射方向有多对着视线：越对齐值越接近 1.0，高光越亮。

---

## 3. pow 的作用

`pow(x, 32.0)` 把接近 1.0 的部分保留、其余快速衰减为 0。指数越大高光点越小越锐（金属/镜面），越小越大越柔和（哑光）。32 ≈ 中等光滑，类似喷漆塑料。

---

## 4. 试着改一改

| 效果 | 写法 |
|------|------|
| 高光变大变柔（哑光） | `32.0` 改成 `8.0` |
| 高光变小变锐（金属/镜面） | `32.0` 改成 `128.0` |
| 高光变暖金色 | `float3(1.0, 1.0, 1.0)` 改成 `float3(1.0, 0.8, 0.4)` |

---

## 5. 练习

练习代码里 `specular = 0.0`，没有高光。补全 TODO，计算反射方向并求出 Phong 高光值。

### 答案解析

```hlsl
float3 reflectDir = reflect(-lightDir, normal);
float specular = pow(max(dot(reflectDir, viewDir), 0.0), 32.0);
```

初始状态 `specular = 0.0`，球体只有漫反射。先用 `reflect(-lightDir, normal)` 算出反射方向，再用 `dot(reflectDir, viewDir)` 判断反射方向和视线多对齐，最后 `pow(..., 32.0)` 让高光集中在小区域。

试着把指数 32.0 改成 4.0，看高光变成什么形状。

---

## 6. 【小灶解析】专家补充

### ① reflect 的参数顺序是「镜面反射」

HLSL 的 `reflect(incident, normal)` 返回入射光关于法线的镜像。因为 `lightDir` 指向光源（而不是从光源来），所以传 `-lightDir`。反射方向公式是 `reflectDir = 2 * dot(normal, lightDir) * normal - lightDir`——你可以手算验证。

### ② 高光为什么「跟着相机走」

高光位置由 `dot(reflectDir, viewDir)` 决定，而 `viewDir` 随相机移动。所以**高光点会跟着你的视角移动**——这是镜面反射区别于漫反射的本质特征。转一下视角，高光在球面上滑动，你就理解了。

### ③ Phong 高光 vs Blinn-Phong 高光

本课是 Phong（反射向量），第 41 课是 Blinn-Phong（半向量）。同一个高光，两种算法。工程上 Blinn-Phong 更常用，但 Phong 更直观——先懂 Phong，再换半向量，理解会更扎实。
