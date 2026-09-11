> 原文：[MonoBehaviour.OnParticleTrigger](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnParticleTrigger.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnParticleTrigger

## 声明

~~~csharp
public void OnParticleTrigger(...);
~~~

## 描述

粒子系统触发器事件发生时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class TriggerScript :  MonoBehaviour 
{
    void OnParticleTrigger()
    {
         ParticleSystem  ps = GetComponent< ParticleSystem >();

        // particles
        List< ParticleSystem.Particle > enter = new List< ParticleSystem.Particle >();
        List< ParticleSystem.Particle > exit = new List< ParticleSystem.Particle >();

        // get
        int numEnter = ps.GetTriggerParticles( ParticleSystemTriggerEventType.Enter , enter);
        int numExit = ps.GetTriggerParticles( ParticleSystemTriggerEventType.Exit , exit);

        // iterate
        for (int i = 0; i < numEnter; i++)
        {
             ParticleSystem.Particle  p = enter[i];
            p.startColor = new  Color32 (255, 0, 0, 255);
            enter[i] = p;
        }
        for (int i = 0; i < numExit; i++)
        {
             ParticleSystem.Particle  p = exit[i];
            p.startColor = new  Color32 (0, 255, 0, 255);
            exit[i] = p;
        }

        // set
        ps.SetTriggerParticles( ParticleSystemTriggerEventType.Enter , enter);
        ps.SetTriggerParticles( ParticleSystemTriggerEventType.Exit , exit);
    }
}
~~~

---

## 文档导航

- 上一页：[[46-OnParticleSystemStopped]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[48-OnParticleUpdateJobScheduled]]





