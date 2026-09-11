> 原文：[CharacterController.Move](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/CharacterController.Move.html)

# [CharacterController](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/CharacterController.html).Move

public CollisionFlags Move(Vector3 motion);

### 描述

提供带有 CharacterController 组件的 GameObject 的移动。

CharacterController.Move 会使 GameObject 沿给定方向移动。给定方向需要使用绝对移动增量值。碰撞会限制 CharacterController.Move 的执行。返回值 CollisionFlags 表示碰撞方向：None、Sides、Above 和 Below。CharacterController.Move 不使用重力。

下面的示例演示如何使用 CharacterController.Move。Update 会使 CharacterController.Move 重新定位玩家。此外，Jump 会沿垂直方向改变玩家位置。

```csharp
// This first example shows how to move using Input System Package (New)

using UnityEngine;
using UnityEngine.InputSystem;

public class Example : MonoBehaviour
{
    private float playerSpeed = 5.0f;
    private float jumpHeight = 1.5f;
    private float gravityValue = -9.81f;

    public CharacterController controller;
    private Vector3 playerVelocity;
    private bool groundedPlayer;

    [Header("Input Actions")]
    public InputActionReference moveAction;
    public InputActionReference jumpAction;

    private void OnEnable()
    {
        moveAction.action.Enable();
        jumpAction.action.Enable();
    }

    private void OnDisable()
    {
        moveAction.action.Disable();
        jumpAction.action.Disable();
    }

    void Update()
    {
        groundedPlayer = controller.isGrounded;

        if (groundedPlayer)
        {
            // Slight downward velocity to keep grounded stable
            if (playerVelocity.y < -2f)
                playerVelocity.y = -2f;
        }

        // Read input
        Vector2 input = moveAction.action.ReadValue<Vector2>();
        Vector3 move = new Vector3(input.x, 0, input.y);
        move = Vector3.ClampMagnitude(move, 1f);

        if (move != Vector3.zero)
            transform.forward = move;

        // Jump using WasPressedThisFrame()
        if (groundedPlayer && jumpAction.action.WasPressedThisFrame())
        {
            playerVelocity.y = Mathf.Sqrt(jumpHeight * -2f * gravityValue);
        }

        // Apply gravity
        playerVelocity.y += gravityValue * Time.deltaTime;

        // Move
        Vector3 finalMove = move * playerSpeed + Vector3.up * playerVelocity.y;
        controller.Move(finalMove * Time.deltaTime);
    }
}
```
