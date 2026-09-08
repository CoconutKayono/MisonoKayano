# A06｜Mesh、子网格、顶点布局与索引：一个角点为什么会有多个顶点

> **GPU 的一个顶点记录通常是一组属性，不只是位置。同一几何角点如果需要不同法线、UV 或切线，往往必须对应多个顶点记录；仅按位置合并可能破坏 NPR 明暗和描边。**

## 1. 范围与必需概念

本卡解释 Unity 普通 Mesh 的数据表示和读取方式，采用索引化 Triangle List，即每三个索引描述一个三角形。不讨论 Mesh Shader、复杂蒙皮布局和间接绘制的完整实现。

**属性**是位置、法线、UV 等顶点数据；**缓冲**是 GPU 可访问的数据存储；**索引**是选取顶点记录的整数；**步长 stride**是同一数据流中相邻顶点记录起始位置的字节距离。1 字节等于 8 位，MiB 等于 1,048,576 字节。

文档基线：本地 Unity **6.7 Beta / 6000.7，2026-06-26**。公开 C# 源码例子固定 UnityCsReference `9d487cab41b00c50af020b56d27a3c768d54f770`，不声称它逐行匹配本地 Editor。

## 2. 几何角点与渲染顶点

一个立方体几何上有 8 个角点，但硬边、每面独立 UV 的常见表示为每个面 4 个顶点，共 24 个顶点记录。一个角点在三个面上的位置相同，但三份法线各自指向不同面，UV 也可能不同。

Triangle List 下，六个面、每面两个三角形，需要 `6×2×3=36` 个索引。**8 个角点、24 个顶点记录、36 个索引、12 个三角形，是四种不同计数。** 这不是所有立方体必须采用的唯一布局，而是明确条件下的常见例子。

Unity 常规 Mesh 的一个索引会选择该顶点的整套属性。不能在一个普通三角形索引里同时写“位置用第 3 项、UV 用第 9 项、法线用第 12 项”；这需要事先统一成顶点记录，或采用另外设计的顶点拉取方案。

## 3. 顶点布局：GPU 怎样解释字节

采用一个未压缩、单数据流布局：

| 属性 | 格式 | 分量数 | 字节数 | 记录内偏移 |
| --- | --- | --- | --- | --- |
| Position | Float32 | 3 | 12 | 0 |
| Normal | Float32 | 3 | 12 | 12 |
| UV0 | Float32 | 2 | 8 | 24 |
| 合计 | — | 8 | 32 | stride=32 |

属性地址的逻辑计算是：

$$
address=bufferBase+vertexIndex\times stride+attributeOffset
$$

这不是保证每次 Shader 输入都会单独发起对应 DRAM 读取；硬件可能合并请求并使用缓存。地址公式描述布局，实际流量还取决于缓存、格式和读取粒度。

同一顶点可以分布在多个 stream，例如位置与法线在 stream 0，颜色在 stream 1。每个 stream 有自己的 stride，属性还有 format/dimension/stream/offset。不要把 `float3` 的 C# 结构体大小直接当作任意 GPU Buffer、常量缓冲和 Shader 结构的共同布局规则。[Unity GetVertexBufferStride](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Mesh.GetVertexBufferStride.html)

`NORMAL`、`TEXCOORD0` 等 Shader 输入语义连接属性用途；格式还决定数据怎样转换，例如 UNorm8 将一个字节解释成 `k/255`。格式和语义共同参与正确读取，不能只看属性名称。

## 4. 索引范围、baseVertex 与子网格

单个子网格描述一段拓扑与索引使用信息，通常对应一个材质槽。多个子网格可以共享顶点缓冲；子网格不是一定拥有一份独立 Mesh。

绘制的逻辑输入常包含索引起点、索引数量与 baseVertex。简化地，最终顶点位置由“读出的索引 + baseVertex”定位。子网格和 baseVertex 的存在意味着局部索引范围与整个 Mesh 顶点总数不能机械画等号。

| 格式 | 每索引字节 | 注意事项 |
| --- | --- | --- |
| UInt16 | 2 | 数学上有 65536 个编码值，但最大码值可能在某些 API/GPU 上不可用，不能假定可跨平台安全引用 0xFFFF |
| UInt32 | 4 | 扩展索引范围，但需目标平台支持 |

Unity 默认常使用 16 位格式。`indexFormat` 改变时会清空索引缓冲并重设子网格数量，不能在已经填好的 Mesh 上随意修改而不重建相关数据。[Unity indexFormat](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Mesh-indexFormat.html)

## 5. 一个小而完整的容量计算

对上述明确的立方体布局：

- 顶点数据：`24×32=768` 字节。
- UInt16 索引：`36×2=72` 字节。
- 两者逻辑有效负载：840 字节。
- 改为 UInt32 索引：索引 144 字节，总计 912 字节。

