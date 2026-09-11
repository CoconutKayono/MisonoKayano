> 原文：[CharacterController.SimpleMove](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/CharacterController.SimpleMove.html)

# [CharacterController](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/CharacterController.html).SimpleMove

public bool SimpleMove(Vector3 speed);

### 描述

以 speed 速度移动角色。

y 轴方向的速度会被忽略。速度单位为单位/秒。会自动应用重力。如果角色着地，则返回 true。

建议每帧只调用一次 CharacterController.Move 或 CharacterController.SimpleMove。

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(CharacterController))]
public class CharacterMover : MonoBehaviour
{
    private float moveSpeed = 3.0f;
    private float rotationSpeed = 90.0f; // degrees per second

    public CharacterController characterController;

    [Header("Input Actions")]
    public InputActionReference moveAction;

    private void OnEnable()
    {
        moveAction.action.Enable();
    }

    private void OnDisable()
    {
        moveAction.action.Disable();
    }

    void Update()
    {
        // Rotate character
        transform.Rotate(Vector3.up, moveAction.action.ReadValue<Vector2>().x * rotationSpeed * Time.deltaTime);

        // Move character
        Vector3 moveDirection = transform.forward * moveAction.action.ReadValue<Vector2>().y * moveSpeed;
        
        characterController.SimpleMove(moveDirection);
    }
}
```
