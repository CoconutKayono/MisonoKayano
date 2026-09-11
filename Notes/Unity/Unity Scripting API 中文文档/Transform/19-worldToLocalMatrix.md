> 原文：[Transform.worldToLocalMatrix](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-worldToLocalMatrix.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).worldToLocalMatrix

public Matrix4x4 worldToLocalMatrix;

### 描述

将点从世界空间变换到局部空间的矩阵。（只读）

也可以使用 Transform.InverseTransformPoint 代替此矩阵来变换坐标。不要使用此矩阵设置着色器参数或执行与渲染有关的计算。请改用 Renderer.worldToLocalMatrix。


