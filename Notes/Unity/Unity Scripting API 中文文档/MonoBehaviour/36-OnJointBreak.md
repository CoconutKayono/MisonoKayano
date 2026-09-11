> 原文：[MonoBehaviour.OnJointBreak](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnJointBreak.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnJointBreak

## 声明

~~~csharp
public void OnJointBreak(...);
~~~

## 描述

关节断裂时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnJointBreak(float breakForce)
    {
         Debug.Log (" Joint  Broke!, force: " + breakForce);
    }
}
~~~

## 相关资源

- [Joint.breakForce](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Joint-breakForce.html)

---

## 文档导航

- 上一页：[[35-OnGUI]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[37-OnJointBreak2D]]






