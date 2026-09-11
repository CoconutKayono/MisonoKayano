> 原文：[MonoBehaviour.OnTriggerExit2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerExit2D.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnTriggerExit2D

## 声明

~~~csharp
public void OnTriggerExit2D(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 参与此次碰撞的另一个 Collider2D。 |

## 描述

另一个 Collider2D 离开此 Collider2D 的触发器时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public bool characterInQuicksand;

    void OnTriggerExit2D( Collider2D  other)
    {
        characterInQuicksand = false;
    }
}
~~~

## 相关资源

- [Collider2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider2D.html)
- [OnTriggerEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerEnter2D.html)
- [OnTriggerStay2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerStay2D.html)

---

## 文档导航

- 上一页：[[58-OnTriggerExit]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[60-OnTriggerStay]]









