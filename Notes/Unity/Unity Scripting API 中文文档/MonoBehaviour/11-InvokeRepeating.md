> 原文：[MonoBehaviour.InvokeRepeating](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.InvokeRepeating.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).InvokeRepeating

## 声明

~~~csharp
public void InvokeRepeating(string methodName, float time, float repeatRate);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| methodName | 要调用的方法名称。 |
| time | Time to wait in seconds before the first invocation. |
| repeatRate | Interval in seconds between method invocations. |

## 描述

在指定延迟后调用方法，并按指定间隔重复调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections.Generic;

// After an initial 2 second wait, launch a projectile every 0.3 seconds

public class ExampleScript :  MonoBehaviour 
{
    public  Rigidbody  projectile;

    void Start()
    {
        InvokeRepeating(nameof(LaunchProjectile), 2.0f, 0.3f);
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

- 上一页：[[10-Invoke]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[12-IsInvoking]]






