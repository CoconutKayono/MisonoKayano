# C04｜MSAA、覆盖、Alpha-to-Coverage 与 Resolve

> **核心问题：开启 4× MSAA 后，为什么模型轮廓变平滑，头发贴图的硬边却仍然锯齿？**
> 
> MSAA 增加的是像素内部的覆盖及附件样本，通常不会自动为每个样本重算所有着色。几何轮廓、Shader 裁剪边界与连续 Alpha 是不同信号，需要分别处理。

## 1. 范围与必要概念

本卡使用 Unity 6 / URP 中的独立离屏实验，目标是普通 UNorm 颜色附件。文档基线为本地 Unity 6.7 Beta / 6000.7、2026-06-26 构建。实验自行创建 MSAA 目标，与 URP 相机的 MSAA 设置分开；不依赖后处理。

- **像素（pixel）**：输出图像的栅格位置。
- **样本（sample）**：MSAA 像素内部保存覆盖、颜色、深度/模板结果的采样位置；具体布局依后端实现。
- **覆盖掩码（coverage mask）**：哪些样本被几何覆盖、允许更新的位集合。
- **Alpha-to-Coverage（A2C）**：根据片元 Alpha 生成样本覆盖掩码，再与其他覆盖约束组合。
- **Resolve**：将多样本资源转换成可供普通后续使用的单样本结果；规则与资源类型/格式有关。

## 2. 为什么 4× 不等于四倍完整着色

普通像素频率着色下，一个片元结果可用于该像素中多个被覆盖的样本，而覆盖、深度/模板、混合等按对应样本处理。请求样本频率着色会改变调用频率；不能把这个默认模型当作所有 Shader 的保证。边缘执行粒度、不同图元和辅助 lane 也会影响实际调用数。[Microsoft 光栅化规则](https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-rasterizer-stage-rules)

因此：

| 信号变化位置 | 普通 MSAA 能直接改善什么 | 仍需注意什么 |
| --- | --- | --- |
| 三角形外轮廓 | 子像素几何覆盖 | 不能保证时间稳定或极细线完全保留 |
| 片元内部 `clip(alpha-cutoff)` | 不自动把一次二值裁剪变成多级透明 | 可考虑 A2C、解析平滑或其他抗锯齿方案 |
| Ramp 硬阈值、高频高光、贴图细节 | 不保证增加这些信号的着色采样 | 过滤、导数、Mip、时间方法仍有作用 |

若普通片元调用算出 `alpha < cutoff` 并丢弃，不能期待 GPU 自动为每个 MSAA 样本重新采样 Alpha 得到不同裁剪结论。

## 3. 用四个样本手算 Resolve

以本卡线性 RGBA8 UNorm 颜色的常规颜色 Resolve 为例：像素有四个样本，两个写白色，另两个仍是黑色。颜色平均为：

`C_resolved = (1+1+0+0)/4 = 0.5`

几何边缘由此得到中间亮度。它是线性结果，显示编码后的字节不必是 128。样本中的颜色可以来自不同图元，不能将四个样本都视为同一个表面的四次着色。

**这个平均公式不能推广到所有数据。** 对象 ID 3 和 7 的均值 5 是假 ID；前后表面的深度均值也未必对应任何真实表面。深度、模板、整数或自定义语义需要支持的专用策略，不能把颜色 Resolve 当通用数据缩减函数。

256×256、RGBA8 的单样本颜色有效载荷为 256 KiB，4× 的未压缩颜色样本有效载荷为 1 MiB；额外 Resolve 目标再占 256 KiB。还未计入深度、对齐、元数据和压缩。这个容量模型不是显存实际分配量，更不是四倍 GPU 时间或四倍外部带宽的承诺。

## 4. Alpha-to-Coverage 改的是覆盖

在 D3D11 语义下，A2C 使用 `SV_Target0.a` 生成掩码，与几何覆盖及样本掩码做 AND。Alpha 到具体样本图案的映射由实现决定，不能把 `round(alpha×N)` 及固定样本顺序当成跨平台标准。A2C 本身不把送到混合器的 Alpha 改为 1，且与是否启用混合是独立状态。[Microsoft A2C 说明](https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-blend-state)

例如，在几何全覆盖的位置，若 Alpha=0.5 恰好选中 4 个样本中的 2 个：

- A2C 开启、Blend Off，选中的两个样本写完整源颜色；黑底 Resolve 后贡献约为 0.5 倍颜色。
- 再开启 SrcAlpha 混合，选中样本内又乘一次 0.5，贡献约为 0.25 倍。

这是给定掩码的教学算例，并非保证所有像素或 GPU 在 Alpha=0.5 时都选中相同样本。A2C 与混合可以有意组合，但若目标只是让不透明发丝边缘表达覆盖，重复衰减往往不是想要的结果。

