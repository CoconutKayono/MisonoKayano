> 原文：[MonoBehaviour.OnTriggerEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerEnter2D.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnTriggerEnter2D

## 声明

~~~csharp
public void OnTriggerEnter2D(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 参与此次碰撞的另一个 Collider2D。 |

## 描述

另一个 Collider2D 进入此 Collider2D 的触发器时调用。

## 示例

~~~csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Example1 :  MonoBehaviour 
{
    private  BoxCollider2D  bc;
    private  Rigidbody2D  rb;

    void Awake()
    {
         SpriteRenderer  sprRend = gameObject.AddComponent< SpriteRenderer >() as  SpriteRenderer ;
        sprRend.color = new  Color (0.9f, 0.9f, 0.9f, 1.0f);

        bc = gameObject.AddComponent< BoxCollider2D >() as  BoxCollider2D ;
        bc.size = new  Vector2 (1.3f, 1.3f);
        bc.isTrigger = true;

        rb = gameObject.AddComponent< Rigidbody2D >() as  Rigidbody2D ;
        rb.bodyType =  RigidbodyType2D.Kinematic ;
    }

    void Start()
    {
        gameObject.GetComponent< SpriteRenderer >().sprite =  Resources.Load < Sprite >("logo");
        gameObject.transform.Translate(4.0f, 0.0f, 0.0f);
        gameObject.transform.localScale = new  Vector2 (2.0f, 2.0f);
    }
}
~~~

~~~csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Example2 :  MonoBehaviour 
{
    private float spriteMove;

    void Awake()
    {
         SpriteRenderer  sprRend;
        sprRend = gameObject.AddComponent< SpriteRenderer >() as  SpriteRenderer ;
        sprRend.color = new  Color (0.9f, 0.9f, 0.9f, 1.0f);

         BoxCollider2D  bc;
        bc = gameObject.AddComponent< BoxCollider2D >() as  BoxCollider2D ;
        bc.size = new  Vector2 (1.3f, 1.3f);
        bc.isTrigger = true;
    }

    void Start()
    {
        gameObject.GetComponent< SpriteRenderer >().sprite =  Resources.Load < Sprite >("circle");
        gameObject.transform.Translate(-4.0f, 0.0f, 0.0f);
        spriteMove = 0.1f;
    }

    void  FixedUpdate ()
    {
        gameObject.transform.Translate(spriteMove, 0.0f, 0.0f);

        if (gameObject.transform.position.x < -4.0f)
        {
            // move GameObject2 to the right
            spriteMove = 0.1f;
        }
    }

    // when the GameObjects collider arrange for this  GameObject  to travel to the left of the screen
    void OnTriggerEnter2D( Collider2D  col)
    {
         Debug.Log (col.gameObject.name + " : " + gameObject.name + " : " +  Time.time );
        spriteMove = -0.1f;
    }
}
~~~

## 相关资源

- [Collider2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider2D.html)
- [OnTriggerExit2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerExit2D.html)
- [OnTriggerStay2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerStay2D.html)
- [OnTriggerEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTriggerEnter2D.html)
- [Rigidbody2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rigidbody2D.html)
- [OnCollisionEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionEnter2D.html)

---

## 文档导航

- 上一页：[[56-OnTriggerEnter]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[58-OnTriggerExit]]









