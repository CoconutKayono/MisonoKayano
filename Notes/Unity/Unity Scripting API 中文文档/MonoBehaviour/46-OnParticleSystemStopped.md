> 原文：[MonoBehaviour.OnParticleSystemStopped](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnParticleSystemStopped.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnParticleSystemStopped

## 声明

~~~csharp
public void OnParticleSystemStopped(...);
~~~

## 描述

粒子系统停止播放时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class StoppedScript :  MonoBehaviour 
{
    void Start()
    {
        var main = GetComponent< ParticleSystem >().main;
        main.stopAction =  ParticleSystemStopAction.Callback ;
    }

    void OnParticleSystemStopped()
    {
         Debug.Log (" System  has stopped!");
    }
}
~~~

---

## 文档导航

- 上一页：[[45-OnParticleCollision]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[47-OnParticleTrigger]]





