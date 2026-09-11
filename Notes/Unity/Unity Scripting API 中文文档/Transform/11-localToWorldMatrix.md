> 原文：[Transform.localToWorldMatrix](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-localToWorldMatrix.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).localToWorldMatrix

public Matrix4x4 localToWorldMatrix;

### 描述

将点从局部空间变换到世界空间的矩阵。（只读）

也可以使用 Transform.TransformPoint 代替此矩阵来变换坐标。不要使用此矩阵设置着色器参数或执行与渲染有关的计算。请改用 Renderer.localToWorldMatrix。