Unity 用 `AlphaToMask On` 设置 A2C。无 MSAA 时的结果可能因 API/GPU 而异，本卡在实际只有一个样本时不执行 A2C 模式。[Unity AlphaToMask](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-AlphaToMask.html)；已核对本地 `Manual/writing-shader-alpha-to-mask.html` 的适用范围。

A2C 不等于真实半透明，也不是任意层数的顺序无关透明。深度写入可让不同样本保存不同表面，但低样本数、掩码相关性和运动仍可能产生颗粒感、条带或闪烁。

## 5. Unity 资源路径：请求、查询、创建、Resolve

`GetRenderTextureSupportedMSAASampleCount(descriptor)` 返回请求支持的样本数或更低的回退值；还应检查创建结果。`bindTextureMS=true` 用于保持可直接访问的多样本表面，避免默认自动 Resolve；本实验显式记录 `ResolveAntiAliasedSurface(source,target)`，且两者尺寸和颜色格式相同、目标为单样本。[Unity 样本数查询](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SystemInfo.GetRenderTextureSupportedMSAASampleCount.html)、[bindTextureMS](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/RenderTexture-bindTextureMS.html)、[Resolve API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Rendering.CommandBuffer.ResolveAntiAliasedSurface.html)

固定 UnityCsReference 提交 `9d487cab41b00c50af020b56d27a3c768d54f770` 的 `RenderingCommandBuffer.cs` 中，`ResolveAntiAliasedSurface` 检查源非空，转入 `Internal_ResolveAntiAliasedSurface`。它证明托管入口到原生调用边界，不能证明所有平台底层使用同一条指令。[固定提交源码](https://github.com/Unity-Technologies/UnityCsReference/blob/9d487cab41b00c50af020b56d27a3c768d54f770/Runtime/Export/Graphics/RenderingCommandBuffer.cs)

## 6. Unity 实验：四种边缘处理方式

保存 `C04CoverageLab.shader` 和 `C04MSAALab.cs`。URP 场景建空物体，挂脚本，将 Shader 资源拖入 Lab Shader。脚本自行创建材质、纹理、Mesh 和两张目标；不需要图片文件。独立副本：[Shader](../实验/C04CoverageLab.shader)、[C#](../实验/C04MSAALab.cs)。

Shader 四个 Pass 分别是忽略 Alpha、Alpha Clip、A2C、普通 Alpha 混合。它们由 CommandBuffer 指定 Pass 索引执行，不依赖相机自动选择多 Pass。

```shaderlab
Shader "Encyclopedia/C04CoverageLab"
{
    Properties { _Mask("Alpha Mask",2D)="white" {} }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        TEXTURE2D(_Mask);
        SAMPLER(sampler_Mask);
        struct Attributes { float3 position:POSITION; float2 uv:TEXCOORD0; };
        struct Varyings { float4 positionCS:SV_POSITION; float2 uv:TEXCOORD0; };
        Varyings Vert(Attributes input)
        {
            Varyings o;
            o.positionCS=float4(input.position.xy,0.5,1);
            o.uv=input.uv;
            return o;
        }
        float4 Frag(Varyings input):SV_Target
        {
            float a=SAMPLE_TEXTURE2D(_Mask,sampler_Mask,input.uv).a;
            return float4(0.15,0.8,0.3,a);
        }
        float4 FragClip(Varyings input):SV_Target
        {
            float4 c=Frag(input);
            clip(c.a-0.5);
            return c;
        }
        ENDHLSL
        Pass
        {
            Name "SolidAlphaIgnored"
            Cull Off ZTest Always ZWrite On Blend Off AlphaToMask Off
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            ENDHLSL
        }
        Pass
        {
            Name "Clip"
            Cull Off ZTest Always ZWrite On Blend Off AlphaToMask Off
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment FragClip
            ENDHLSL
        }
        Pass
        {
            Name "AlphaToCoverage"
            Cull Off ZTest Always ZWrite On Blend Off AlphaToMask On
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            ENDHLSL
        }
        Pass
        {
            Name "AlphaBlend"
            Cull Off ZTest Always ZWrite Off AlphaToMask Off
            Blend SrcAlpha OneMinusSrcAlpha, One OneMinusSrcAlpha
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            ENDHLSL
        }
    }
}
```

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Experimental.Rendering;

public class C04MSAALab : MonoBehaviour
{
    public enum ViewMode { SolidAlphaIgnored, Clip, AlphaToCoverage, AlphaBlend }
    public Shader labShader;
    public ViewMode mode;
    [Tooltip("Use 1, 2, 4 or 8. In Play mode call Rebuild Targets after changing.")]
    public int requestedSamples=4;
    RenderTexture source, resolved;
    Material material;
    Texture2D mask;
    Mesh quad;
    CommandBuffer commands;
    int actualSamples;
    bool ready;

    void Start()
    {
        if(labShader==null || !labShader.isSupported)
        {
            Debug.LogError("Assign the supported C04 shader.");
            return;
        }
        material=new Material(labShader);
        mask=new Texture2D(128,128,TextureFormat.RGBA32,false,true);
        mask.name="C04 Owned Linear Alpha Mask";
        mask.wrapMode=TextureWrapMode.Clamp;
        mask.filterMode=FilterMode.Bilinear;
        var pixels=new Color32[128*128];
        for(int y=0;y<128;y++) for(int x=0;x<128;x++)
        {
            float u=(x+0.5f)/128-0.5f, v=(y+0.5f)/128-0.5f;
            float a=1-Mathf.InverseLerp(0.30f,0.38f,Mathf.Sqrt(u*u+v*v));
            pixels[y*128+x]=new Color32(255,255,255,(byte)Mathf.RoundToInt(a*255));
        }
        mask.SetPixels32(pixels);
        mask.Apply(false,true);
        material.SetTexture("_Mask",mask);
        quad=new Mesh { name="C04 Owned Tilted Quad" };
        quad.vertices=new Vector3[] {
            new Vector3(-0.85f,-0.65f,0),new Vector3(0.65f,-0.85f,0),
            new Vector3(0.85f,0.65f,0),new Vector3(-0.65f,0.85f,0) };
        quad.uv=new Vector2[] { Vector2.zero,Vector2.right,Vector2.one,Vector2.up };
        quad.triangles=new int[] {0,1,2,0,2,3};
        commands=new CommandBuffer { name="C04 Coverage And Explicit Resolve" };
        RebuildTargets();
    }

    [ContextMenu("Rebuild Targets")]
    public void RebuildTargets()
    {
        if(!Application.isPlaying || material==null) return;
        ready=false;
        commands.Clear();
        ReleaseTarget(ref source);
        ReleaseTarget(ref resolved);
        if(requestedSamples!=1 && requestedSamples!=2 &&
           requestedSamples!=4 && requestedSamples!=8)
        {
            Debug.LogError("Requested samples must be 1, 2, 4 or 8.");
            return;
        }
        var d=new RenderTextureDescriptor(256,256);
        d.graphicsFormat=GraphicsFormat.R8G8B8A8_UNorm;
        d.depthStencilFormat=GraphicsFormat.D24_UNorm_S8_UInt;
        d.msaaSamples=requestedSamples;
        d.msaaSamples=SystemInfo.GetRenderTextureSupportedMSAASampleCount(d);
        if(d.msaaSamples<1) { Debug.LogError("No supported sample count."); return; }
        d.bindMS=d.msaaSamples>1;
        source=new RenderTexture(d) { name="C04 MSAA Source" };
        if(!source.Create() || source.graphicsFormat!=GraphicsFormat.R8G8B8A8_UNorm ||
           source.depthStencilFormat==GraphicsFormat.None)
        {
            Debug.LogError("C04 source creation/format failed.");
            return;
        }
        actualSamples=source.antiAliasing;
        d.graphicsFormat=source.graphicsFormat;
        d.depthStencilFormat=GraphicsFormat.None;
        d.msaaSamples=1;
        d.bindMS=false;
        resolved=new RenderTexture(d) { name="C04 Resolved", filterMode=FilterMode.Point };
        if(!resolved.Create() || resolved.graphicsFormat!=source.graphicsFormat)
        {
            Debug.LogError("C04 resolve target creation/format failed.");
            return;
        }
        ready=true;
        Debug.Log("C04 requested/actual samples: "+requestedSamples+"/"+actualSamples);
    }

    void Update()
    {
        if(!ready) return;
        commands.Clear();
        commands.SetRenderTarget(source);
        commands.SetViewport(new Rect(0,0,256,256));
        commands.ClearRenderTarget(true,true,Color.black);
        if(mode!=ViewMode.AlphaToCoverage || actualSamples>1)
            commands.DrawMesh(quad,Matrix4x4.identity,material,0,(int)mode);
        if(actualSamples>1) commands.ResolveAntiAliasedSurface(source,resolved);
        else commands.Blit(source,resolved);
        Graphics.ExecuteCommandBuffer(commands);
    }

    void OnGUI()
    {
        if(!ready) return;
        string status=mode+" | requested/actual: "+requestedSamples+"/"+actualSamples;
        if(mode==ViewMode.AlphaToCoverage && actualSamples==1)
            status+=" | A2C skipped: MSAA required";
        GUI.Label(new Rect(10,10,760,25),status);
        GUI.DrawTexture(new Rect(10,40,512,512),resolved,ScaleMode.ScaleToFit,false);
    }

    void ReleaseTarget(ref RenderTexture target)
    {
        if(target==null) return;
        target.Release();
        Destroy(target);
        target=null;
    }

    void OnDestroy()
    {
        if(commands!=null) commands.Release();
        ReleaseTarget(ref source);
        ReleaseTarget(ref resolved);
        if(material!=null) Destroy(material);
        if(mask!=null) Destroy(mask);
        if(quad!=null) Destroy(quad);
    }
}
```

## 7. 操作、预期画面和定位

1. 进入 Play，先确认日志 actual samples。改变 Requested Samples 后，使用组件菜单 **Rebuild Targets** 重新创建。填写 4 而实际只有 2，后续只能按 2× 解释。
2. SolidAlphaIgnored 模式分别查看实际 1× 和多样本结果。预测整个倾斜方块都可见，只有几何轮廓受 MSAA 改善；Shader 虽输出 Alpha，Blend Off/A2C Off 下它不自动隐藏 RGB。
3. Clip 模式出现硬边圆形。提高 MSAA 并不保证圆边获得与几何边缘相同的多级覆盖，因为圆边来自 Shader 内二值裁剪。
4. A2C 模式要求 actual>1。圆边的渐变 Alpha 转为覆盖等级，可出现分级或抖动；它不应被描述成每像素无限精度透明度。actual=1 时脚本跳过 Draw 并提示，避免解释未定义平台差异。
5. AlphaBlend 模式即使在 1× 也能有柔和圆边，因为纹理 Alpha 是连续权重。它的软边宽度、深度写入与多层排序性质不同于 A2C，不能据此认定其中一个普遍更好。
6. 定位 `C04 Coverage And Explicit Resolve`，检查源样本数、选中的 Pass、AlphaToMask/Blend 状态及单样本目标。程序只在 actual>1 时提交 Resolve；1× 使用普通 Blit 复制，不称其为多样本 Resolve。

预览使用 Point 放大，故意保留输出像素的台阶便于比较。它不是高分辨率重渲染；不要把放大后的块状边缘误判成 Resolve 无效。实验用 `ZTest Always` 和单个面隔离覆盖，不能据此验证复杂头发的深度遮挡或透明排序。

排查：先查 actual 样本数和重建是否执行，再查当前模式及资源格式；全粉色查 URP 编译；圆形全方块先查模式/Alpha 采样；A2C 黑屏先看是否被单样本保护跳过；Resolve 失败核对尺寸、格式、源/目标样本数和设备支持。

## 8. NPR 的使用判断

模型外轮廓、反壳描边外缘可以受 MSAA 帮助；头发 Alpha 边界可评估 A2C；脸部 SDF 阈值、Ramp 色阶和高频高光还需处理着色信号本身的频率。效果在静止时平滑，不代表转头和缩放时稳定，后续仍要讨论导数、Mip 和时间采样。

若 MRT 同时保存颜色和 ID，还必须分别设计各自的样本读取/归并语义。不能为了让颜色边缘平滑而把 ID 边界平均成错误分类。

## 9. 自测与答案

1. **4× MSAA 等于片元程序执行四遍吗？** 不保证。普通像素频率着色可复用结果；样本频率、图元覆盖及执行粒度会改变实际调用数。
2. **Alpha=0.5 是否保证固定两个样本被选中？** 不能跨平台保证；具体掩码映射与图案由实现决定，且还要与几何覆盖相交。
3. **A2C 后为什么可能不该再做 SrcAlpha 混合？** 覆盖已承担一次衰减，再混合可能形成第二次权重。
4. **只有 Camera 勾选 MSAA，能证明此离屏目标是 4× 吗？** 不能，必须检查这张资源的描述、能力查询与创建结果。
5. **Resolve 能否直接用于 ID 平均？** 不能按颜色平均去保持离散 ID 的语义，需要专门策略。

记住：MSAA 采样覆盖；A2C 把 Alpha 映射到覆盖；Resolve 必须匹配数据语义；请求数不等于实际数。

## 10. 验证范围与继续阅读

已核对上述官方文档及固定托管源码；本地文档根目录为 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`，对应 `ScriptReference/SystemInfo.GetRenderTextureSupportedMSAASampleCount.html`、`ScriptReference/RenderTexture-bindTextureMS.html`、`ScriptReference/Rendering.CommandBuffer.ResolveAntiAliasedSurface.html`。线上 Unity 链接为 6000.0 参考入口，实际 API 核对来自本地 6000.7。

所有画面描述均为预期；代码尚未在 Unity 编译、播放或 GPU 抓帧，未测量性能。托管源码不是目标 Editor 原生后端的完整源码。

前一张：[C03 附件与 MRT](C03-颜色深度附件MRT与写掩码.md)。下一张：[C05 分块 GPU、tile memory 与 Load/Store](C05-分块GPU与附件LoadStore.md)，继续区分逻辑附件更新与物理存储流量。
