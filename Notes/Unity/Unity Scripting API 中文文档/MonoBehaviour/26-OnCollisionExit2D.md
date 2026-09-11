> 原文：[MonoBehaviour.OnCollisionExit2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionExit2D.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnCollisionExit2D

## 声明

~~~csharp
public void OnCollisionExit2D(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 与此碰撞关联的 Collision2D 数据。 |

## 描述

另一个对象上的 Collider 停止接触此对象的 Collider 时发送（仅限 2D 物理）。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public bool characterInQuicksand;

    void OnCollisionExit2D( Collision2D  other)
    {
        characterInQuicksand = false;
    }
}
~~~

## 相关资源

- [Collision2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collision2D.html)
- [OnCollisionEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionEnter2D.html)
- [OnCollisionStay2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionStay2D.html)

---

## 文档导航

- 上一页：[[25-OnCollisionExit]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[27-OnCollisionStay]]






