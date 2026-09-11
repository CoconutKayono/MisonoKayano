> 原文：[MonoBehaviour.OnCollisionEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionEnter2D.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnCollisionEnter2D

## 声明

~~~csharp
public void OnCollisionEnter2D(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| other | 与此碰撞关联的 Collision2D 数据。 |

## 描述

传入的 Collider 与此对象的 Collider 接触时发送（仅限 2D 物理）。

## 示例

~~~csharp
using UnityEngine;

// Create a box sprite which falls and hits a floor sprite.  The box can be moved/animated
// with the up, left, right, and down keys.  Moving the box sprite upwards and letting it
// fall will increase the number of calls from OnCollisionEnter2D.

public class Example1 :  MonoBehaviour 
{
    public  Texture2D  tex;

    void Awake()
    {
         SpriteRenderer  sr = gameObject.AddComponent< SpriteRenderer >() as  SpriteRenderer ;
        transform.position = new  Vector3 (0.0f, 2.5f, 0.0f);

         Sprite  sp =  Sprite.Create (tex, new  Rect (0.0f, 0.0f, tex.width, tex.height), new  Vector2 (0.5f, 0.5f), 100.0f);
        sr.sprite = sp;

        gameObject.AddComponent< BoxCollider2D >();

         Rigidbody2D  rb = gameObject.AddComponent< Rigidbody2D >();
        rb.bodyType =  RigidbodyType2D.Dynamic ;
    }

    void  FixedUpdate ()
    {
        float moveHorizontal =  Input.GetAxis ("Horizontal");
        float moveVertical =  Input.GetAxis ("Vertical");

        gameObject.transform.Translate(moveHorizontal * 0.05f, moveVertical * 0.25f, 0.0f);
    }

    // called when the cube hits the floor
    void OnCollisionEnter2D( Collision2D  col)
    {
         Debug.Log ("OnCollisionEnter2D");
    }
}
~~~

~~~csharp
using UnityEngine;

public class Example2 :  MonoBehaviour 
{
    public  Texture2D  tex;

    void Awake()
    {
         SpriteRenderer  sr = gameObject.AddComponent< SpriteRenderer >() as  SpriteRenderer ;
        transform.position = new  Vector3 (0.0f, -2.0f, 0.0f);

         Sprite  sp =  Sprite.Create (tex, new  Rect (0.0f, 0.0f, tex.width, tex.height), new  Vector2 (0.5f, 0.5f), 100.0f);
        sr.sprite = sp;

        gameObject.AddComponent< BoxCollider2D >();
    }
}
~~~

## 相关资源

- [Collision2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collision2D.html)
- [OnCollisionExit2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionExit2D.html)
- [OnCollisionStay2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionStay2D.html)
- [OnCollisionEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionEnter2D.html)
- [OnCollisionEnter2D](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnCollisionEnter2D.html)

---

## 文档导航

- 上一页：[[23-OnCollisionEnter]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[25-OnCollisionExit]]






