# 新手分支的 Unity 示例

四个 Shader 分别对应 N00—N03，完整内容也保留在各张卡末尾。只复制正在学的那一个到 URP 项目的 `Assets/BeginnerNPR/`，创建材质并选择对应 Shader，再赋给 Cube。

| 文件 | 材质 Shader 名称 |
| --- | --- |
| [N00Color.shader](N00Color.shader) | BeginnerNPR/N00Color |
| [N01VectorMove.shader](N01VectorMove.shader) | BeginnerNPR/N01VectorMove |
| [N02UnitDirection.shader](N02UnitDirection.shader) | BeginnerNPR/N02UnitDirection |
| [N03SpaceMove.shader](N03SpaceMove.shader) | BeginnerNPR/N03SpaceMove |

使用 Unity 6 URP 测试场景，Cube 先保持单位缩放，固定相机并留出移动空间。若开启 Depth Priming，本组先关闭；这批简短 Shader 不包含它所需的额外深度 Pass，原理现在不用学。

示例不计算灯光、不接收阴影。N01—N03 只改变绘制位置，不改变 Transform 或碰撞体。它们用于学习单个问题，不是角色生产材质。

先预测，再按卡片改变一个变量。文件与文内完整示例应一致；本轮尚未在 Unity 编译或运行，不将文字预测当作实测结果。没有 Python 学习实验。