这些数不包含对象元数据、对齐、CPU 可读副本、驱动分配、额外流、骨骼和 Blend Shape 数据。不能把 840 字节当作 Profiler 必须显示的全部运行时内存。

也不能用 36 个索引断定 VS 恰好调用 36 次。重复索引可能复用顶点结果，具体复用受硬件、拓扑、实例及 Draw 边界影响。多次 Pass 重绘也不保证免费共享上次 VS 的结果。

## 6. 为什么 RecalculateNormals 可能制造接缝

法线重算通常根据共享顶点及相关三角形产生结果。如果 UV 接缝让同一位置拆成两个顶点，它们未必共享参与计算的面，因此重算后可能在此出现不平滑边界。法线重算也不会自动生成切线；需要时还要处理切线。[Unity RecalculateNormals](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Mesh.RecalculateNormals.html)

**NPR 的两个不同需求：**

1. 主体着色法线可能故意保持硬边或由美术编辑。
2. 反壳描边外扩方向可能希望在位置接缝处平滑。

因此“按位置焊接所有顶点”“重算所有法线”“让描边沿主体法线扩张”都不能当作无条件修复。先定义每一套属性的用途，再决定是否增加独立平滑法线通道。硬边立方体就是能暴露错误合并的反例。

## 7. 只读 Mesh 审计脚本

保存为 `A06MeshAudit.cs`，挂到含 MeshFilter 的对象，运行组件菜单“Print Mesh Layout”。它只读取 `sharedMesh` 的布局与索引元数据，不重算法线，也不修改资源。

```csharp
using UnityEngine;

[RequireComponent(typeof(MeshFilter))]
public class A06MeshAudit : MonoBehaviour
{
    [ContextMenu("Print Mesh Layout")]
    private void PrintLayout()
    {
        Mesh mesh = GetComponent<MeshFilter>().sharedMesh;
        if (mesh == null) { Debug.Log("No mesh assigned."); return; }
        Debug.Log($"Mesh={mesh.name}, Vertices={mesh.vertexCount}, SubMeshes={mesh.subMeshCount}, IndexFormat={mesh.indexFormat}, Readable={mesh.isReadable}");
        long logicalVertexBytes = 0;
        for (int stream = 0; stream < mesh.vertexBufferCount; stream++)
        {
            int stride = mesh.GetVertexBufferStride(stream);
            logicalVertexBytes += (long)mesh.vertexCount * stride;
            Debug.Log($"Stream {stream}: stride={stride}");
        }
        foreach (var attribute in mesh.GetVertexAttributes())
        {
            int offset = mesh.GetVertexAttributeOffset(attribute.attribute);
            Debug.Log($"{attribute.attribute}: {attribute.format} x{attribute.dimension}, stream={attribute.stream}, offset={offset}");
        }
        for (int sub = 0; sub < mesh.subMeshCount; sub++)
            Debug.Log($"SubMesh {sub}: topology={mesh.GetTopology(sub)}, indexCount={mesh.GetIndexCount(sub)}, baseVertex={mesh.GetBaseVertex(sub)}");
        Debug.Log($"Logical vertex bytes={logicalVertexBytes}; excludes allocation overhead and other mesh data.");
    }
}
```

该脚本面向普通 MeshFilter、普通顶点流。它没有试图统计骨骼、Blend Shape 或所有底层分配，也没有把子网格索引数量之和当作严格去重的索引缓冲总容量。

实验步骤：检查一个 Cube 和一个平滑 Sphere，再检查带 UV 接缝的导入模型；记录顶点数、流布局、索引格式。对每一个重复位置，尝试说明哪些属性需要不同，而不是先认定它是浪费。

## 8. 源码边界、自测与验证

[固定提交的 Mesh.cs](https://github.com/Unity-Technologies/UnityCsReference/blob/9d487cab41b00c50af020b56d27a3c768d54f770/Runtime/Export/Graphics/Mesh.cs) 可追踪 `GetVertexAttributes`、`GetIndexCount`、`UploadMeshData` 等 C# 包装及调用入口；原生数据分配、实际 GPU 顶点缓存结构不由这些包装完整公开。

1. 为什么几何上 8 角点的立方体常有 24 顶点？**属性组合在面边界不同。**
2. 36 索引是否必然对应 12 三角形？**只在此处规定的 Triangle List 且数量有效等条件下成立。**
3. stride=32 是否等于 Normal 偏移？**否，此例 Normal 偏移是 12。**
4. RecalculateNormals 会自动恢复作者所有平滑与硬边意图吗？**不会。**

数值验证覆盖布局地址和容量例子；审计脚本已静态核对接口，尚未在 Editor 编译运行。本地来源：`E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en` 下的 `ScriptReference/Mesh-indexFormat.html`、`Mesh.RecalculateNormals.html`、`Mesh.GetVertexBufferStride.html`。

下一张：[A07｜GPU 资源、内存、缓存与上传](A07-GPU资源内存缓存与上传.md)。
