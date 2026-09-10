# 概述
DouyinSDK 是一款基于 Unity 开发的 SDK（软件开发工具包），因此你可以使用 UGUI（Unity 图形用户界面系统）对任意界面（UI）进行自定义开发。

* 世界主UI当前设计如下，当前已支持横竖屏切换模式
* **如果需要新增UI的创作者，请先避开已有内容区域**；后续也会提供扩展菜单功能，支持更多功能入口显示在世界主菜单内

目前我们支持[UGUI](https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/index.html)自定义任何 UI 界面，界面符合移动端规范即可。
可使用[Canvas Scaler ](https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/script-CanvasScaler.html)来适配界面，分辨率建议1170*2532。
为了UI的清晰，建议手动在UI图Inspector 面板中取消“生成 Mip Maps”的选项。

# 默认UI布局样式
抖音造世界提供用于创建世界的基本用户界面功能。如果您不进行任何操作，进入世界后将看到如下所示的用户界面：
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/6f7048a538be4befabaae15ec92ee026~tplv-goo7wpa0wc-image.image)
# 层级规则
我们世界里提供了大量原生的UI，部分UI的层级独立于Unity的UI层级，参照上图的区域分类，下表描述了各类的UI层级。
| **层级定义** | **UI规则** | **Unity层级Sort Order区间** | **UI类型** |
| --- | --- | --- | --- |
| 世界玩法UI | 创作者自定义UI区间，该层级会展示在官方主界面&角色UI之下 | < -10 | UGUI <br>  |
| 小火人层UI | 角色昵称 | -10 到 -1 <br>  |  |
|  | 角色聊天气泡 |  |  |
| 主界面UI | 包含操作区域、用户聊天区域 | 0 |  |
| 世界玩法 UI | 创作者自定义UI区间，该层级会展示在官方主界面层级&角色UI之上 | 1 - 999 |  |
| 系统级原生应用层UI <br>  | 平台功能UI：包含相机、分享、横竖屏切换、表情动作等功能按钮区域 | 无限高，该层级的UI仅支持通过部分API进行隐藏或禁用 <br>  | Native |
|  | 世界通知弹窗 |  |  |
|  | 世界Loading UI |  |  |
|  | 系统通知弹窗（断线重连） |  |  |

* 作为创作者，世界内玩法UI 可以满足您的需求。创建 UI 层时，将其排序调整到推荐值将为您带来最佳的视觉体验。
* 希望您能从以上层级规范中，并创造出具有出色视觉效果的世界！

# UI层级设计参考（以官方口袋营地玩法为例）
| 命名 | Sort order | 建议实现 |
| --- | --- | --- |
| Lowest | -100 - 0 | 最低层级，通常用于部分世界3D场景物体挂载的2DUI |
| Low | 1 - 99 | 低层级，用于实现世界主玩法功能导航 |
| Normal | 100 - 199 | 展开式功能面板，用于实现例如新手引导等功能 |
| High | 200 - 299 | 弹出式功能面板（例如：任务面板、背包界面） |
| Top | 300 - 399 | 高优先级通知弹窗（例如：更新公告、游戏通知） |
| None | 400 - 499 | 重要系统级通知弹窗（例如：系统级通知、停服更新等） |
## 部分UI界面的显隐藏API导航

1. 隐藏所有的非Unity层级的官方UI界面：[DouyinUIService.SetNativeUIVisible](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=hprylxp2)
2. 禁用/隐藏部分功能的UI界面：
   1. 禁用/隐藏飞行：[DouyinActor.DisableFly(bool hideUI)](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=2jpwykdn)
   2. 禁用/隐藏牵手：[DouyinActor.DisableHoldHand(bool hideUI = true)](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=poqilqxg)
   3. 禁用合养精灵形象切换：[DouyinPlayerSettings.allowActorChange](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=w5k1e7k0)
   4. 禁用合养精灵动作：[DouyinPlayerSettings.allowAction](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=mu7s8uxh)
   5. 禁用合养精灵表情：[DouyinPlayerSettings.allowEmotion](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=pioq15ec)
   6. 禁用合养精灵重生功能：[DouyinPlayerSettings.allowRespawn](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fpn1oipz)

# 保持UI清晰
为了使世界运行更流畅，在云处理过程中，世界中超过 1024 x 1024 尺寸的纹理将被压缩。然而，UI Sprite通常需要清晰显示。因此，如果您发现某个应该清晰显示的UI Sprite被压缩了，请在 Unity 项目中找到对应的UI Sprite，并在 Inspector 面板中取消选中“生成 Mip Maps”，这将防止纹理被压缩。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/3e3c5a3ab761459b946517b6761f201d~tplv-goo7wpa0wc-image.image" width="264px" /></div>


