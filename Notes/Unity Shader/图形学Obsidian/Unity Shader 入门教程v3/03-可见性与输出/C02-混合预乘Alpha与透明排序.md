# C02｜混合、预乘 Alpha 与透明排序

> **核心问题：片元着色器输出了正确的 RGBA，为什么透明头发仍然发黑、发亮或穿插错误？**
> 
> 输出颜色的表示方式、GPU 混合因子、绘制顺序必须配套。预乘 Alpha 能改善合成与过滤的表达，但不会让透明绘制变成与顺序无关。

## 1. 范围与必要概念

本卡讨论 `BlendOp Add` 的普通 Over 合成，示例为 Unity 6 / URP。依据本地 Unity 6.7 Beta / 6000.7 文档（2026-06-26 构建）；不涵盖折射、物理介质透射、OIT 或所有混合操作。

- **源 S**：本次片元输出；**目标 D**：颜色附件中已有值。
- **Alpha A**：本卡作为不透明度/合成权重；它也可能被工程定义为其他数据，不能看到第四通道就自动套本卡公式。
- **直通 Alpha（straight / unassociated）**：RGB 保存未乘 Alpha 的颜色 `C`。
- **预乘 Alpha（premultiplied / associated）**：RGB 保存 `P=C×A`。
- **颜色附件**：GPU 接受输出的可渲染资源；合成结果通常还要经过后续 Pass 和显示转换。

公式中的颜色均处于线性工作空间，先忽略量化、饱和及格式限制。截图上的 sRGB 字节不能直接代入线性合成公式。

## 2. 把 RGB 与 Alpha 分开推导

加法混合的一般形式为：

`RGB_out = RGB_s × F_s + RGB_d × F_d`

RGB 因子与 Alpha 因子可以独立设置。对 Over 合成，Alpha 为：

`A_out = A_s + A_d × (1 - A_s)`

假设目标已经保存预乘合成结果 `P_d`（不透明目标因 A=1，同样成立），则两种源表示的正确配置为：

| 源表示 | Shader 输出 RGB | Unity 状态 | 合成 RGB |
| --- | --- | --- | --- |
| Straight | `C_s` | `Blend SrcAlpha OneMinusSrcAlpha, One OneMinusSrcAlpha` | `C_s A_s + P_d(1-A_s)` |
| Premultiplied | `P_s=C_s A_s` | `Blend One OneMinusSrcAlpha, One OneMinusSrcAlpha` | `P_s + P_d(1-A_s)` |

**两种配置合成到透明清除目标后，保存的 RGB 都是预乘结果。** 若后续拿这张 RenderTexture 当 straight 图像再乘一次 Alpha，会出现二次衰减。若明确需要 unassociated 结果，需在 A>0 时处理除法及 A=0 的约定。

Unity 支持用逗号分别指定 RGB 与 Alpha 因子。本卡状态语法依据本地 `Manual/SL-Blend.html`；同名线上参考为 [ShaderLab Blend](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Blend.html)（线上链接为 Unity 6.0 入口，本地核对版本为 6000.7）。

### 一个非常隐蔽的 Alpha 错误

只写 `Blend SrcAlpha OneMinusSrcAlpha` 会把同一组因子应用于 Alpha，得到：

`A_out = A_s² + A_d(1-A_s)`

`A_s=0.5` 画到全透明目标上，得到 `0.25` 而非 Over 应有的 `0.5`。画到不透明目标，得到 `0.75` 而非 `1`。屏幕可能暂时看不出，因为显示阶段未使用 Alpha；把结果继续合成时才暴露。

## 3. 为什么透明排序无法省掉

两张半透明平面，红色 R=(1,0,0)、蓝色 B=(0,0,1)，Alpha 都为 0.5，目标是不透明黑色。在线性空间手算：

| 提交顺序 | 第一次合成 | 第二次合成结果 |
| --- | --- | --- |
| 红，再蓝 | `(0.5,0,0)` | `(0.25,0,0.5)` |
| 蓝，再红 | `(0,0,0.5)` | `(0.5,0,0.25)` |

两者 Alpha 都为 1，颜色不同。源颜色改成预乘后会得到同样两组结果，**预乘没有改变 Over 不满足交换律的事实**。理想预乘 Over 具有结合性，也不能推出可以任意交换前后层。

普通透明策略常采用先画不透明，再把透明对象按所需远近顺序绘制，并用 `ZWrite Off` 避免先画的透明面把后画层硬挡住。但 `ZTest` 仍可让透明面被已有不透明物遮挡。

按 Renderer 排序不能解决所有逐像素顺序：相交平面可能在左边 A 靠前、右边 B 靠前，一个对象级顺序无法同时满足两边。一个 Mesh 内的多个三角形也不能指望普通透明队列自动逐像素重排。复杂头发需要拆分、裁剪、专门合成或更高级透明方案。

## 4. 预乘必须贯穿过滤与合成

考虑纹理两个 texel：不透明红 `(1,0,0,1)` 与透明黑 `(0,0,0,0)`，在线性空间各占过滤权重 1/2。

- 直接过滤 straight 数据得到 `(0.5,0,0,0.5)`，再按 straight 混合到黑色，红色贡献为 `0.25`。
- 先在 texel 层表示为预乘，再过滤，得到预乘 `(0.5,0,0,0.5)`，按 `One` 混合，红色贡献为 `0.5`。

两次过滤后的四个数恰好相同，但其语义不同，混合因子也不同。第一条路径已经把透明黑混入了未关联颜色；采样后才执行 `rgb *= alpha` 不能找回丢失的颜色。

