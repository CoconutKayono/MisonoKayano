# D 阶段检查点｜把相机调度、资源、光源与错误像素连起来

## 1. 阶段目标与当前状态

本阶段训练从 Unity 相机组织一直追到 GPU 可见状态的能力：谁筛选对象、谁选择 Shader Pass、谁生产纹理、谁读取光源，以及哪个事件第一次产生错误结果。它不是要求记住所有源码行号。

D01—D08 八张独立卡已生成。本文为实验导航与验收题；**卡片生成不代表 Unity 已编译运行，也不代表读者已经掌握**。各卡保留完整必要代码与操作条件，可脱离本导航使用。

本地文档为 Unity 6.7 Beta / 6000.7、2026-06-26 构建，根目录 `E:\Claude Skills\学习仓库\09_Unity官方文档\Documentation\en`。固定 Graphics 提交 `275a7f9ad9330e3cf7f3ea57a0b242a551fde291` 的包 manifest 是 URP/Core 17.0.4、6000.0。特别注意 D07 完整 Shader 使用本地 6000.7 的 `_CLUSTER_LIGHT_LOOP` 接口；旧接口的替换表在卡片内。

## 2. 实验入口

| 卡片 | 文件或操作入口 | 要留下的证据 |
| --- | --- | --- |
| [D01 相机与 RendererList](../04-Unity与URP调度/D01-相机入口剔除与RendererList.md) | [D01RendererListFeature.cs](D01RendererListFeature.cs)、[D01ListLab.shader](D01ListLab.shader) | 对象为何进入或离开绘制列表 |
| [D02 Pass 与状态](../04-Unity与URP调度/D02-PassLightMode与状态覆盖.md) | [D02StateOverrideFeature.cs](D02StateOverrideFeature.cs)、[D02PassLab.shader](D02PassLab.shader) | Pass 标签与最终深度状态的对应 |
| [D03 图记录与执行](../04-Unity与URP调度/D03-RenderGraph记录编译与执行.md) | [D03PosterizeFeature.cs](D03PosterizeFeature.cs)、[D03Posterize.shader](D03Posterize.shader) | 记录、执行回调与颜色生产消费关系 |
| [D04 资源寿命](../04-Unity与URP调度/D04-RenderGraph资源寿命依赖与导入.md) | [D04LifetimeFeature.cs](D04LifetimeFeature.cs) | 内部无用结果与导入资源写入的裁剪区别 |
| [D05 相机数据](../04-Unity与URP调度/D05-相机深度法线与运动矢量生产路径.md) | [D05CameraDataFeature.cs](D05CameraDataFeature.cs)、[D05CameraData.shader](D05CameraData.shader) | 深度、法线、运动分别由哪个节点生成，包含哪些对象 |
| [D06 提交机制](../04-Unity与URP调度/D06-排序SRPBatcher实例化与GPU驱动.md) | [D06SubmissionLab.cs](D06SubmissionLab.cs)，外部输入为 URP/Lit 材质 | SRP batch、Draw、instance count 与计时分开记录 |
| [D07 光源循环](../04-Unity与URP调度/D07-URP光源数据与ForwardPlus.md) | [D07LightLoop.shader](D07LightLoop.shader) | 路径关键字、附加方向光/局部光响应、循环访问次数 |
| [D08 像素追踪](../04-Unity与URP调度/D08-从像素到抓帧事件与源码.md) | [D08TraceLab.shader](D08TraceLab.shader)，两个 Quad | 黑色中心的颜色与深度因果链、两种单变量修复 |

前四张具体设置也集中于 [D01—D04 实验说明](D01-D04实验说明.md)。新增五份 Unity 文件从 D05—D08 正文导出，没有新增 Python 学习实验。

## 3. 推荐执行顺序

先在独立的小场景按单卡基线运行。不要同时启用所有 Feature：有的会替换相机颜色，有的额外请求法线/运动，有的覆盖深度状态，会让另一张卡的预测前提失效。

