> 原文：[MonoBehaviour.CancelInvoke](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.CancelInvoke.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).CancelInvoke

## 声明

~~~csharp
public void CancelInvoke();
~~~

## 描述

取消此 MonoBehaviour 上的所有 Invoke 调用。

## 示例

~~~csharp
using UnityEngine;

public class ExampleScript : MonoBehaviour
{
    public GameObject projectile;

    void Update()
    {
        if (Input.GetButton("Fire1"))
            CancelInvoke();
    }
}
~~~

## 声明

~~~csharp
public void CancelInvoke(string methodName);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| methodName | 要取消调用的方法名称。 |

## 描述

取消此行为上名称为 methodName 的所有 Invoke 调用。

---

## 文档导航

- 上一页：[[07-Awake]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[09-FixedUpdate]]
