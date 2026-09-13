# E04｜面部 SDF、角度阈值图与头部光照空间

> 核心问题：如何让脸部明暗遵循设计，同时正确响应光照方向和角色转头？先区分两种常被混称为“面部 SDF”的数据，再为坐标、左右、阈值和垂直光照建立明确约定。

## 1. 纠正术语前提：灰度图不自动是 SDF

真正的有符号距离场 SDF，在给定度量下记录到边界的最近距离并带有内外符号。例如 UV 平面上半径 r、圆心 c 的圆，定义内部为正，则 `d(uv)=r-length(uv-c)`；d=0 是圆边界，数值单位为该 UV 度量中的距离。

为保存到 UNorm，可编码为 `g=saturate(0.5+d/(2×spread))`。在未饱和范围内可解码 `d=(g-0.5)×2×spread`。0.5 是编码边界，不是“光从侧面照来”的自然常数。距离场编码和过滤的原始说明参见 [Chris Green / Valve，2007](https://cdn.fastly.steamstatic.com/apps/valve/2007/SIGGRAPH2007_AlphaTestedMagnification.pdf)。该资料讨论距离场表示，不是本文面部光照算法的来源。

另一种面部数据是**角度阈值图** a(uv)：记录某像素在光照逐渐转向背面时，何时由亮变暗。运行时比较 `a(uv)` 与归一化光照角 t。它可能由多张设计遮罩、距离场插值等流程制作，但最终数值不一定是距离。

| 数据 | 数值单位 | 典型比较 | 不可直接替代的地方 |
| --- | --- | --- | --- |
| 某一光方向的 SDF | UV 距离或 texel 距离，需指定 | 解码 d 后比较 0 | 改零阈值是边界偏移，不自动等于转动光源 |
| 光照角度阈值图 | 归一化角度或另一个单调参数 | a 与 t 比较 | 梯度不保证满足距离场性质，羽化不天然是固定宽度 |
| 普通阴影遮罩 | 覆盖/分类权重 | 直接用值或阈值 | 不保证支持平滑重建或角度变化 |
| Shading Grade 控制图 | 模型指定的调制系数 | 调制 Half-Lambert 等信号 | 不等于以上任意一种标准编码 |

本卡完整实验的 **R 通道是角度阈值图，G 通道是一个圆的真实 UV 距离场编码**。用两个通道直接演示区别，不把程序生成的简单脸部图伪称为高质量角色资产。

## 2. 版本、目标与坐标约定

本地官方文档为 **Unity 6.7 Beta / 6000.7、2026-06-26**。Graphics 固定提交 `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`（URP/Core **17.0.4、Unity 6000.0**）。UTS 对照固定 `1520a78a95292cb045f1edb4d60ea0dba2f213b3`（**0.15.1-preview、Unity 6000.0**）；本卡角度阈值方案为独立教学设计，不声称来自 UTS 的面部 SDF 实现。

定义头部正交坐标：R 为角色右侧、U 为头顶、F 为脸朝前。三者来自一个专门的 HeadFrame Transform 的旋转：局部 +X 为 R、+Y 为 U、+Z 为 F。L 使用 URP 主光的**表面到光方向**。

实验使用方向光，将光投影到头部水平平面：

`h = (dot(L,R), dot(L,F))`，`ĥ = h / length(h)`。

其中 ĥ.x 的符号决定左右；`t = acos(clamp(ĥ.y,-1,1))/π` 决定由正面到背面的角度。t=0 为正面，0.5 为侧面，1 为背面。另一种常见参数 `(1-ĥ.y)/2` 虽也在 0…1，但不是线性角度：60° 时前者为 1/3，后者为 1/4，贴图不能不经转换直接互换。

角色右侧不等于屏幕右侧。相机正面看角色时，角色的右侧通常在屏幕左边；调试时看 HeadFrame 的 +X/+Z 轴，不能看屏幕左右猜符号。

## 3. 一张图如何响应左右光

定义 R 通道按**光在角色右侧**制作，UV 的 u 增大方向对应角色 +X。数值 a 越大，该位置在更偏背面的右侧光下仍能保持明亮。定义亮区为：

`m = step(t, a)`，平滑时使用 `smoothstep(-w,w,a-t)`。

光在左侧时先做 `u'=1-u`，再采样同一张右侧图。此复用只适合两侧可以镜像的设计；非对称脸纹、发型遮挡或不对称 UV 应使用独立左右图或独立通道。不能对已有“双侧编码贴图”再次盲目镜像。

| 方向 | ĥ | t | 采样 |
| --- | --- | --- | --- |
| 正前方 | (0,1) | 0 | 本例全部进入亮区 |
| 角色右前 60° | (0.866,0.5) | 1/3 | 原始 UV |
| 角色正右侧 | (1,0) | 1/2 | 原始 UV |
| 角色左前 60° | (-0.866,0.5) | 1/3 | 镜像 U |
| 正后方 | (0,-1) | 1 | 本例全部进入暗区 |

本例把 a 限制在 0.05…0.95，使正面/背面端点有明确结果。左右符号在正前和正后会换侧，但端点整片同色，避免在那里直接显露两套不一致轮廓。

一张 a 只能让每个像素随单调增加的 t 跨越一次阈值。这意味着它适合一族嵌套明暗区域。若某像素需要“亮→暗→亮”，单个阈值无法表达，应改用多方向数据、分区模型或更多参数。

## 4. 转头、镜像缩放与头顶光

光固定、头旋转时，R/F 改变，局部光角随之改变。如果只使用世界 L.x，就会让脸部暗面不随头正确转动。绑定角色根节点也可能失败：头骨单独转动时，真正需要更新的是头部坐标。

同时对头与光施加同一世界旋转 Q，点积保持不变：`dot(QR,QL)=dot(R,L)`。因此相同 UV 的明暗分类应不变。这是比“看起来差不多”更严格的验证。方向光下，只平移头部而不旋转，也不应改变该分类。

当 L 接近头部 U 方向时，h 的长度趋近零，水平角本来就没有稳定定义。给除法加 epsilon 只能避免 NaN，不能凭空恢复正确的水平光向。本例检测退化后采用“按正面光分类”的显式回退，并提供洋红诊断。它**不保证靠近头顶时连续**；正式角色可选择保留上一有效角、单独的俯仰图或可设计的过渡，但要将该规则纳入模型与历史状态。

HeadFrame 的轴取旋转，不把非均匀缩放当作方向基。实验要求没有负缩放或镜像父级；镜像角色需要同时定义坐标手性与 UV 翻转，否则可能被重复翻面。

## 5. 完整 Unity 实验

先保存 `E04FaceField.shader` 并创建材质。Shader 无需网格法线：脸的分类来自 UV、头部坐标与光方向。没有实时投射阴影、GI、运动矢量或头发遮挡，本卡先验证面部明暗数据本身。

```shaderlab
Shader "Encyclopedia/E04FaceField"
{
    Properties
    {
        _FaceMap("R Angle Threshold, G Circle SDF, A Face Area", 2D) = "white" {}
        _LitColor("Lit Color", Color) = (1,0.7,0.5,1)
        _ShadeColor("Shade Color", Color) = (0.3,0.13,0.2,1)
        _Feather("Angle Parameter Feather", Range(0,0.1)) = 0.01
        [Enum(Face,0,ThresholdData,1,LightAngle,2,DirectionValidity,3,DistanceContour,4)]
        _View("View", Float) = 0
        [HideInInspector] _HeadRightWS("Head Right", Vector) = (1,0,0,0)
        [HideInInspector] _HeadForwardWS("Head Forward", Vector) = (0,0,1,0)
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "E04Forward"
            Tags { "LightMode"="UniversalForward" }
            Cull Off ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            TEXTURE2D(_FaceMap);
            SAMPLER(sampler_FaceMap);
            CBUFFER_START(UnityPerMaterial)
                float4 _LitColor, _ShadeColor, _HeadRightWS, _HeadForwardWS;
                float _Feather, _View;
            CBUFFER_END
            struct Attributes { float4 positionOS : POSITION; float2 uv : TEXCOORD0; };
            struct Varyings { float4 positionCS : SV_POSITION; float2 uv : TEXCOORD0; };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionCS = TransformObjectToHClip(i.positionOS.xyz);
                o.uv = i.uv;
                return o;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                float3 l = GetMainLight().direction;
                float2 h = float2(dot(l, _HeadRightWS.xyz), dot(l, _HeadForwardWS.xyz));
                float len2 = dot(h,h);
                bool valid = len2 > 0.0001;
                h = valid ? h * rsqrt(max(len2,0.0001)) : float2(0,1);
                float t = acos(clamp(h.y,-1.0,1.0)) / PI;
                float2 uv = i.uv;
                if (h.x < 0) uv.x = 1.0 - uv.x;
                float4 data = SAMPLE_TEXTURE2D(_FaceMap, sampler_FaceMap, uv);
                float delta = data.r - t;
                float w = max(max(_Feather, fwidth(delta)), 0.0001);
                float mask = smoothstep(-w,w,delta);
                float d = (data.g - 0.5) * 0.5;
                float dw = max(fwidth(d),0.0001);
                float circle = smoothstep(-dw,dw,d);
                float3 color = lerp(_ShadeColor.rgb, _LitColor.rgb, mask);
                if (_View > 0.5 && _View < 1.5) color = data.rrr;
                else if (_View < 2.5 && _View > 1.5) color = t.xxx;
                else if (_View < 3.5 && _View > 2.5)
                    color = valid ? float3(0.5 + 0.5*h.x, 0.5 + 0.5*h.y, 0) : float3(1,0,1);
                else if (_View > 3.5) color = circle.xxx;
                color = lerp(float3(0.03,0.03,0.03), color, data.a);
                return float4(color,1);
            }
            ENDHLSL
        }
    }
}
```

保存为 `E04FaceFieldBinding.cs`，挂到使用上述材质的 Quad。程序在 Play 中生成数据纹理，并每帧更新头部坐标。纹理 R 是程序设计的角度阈值，G 是 spread=0.25 的圆 SDF，A 只是椭圆脸部区域；代码未调用外部模型、图片或 Python。

```csharp
using UnityEngine;

[RequireComponent(typeof(MeshRenderer))]
public class E04FaceFieldBinding : MonoBehaviour
{
    public Transform headFrame;
    MeshRenderer target;
    Material original, owned;
    Texture2D map;
    void OnEnable()
    {
        if (!Application.isPlaying) return;
        target = GetComponent<MeshRenderer>();
        original = target.sharedMaterial;
        if (headFrame == null || original == null || !original.HasProperty("_FaceMap"))
        {
            Debug.LogWarning("E04: assign HeadFrame and the E04FaceField material.", this);
            return;
        }
        owned = new Material(original);
        const int size = 256;
        map = new Texture2D(size,size,TextureFormat.RGBA32,false,true)
        {
            name = "E04 Angle Threshold And Circle Distance",
            filterMode = FilterMode.Bilinear,
            wrapMode = TextureWrapMode.Clamp
        };
        var pixels = new Color[size * size];
        for (int y = 0; y < size; ++y)
        for (int x = 0; x < size; ++x)
        {
            float u = (x + 0.5f) / size;
            float v = (y + 0.5f) / size;
            float px = u - 0.5f, py = v - 0.55f;
            float nose = 0.18f * Mathf.Exp(-(px*px/0.008f + py*py/0.04f));
            float threshold = Mathf.Clamp(0.15f + 0.7f*u + nose,0.05f,0.95f);
            float distance = 0.3f - new Vector2(u - 0.5f,v - 0.5f).magnitude;
            float encodedDistance = Mathf.Clamp01(0.5f + distance / 0.5f);
            float ex = (u - 0.5f) / 0.42f, ey = (v - 0.5f) / 0.48f;
            float area = ex*ex + ey*ey <= 1 ? 1 : 0;
            pixels[y*size+x] = new Color(threshold,encodedDistance,0,area);
        }
        map.SetPixels(pixels);
        map.Apply(false,false);
        owned.SetTexture("_FaceMap",map);
        target.sharedMaterial = owned;
        UpdateFrame();
    }
    void LateUpdate() { UpdateFrame(); }
    void UpdateFrame()
    {
        if (owned == null || headFrame == null) return;
        Vector3 r = headFrame.right.normalized;
        Vector3 f = headFrame.forward.normalized;
        owned.SetVector("_HeadRightWS",new Vector4(r.x,r.y,r.z,0));
        owned.SetVector("_HeadForwardWS",new Vector4(f.x,f.y,f.z,0));
    }
    void OnDisable()
    {
        if (target != null && owned != null && target.sharedMaterial == owned)
            target.sharedMaterial = original;
        if (owned != null) Destroy(owned);
        if (map != null) Destroy(map);
        owned = null;
        map = null;
    }
}
```

### 场景设置与预测

1. URP Forward、Linear、一个方向主光和一个 Base Game Camera。关闭阴影、GI、附加光、后处理、SSAO、Depth Priming、GPU Resident Drawer、MSAA 与其他 Feature。
2. 创建空对象 HeadFrame，位于原点、旋转零、缩放一。创建其子 Quad，局部位置/旋转零，缩放 `(2,2,1)`，赋本文材质并添加绑定脚本，HeadFrame 字段指向父对象。
3. 相机位置 `(0,0,4)`，旋转 `(0,180,0)`。正面看 HeadFrame 的 +Z；Shader Cull Off 消除 Quad 面朝向干扰。注意此视角下角色 +X 在屏幕左侧。
4. 方向光指定为 Sun Source。为使 L=+Z，光旋转设 `(0,180,0)`；进入 Play 应得到明亮脸部区域。运行时修改 View，要打开 Quad 当前克隆材质。
5. 光旋转设 `(0,-90,0)`，此时 L=+X，即角色右侧光；R 图较大的一侧保持亮。设 `(0,90,0)` 得 L=-X，亮区应镜像。设旋转零得 L=-Z，脸部应变暗。
6. 固定灯，旋转 HeadFrame，观察局部角度响应；只平移 HeadFrame，方向分类不变。若要同时旋转头与光，可将两者置于同一单位缩放空父对象下再转父对象；比较相同 UV，不以屏幕轮廓变化代替着色判断。
7. DirectionValidity 视图下，把光转到近头顶方向；投影足够小时应显示洋红，本例回退按正面分类。跨越退化区可能突变，这是已声明的边界，不是 NaN 被解决后就算模型完整。
8. DistanceContour 视图显示 G 的圆形零等值线区域；旋转水平光不会让该圆变成合理鼻影，因为它是固定图形距离场。ThresholdData 展示 R 的角度阈值变化，两个通道不可交换。

鼻部亮区只是程序场的局部凸起，用于辨认数据驱动的形状，不表示真实鼻梁建模。用于头模时需重新制作 UV 对应的阈值图，不能把 Quad 的纹理直接宣称为通用面部资产。

## 6. 真正的美术数据如何接入

先固定头部坐标、光角参数、亮暗符号和左右采样，再制作正面、侧面、背面等关键角的目标遮罩。若遮罩随角度单调嵌套，可以为每个 UV 记录亮暗切换角，得到本文类型的 a 图；若不满足，应增加独立区段或多个方向层。

如果采用“每个关键角一张真实 SDF”，则每张图需要一致的符号、距离单位与 spread。可在相邻角之间插值其解码距离，再以零分类；但**两个 SDF 的线性插值一般不再是精确距离场**，中间形状也未必符合设计，需要审核中间角和必要的重新设计。单张固定 SDF 改阈值主要产生等距轮廓变化，不能自动表达任意脸部光照序列。

作为标量，角度图应关闭 sRGB 解码，先用无压缩格式验证。R 通道 8 位 UNorm 的单级角度间隔约 `180/255=0.706°`，四舍五入的最大量化角误差约 0.353°，这是 t 线性对应角度且忽略其他误差的估算。压缩、Mip、UV 接缝和双线性重建还会引入额外变化。

fwidth 只根据屏幕局部导数软化分类，不能修复左右制作不一致、头部坐标绑定错误或垂直光照退化。镜像 UV 岛、睫毛和不同材质区域也需要显式分区；真实项目常把面部控制与头发投射阴影分开处理，之后再按设计合成。

## 7. 与 URP / UTS 的连接

URP 的 `GetMainLight` 提供世界光方向，本卡额外提供 HeadFrame 轴，将世界方向转为头部坐标。轴定义可核对本地 `ScriptReference/Transform-right.html`、`Transform-forward.html`，在线参见 [Transform.forward](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Transform-forward.html)。

固定 UTS 的 [ShadingGradeMap](https://github.com/Unity-Technologies/com.unity.toonshader/blob/1520a78a95292cb045f1edb4d60ea0dba2f213b3/com.unity.toonshader/Runtime/Shaders/URP/UniversalToonBodyShadingGradeMap.hlsl) 使用控制量调制其分区信号。所核对的该算法不能作为“所有面部 SDF 都按上述 acos/镜像公式运行”的证据。接入其他资产时，必须取得其生成与采样约定。

## 8. 自测与验证边界

1. **灰度图阈值 0.5 一定是 SDF 边界吗？** 只有编码约定如此时才是；角度图的 0.5 可以表示 90° 切换。
2. **世界 L.x 能直接决定角色左右吗？** 不能，应投影到头部右轴。
3. **acos 参数与 `(1-cos)/2` 可以共用贴图吗？** 不经转换通常不行，角度域不同。
4. **为什么光在头顶时水平角不稳定？** 水平投影趋于零，方位本身退化，需要艺术回退规则。
5. **一张阈值图能表示同一点亮暗反复切换吗？** 对单调 t 不能，需要更多数据或分段模型。
6. **普通软化能补回错误的头骨绑定吗？** 不能，输入空间必须先正确。

已核对距离场原始论文、本地 Transform/Texture2D API、固定 URP 光源接口和固定 UTS 控制图实现。文档根目录 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。**示例未在 Unity 编译、运行或捕获**；程序图是教学资产，真实角色 UV、动画、镜像和时间稳定性仍需专门验证。

前一张：[E03 Ramp 与阴影合成](E03-Ramp色阶阈值与阴影合成.md)。本组实践：[E01—E04 实验说明](../实验/E01-E04实验说明.md)。下一张：[E05 美术法线、平滑法线与轮廓法线](E05-美术法线平滑法线与轮廓法线.md)。完整阶段实践：[E 阶段检查点](../实验/E阶段检查点.md)。
