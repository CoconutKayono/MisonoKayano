# D06｜排序、SRP Batcher、实例化与 GPU 驱动入口

> 核心问题：对象很多时，究竟是在减少 CPU 准备成本、合并 Draw，还是减少 GPU 实际处理的对象？能明确回答，才知道优化是否对准瓶颈。

## 1. 从一次绘制的成本开始

一个 Draw 指定几何范围、Shader/管线状态、资源与绘制参数。CPU 需要组织这些信息，GPU 需要读取几何、执行 Shader 并写入附件。多个对象可共享材质，但仍有各自变换与可见性；共享数据并不自动让它们变成一个 Draw。

教学成本模型可以写成：

`CPU 提交成本 ≈ 可见性/排序成本 + 状态准备次数 × 单次准备成本 + Draw 数 × 单次记录成本 + 数据更新成本`。

这是用于分类的模型，实际成本未必线性，也存在并行、缓存和引擎批量处理。GPU 时间还取决于几何、覆盖、采样、带宽及等待，不能由这个式子直接得到。

本卡核对本地 Unity **6.7 Beta / 6000.7、2026-06-26** 文档。公共源码固定 Graphics `275a7f9ad9330e3cf7f3ea57a0b242a551fde291`（manifest：URP/Core **17.0.4、Unity 6000.0**）。批处理核心部分涉及未公开原生实现，下文不虚构完整 C++ 调用栈。

## 2. 四种机制，四种证据

| 机制 | 主要改变什么 | 仍可能保留什么成本 | 应查看的证据 |
| --- | --- | --- | --- |
| 排序 | 调整对象/状态提交顺序，兼顾绘制语义、状态切换与遮挡 | 对象数和 Draw 数未必减少 | 队列、排序条件、事件顺序、透明合成结果 |
| SRP Batcher | 优化兼容 Shader 变体的材质/逐对象数据准备与连续提交 | 多个对象通常仍有多个 Draw | SRP batch、变体切换原因、CPU 渲染时间 |
| GPU Instancing | 一个实例化 Draw 处理同网格/同材质的多个实例 | 各实例的顶点与可见像素仍需处理 | Draw 的 instance count、实例数据和实际 Draw 数 |
| GPU Resident Drawer / BRG 等 | 以另一套对象数据和批量提交方式组织绘制，具体功能可结合 GPU 剔除 | CPU 调度、更新、GPU 剔除/绘制开销仍存在 | BRG 路径、实际兼容对象、剔除统计及 CPU/GPU 时间 |

