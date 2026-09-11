> 原文：[MonoBehaviour.OnAnimatorMove](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnAnimatorMove.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnAnimatorMove

## 声明

~~~csharp
public void OnAnimatorMove(...);
~~~

## 描述

用于处理动画移动、修改根运动的回调。

## 示例

~~~csharp
// Attach this script to your character  GameObject  that has an  Animator  and optionally a  Rigidbody .
// Enable "Apply Root  Motion " on the  Animator . Adjust rootMotionMultiplier to speed up or slow down root motion.

using UnityEngine;

[ RequireComponent (typeof( Animator ))]
public class RootMotionModifier :  MonoBehaviour 
{
    public float rootMotionMultiplier = 2.0f; //  Scale  the root motion

    private  Animator  animator;
    private  Rigidbody  rb;

    void Awake()
    {
        animator = GetComponent< Animator >();
        rb = GetComponent< Rigidbody >();
    }

    void OnAnimatorMove()
    {
        // Only modify root motion if we have a  Rigidbody 
        if (rb != null)
        {
            // Get the deltaPosition from the  Animator 
             Vector3  deltaPosition = animator.deltaPosition * rootMotionMultiplier;
            // Preserve vertical velocity (for example, gravity)
             Vector3  velocity = deltaPosition /  Time.deltaTime ;
            velocity.y = rb.velocity.y;
            rb.velocity = velocity;

            // Optionally apply root rotation
            rb.MoveRotation(rb.rotation * animator.deltaRotation);
        }
        else
        {
            // If no  Rigidbody , just move the transform
            transform.position += animator.deltaPosition * rootMotionMultiplier;
            transform.rotation *= animator.deltaRotation;
        }
    }
}
~~~

## 相关资源

- [Root motion](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/../Manual/RootMotion.html)

---

## 文档导航

- 上一页：[[14-OnAnimatorIK]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[16-OnApplicationFocus]]






