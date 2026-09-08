# B08｜Stencil 模板测试与操作

> 核心问题：怎样只在指定区域显示一个效果？`Ref`、读写掩码，以及 Fail、ZFail、Pass 究竟控制什么？
>
> 结论：模板缓冲保存离散位信息；先按参考值和读掩码比较，再依据模板/深度结果选择模板操作，最后用写掩码决定哪些位可改变。它是状态与位运算，不是另一张自动参与颜色混合的遮罩贴图。

本卡面向 Unity NPR（非真实感渲染），采用 8 位模板值、单采样、普通 Draw、无 Shader discard 和额外副作用的教学条件。文档依据 Unity 6.7 Beta / 6000.7（2026-06-26）。实验自己创建带模板的离屏目标，避免默认相机格式、Deferred 保留位和其他 Renderer Feature 影响结果。

## 1. 模板值、参考值和资源

**Stencil S** 是某个样本在模板缓冲中已有的整数，范围 `0…255`；**Ref R** 是当前状态的参考值。模板一般属于深度模板附件的一部分，但“支持深度”不等于格式必然包含模板，例如仅深度格式没有 S8 位。

模板可以给样本打标签，供后续 Draw 限制作用区域。它不保存颜色、连续距离或全部对象 ID，也不自动跨目标、跨相机共享。若目标被清除、替换、丢弃或重建，前次标签是否存在必须重新确认。[Microsoft 深度模板资源](https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-depth-stencil)

## 2. 比较顺序：参考值在左

设读掩码为 M，Unity 模板比较使用：

$$Compare(R\mathbin{\&}M,\;S\mathbin{\&}M)$$

`&` 是逐位 AND。`Comp Less` 表示左侧参考值小于右侧已有模板值；`Equal` 对称，但 Less/Greater 不对称。[Unity Stencil 参考](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Stencil.html)

例一：R=3、S=5、M=255，则 Less 通过，因为 `3<5`。把两边看反，会得到相反结果。

例二：R=8（`00001000`）、S=10（`00001010`）、M=8，只比较第 3 位（从最低位 0 开始），双方都得到 8，所以 Equal 通过。它不要求完整的 S 等于 8。

`ReadMask 0` 让双方都变为 0；Equal 因而通过、NotEqual 失败。它不是关闭整个模板阶段。

## 3. Fail、ZFail 与 Pass

在本卡无 discard 等额外条件的逻辑模型里：

| 模板测试 | 深度测试 | 模板操作选择 | 当前颜色/深度贡献 |
| --- | --- | --- | --- |
| 失败 | 无需用于决定此结果 | Fail | 不通过 |
| 通过 | 失败 | ZFail | 不通过 |
| 通过 | 通过 | Pass | 仍受颜色写掩码、深度写开关等控制 |

这里的 Pass 是“两个测试都通过时采用的模板操作”，不是一个新的 ShaderLab Pass，也不是在说 GPU 一定先执行完整片元 Shader 再做这些事。Early/Late 测试会影响执行时机；本卡只说明限定条件下的可观察状态结果。

操作包括 Keep、Zero、Replace、饱和增减、回绕增减、Invert。Replace 使用参考值；Invert 翻转各位。IncrSat 在 255 停住，IncrWrap 则从 255 回到 0。它们不是颜色计算函数。

## 4. 写掩码只允许部分位改变

先根据操作得到候选值 C，再使用写掩码 W 合并，限定在 8 位内：

$$S_{new}=(S\mathbin{\&}(255\mathbin{\oplus}W))\;|\;(C\mathbin{\&}W)$$

`|` 是逐位 OR，`⊕` 是 XOR；`255 XOR W` 相当于 8 位取反。WriteMask=0 表示全部旧位保留，**不是写入数值 0**。

例如 S=170（`10101010`），Replace 的 R=4（`00000100`），W=15（`00001111`）：旧高四位保留为 160，新低四位为 4，最终 164（`10100100`）。读掩码不负责保存高位，保存哪些位由写掩码决定。

也不要把“增量 + WriteMask”当成独立子字段计数器。操作针对完整候选值，再合并掩码。例如 S=7、W=8、IncrWrap：候选从 7 到 8，最终旧低三位仍为 7，加上允许写入的第 3 位变成 15，而不是只将原数字从 7 写为 8。

## 5. NPR 中先规划位和生产顺序

