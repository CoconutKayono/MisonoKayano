> 原文：[Transform.forward](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-forward.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).forward

public Vector3 forward;

#### 描述

返回一个表示变换在世界空间中的蓝轴的归一化向量。

与 [Vector3.forward](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-forward.html)（世界空间中的固定方向）不同，[Transform.forward](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-forward.html) 是此 GameObject 的局部前进方向。旋转此 GameObject 会改变 [Transform.forward](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-forward.html) 方向。

下面的示例展示了如何沿变换在世界空间中的 Z 轴（蓝轴）操纵 GameObject 的位置。

```csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    Rigidbody m_Rigidbody;
    float m_Speed;

    void Start()
    {
        //Fetch the Rigidbody component you attach from your GameObject
        m_Rigidbody = GetComponent<Rigidbody>();
        //Set the speed of the GameObject
        m_Speed = 10.0f;
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.UpArrow))
        {
            //Move the Rigidbody forwards constantly at speed you define (the blue arrow axis in Scene view)
            m_Rigidbody.velocity = transform.forward * m_Speed;
        }

        if (Input.GetKey(KeyCode.DownArrow))
        {
            //Move the Rigidbody backwards constantly at the speed you define (the blue arrow axis in Scene view)
            m_Rigidbody.velocity = -transform.forward * m_Speed;
        }

        if (Input.GetKey(KeyCode.RightArrow))
        {
            //Rotate the sprite about the Y axis in the positive direction
            transform.Rotate(new Vector3(0, 1, 0) * Time.deltaTime * m_Speed, Space.World);
        }

        if (Input.GetKey(KeyCode.LeftArrow))
        {
            //Rotate the sprite about the Y axis in the negative direction
            transform.Rotate(new Vector3(0, -1, 0) * Time.deltaTime * m_Speed, Space.World);
        }
    }
}
```

另一个示例：

```csharp
using UnityEngine;

// Computes the angle between the direction of the target from this object and this object's viewing direction (forward).

public class Example : MonoBehaviour
{
    public float angleBetween = 0.0f;
    public Transform target;

    void Update()
    {
        Vector3 targetDir = target.position - transform.position;
        angleBetween = Vector3.Angle(transform.forward, targetDir);
    }
}
```


