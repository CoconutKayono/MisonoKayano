> 原文：[MonoBehaviour.Invoke](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.Invoke.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).Invoke

## 声明

~~~csharp
public void Invoke(string methodName, float time);
~~~

## 描述

在指定延迟后调用方法。

## 示例

~~~csharp
using UnityEngine;
using System.Collections.Generic;

public class ExampleScript :  MonoBehaviour 
{
    // Launches a projectile in 2 seconds

     Rigidbody  projectile;

    void Start()
    {
        Invoke(nameof(LaunchProjectile), 2.0f);
    }

    void LaunchProjectile()
    {
         Rigidbody  instance = Instantiate(projectile);
        instance.velocity =  Random.insideUnitSphere  * 5.0f;
    }
}
~~~

---

## 文档导航

- 上一页：[[09-FixedUpdate]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[11-InvokeRepeating]]