面部区域、头发局部覆盖或描边限制可以用模板位标记，但同一个位不能被多个不协调的效果随意复用。应记录：谁清除、谁写、谁读、哪些位归谁，以及读写发生在哪个目标和时点。

`ColorMask 0` 的模板写入 Pass 可以不显示颜色，却改变后续可见区域；它也可能写深度，必须明确 ZWrite。若希望只标记未被遮挡的表面，写入时要进行正确深度测试，并确保需要的遮挡深度已经存在。仅把 Writer 放在 Reader 前面，不保证其他遮挡物先写好了深度。

在 URP/HDRP 正式集成时，先核对管线使用的模板位和深度模板附件；不要从“本实验使用 bit 3”推断 bit 3 在所有项目都空闲。反向深度不改变模板整数比较的方向。

## 6. 完整离屏实验

创建空对象挂 `B08StencilLab.cs`，用后附 Shader 创建材质，拖到 Lab Material。进入 Play Mode，在 Game 窗口观察预览。脚本请求 D24/S8 并核对实际格式；模板不受支持时停止实验，不用没有模板的目标冒充成功。

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Experimental.Rendering;

public class B08StencilLab : MonoBehaviour
{
    public Material labMaterial;
    [Range(0,255)] public int initialStencil=0;
    public bool readerFirst=false;
    RenderTexture target;
    Mesh quad;
    CommandBuffer commands;
    bool ready;
    void Start()
    {
        if(labMaterial==null || !labMaterial.shader.isSupported) return;
        var descriptor=new RenderTextureDescriptor(128,128);
        descriptor.graphicsFormat=GraphicsFormat.R8G8B8A8_UNorm;
        descriptor.depthStencilFormat=GraphicsFormat.D24_UNorm_S8_UInt;
        descriptor.msaaSamples=1;
        target=new RenderTexture(descriptor) { name="B08 Owned Depth Stencil" };
        if(!target.Create()) { Debug.LogError("RenderTexture creation failed."); return; }
        var actual=target.depthStencilFormat;
        if(actual!=GraphicsFormat.D24_UNorm_S8_UInt &&
           actual!=GraphicsFormat.D32_SFloat_S8_UInt)
        {
            Debug.LogError("This lab requires a verified stencil format: "+actual);
            return;
        }
        quad=new Mesh { name="B08 Owned Quad" };
        quad.vertices=new Vector3[] {
            new Vector3(-1,-1,0),new Vector3(1,-1,0),
            new Vector3(1,1,0),new Vector3(-1,1,0) };
        quad.triangles=new int[] {0,1,2,0,2,3};
        commands=new CommandBuffer { name="B08 Stencil Writer Reader" };
        ready=true;
        Debug.Log("Actual depth/stencil format: "+actual);
    }
    void Update()
    {
        if(!ready || labMaterial==null) return;
        commands.Clear();
        commands.SetRenderTarget(target);
        commands.SetViewport(new Rect(0,0,128,128));
        commands.ClearRenderTarget(true,true,Color.black,1f,(uint)initialStencil);
        commands.DrawMesh(quad,Matrix4x4.identity,labMaterial,0,readerFirst ? 1 : 0);
        commands.DrawMesh(quad,Matrix4x4.identity,labMaterial,0,readerFirst ? 0 : 1);
        Graphics.ExecuteCommandBuffer(commands);
    }
    void OnGUI()
    {
        if(ready) GUI.DrawTexture(new Rect(10,10,256,256),target,ScaleMode.ScaleToFit,false);
    }
    void OnDestroy()
    {
        if(commands!=null) commands.Release();
        if(target!=null) { target.Release(); Destroy(target); }
        if(quad!=null) Destroy(quad);
    }
}
```

下面完整保存为 `B08StencilLab.shader`。Writer 覆盖中心一半宽高，Reader 覆盖整个目标。Writer 的 Fail 固定为 Zero，ZFail 固定为 Invert，便于观察三种路径；Reader 固定读取 bit 3，完全不写模板。

```shaderlab
Shader "Encyclopedia/B08StencilLab"
{
    Properties
    {
        [IntRange] _Ref("Writer Ref",Range(0,255))=8
        [IntRange] _ReadMask("Writer ReadMask",Range(0,255))=8
        [IntRange] _WriteMask("Writer WriteMask",Range(0,255))=8
        [Enum(UnityEngine.Rendering.CompareFunction)] _Comp("Writer Comp",Float)=8
        [Enum(UnityEngine.Rendering.CompareFunction)] _MaskZTest("Writer ZTest",Float)=8
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        HLSLINCLUDE
        float4 VertMask(float3 p:POSITION):SV_POSITION { return float4(p.xy*0.5,0.5,1); }
        float4 VertFull(float3 p:POSITION):SV_POSITION { return float4(p.xy,0.5,1); }
        float4 FragMask():SV_Target { return 0; }
        float4 FragColor():SV_Target { return float4(0,0.5,1,1); }
        ENDHLSL
        Pass
        {
            Name "Writer"
            Cull Off
            ZWrite Off
            ZTest [_MaskZTest]
            ColorMask 0
            Stencil
            {
                Ref [_Ref]
                ReadMask [_ReadMask]
                WriteMask [_WriteMask]
                Comp [_Comp]
                Pass Replace
                Fail Zero
                ZFail Invert
            }
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex VertMask
            #pragma fragment FragMask
            ENDHLSL
        }
        Pass
        {
            Name "Reader"
            Cull Off
            ZWrite Off
            ZTest Always
            Blend Off
            Stencil
            {
                Ref 8
                ReadMask 8
                WriteMask 0
                Comp Equal
                Pass Keep
                Fail Keep
                ZFail Keep
            }
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex VertFull
            #pragma fragment FragColor
            ENDHLSL
        }
    }
}
```

这个受控实验只用 Always/Never 区分深度测试路径，不依赖透视投影或深度远近。清除的 depth 参数不用于推导 Reversed-Z 行为。默认 Initial Stencil=0、Ref=8、两个 Mask=8、Comp=Always、ZTest=Always、Reader First 关闭：中心出现蓝色矩形。

| 从基准修改 | 预测与原因 |
| --- | --- |
| WriteMask=0 | 全黑：Writer 不改变任何模板位 |
| Reader First 开启 | 全黑：Reader 读取清除后的 0，Writer 后写也不会补画；每帧重新清除 |
| Initial Stencil=8，Comp=Never | 外蓝内黑：中心走 Fail/Zero，写掩码清掉 bit 3 |
| Initial Stencil=8，Comp=Always，ZTest=Never | 外蓝内黑：中心走 ZFail/Invert，bit 3 从 1 翻成 0 |
| Initial Stencil=8，Ref=0，ReadMask=8，Comp=Less，ZTest=Always | 外蓝内黑：`0<8` 通过，Replace 把中心 bit 3 清零 |

每项都从基准重新设置；不要把上一项的参数残留误当成新结论。前三种修改可能产生相似画面，却来自不同状态路径，必须通过状态检查与模板值辨认，而不是只看最终颜色猜原因。

## 7. 源码边界、自测与验证

`CommandBuffer.DrawMesh` 记录显式 Pass 0/1，托管入口参考 [固定提交 RenderingCommandBuffer.cs](https://github.com/Unity-Technologies/UnityCsReference/blob/9d487cab41b00c50af020b56d27a3c768d54f770/Runtime/Export/Graphics/RenderingCommandBuffer.cs)。实际模板比较与更新不是这段 C# 在 CPU 上逐像素实现。

资源格式与清除接口已核对 [depthStencilFormat](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/RenderTextureDescriptor-depthStencilFormat.html)、[ClearRenderTarget](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Rendering.CommandBuffer.ClearRenderTarget.html)。本地 6.7 文档明确 bool clearDepth 表示清除深度和模板；本例还显式传 stencil 初值。

自测：① WriteMask=0 会写零吗？**保留全部旧位。** ② ZFail 是模板失败吗？**模板通过但深度失败。** ③ 模板 Pass 一定写颜色吗？**还受 ColorMask 等控制。** ④ Reader 放前面能读取后面的写入吗？**不能靠未来写入改变已经完成的测试。**

本文的比较和位运算可以按公式逐步核算；实际验证使用文内离屏 Unity 实验，不把算术模型当作 GPU 状态机仿真。C#/Shader 尚未在 Unity 编译运行或抓帧。本地文档根目录为 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`，已核对 `Manual/SL-Stencil.html`、`ScriptReference/Rendering.CommandBuffer.ClearRenderTarget.html`、`RenderTextureDescriptor-depthStencilFormat.html`。

完成本卡后进入 [B 阶段检查点](../实验/B阶段检查点.md)。下一阶段从 [C01《Early-Z、Late-Z 与层次化深度》](../03-可见性与输出/C01-EarlyZLateZ与层次化深度.md) 开始。
