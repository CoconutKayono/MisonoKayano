> 原文：[MonoBehaviour.OnControllerColliderHit](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnControllerColliderHit.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnControllerColliderHit

## 声明

~~~csharp
public void OnControllerColliderHit(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| hit | 与此碰撞关联的 ControllerColliderHit 数据。 |

## 描述

CharacterController 在移动过程中碰撞 Collider 时调用。

## 示例

~~~csharp
// This script pushes all rigidbodies that the character touches

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public float pushPower = 2.0F;

    void OnControllerColliderHit( ControllerColliderHit  hit)
    {
         Rigidbody  body = hit.collider.attachedRigidbody;

        // no rigidbody
        if (body == null || body.isKinematic)
            return;

        // We dont want to push objects below us
        if (hit.moveDirection.y < -0.3f)
            return;

        // Calculate push direction from move direction,
        // we only push objects to the sides never up and down
         Vector3  pushDir = new  Vector3 (hit.moveDirection.x, 0, hit.moveDirection.z);

        // If you know how fast your character is trying to move,
        // then you can also multiply the push velocity by that.

        // Apply the push
        body.velocity = pushDir * pushPower;
    }
}
~~~

## 相关资源

- [CharacterController](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/CharacterController.html)
- [Collider](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider.html)

---

## 文档导航

- 上一页：[[28-OnCollisionStay2D]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[30-OnDestroy]]






