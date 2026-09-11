# Occlusion Culling 窗口参考

> 原文：[Occlusion Culling window reference](https://docs.unity3d.com/6000.7/Documentation/Manual/occlusion-culling-window.html)

从顶部菜单选择 **Window > Rendering > Occlusion Culling**，打开 Occlusion Culling 窗口。

Occlusion Culling 窗口包含 **Object**、**Bake** 和 **Visualization** 三个选项卡。当 Occlusion Culling 窗口和 Scene view 都可见时，Scene view 中还会显示 Occlusion Culling popup。

## Object 选项卡

![Mesh Renderer 的 Occlusion Culling 窗口](OcclusionCullingInspectorObject.png)

在 **Object** 选项卡中，可以点击 **All**、**Renderers** 和 **Occlusion Areas** 按钮，过滤 Hierarchy 窗口中的内容。

启用 **Renderers** 过滤器时，在 Hierarchy 窗口或 Scene view 中选择 Renderer，可以在 Occlusion Culling 窗口中查看和更改其 Occlusion Culling 设置。

启用 **Occlusion Areas** 过滤器时，在 Hierarchy 窗口或 Scene view 中选择 Occlusion Area，可以在 Occlusion Culling 窗口中查看和更改其 **Is View Volume** 设置。也可以点击 **Create New Occlusion Area**，在 Scene 中创建新的 Occlusion Area。

## Bake 选项卡

在 **Bake** 选项卡中，可以微调 Occlusion Culling 烘焙过程的参数，在烘焙时间、运行时数据大小和视觉效果之间取得平衡。

**Set Default Parameters** 按钮会将参数重置为默认值。

![Occlusion Culling Inspector 的 Bake 选项卡](OcclusionCullingInspectorBake.png)

| 设置 | 说明 |
| --- | --- |
| **Smallest Occluder** | 能够遮挡其他 GameObject 的最小 GameObject 尺寸，单位为米。通常应选择能够在 Scene 中产生良好结果的最高值，以获得最小文件和最快烘焙速度。 |
| **Smallest Hole** | Camera 能够看到的最小间隙直径，单位为米。通常应选择能够在 Scene 中产生良好结果的最高值，以获得最小文件和最快烘焙速度。 |
| **Backface Threshold** | 如果需要减少烘焙数据大小，Unity 可以在烘焙时对 Scene 进行采样，排除可见遮挡物几何体中背面超过指定百分比的区域。背面比例高的区域可能位于几何体下方或内部，不太可能是 Camera 运行时所在的位置。默认值 100 不会从数据中移除区域；较低值会减小文件大小，但可能造成视觉伪影。 |

Bake 选项卡底部有 **Bake** 和 **Clear** 按钮。点击 **Bake** 烘焙 Occlusion Culling 数据，点击 **Clear** 移除之前烘焙的数据。

## Visualization 选项卡

当 **Visualization** 选项卡可见时，在 Scene view 或 Hierarchy 窗口中选择 Camera，Unity 会更新 Scene view，从所选 Camera 的视角显示 Occlusion Culling 效果。可以使用 Scene view 中的 Occlusion Culling popup 配置可视化效果。

## Scene view 中的 Occlusion Culling popup

Occlusion Culling popup 有 **Edit** 和 **Visualization** 两种模式，可以使用下拉菜单切换。

### Edit 模式

| 设置 | 说明 |
| --- | --- |
| **View Volumes** | 启用时，Scene view 中会显示代表 Occlusion Culling 数据中 cells 的蓝线。cell 大小受 **Smallest Occluder** 设置影响：值越低，cell 越多且越小，精度越高，文件也越大。 |

## Visualization 模式

Visualization 模式可以从指定 Camera 的视角预览 Occlusion Culling 结果。如果已选择 Camera，预览与该 Camera 相关；否则，预览与上次在 Visualization 模式中选择的 Camera 相关。

| 设置 | 说明 |
| --- | --- |
| **Camera Volumes** | 启用时，可以看到表示 Unity 生成 Occlusion Culling 数据区域的黄色线框。该区域根据 Scene 几何体以及使用 Occlusion Area 定义的 View Volume 确定。当 Camera 位于黄色线框外时，Unity 不执行 Occlusion Culling。还可以看到表示 Camera 当前所在 cell 及其细分的灰线。**Smallest Hole** 设置定义 cells 内细分的最小大小：值越低，每个 cell 中的细分越多且越小，精度越高，文件也越大。 |
| **Visibility Lines** | 启用时，可以看到表示当前选中 Camera 能看到内容的绿色线。 |
| **Portals** | 启用时，可以看到表示 Occlusion 数据中 cells 之间连接的线。当前可见的 Portals 是当前选中 Camera 能看到的 Portals。 |

---

## 文档导航
- 上一页：[[06-使用Occlusion Portal控制区域遮挡]]
- 目录：[[00-使用遮挡剔除排除隐藏对象]]
- 下一页：[[00-CullingGroup API]]
