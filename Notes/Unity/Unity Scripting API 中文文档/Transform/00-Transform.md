> 原文：[Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html)

# Transform

- 命名空间：UnityEngine
- 继承自：[Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)

### 描述

对象的位置、旋转和缩放。

Scene 中的每个对象都有一个 Transform。Transform 用于存储和操作对象的位置、旋转和缩放。每个 Transform 都可以有一个父级，从而可以按层级应用位置、旋转和缩放，这就是 Hierarchy 窗口中显示的层级。

Transform 还支持枚举器，因此可以使用 foreach 遍历子对象：

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    // 将所有 Transform 子对象向上移动 10 个单位。
    void Start()
    {
        foreach (Transform child in transform)
        {
            child.position += Vector3.up * 10.0f;
        }
    }
}
~~~

相关资源：[Transform 组件参考](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Transform.html)、[Physics](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Physics.html)。

### 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-childCount]] | childCount | 父 Transform 拥有的子对象数量。 |
| [[02-eulerAngles]] | eulerAngles | 以度数表示的 Euler 角旋转。 |
| [[03-forward]] | forward | 返回表示 Transform 世界空间蓝轴的归一化向量。 |
| [[04-hasChanged]] | hasChanged | 自上次将标志设为 false 后，Transform 是否发生了变化。 |
| [[05-hierarchyCapacity]] | hierarchyCapacity | Transform 层级数据结构的容量。 |
| [[06-hierarchyCount]] | hierarchyCount | Transform 层级数据结构中的 Transform 数量。 |
| [[07-localEulerAngles]] | localEulerAngles | 相对于父 Transform 旋转、以度数表示的 Euler 角旋转。 |
| [[08-localPosition]] | localPosition | 相对于父 Transform 的位置。 |
| [[09-localRotation]] | localRotation | 相对于父 Transform 旋转的 Transform 旋转。 |
| [[10-localScale]] | localScale | 相对于 GameObject 父级的 Transform 缩放。 |
| [[11-localToWorldMatrix]] | localToWorldMatrix | 将点从局部空间变换到世界空间的矩阵。（只读） |
| [[12-lossyScale]] | lossyScale | 对象的全局缩放。（只读） |
| [[13-parent]] | parent | Transform 的父级。 |
| [[14-position]] | position | Transform 的世界空间位置。 |
| [[15-right]] | right | Transform 在世界空间中的红轴。 |
| [[16-root]] | root | 返回层级中最顶层的 Transform。 |
| [[17-rotation]] | rotation | 在世界空间中存储 Transform 旋转的 Quaternion。 |
| [[18-up]] | up | Transform 在世界空间中的绿轴。 |
| [[19-worldToLocalMatrix]] | worldToLocalMatrix | 将点从世界空间变换到局部空间的矩阵。（只读） |

### 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[20-DetachChildren]] | DetachChildren | 解除目标对象所有子对象的父级关系。 |
| [[21-Find]] | Find | 按名称查找子对象并返回它。 |
| [[22-GetChild]] | GetChild | 按索引返回 Transform 子对象。 |
| [[23-GetLocalPositionAndRotation]] | GetLocalPositionAndRotation | 使用当前局部空间位置和旋转更新 out 参数。 |
| [[24-GetPositionAndRotation]] | GetPositionAndRotation | 使用当前世界空间位置和旋转更新 out 参数。 |
| [[25-GetSiblingIndex]] | GetSiblingIndex | 获取此 Transform 相对于其同级对象的索引。 |
| [[26-InverseTransformDirection]] | InverseTransformDirection | 将方向从世界空间变换到局部空间。 |
| [[27-InverseTransformDirections]] | InverseTransformDirections | 将多个方向从世界空间变换到局部空间，并覆盖原方向。 |
| [[28-InverseTransformPoint]] | InverseTransformPoint | 将位置从世界空间变换到局部空间。 |
| [[29-InverseTransformPoints]] | InverseTransformPoints | 将多个位置从世界空间变换到局部空间，并覆盖原位置。 |
| [[30-InverseTransformVector]] | InverseTransformVector | 将向量从世界空间变换到局部空间。 |
| [[31-InverseTransformVectors]] | InverseTransformVectors | 将多个向量从世界空间变换到局部空间，并覆盖原向量。 |
| [[32-IsChildOf]] | IsChildOf | 判断此 Transform 是否是 parent 的子对象。 |
| [[33-LookAt]] | LookAt | 旋转 Transform，使 forward 向量指向 target 的当前位置。 |
| [[34-Rotate]] | Rotate | 以多种方式旋转 GameObject。 |
| [[35-RotateAround]] | RotateAround | 围绕穿过世界坐标 point 的轴旋转 Transform。 |
| [[36-SetAsFirstSibling]] | SetAsFirstSibling | 将 Transform 移到局部 Transform 列表的开头。 |
| [[37-SetAsLastSibling]] | SetAsLastSibling | 将 Transform 移到局部 Transform 列表的末尾。 |
| [[38-SetLocalPositionAndRotation]] | SetLocalPositionAndRotation | 在局部空间中设置 Transform 的位置和旋转。 |
| [[39-SetParent]] | SetParent | 设置 Transform 的父级。 |
| [[40-SetPositionAndRotation]] | SetPositionAndRotation | 设置 Transform 的世界空间位置和旋转。 |
| [[41-SetSiblingIndex]] | SetSiblingIndex | 设置同级索引。 |
| [[42-TransformDirection]] | TransformDirection | 将方向从局部空间变换到世界空间。 |
| [[43-TransformDirections]] | TransformDirections | 将多个方向从局部空间变换到世界空间，并覆盖原方向。 |
| [[44-TransformPoint]] | TransformPoint | 将位置从局部空间变换到世界空间。 |
| [[45-TransformPoints]] | TransformPoints | 将多个点从局部空间变换到世界空间，并覆盖原点。 |
| [[46-TransformVector]] | TransformVector | 将向量从局部空间变换到世界空间。 |
| [[47-TransformVectors]] | TransformVectors | 将多个向量从局部空间变换到世界空间，并覆盖原向量。 |
| [[48-Translate]] | Translate | 沿 Transform 的 x、y、z 轴移动。 |

### 继承成员

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[../Object/01-hideFlags]] | hideFlags | 控制对象是否隐藏、是否随场景保存以及用户是否可以编辑对象。 |
| [[../Object/02-name]] | name | 对象的名称。 |
| [[../Object/03-GetEntityId]] | GetEntityId | 获取对象的 EntityId。 |
| [[../Object/04-GetHashCode]] | GetHashCode | 返回对象的哈希代码。 |
| [[../Object/05-ToString]] | ToString | 返回对象的名称。 |

### 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    // Moves all transform children 10 units upwards!
    void Start()
    {
        foreach ( Transform  child in transform)
        {
            child.position +=  Vector3.up  * 10.0f;
        }
    }
}
~~~


