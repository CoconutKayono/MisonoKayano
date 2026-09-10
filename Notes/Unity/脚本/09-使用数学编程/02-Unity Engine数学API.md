# Unity Engine 数学 API

> 原文：[Unity Engine math APIs](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-engine-math.html)

`UnityEngine` 包含最适合在使用 [Mono Scripting Backend](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-mono.html) 进行即时编译（JIT）的项目中使用的数学 API。其中包括用于常见数学函数的 [`Mathf`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.html) 类，支持三角函数、对数函数和其他运算；以及用于表示数据结构的 [`Vector2`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html)、[`Vector3`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html)、[`Matrix4x4`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Matrix4x4.html)、[`Quaternion`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Quaternion.html) 和 [`UnityEngine.Random`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Random.html) 等类。

对于未使用 [Burst](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html) 编译的代码，建议使用 `UnityEngine` 数学 API。在由 Burst 编译的代码中，应改用针对 Burst 编译进行优化的 [`Unity.Mathematics`](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-mathematics.html) API。

| 页面 | 说明 |
| --- | --- |
| [[02-Unity Engine数学API/01-使用Mathf进行常见数学运算]] | 使用 Unity 的 [`Mathf`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Mathf.html) 类，执行游戏开发中常用的三角函数、对数函数和其他数学函数。 |
| [[02-Unity Engine数学API/02-使用Vector类移动对象]] | 使用 Unity 的 2D、3D 和 4D Vector 类执行 Vector 运算，以管理对象的位置和速度，以及对象之间的距离。 |
| [[02-Unity Engine数学API/03-使用Random类生成随机数]] | 使用 [`Random`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Random.html) 类生成游戏开发中常用的各种随机值。 |
| [[02-Unity Engine数学API/04-使用Quaternion控制旋转]] | 在 Unity 的左手坐标系中使用 Euler 角或 Quaternion，控制 GameObject 的旋转和朝向。 |

## 其他资源

- [Unity Mathematics API](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-mathematics.html)


---

## 文档导航

- 上一页：[[01-Unity数学编程简介]]
- 目录：[[00-使用数学编程]]
- 下一页：[[03-Unity Mathematics API]]
