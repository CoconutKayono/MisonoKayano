# 图形学百科全书实验入口

这里集中说明 A 阶段 Unity 实验；B01—B04 见 [Shader 执行与图元实验](B01-B04实验说明.md)，B05—B08 见 [B 阶段检查点](B阶段检查点.md)，C01—C04 见 [深度优化、合成与附件实验](C01-C04实验说明.md)，C05—C08 与阶段汇总见 [C 阶段检查点](C阶段检查点.md)，D01—D04 见 [URP 调度与图实验](D01-D04实验说明.md)，D05—D08 与阶段汇总见 [D 阶段检查点](D阶段检查点.md)。后续实践以 Unity 操作、预期画面与排查方法为主，不要求使用 Python。

E01—E04 的明暗、阴影、Ramp 和面部空间实验见 [NPR 明暗实验说明](E01-E04实验说明.md)，包含六份可复制的 Unity 文件。E05—E08 的九份文件与完整阶段验收见 [E 阶段检查点](E阶段检查点.md)。

## 1. 从 Unity 实验开始

按卡片顺序复制下面的 C#/Shader，先预测修改结果，再在小场景里观察。数值例子保留在 Markdown 正文，不需要另开 Python。之前的三个 Python 脚本保留作历史核对资料，可完全跳过；以后不再新增。

## 2. Unity 数值实验

在已有或单独的 Unity 实验项目中，将下列文件复制到 `Assets/KnowledgeCards/`。每个类名与文件名相同，不需要其他自定义脚本。

| 文件 | 使用方法 | 关键预期 |
| --- | --- | --- |
| [A02SpaceLab.cs](A02SpaceLab.cs) | 挂到空对象，组件菜单执行 Print Space Experiment | 点 `(9,2,0)`，位移 `(-1,2,0)`，只旋转 `(-1,1,0)` |
| [A03ProjectionLab.cs](A03ProjectionLab.cs) | 挂到空对象，组件菜单执行 Print Projection Experiment | 近/远深度为 0/1；两个示例 xNDC 为 0.5/0.25 |
| [A04NormalLab.cs](A04NormalLab.cs) | 挂到空对象，组件菜单执行 Print Normal Experiment | 垂直检查 0.6/0；朝 +Y 光照约 0.447214/0.894427 |
| [A05ColorLab.cs](A05ColorLab.cs) | 挂到空对象，组件菜单执行 Print Color Experiment | 0.5 解码约 0.214041；线性 0.5 编码约 0.735357 |
| [A06MeshAudit.cs](A06MeshAudit.cs) | 挂到含 MeshFilter 的对象，执行 Print Mesh Layout | 输出真实顶点数、流步长与子网格元数据 |
| [A07BufferLab.cs](A07BufferLab.cs) | 挂到空对象，执行 Run Buffer Upload Example | 64 B 缓冲，16 B 部分写入；没有 Draw 或读回 |

[A08TextureAudit.cs](A08TextureAudit.cs) 使用 `UnityEditor`，应单独放入 `Assets/Editor/`。选中导入的 Texture2D，执行 `Tools/Encyclopedia/A08 Audit Selected Texture`；输出当前 Editor 纹理格式和导入设置，不代表设备驻留内存。

A03 自行构造教学矩阵，不读取项目真实相机的 GPU 投影。A02 与 A04 也自行构造矩阵，不修改对象 Transform。

## 3. Unity 明暗可视化

1. 使用 URP Forward 项目，将 [A01VectorLab.shader](A01VectorLab.shader) 复制到 `Assets/KnowledgeCards/`。
2. 创建材质选择 `Encyclopedia/A01VectorLab`，赋给一个有法线的 Sphere。
3. 关闭 Depth Priming、SSAO、额外 Renderer Feature 和后处理，使用普通单相机。实验使用材质指定的世界光方向，不需要场景灯光。
4. Normalize Normal 开启时，将 Normal Length Multiplier 从 1 改为 2，边界应不变。
5. 关闭 Normalize Normal 后再改长度，亮部应扩大。关闭 Show Two Bands 可看连续点积灰度。
6. 如果正面暂时全暗，调整 Surface To Light 的方向或相机观察位置，观察球体整体明暗关系。

这是一份只演示主体前向输出的教学 Shader，不包含完整阴影、深度法线、运动矢量、XR 或实例化支持。理解每个设置的范围后再扩展它。

## 4. 记录观察

完成单卡实验后，进入 [A 阶段检查点](A阶段检查点.md)，将 [AStageDataLab.shader](AStageDataLab.shader) 复制到 URP 项目。它提供法线、UV、位置、NdotL、颜色渐变五种视图；完整代码、项目条件和预期都保留在检查点 Markdown 内。

建议记录“输入与设置、修改前预测、实际数值或截图、是否吻合、仍未解释的问题”。用于准确读数时注意渲染目标和显示色彩编码；性能测量与调试抓帧另行进行。

A 阶段历史批次已运行数学校验；后续不再新增 Python 学习实验。上述 Unity 示例仅做源码接口和文本结构核对，尚未在 Editor 编译运行或进行 GPU 抓帧。用户完成实验后，才能更新对应的个人学习状态。
