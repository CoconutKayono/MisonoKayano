> 原文：[MonoBehaviour.OnAnimatorIK](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnAnimatorIK.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnAnimatorIK

## 声明

~~~csharp
public void OnAnimatorIK(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| layerIndex | 调用 IK 求解器所在层的索引。 |

## 描述

用于设置动画 IK（反向运动学）的回调。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    float leftFootPositionWeight;
    float leftFootRotationWeight;
     Transform  leftFootObj;

    private  Animator  animator;

    void Start()
    {
        animator = GetComponent< Animator >();
    }

    void OnAnimatorIK(int layerIndex)
    {
        animator.SetIKPositionWeight( AvatarIKGoal.LeftFoot , leftFootPositionWeight);
        animator.SetIKRotationWeight( AvatarIKGoal.LeftFoot , leftFootRotationWeight);
        animator.SetIKPosition( AvatarIKGoal.LeftFoot , leftFootObj.position);
        animator.SetIKRotation( AvatarIKGoal.LeftFoot , leftFootObj.rotation);
    }
}
~~~

## 相关资源

- [AnimatorController](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Animations.AnimatorController.html)
- [Avatar](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Avatar.html)
- [Animator](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Animator.html)
- [Animator.SetIKPosition](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Animator.SetIKPosition.html)
- [Animator.SetIKPositionWeight](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Animator.SetIKPositionWeight.html)
- [Animator.SetIKRotation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Animator.SetIKRotation.html)
- [Animator.SetIKRotationWeight](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Animator.SetIKRotationWeight.html)

---

## 文档导航

- 上一页：[[13-LateUpdate]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[15-OnAnimatorMove]]