SRP Batcher 将兼容材质数据保留在 GPU 常量缓冲并优化更新/绑定流程，受 Shader 变体和数据布局约束。它的“batch”不能直接翻译成“单个 GPU Draw”。Unity 官方描述的是准备及分发绘制的优化，参见 [SRP Batcher](https://docs.unity3d.com/6000.0/Documentation/Manual/SRPBatcher.html)。

普通 Renderer 的自动 GPU Instancing 与 SRP Batcher 有选择优先级：符合 SRP Batcher 的对象通常走 SRP Batcher，不能只凭材质的 Enable GPU Instancing 勾选推定已经实例化。显式 `Graphics.RenderMeshInstanced` 则主动请求实例绘制，不经过同一普通 Renderer 自动选择流程。对照本地 `Manual/GPUInstancing.html` 与 [RenderMeshInstanced API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Graphics.RenderMeshInstanced.html)。

## 3. 排序如何连接正确性与效率

不透明绘制通常允许在一定范围内重排。大致从前到后有利于提前拒绝被遮挡片元，相近状态连续绘制有利于降低准备成本；两者不一定同时达到最优。`SortingCriteria.CommonOpaque` 是组合条件，不能理解成精确逐像素前后排序。

透明混合常依赖从后到前。即使两片头发共享材质，强行按材质聚在一起也可能改变合成顺序。透明排序基于对象/排序数据，无法普遍解决同一网格内部交叉的三角形。排序正确性要先于减少状态切换的愿望。

Shader 关键字改变变体，可能中断 SRP batch；修改同一变体的材质参数则不一定。`MaterialPropertyBlock` 在常规 Renderer 使用中会影响 SRP Batcher 兼容性，不能把“少创建一个材质”直接等同于“更快”。实例化属性另有声明与数据通路，不能和普通 uniform 属性混用。

固定 URP 相机剔除与逐对象数据设置可从 [UniversalRenderPipeline.cs](https://github.com/Unity-Technologies/Graphics/blob/275a7f9ad9330e3cf7f3ea57a0b242a551fde291/Packages/com.unity.render-pipelines.universal/Runtime/UniversalRenderPipeline.cs) 向下追。公共托管入口只能证明参数与调用边界，不能证明驱动最终如何分配硬件任务。

## 4. 实例化为什么不是“GPU 工作除以对象数”

假设 100 个立方体使用一个 24 顶点记录的网格。实例化让 Draw 参数引用同一份几何和 100 组变换；这不代表 GPU 只计算一个立方体的顶点，再把最终屏幕像素复制 100 次。不同实例的变换、裁剪、覆盖和深度结果各不相同。

`RenderMeshInstanced` 也有批次容量。官方 API 给出的上限为 1023，但有效数量受实例数据大小影响；默认保存 object-to-world 与 world-to-object 时，文档给出的默认上限是 **511**。本例限制在 400，避免把 1023 当成所有 Shader/布局通用的有效容量。

显式实例批次按整体边界进行剔除与排序，不能假定会自动对其中每个实例进行独立视锥剔除或透明排序。把整座城市塞入一个巨大批次可能减少 CPU Draw，却保留更多 GPU 无用工作。空间分组必须同时考虑提交成本和剔除粒度。

## 5. 完整 Unity 实验：相同立方体，不同提交入口

创建 URP/Lit 材质，保存下面代码为 `D06SubmissionLab.cs` 并挂到空对象。材质通过组件字段赋值，运行时克隆，不修改输入材质资产。脚本从自己创建的隐藏 Cube 取得 Unity 内置网格，不需要模型文件，也不释放内置网格。

```csharp
using UnityEngine;
using UnityEngine.Rendering;

public class D06SubmissionLab : MonoBehaviour
{
    public enum Submission { Renderers, ExplicitInstancing }
    public Submission submission;
    [Range(1, 20)] public int side = 10;
    public Material sourceMaterial;
    public Camera targetCamera;
    GameObject generatedRoot;
    Material ownedMaterial;
    Mesh mesh;
    Matrix4x4[] matrices;
    Submission builtSubmission;

    void OnEnable() { if (Application.isPlaying) Rebuild(); }

    [ContextMenu("Rebuild")]
    public void Rebuild()
    {
        if (!Application.isPlaying) return;
        Cleanup();
        builtSubmission = submission;
        if (sourceMaterial == null || targetCamera == null)
        {
            Debug.LogWarning("D06: assign a URP/Lit material and the single Game Camera.", this);
            return;
        }
        if (submission == Submission.ExplicitInstancing && !SystemInfo.supportsInstancing)
        {
            Debug.LogWarning("D06: this device does not support instancing.", this);
            return;
        }
        ownedMaterial = new Material(sourceMaterial) { enableInstancing = true };
        generatedRoot = new GameObject("D06 Generated");
        generatedRoot.transform.SetParent(transform, false);
        var template = GameObject.CreatePrimitive(PrimitiveType.Cube);
        template.name = "D06 Mesh Source (inactive)";
        template.transform.SetParent(generatedRoot.transform, false);
        mesh = template.GetComponent<MeshFilter>().sharedMesh;
        template.SetActive(false);
        int n = Mathf.Clamp(side, 1, 20);
        matrices = new Matrix4x4[n * n];
        for (int z = 0; z < n; ++z)
        for (int x = 0; x < n; ++x)
        {
            var localPosition = new Vector3((x - (n - 1) * 0.5f) * 1.4f, 0,
                                           (z - (n - 1) * 0.5f) * 1.4f);
            matrices[z * n + x] = transform.localToWorldMatrix *
                Matrix4x4.TRS(localPosition, Quaternion.identity, Vector3.one);
            if (submission != Submission.Renderers) continue;
            var item = new GameObject("D06 Cube " + (z * n + x));
            item.transform.SetParent(generatedRoot.transform, false);
            item.transform.localPosition = localPosition;
            item.AddComponent<MeshFilter>().sharedMesh = mesh;
            var r = item.AddComponent<MeshRenderer>();
            r.sharedMaterial = ownedMaterial;
            r.shadowCastingMode = ShadowCastingMode.Off;
            r.receiveShadows = false;
            r.lightProbeUsage = LightProbeUsage.Off;
            r.reflectionProbeUsage = ReflectionProbeUsage.Off;
        }
    }
    void Update()
    {
        if (submission != builtSubmission) Rebuild();
        if (submission != Submission.ExplicitInstancing || matrices == null || ownedMaterial == null) return;
        var rp = new RenderParams(ownedMaterial)
        {
            camera = targetCamera,
            shadowCastingMode = ShadowCastingMode.Off,
            receiveShadows = false,
            lightProbeUsage = LightProbeUsage.Off,
            reflectionProbeUsage = ReflectionProbeUsage.Off
        };
        Graphics.RenderMeshInstanced(rp, mesh, 0, matrices);
    }
    void OnDisable() { Cleanup(); }
    void Cleanup()
    {
        if (generatedRoot != null)
        {
            generatedRoot.SetActive(false);
            Destroy(generatedRoot);
        }
        if (ownedMaterial != null) Destroy(ownedMaterial);
        generatedRoot = null;
        ownedMaterial = null;
        matrices = null;
        mesh = null;
    }
}
```

脚本用于 **Play 模式**。组件对象保持单位缩放与固定 Transform；修改位置、缩放或 Side 后执行组件菜单 Rebuild，使普通 Renderer 和缓存实例矩阵一致。Rebuild 的创建/销毁成本不属于稳定提交测量区间。普通 Renderer 会被其他相机看到，故基线只保留一个 Game Camera，并在测量时关闭 Scene 视图的持续渲染。

### 基线与三组对照

使用 URP Forward、一个方向光、不透明 URP/Lit 材质。关闭静态/动态合批、GPU Resident Drawer、Depth Priming、SSAO、阴影、后处理与额外 Renderer Feature。不要把对象标成 Batching Static。相机放在 `(0,15,-20)` 左右并朝向原点，使 10×10 阵列全部进入视野；远裁剪面足够大。

| 对照 | 设置 | 预测与核对方式 |
| --- | --- | --- |
| A | Renderers，SRP Batcher 开 | 相同变体有机会进入连续 SRP batch；逐对象 Draw 不必消失 |
| B | 保持 Renderers，关闭 SRP Batcher | 材质已启用实例化，检查是否出现自动实例 Draw；若没有，查兼容性/变体/Pass 条件 |
| C | ExplicitInstancing | 检查不透明颜色绘制事件的 instance count 是否等于 `side²`；其他相机任务仍有自身 Draw |

先在 Frame Debugger 记录 A/B/C 的事件和 instance count，再关闭抓帧工具测 CPU/GPU。调整 Side 后先 Rebuild，等待稳定再记录。普通 Renderer 与显式 API 的剔除/组织方式不同，这组实验验证入口差异，不能将测得的全部时间差归给单一缓冲绑定操作。

若 100 个对象过轻，计时差可能小于噪声；可以增加至 400 并记录多帧分布。不能因为 Draw 数明显下降，就省略 GPU 时间检查。正式性能结论需要在目标设备 Player、固定分辨率与相同画面下测量。

## 6. GPU Resident Drawer 的正确入口

本地 6000.7 文档把 GPU Resident Drawer 描述为基于 `BatchRendererGroup` 的实例绘制组织方式，要求兼容的渲染路径、平台、材质/Shader 和对象条件。当前本地条目列出 Forward+ 或 Deferred+ 路径，支持 compute 的平台但排除部分 API/平台，并要求相应 BRG 变体保留；实际项目应以该版本条件表逐项判断。

它不是打开后把所有 GameObject 自动变为同一种绘制，也不意味着 CPU 从此不参与。GPU occlusion culling 是相关但应单独验证的可见性机制，不能仅凭开启 GPU Resident Drawer 就声称所有遮挡工作已由 GPU 正确完成。参见 [官方启用入口](https://docs.unity3d.com/6000.0/Documentation/Manual/urp/gpu-resident-drawer.html)，以及本地同路径的 6000.7 条件。

本实验 A/B/C 先关闭该功能，避免普通 MeshRenderer 被另一机制接管。需要继续验证时，另外建立 GPU Resident Drawer 对照，记录所有新增条件，不能把它与“仅切 SRP Batcher”的结果混在一起。

## 7. NPR 迁移、自测与证据边界

大量同类饰品、石块、草叶适合考察实例化；每个角色独立面部 SDF、描边参数和多 Pass，可能先遇到变体与数据布局问题。应先统计真正相同的几何、材质和 Pass，再决定参数放入材质还是实例数据。透明发丝还必须保持合成正确性。

1. **100 个对象共享材质，是否一个 Draw？** 不保证；要看提交机制、Pass 和实际实例数。
2. **SRP batch 内有 100 个 Draw，是否说明优化失败？** 不能，目标可能是降低这些 Draw 的 CPU 准备成本。
3. **实例数 100 是否代表 GPU 只做一个对象的顶点工作？** 不是，各实例仍具有独立变换与覆盖。
4. **实例批次越大越好吗？** 未必，粗粒度剔除和排序可能增加无用 GPU 工作或破坏透明结果。
5. **为什么 A/B 对照要关闭 GPU Resident Drawer？** 为了避免普通 Renderer 被另一提交路径接管，掩盖当前比较变量。

已核对本地 `ScriptReference/Graphics.RenderMeshInstanced.html`、`RenderParams.html`、`Manual/SRPBatcher.html`、`GPUInstancing.html` 与 `urp/gpu-resident-drawer.html`，根目录 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。示例**未在 Unity 编译、运行或测时**，不存在已证实的性能倍数。

前一张：[D05 相机数据](D05-相机深度法线与运动矢量生产路径.md)。下一张：[D07 光源数据](D07-URP光源数据与ForwardPlus.md)。实践汇总：[D 阶段检查点](../实验/D阶段检查点.md)。
