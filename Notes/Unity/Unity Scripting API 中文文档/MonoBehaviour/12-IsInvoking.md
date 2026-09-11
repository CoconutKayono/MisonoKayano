> 原文：[MonoBehaviour.IsInvoking](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.IsInvoking.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).IsInvoking

## 声明

~~~csharp
public bool IsInvoking();
~~~

## 描述

检查此 MonoBehaviour 上是否有任何 Invoke 正在等待。

## 声明

~~~csharp
public bool IsInvoking(string methodName);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| methodName | 要检查的方法名称。 |

## 描述

检查 methodName 方法的 Invoke 是否正在等待。

## 示例

~~~csharp
using UnityEngine;
using System.Collections.Generic;

// Instantiates a projectile two seconds after the spacebar was pressed.
// LaunchProjectile is called when a previous RigidBody has finished the Invoke.

public class ExampleScript :  MonoBehaviour 
{
    public  Rigidbody  projectile;

    void  Update ()
    {
        if ( Input.GetKeyDown ( KeyCode.Space ) && !IsInvoking(nameof(LaunchProjectile)))
            Invoke(nameof(LaunchProjectile), 2.0f);
    }

    void LaunchProjectile()
    {
         Rigidbody  instance = Instantiate(projectile);
        instance.velocity =  Random.insideUnitSphere  * 5;
    }
}
~~~

---

## 文档导航

- 上一页：[[11-InvokeRepeating]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[13-LateUpdate]]

