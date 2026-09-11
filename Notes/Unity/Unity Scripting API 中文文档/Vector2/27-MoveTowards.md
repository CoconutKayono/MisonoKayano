> 原文：[Vector2.MoveTowards](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.MoveTowards.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).MoveTowards

## 声明

~~~csharp
public static Vector2 MoveTowards(Vector2 current, Vector2 target, float maxDistanceDelta);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| current | 当前位置。 |
| target | 目标位置。 |
| maxDistanceDelta | 每次调用允许移动的最大距离。 |

## 返回值

返回操作结果。

## 描述

将点 current 移向 target。

## 示例

~~~csharp
using UnityEngine;

// 2D MoveTowards example
// Move the sprite to where the mouse is clicked
//
// Set speed to -1.0f and the sprite will move
// away from the mouse click position forever

public class ExampleClass :  MonoBehaviour 
{
    private float speed = 10.0f;
    private  Vector2  target;
    private  Vector2  position;
    private  Camera  cam;

    void Start()
    {
        target = new  Vector2 (0.0f, 0.0f);
        position = gameObject.transform.position;

        cam =  Camera.main ;
    }

    void  Update ()
    {
        float step = speed *  Time.deltaTime ;

        // move sprite towards the target location
        transform.position =  Vector2.MoveTowards (transform.position, target, step);
    }

    void OnGUI()
    {
         Event  currentEvent =  Event.current ;
         Vector2  mousePos = new  Vector2 ();
         Vector2  point = new  Vector2 ();

        // compute where the mouse is in world space
        mousePos.x = currentEvent.mousePosition.x;
        mousePos.y = cam.pixelHeight - currentEvent.mousePosition.y;
        point = cam.ScreenToWorldPoint(new  Vector3 (mousePos.x, mousePos.y, 0.0f));

        if ( Input.GetMouseButtonDown (0))
        {
            // set the target to the mouse click location
            target = point;
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[26-Min]]
- 目录：[[00-Vector2]]
- 下一页：[[28-Normalize]]