这是用于解释黑边的两点模型；实际管线还涉及边缘扩色、Mip 生成、sRGB 解码和贴图压缩。预乘应在线性颜色域完成，并确保导入、Mip、采样、输出及后续合成有一致约定。不能仅勾选一个材质选项就假设源纹理全链路已转换。

## 5. Unity 实验：四种组合与两种顺序

下面使用常量材质颜色，只隔离“源表示与混合因子”，不声称它验证了纹理过滤。保存为 `C02BlendLab.shader`，或复制 [独立 Shader](../实验/C02BlendLab.shader)。

```shaderlab
Shader "Encyclopedia/C02BlendLab"
{
    Properties
    {
        _Color("Color",Color)=(1,0,0,0.5)
        [Enum(UnityEngine.Rendering.BlendMode)] _SrcBlend("RGB Source Factor",Float)=5
        [Toggle] _Premultiply("Premultiply RGB",Float)=0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Transparent" "RenderType"="Transparent" }
        Pass
        {
            Tags { "LightMode"="SRPDefaultUnlit" }
            Cull Off ZTest LEqual ZWrite Off
            Blend [_SrcBlend] OneMinusSrcAlpha, One OneMinusSrcAlpha
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _Color;
                float _SrcBlend, _Premultiply;
            CBUFFER_END
            struct Attributes { float3 positionOS:POSITION; };
            struct Varyings { float4 positionCS:SV_POSITION; };
            Varyings Vert(Attributes input)
            {
                Varyings o;
                o.positionCS=TransformObjectToHClip(input.positionOS);
                return o;
            }
            float4 Frag(Varyings input):SV_Target
            {
                float4 c=_Color;
                c.rgb*=lerp(1.0,c.a,step(0.5,_Premultiply));
                return c;
            }
            ENDHLSL
        }
    }
}
```

1. 在 URP Forward 单相机场景使用两个略有前后距离、部分重叠的 Quad，分别赋红、蓝材质，Alpha=0.5。相机用纯黑背景；项目使用 Linear，关闭后处理、Depth Priming、SSAO 和额外 Renderer Feature，以减少其他路径对实验的干扰。
2. 两个材质都设 `Premultiply=Off`、`RGB Source Factor=SrcAlpha`。通过材质自定义 Render Queue 固定红 3000、蓝 3001，在 Frame Debugger 中确认顺序。预测重叠处偏蓝。
3. 交换两个队列，预测重叠处偏红。Hierarchy 中的排列不是可靠的透明提交顺序控制方式。
4. 两个材质同时设 `Premultiply=On`、源因子 `One`。保持相同队列，预测结果与步骤 2 或 3 对应结果一致。
5. 故意设 `Premultiply=On`、`SrcAlpha`：源贡献额外乘一次 Alpha，变暗。设 `Premultiply=Off`、`One`：源贡献没有按透明度减弱，通常变亮，UNorm 目标还可能截断。
6. 用第三个不透明 Quad 挡在前面，预测透明物仍被遮挡。这验证 `ZWrite Off` 不等于 `ZTest Off`。

需要检查准确数值时，查看无后处理线性附件中的值，并确认目标格式、背景 Alpha 与颜色空间。不能用显示截图的字节直接要求出现 `0.25/0.5`。若要验证 Alpha 的反例，应额外渲染到 Alpha 清零的 RenderTexture 并检查其通道；普通 Game 视图不足以证明 Alpha 正确。

排查顺序：先查实际 Draw 顺序和 Pass 状态，再查颜色是否已预乘，再查目标 Alpha 的用途、纹理导入和过滤，最后查后处理。不要用加亮材质颜色掩盖重复乘 Alpha。

## 6. NPR 中的取舍

透明发梢、眼睛高光卡片、半透明描边和特效常需要合成。若希望发丝成为具有明确遮挡的表面，Alpha Clip 或覆盖方法可能更贴近目标；若需要透出多层颜色，必须正视排序与层叠成本。预乘解决的是表示与合成配套问题，不能替代头发的几何分层设计。

混合通常带来对目标颜色的依赖；缓存、压缩、tile memory 和具体硬件会影响实际带宽。不能把一次混合机械算成一次外部显存读取再加一次写入，也不能说启用混合一定使所有早期深度拒绝失效。

## 7. 自测与答案

1. **把 Blend 改为 One 后就完成预乘了吗？** 没有，源 RGB 必须已经含 Alpha 权重；贴图过滤链也要一致。
2. **Over 的 Alpha 为什么不是源 Alpha 的平方？** 新层贡献其自身覆盖，剩余部分再由旧层覆盖：`As+(1-As)Ad`。
3. **Straight 源合成到透明 RT 后，结果 RGB 还是 straight 吗？** 按本文公式不是，它保存预乘合成结果，下一次使用必须匹配。
4. **预乘为什么不能解决相交头发排序？** 不同前后关系仍生成不同颜色，表示转换没有让 Over 满足交换律。

记住：RGB 与 Alpha 分开推导；预乘是数据约定；过滤顺序有意义；透明顺序仍然决定画面。

## 8. 来源、验证边界与后续

已核对本地 `Manual/SL-Blend.html`、`Manual/SL-BlendOp.html`，完整根目录为 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。上述算例是依据公式的手算；示例尚未在 Unity 编译或运行。没有宣称测得透明性能。

前一张：[C01 深度优化](C01-EarlyZLateZ与层次化深度.md)。下一张：[C03 附件、MRT 与写掩码](C03-颜色深度附件MRT与写掩码.md)。
