> 原文：[Transform.right](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-right.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).right

public Vector3 right;

### 描述

Transform 在世界空间中的红轴。

沿变换在世界空间中的 X 轴（红轴）操纵 GameObject 的位置。与 Vector3.right 不同，Transform.right 移动 GameObject 时还会考虑其旋转。当 GameObject 旋转时，表示 GameObject X 轴的红色箭头也会改变方向。Transform.right 会沿红色箭头的轴（X 轴）移动 GameObject。若要忽略旋转、沿 X 轴移动 GameObject，请参阅 Vector3.right。

### 示例

~~~csharp
//Attach this script to a  GameObject  with a  Rigidbody2D  component. Use the left and right arrow keys to see the transform in action.
//Use the up and down keys to change the rotation, and see how using  Transform.right  differs from using  Vector3.right 

using UnityEngine;

public class Example :  MonoBehaviour 
{
     Rigidbody2D  m_Rigidbody;
    float m_Speed;

    void Start()
    {
        //Fetch the  Rigidbody  component you attach from your  GameObject 
        m_Rigidbody = GetComponent< Rigidbody2D >();
        //Set the speed of the  GameObject 
        m_Speed = 10.0f;
    }

    void  Update ()
    {
        if ( Input.GetKey ( KeyCode.RightArrow ))
        {
            //Move the  Rigidbody  to the right constantly at speed you define (the red arrow axis in  Scene  view)
            m_Rigidbody.linearVelocity = transform.right * m_Speed;
        }

        if ( Input.GetKey ( KeyCode.LeftArrow ))
        {
            //Move the  Rigidbody  to the left constantly at the speed you define (the red arrow axis in  Scene  view)
            m_Rigidbody.linearVelocity = -transform.right * m_Speed;
        }

        if ( Input.GetKey ( KeyCode.UpArrow ))
        {
            //rotate the sprite about the Z axis in the positive direction
            transform.Rotate(new  Vector3 (0, 0, 1) *  Time.deltaTime  * m_Speed,  Space.World );
        }

        if ( Input.GetKey ( KeyCode.DownArrow ))
        {
            //rotate the sprite about the Z axis in the negative direction
            transform.Rotate(new  Vector3 (0, 0, -1) *  Time.deltaTime  * m_Speed,  Space.World );
        }
    }
}
~~~



