> 原文：[MonoBehaviour.OnJointBreak2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnJointBreak2D.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnJointBreak2D

## 声明

~~~csharp
public void OnJointBreak2D(...);
~~~

## 描述

2D 关节断裂时调用。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnJointBreak2D( Joint2D  brokenJoint)
    {
         Debug.Log ("A joint has just been broken!");
         Debug.Log ("The broken joint exerted a reaction force of " + brokenJoint.reactionForce);
         Debug.Log ("The broken joint exerted a reaction torque of " + brokenJoint.reactionTorque);
    }
}
~~~

## 相关资源

- [Joint2D.breakForce](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Joint2D-breakForce.html)
- [Joint2D.breakTorque](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Joint2D-breakTorque.html)
- [Joint2D.reactionForce](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Joint2D-reactionForce.html)
- [Joint2D.reactionTorque](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Joint2D-reactionTorque.html)

---

## 文档导航

- 上一页：[[36-OnJointBreak]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[38-OnMouseDown]]






