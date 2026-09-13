# 四元数：为什么适合旋转插值以及如何在 Unity 中应用

> GAMES101 中没讲四元数。我不理解为什么说它主要解决插值问题，也不知道应该如何应用。

本文是连接 GAMES101 变换知识与 Unity 应用的补充，不是课件内容摘录。

## 1. 先把它理解为一种旋转表示

**在旋转问题中，单位四元数用四个数编码一个三维旋转。** 它既可以表示物体相对于参考坐标系的姿态，也可以表示一次要施加的旋转。

它不直接表示位置、缩放或旋转耗时。四个分量也不是四个空间坐标，更不是 X、Y、Z 三个欧拉角加一个额外角度。

| 表示方式  | 入门直觉            | 特点                         |
| ----- | --------------- | -------------------------- |
| 欧拉角   | 按指定顺序，绕三根轴分别转多少 | 适合人输入；有顺序、角度绕回与万向节锁问题      |
| 旋转矩阵  | 变换每个向量的坐标       | 适合参与整个矩阵变换管线；逐元素插值未必仍是旋转矩阵 |
| 单位四元数 | 把整体旋转编码成四个数     | 便于组合旋转、保持旋转表示、进行姿态插值       |

Unity 内部用四元数存储旋转，Inspector 通常显示欧拉角，方便编辑。[Unity 官方：旋转与方向](https://docs.unity3d.com/6000.0/Documentation/Manual/QuaternionAndEulerRotationsInUnity.html)

## 2. 插值究竟在问什么？

插值就是：**已知起点和终点，求处于进度 t 的中间状态。**

位置从 0 移到 10，半程是 5。旋转插值则在问：“物体从姿态 A 转到姿态 B，半程应该是什么姿态？”

只看绕一根固定轴的旋转：从 350° 转到 10°。

| 进度 | 把角度当普通数字插值 | 沿较短的旋转路径 |
| --- | --- | --- |
| 0 | 350° | 350° |
| 0.5 | 180° | 0°，也可写成 360° |
| 1 | 10° | 10° |

普通算术的中点 $(350+10)/2=180$ 没算错，但它选了倒退 340° 的长路，而不是向前 20° 的短路。

**单轴问题用角度专用插值就可以处理，并不非得用四元数。** 这个例子只是帮助区分“数字之间的中点”和“旋转之间的中间姿态”。

三维中分别插值 X、Y、Z 欧拉角，又会受到旋转顺序、同一姿态的不同角度表示、万向节锁等影响，未必得到希望的整体转动路径。

## 3. 四元数为什么适合插值？

用于旋转的四元数满足：

$$
x^2+y^2+z^2+w^2=1
$$

可以类比“单位圆上的点”：沿圆弧走，中间点仍在圆上；两点直接取坐标平均，却可能落在圆内。单位四元数实际上位于四维空间的单位球面，这个二维圆只是帮助想象，不能当成三维物体的实际运动轨迹。

**Slerp 沿单位四元数球面上的弧线插值，中间结果仍是有效的旋转。** 对固定起终点、选择短弧并让 t 均匀增加时，对应恒定角速度的旋转。

还需知道：q 和 -q 表示相同旋转。常见最短路径插值会处理这个符号选择，而不是随便对四个分量取平均。恰好相差 180° 时，最短方向可能不唯一。

因此，“四元数解决插值”更准确地说是：它提供适合插值的表示，再配合正确的插值算法。它也用于存储和组合旋转，并非只用来插值。[Unity 官方：Quaternion.Slerp](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Quaternion.Slerp.html)

## 4. 为什么四个数能表示旋转？现在理解到轴角就够了

绕原点的三维旋转，可以描述成：**绕一根单位轴 n 转 θ 角度。**

设 $\mathbf n=(n_x,n_y,n_z)$，单位四元数的一种写法为：

$$
q=(x,y,z,w)=\left(n_x\sin\frac\theta2,\ n_y\sin\frac\theta2,\ n_z\sin\frac\theta2,\ \cos\frac\theta2\right)
$$

前三个数将轴与角度共同编码，第四个数也参与编码角度。因为存在单位长度约束，四个数并不是四个独立自由度。

例：绕 Y 轴旋转 90°，得到近似 $(0,0.7071,0,0.7071)$，不是 $(0,90,0,1)$。

半角来自四元数表示旋转的数学构造，与通过 $qvq^{-1}$ 作用到向量、q 和 -q 表示同一旋转等性质相联系。**这里不把它当成已经推导出的结论；目前使用 Unity 不需要先证明半角，也不需要手写分量。**

```csharp
Quaternion q = Quaternion.AngleAxis(90f, Vector3.up);
```

让 API 做这个编码即可，角度参数使用度。[Unity 官方：Quaternion.AngleAxis](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Quaternion.AngleAxis.html)

## 5. Unity 的实际用法

### A. 表示与应用旋转

```csharp
// 从便于人理解的欧拉角生成一个旋转。
Quaternion q = Quaternion.Euler(0f, 90f, 0f);

// 设置物体的世界姿态：直接到达，没有动画过程。
transform.rotation = q;

// 用该旋转转动一个方向向量。
Vector3 rotatedDirection = q * Vector3.forward;
```

`q * v` 得到旋转后的向量，不会平移。`rotation` 是世界姿态，`localRotation` 是相对父物体的姿态。

### B. 组合旋转

```csharp
Quaternion combined = qA * qB;
Vector3 result = combined * v;
// 等价于 qA * (qB * v)
```

对同一固定坐标系中的向量作用，右边的 qB 先作用。Unity 文档也会从“先 A，再绕 A 转过后的局部轴做 B”解释同一乘积；这是局部轴与固定轴描述的差别。乘法一般不可交换。[Unity 官方：四元数乘法](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Quaternion-operator_multiply.html)

### C. 角色逐渐转向目标：限制每秒转多少度

下面是可保存为 `TurnTowardsTarget.cs` 的示例。假设模型本地 +Z 是前方，并只在水平面转向。

```csharp
using UnityEngine;

public class TurnTowardsTarget : MonoBehaviour
{
    public Transform target;
    [Min(0f)] public float degreesPerSecond = 90f;

    void Update()
    {
        if (target == null) return;

        Vector3 direction = target.position - transform.position;
        direction.y = 0f;
        if (direction.sqrMagnitude < 0.000001f) return;

        Quaternion desired = Quaternion.LookRotation(direction, Vector3.up);
        transform.rotation = Quaternion.RotateTowards(
            transform.rotation, desired,
            degreesPerSecond * Time.deltaTime);
    }
}
```

这里 direction 表示“目标在哪个方向”；LookRotation 构造“使本地 +Z 朝向它的姿态”；RotateTowards 每帧朝目标姿态迈出有限角度。前方与上方共同用于确定姿态，只有一根朝向不能唯一确定物体绕自身前方轴的滚转。

来源：[LookRotation](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Quaternion.LookRotation.html)、[RotateTowards](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Quaternion.RotateTowards.html)。

### D. 两秒从固定姿态 A 转到固定姿态 B

下面的方法放进一个 MonoBehaviour 类，通过 `StartCoroutine(RotateOverTime(goal, 2f))` 启动，同一物体不要同时启动多个相互争夺旋转的协程。

```csharp
System.Collections.IEnumerator RotateOverTime(Quaternion goal, float duration)
{
    Quaternion start = transform.rotation;
    if (duration <= 0f)
    {
        transform.rotation = goal;
        yield break;
    }

    float elapsed = 0f;
    while (elapsed < duration)
    {
        elapsed += Time.deltaTime;
        float t = Mathf.Clamp01(elapsed / duration);
        transform.rotation = Quaternion.Slerp(start, goal, t);
        yield return null;
    }
    transform.rotation = goal;
}
```

关键是 start 与 goal 在这一段动画中固定，t 是从 0 到 1 的进度。不是每一帧重新用当前旋转当作固定起点。

`Slerp(current, goal, speed * deltaTime)` 是另一种反复接近目标的用法：目标固定时通常越接近越慢；不能把那个 speed 当成“度/秒”，也不能保证指定时间到达。固定时长用固定端点与时间进度；限制角速度用 RotateTowards。

## 6. 它不会自动解决什么？

- 四元数保存姿态，不保存转过几圈。0° 和 360° 终态相同；要做连续多圈动画，需要额外保存累计角度或路径。
- 用四元数保存，不等于每帧读取欧拉角再插值就能避开欧拉角问题。
- 平滑姿态插值不会自动保证摄像机不穿墙、角色不碰撞。
- 想指定特殊轨迹或大于 180° 的长路，需要额外设计，不能只给两端姿态。

## 7. 当前只需记住

> **四元数表示整体旋转；乘向量是应用旋转；乘四元数是组合旋转；Slerp 是求中间姿态。**

现在不必背分量公式。先会“生成目标姿态 → 选择如何转过去 → 应用到物体”，再研究内部代数。

代码根据官方 API 核对，未在 Unity 编辑器内运行验证。

相关笔记：[[FAQ索引]] · [[变换顺序：为什么TRS是先缩放再旋转最后平移]] · [[Unity是左手坐标系还是右手坐标系]]
