> 原文：[MonoBehaviour.OnParticleUpdateJobScheduled](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnParticleUpdateJobScheduled.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnParticleUpdateJobScheduled

## 声明

~~~csharp
public void OnParticleUpdateJobScheduled(...);
~~~

## 描述

粒子系统安排粒子更新作业时调用。

## 示例

~~~csharp
using UnityEngine;
using UnityEngine.ParticleSystemJobs;

public class JobScript :  MonoBehaviour 
{
    void OnParticleUpdateJobScheduled()
    {
         ParticleSystem  ps = GetComponent< ParticleSystem >();
        new UpdateParticlesJob { m_DeltaTime =  Time.deltaTime  }.Schedule(ps);
    }

    struct UpdateParticlesJob :  IJobParticleSystem 
    {
        public float m_DeltaTime;

        public void Execute( ParticleSystemJobData  particles)
        {
            var positionsY = particles.positions.x;

            for (int i = 0; i < particles.count; i++)
            {
                positionsY[i] += 3.0f * m_DeltaTime;
            }
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[47-OnParticleTrigger]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[49-OnPostRender]]





