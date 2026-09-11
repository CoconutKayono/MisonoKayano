> 原文：[MonoBehaviour.OnDrawGizmosSelected](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDrawGizmosSelected.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnDrawGizmosSelected

## 声明

~~~csharp
public void OnDrawGizmosSelected(...);
~~~

## 描述

选中 GameObject 时用于绘制 Gizmos 的回调。

## 示例

~~~csharp
using UnityEngine;

public class GizmoTest :  MonoBehaviour 
{
    public float explosionRadius = 5.0f;

    void OnDrawGizmosSelected()
    {
        //  Display  the explosion radius when selected
         Gizmos.color  = new  Color (1, 1, 0, 0.75F);
         Gizmos.DrawSphere (transform.position, explosionRadius);
    }
}
~~~

## 相关资源

- [OnDrawGizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDrawGizmos.html)

---

## 文档导航

- 上一页：[[32-OnDrawGizmos]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[34-OnEnable]]






