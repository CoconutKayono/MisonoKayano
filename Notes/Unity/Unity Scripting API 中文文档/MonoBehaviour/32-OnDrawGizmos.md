> 原文：[MonoBehaviour.OnDrawGizmos](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDrawGizmos.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnDrawGizmos

## 声明

~~~csharp
public void OnDrawGizmos(...);
~~~

## 描述

用于绘制可视化 Gizmos 的回调。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnDrawGizmos()
    {
        // Draw a yellow sphere at the transform's position
         Gizmos.color  =  Color.yellow ;
         Gizmos.DrawSphere (transform.position, 1);
    }
}
~~~

## 相关资源

- [OnDrawGizmosSelected](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnDrawGizmosSelected.html)

---

## 文档导航

- 上一页：[[31-OnDisable]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[33-OnDrawGizmosSelected]]