1. 完成 D01/D02，区分“对象筛选”“Pass 选择”“最后是否写入像素”。
2. 完成 D03/D04，画出至少一个资源生产者与消费者，解释一个被裁剪节点。
3. 单独开启 D05，依次观察 Depth、Normals、Motion，记录每种模式生产图的变化。
4. 关闭数据视图，完成 D06 的 Renderers / 显式实例化对照；核对事件后关闭抓帧工具再测性能。
5. 使用 D07 独立材质场景，先少量光，再增加光源，比较 Forward 与 Forward+。不要同时开启 D05 的法线需求来判断这个只有主体 Pass 的 Shader 是否完整。
6. 最后独立运行 D08 的两个 Quad。先写出中心像素预测，再逐事件确认颜色与深度。

## 4. 阶段作品：一份可复核的渲染诊断记录

作品不是复杂角色成片，而是一份小场景诊断文档，应包含以下六项：

| 项目 | 合格标准 |
| --- | --- |
| 工程基线 | Unity、URP、图形 API、GPU、相机、Renderer、分辨率与开关明确 |
| 对象与 Pass | 指出一个对象为何出现在主体 Pass，却未必出现在法线或运动 Pass |
| 资源生产消费图 | 标出至少一张数据纹理的生产节点、读取节点与当前帧有效时机 |
| 提交证据 | 用一个例子说明 Draw、SRP batch 与 instance count 不是同一数量 |
| 光源证据 | 记录实际关键字，并说明非主方向光与局部光如何进入循环 |
| 错误像素因果链 | 找到首次偏离预期的资源/事件，用单变量修改验证原因 |

不用额外写脚本来“证明自己学会”。Unity 观察、必要数值和抓帧证据足以支撑上述记录；不能把无实测的预测截图或毫秒数填入结果栏。

## 5. 过关题与参考答案

1. **主体可见、法线图没有角色，最先查什么？** 法线资源的生产路径、匹配 Pass、对象筛选与几何一致性，而不是最终描边阈值。
2. **UseTexture(Read) 能替代 ConfigureInput(Motion) 吗？** 不能。前者声明图依赖，后者把输入需求提供给 URP 的生产安排。
3. **CPU 日志出现“图回调执行”，GPU 是否已经完成？** 不能推出；回调主要记录 GPU 命令。
4. **导入纹理只被读取，输出没人用，Pass 是否必定保留？** 不必。固定源码区分只读和写入外部资源的副作用。
5. **SRP Batcher 开启后 Draw 数没降，如何判断价值？** 核对兼容批次及 CPU 准备/提交时间，不能只看 Draw 数。
6. **一个实例 Draw 是否自动保证逐实例透明排序？** 不保证，整体批次的排序粒度必须符合场景需求。
7. **Forward+ 下手写 count 次循环为何可能漏光？** 固定旧实现的 count 返回零，而宏实际遍历空间分组；还需单独处理非主方向光。
8. **两个灯各为 0.4，阈值 0.5，先阈值后求和与先求和后阈值相同吗？** 不同，分别为 0 和 1，说明 NPR 色阶的合成顺序是模型的一部分。
9. **一个红色 Shader 产生黑色中心，是否必定编译失败？** 不必，D08 的 ColorMask 0 保留背景，深度仍遮挡后方物体。
10. **图 Viewer、Frame Debugger、RenderDoc 的三个事件数不同，是否有工具错了？** 不必，它们观察的抽象层不同，需要通过资源与状态建立对应。

## 6. 下一阶段

D 阶段补齐了“数据从哪里来、哪些命令真正影响像素”的链路。下一张是 [E01：Lambert 基线与艺术化明暗](../05-NPR明暗材质与描边/E01-Lambert基线与艺术化明暗.md)。E01—E08 已全部生成，前半入口见 [E01—E04 实验说明](E01-E04实验说明.md)，完整阶段验收见 [E 阶段检查点](E阶段检查点.md)。

当前仅完成文档、固定源码/API 核对与文件结构检查；**Unity 编译、GPU 捕获、设备测时和个人学习验证均待执行**。完整状态见 [学习进度](../00-学习导航/学习进度.md)。
